from __future__ import annotations

from typing import Dict, List, Optional, TYPE_CHECKING

from .graph_serializer import GraphSerializer

if TYPE_CHECKING:
    from ..node import Node


class CudaSpreadingAlgorithm:
    """
    GPU-accelerated spreading activation via sparse matrix multiplication.

    Replaces the object-oriented pulse loop of SpreadingAlgorithm with a
    single repeated SpMM kernel on the GPU:

        x' = W @ x              (cuSPARSE SpMM via torch.sparse.mm)
        x  = x' * (|x'| > θ)   (elementwise threshold mask)

    where W[target, source] = link weight  and  x[i] = activation of node i.

    Constraints
    -----------
    * Works only with *scalar-activation* algorithms (DoubleMarker style).
      Symbolic markers (PathMarker, InferencePath) cannot be tensorised and
      must remain on the CPU SpreadingAlgorithm.
    * The full graph topology must be known before execute() is called.
      Lazy graph expansion during spreading is not supported.
    * Requires torch (pip install torch). CUDA is used when available;
      falls back to CPU tensors transparently so the logic can be tested
      without a GPU.

    Typical usage
    -------------
        serializer = GraphSerializer(nodes)
        algo = CudaSpreadingAlgorithm(serializer, threshold=0.064, max_pulses=80)
        algo.set_activation(cat_node, 1.0)
        algo.set_activation(dog_node, 1.0)
        algo.execute()
        print(algo.get_activation(some_node))
        print(algo.get_all_activations())   # Dict[Node, float]

    Batched usage (K seed concepts in parallel)
    --------------------------------------------
    Pass a list of activation dicts — one per seed concept — to execute_batched().
    The GPU evaluates all K concepts simultaneously in one [N x K] SpMM.

        results = algo.execute_batched([{cat_node: 1.0}, {dog_node: 1.0}])
        # results[0][node] = activation of node for cat seed
        # results[1][node] = activation of node for dog seed
    """

    def __init__(
        self,
        serializer: GraphSerializer,
        threshold: float = 0.064,
        max_pulses: int = 80,
        convergence_eps: float = 1e-6,
        device: Optional[str] = None,
    ) -> None:
        try:
            import torch
        except ImportError as exc:
            raise ImportError(
                "torch is required for GPU acceleration: pip install torch"
            ) from exc

        self._torch = torch
        self._serializer = serializer
        self._threshold = threshold
        self._max_pulses = max_pulses
        self._eps = convergence_eps

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self._device = torch.device(device)

        # build sparse weight matrix W once
        self._W = self._build_sparse_W()

        # initial activation vector (mutable before execute())
        self._x0: List[float] = [0.0] * serializer.n

        # result tensor (populated after execute())
        self._x_final: Optional["torch.Tensor"] = None

        self._pulses_run: int = 0

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------

    def set_activation(self, node: "Node", value: float) -> None:
        """Set the initial activation for a single node before execute()."""
        idx = self._serializer.node_to_idx.get(node)
        if idx is None:
            raise KeyError(f"Node {node!r} was not part of the graph passed to GraphSerializer")
        self._x0[idx] = float(value)

    def set_activations(self, activations: Dict["Node", float]) -> None:
        """Convenience: set multiple nodes at once."""
        for node, value in activations.items():
            self.set_activation(node, value)

    def reset(self) -> None:
        """Clear all initial activations (keep the graph)."""
        self._x0 = [0.0] * self._serializer.n
        self._x_final = None
        self._pulses_run = 0

    def execute(self) -> int:
        """
        Run the SpMM pulse loop on the configured device.
        Returns the number of pulses actually executed.
        Stops early if the activation vector converges (max delta < eps).
        """
        torch = self._torch
        x = torch.tensor(self._x0, dtype=torch.float32, device=self._device)

        for pulse in range(self._max_pulses):
            x_new = torch.sparse.mm(self._W, x.unsqueeze(1)).squeeze(1)

            # threshold mask on absolute values (handles negative link weights)
            mask = x_new.abs() > self._threshold
            x_new = x_new * mask

            # convergence check (stays on device — no CPU sync in the hot path)
            delta = (x_new - x).abs().max()
            x = x_new
            if delta.item() < self._eps:
                self._pulses_run = pulse + 1
                break
        else:
            self._pulses_run = self._max_pulses

        self._x_final = x.cpu()
        return self._pulses_run

    def execute_batched(
        self,
        activation_dicts: List[Dict["Node", float]],
    ) -> List[Dict["Node", float]]:
        """
        Evaluate K independent seed-concept activation vectors simultaneously.

        All K vectors are stacked into an [N x K] matrix; one SpMM call per
        pulse propagates all K simultaneously.  This is the primary GPU win:
        throughput scales nearly linearly with K at negligible extra cost.

        Parameters
        ----------
        activation_dicts : list of {Node: float}
            One dict per seed concept.  Missing nodes default to 0.0.

        Returns
        -------
        list of {Node: float}
            One result dict per input seed concept.
        """
        torch = self._torch
        n = self._serializer.n
        k = len(activation_dicts)

        # build [N x K] initial matrix
        X = torch.zeros(n, k, dtype=torch.float32, device=self._device)
        for col, act_dict in enumerate(activation_dicts):
            for node, value in act_dict.items():
                idx = self._serializer.node_to_idx.get(node)
                if idx is not None:
                    X[idx, col] = float(value)

        for _ in range(self._max_pulses):
            # W is [N x N] sparse, X is [N x K] dense → result [N x K]
            X_new = torch.sparse.mm(self._W, X)
            mask = X_new.abs() > self._threshold
            X_new = X_new * mask

            delta = (X_new - X).abs().max()
            X = X_new
            if delta.item() < self._eps:
                break

        X_cpu = X.cpu()
        nodes = self._serializer.nodes

        results: List[Dict["Node", float]] = []
        for col in range(k):
            col_vals = X_cpu[:, col].tolist()
            results.append({node: col_vals[i] for i, node in enumerate(nodes)})
        return results

    def get_activation(self, node: "Node") -> float:
        """Return the activation of a single node after execute()."""
        self._require_executed()
        idx = self._serializer.node_to_idx.get(node)
        if idx is None:
            raise KeyError(f"Node {node!r} not in graph")
        return float(self._x_final[idx].item())

    def get_all_activations(self) -> Dict["Node", float]:
        """Return a dict mapping every node to its final activation."""
        self._require_executed()
        vals = self._x_final.tolist()
        return {node: vals[i] for i, node in enumerate(self._serializer.nodes)}

    @property
    def pulses_run(self) -> int:
        """Number of pulses executed in the last execute() call."""
        return self._pulses_run

    @property
    def device(self) -> str:
        return str(self._device)

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _build_sparse_W(self) -> "torch.Tensor":
        """Convert GraphSerializer COO data to a sparse float32 tensor on device."""
        torch = self._torch
        rows, cols, vals = self._serializer.build_coo()
        n = self._serializer.n

        if not vals:
            # empty graph — return zero sparse matrix
            indices = torch.zeros(2, 0, dtype=torch.long)
            values = torch.zeros(0, dtype=torch.float32)
        else:
            indices = torch.tensor([rows, cols], dtype=torch.long)
            values = torch.tensor(vals, dtype=torch.float32)

        W = torch.sparse_coo_tensor(indices, values, size=(n, n))
        # coalesce sums duplicate (row,col) pairs — correct for multi-edges
        W = W.coalesce().to(self._device)
        return W

    def _require_executed(self) -> None:
        if self._x_final is None:
            raise RuntimeError("Call execute() before reading activations")
