import logging
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from typing import TypeVar

from tqdm import tqdm

logger = logging.getLogger(__name__)

R = TypeVar("R")

Task = Callable[[], R]


class TaskExecutionError(RuntimeError):
    """Raised when a processing task fails."""


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
        tasks = list(tasks)

        results = []
        failed = 0

        for task in tqdm(
                tasks,
                desc="Processing",
                unit="task",
        ):
            try:
                results.append(
                    task()
                )
            except TaskExecutionError:
                failed += 1
                logger.exception(
                    "Task failed."
                )

        if failed:
            logger.warning(
                "%d of %d tasks failed.",
                failed,
                len(tasks),
            )

        return results