from __future__ import annotations

from typing import Dict, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ..node import Node


def _link_weight(link: object) -> float:
    """Extract a scalar weight from any Link object by duck-typing."""
    if hasattr(link, "weight"):
        return float(link.weight)
    if hasattr(link, "get_weight"):
        return float(link.get_weight())
    return 1.0


class GraphSerializer:
    """
    Converts a CPU-side Node/Link graph into a sparse COO weight matrix
    and a dense initial-activation vector, ready for GPU transfer.

    Weight matrix convention: W[target, source] = link weight.
    One SpMM step  x' = W @ x  then propagates activation from sources
    to targets — exactly what one spreading pulse does.

    Negative link weights (antonyms, definitions) are preserved as-is;
    the threshold mask in CudaSpreadingAlgorithm operates on |x|.
    """

    def __init__(self, nodes: List["Node"]) -> None:
        self.nodes: List["Node"] = list(nodes)
        self.node_to_idx: Dict["Node", int] = {n: i for i, n in enumerate(self.nodes)}
        self._n = len(self.nodes)

    @property
    def n(self) -> int:
        return self._n

    def build_coo(self) -> Tuple[List[int], List[int], List[float]]:
        """
        Return (row_indices, col_indices, values) in COO format.
        row = target node index, col = source node index.
        """
        rows: List[int] = []
        cols: List[int] = []
        vals: List[float] = []

        for node in self.nodes:
            src_idx = self.node_to_idx[node]
            for link in node.get_links():
                # resolve target: follow link in forward direction
                target = None
                if hasattr(link, "target"):
                    target = link.target
                elif hasattr(link, "get_target_node"):
                    target = link.get_target_node()

                if target is None or target not in self.node_to_idx:
                    continue

                tgt_idx = self.node_to_idx[target]
                rows.append(tgt_idx)
                cols.append(src_idx)
                vals.append(_link_weight(link))

        return rows, cols, vals

    def initial_activation_vector(
        self,
        activations: Dict["Node", float],
    ) -> List[float]:
        """
        Build a dense activation vector x0 of length N.
        activations maps Node -> initial float value.
        Nodes not in the dict receive 0.0.
        """
        x: List[float] = [0.0] * self._n
        for node, value in activations.items():
            idx = self.node_to_idx.get(node)
            if idx is not None:
                x[idx] = float(value)
        return x
