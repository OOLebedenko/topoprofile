from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Worker(ABC):
    """Base interface for processing a collection of items."""

    @abstractmethod
    def process(
        self,
        task: Callable[[T], R],
        items: Iterable[T],
    ) -> list[R]:
        """Apply a task to each input item."""


class SequentialWorker(Worker):
    """Process items sequentially."""

    def process(
        self,
        task: Callable[[T], R],
        items: Iterable[T],
    ) -> list[R]:
        return [
            task(item)
            for item in items
        ]