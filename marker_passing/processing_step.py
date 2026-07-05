from abc import ABC, abstractmethod


class ProcessingStep(ABC):
    """
    A single pre- or post-processing action executed around each pulse.
    Implementations can perform normalization, decay, logging, etc.
    """

    @abstractmethod
    def execute(self) -> None:
        ...
