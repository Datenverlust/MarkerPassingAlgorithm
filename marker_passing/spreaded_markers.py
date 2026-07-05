from __future__ import annotations
from collections import defaultdict
from typing import Collection, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node
    from .spreading_step import SpreadingStep


class SpreadedMarkers:
    """
    Collects spreading steps grouped by their target node, ready for in-function processing.
    """

    def __init__(self) -> None:
        self._markers: Dict["Node", List["SpreadingStep"]] = defaultdict(list)

    def add_all(self, steps: Collection["SpreadingStep"]) -> None:
        for step in steps:
            target = step.get_target_node()
            self._markers[target].append(step)

    def get_target_nodes(self) -> Collection["Node"]:
        return self._markers.keys()

    def get_input_for_target(self, target_node: "Node") -> List["SpreadingStep"]:
        return self._markers[target_node]
