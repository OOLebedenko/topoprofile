from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import TypeVar

R = TypeVar("R")

Task = Callable[[], R]


class Worker(ABC):
    """Base interface for executing tasks."""

    @abstractmethod
    def execute(
            self,
            tasks: Iterable[Task[R]],
    ) -> list[R]:
        """Execute tasks and return their results."""


class SequentialWorker(Worker):
    """Execute tasks sequentially."""

    def execute(
            self,
            tasks: Iterable[Task[R]],
    ) -> list[R]:
        return [
            task()
            for task in tasks
        ]
