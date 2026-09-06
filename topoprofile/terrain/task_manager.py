from collections.abc import Callable
from functools import partial

from topoprofile.terrain.task import Task


class TerrainTaskManager[**ParamsT, ResultT]:
    """Create executable terrain tasks."""

    def __init__(
            self,
            task: Task[ParamsT, ResultT],
    ) -> None:
        self._task = task

    def create_task(
            self,
            *args: ParamsT.args,
            **kwargs: ParamsT.kwargs,
    ) -> Callable[[], ResultT]:
        return partial(
            self._task,
            *args,
            **kwargs,
        )
