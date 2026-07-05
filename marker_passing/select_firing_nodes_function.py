from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Collection, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node


class SelectFiringNodesFunction(ABC):
    """
    Selects which active nodes will fire in the next pulse.
    A standard implementation fires all active nodes.
    """

    @abstractmethod
    def compute(self, active_nodes: Collection["Node"]) -> Collection["Node"]:
        ...
