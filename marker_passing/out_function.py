from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Collection, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node
    from .spreading_step import SpreadingStep


class OutFunction(ABC):
    """
    Defines how markers are passed to outgoing links when a node fires.
    May apply weighting, filtering, or enrichment to the markers.
    """

    @abstractmethod
    def compute(self, node: "Node") -> Collection["SpreadingStep"]:
        ...
