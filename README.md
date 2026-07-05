# MarkerPassingAlgorithm

A generalised implementation of the Marker Passing algorithm based on
[Crestani (1997)](https://doi.org/10.1023/A:1006569829653), available in both
**Java** (original) and **Python** (`python` branch).

Marker Passing extends classical Spreading Activation
([Wikipedia](https://en.wikipedia.org/wiki/Spreading_activation)) by replacing
the single floating-point "zorch" with an arbitrary **Marker** object. Every
node in the graph can inspect, transform, and forward markers along its links,
making it possible to encode symbolic information alongside numeric activation.

```
@InProceedings{Faehndrich2018,
  author    = {Fähndrich, Johannes and Weber, Sabine and Kanthak, Hannes},
  title     = {A Marker Passing Approach to Winograd Schemas},
  booktitle = {Semantic Technology},
  year      = {2018},
  publisher = {Springer International Publishing},
  pages     = {165--181},
  doi       = {10.1007/978-3-030-04284-4_11}
}
```

---

## Python package (`python` branch)

### Requirements

- Python 3.9+
- No external dependencies — pure stdlib

### Installation

```bash
git clone https://github.com/Datenverlust/MarkerPassingAlgorithm.git
cd MarkerPassingAlgorithm
git checkout python
# optionally install as an editable package:
pip install -e .
```

### Package structure

```
marker_passing/
├── __init__.py
├── marker.py                       # Marker          — abstract base marker type
├── link.py                         # Link             — abstract directed edge
├── node.py                         # Node             — abstract graph vertex
├── spreading_step.py               # SpreadingStep    — single link traversal + markers
├── spreaded_markers.py             # SpreadedMarkers  — target-node → steps mapping
├── in_function.py                  # InFunction       — activation-aggregation hook
├── out_function.py                 # OutFunction      — activation-emission hook
├── select_firing_nodes_function.py # SelectFiringNodesFunction — node selection
├── processing_step.py              # ProcessingStep   — pre/post-processing hook
├── termination_condition.py        # TerminationCondition — stop condition
└── spreading_algorithm.py          # SpreadingAlgorithm — main pulse loop
```

### Core algorithm

```
execute()
└── while not terminated:
    └── _pulse()
        ├── _preprocess()   — run ProcessingStep list
        ├── select          — SelectFiringNodesFunction picks active nodes
        ├── _spread()       — OutFunction emits SpreadingSteps;
        │                     InFunction absorbs them at target nodes
        ├── _postprocess()  — run ProcessingStep list
        └── _check_termination() — TerminationCondition decides whether to stop
```

### Quick start

```python
from marker_passing import (
    Marker, Link, Node, SpreadingAlgorithm,
    InFunction, OutFunction, SelectFiringNodesFunction,
    TerminationCondition, ProcessingStep, SpreadingStep,
)

# 1. Define a concrete Marker
class DoubleMarker(Marker):
    def __init__(self, value: float) -> None:
        self.value = value

# 2. Define a concrete Link
class SimpleLink(Link):
    def __init__(self, source, target, weight=1.0):
        self._source, self._target, self.weight = source, target, weight

    @property
    def source(self): return self._source
    @source.setter
    def source(self, v): self._source = v

    @property
    def target(self): return self._target
    @target.setter
    def target(self, v): self._target = v

# 3. Define a concrete Node
class SimpleNode(Node):
    def __init__(self, name):
        self.name = name
        self._links, self._markers = [], []
        self.activation = 0.0

    def get_links(self): return self._links
    def get_markers(self): return self._markers
    def check_thresholds(self, mc=None): return self.activation > 0.0

# 4. Wire up the algorithm
algo = SpreadingAlgorithm()

# Nodes
a, b, c = SimpleNode("A"), SimpleNode("B"), SimpleNode("C")
a.get_links().append(SimpleLink(a, b))
b.get_links().append(SimpleLink(b, c))

# Initial marker
a.get_markers().append(DoubleMarker(1.0))
a.activation = 1.0
algo.active_nodes = [a, b, c]

# Hooks
class MyOut(OutFunction):
    def compute(self, node):
        steps = []
        for link in node.get_links():
            for m in node.get_markers():
                if isinstance(m, DoubleMarker):
                    s = SpreadingStep()
                    s.link, s.in_direction = link, True
                    s.markings = [DoubleMarker(m.value * link.weight)]
                    steps.append(s)
        return steps

class MyIn(InFunction):
    def compute(self, input_steps, node):
        for step in input_steps:
            for m in step.markings:
                if isinstance(m, DoubleMarker):
                    node.activation += m.value
                    node.get_markers().append(m)

class AllNodes(SelectFiringNodesFunction):
    def compute(self, active_nodes): return active_nodes

class MaxPulses(ProcessingStep, TerminationCondition):
    def __init__(self, n): self._n, self._i = n, 0
    def execute(self): self._i += 1
    def compute(self): return self._i >= self._n

stop = MaxPulses(3)
algo.out_function = MyOut()
algo.in_function = MyIn()
algo.select_firing_nodes = AllNodes()
algo.termination_condition = stop
algo.preprocessing_steps = [stop]

algo.execute()
print(c.activation)  # propagated activation
```

---

## Java package (original)

### Requirements

- Java 8
- Maven

### Build

```bash
mvn clean install
```

---

## Architecture

![Algorithm](http://fähndrich.de/images/Faehndrich2018.png)

| Java type | Python equivalent |
|---|---|
| Interface | `abc.ABC` + `@abstractmethod` |
| `default` interface method | Concrete method in abstract class |
| `HashMap` | `dict` / `defaultdict` |
| Getters/setters | `@property` |
| Circular type references | `TYPE_CHECKING` guard + string annotations |

---

## Related projects

- **SemanticDecomposition** — builds semantic concept graphs consumed by this algorithm
- **SemanticDecompositionExperiments** — NLP experiments (Winograd schemas, WSD, QA) built on top

---

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)

[Contact](https://twitter.com/Datenverlust)
