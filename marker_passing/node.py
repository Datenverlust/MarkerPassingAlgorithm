from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Collection, TYPE_CHECKING

if TYPE_CHECKING:
    from .link import Link
    from .marker import Marker


class Node(ABC):
    """
    Vertex in the graph. Holds markers and is connected via links.
    """

    def add_link(self, link: "Link") -> None:
        self.get_links().append(link)

    def remove_link(self, link: "Link") -> None:
        self.get_links().remove(link)

    @abstractmethod
    def get_links(self) -> list["Link"]:
        ...

    def add_marker(self, marker: "Marker") -> None:
        self.get_markers().append(marker)

    def remove_marker(self, marker: "Marker") -> None:
        self.get_markers().remove(marker)

    @abstractmethod
    def get_markers(self) -> list["Marker"]:
        ...

    @abstractmethod
    def check_thresholds(self, marker_classes: object) -> bool:
        """
        Returns True if any threshold is reached for the given marker classes,
        meaning this node should be considered active.
        """
        ...
