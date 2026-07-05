from abc import ABC, abstractmethod


class TerminationCondition(ABC):
    """
    Evaluated after each pulse. Returns True when the algorithm should stop.
    """

    @abstractmethod
    def compute(self) -> bool:
        ...
