from collections.abc import Callable
from functools import partial

from topoprofile.osm.task import Task


class OSMTaskManager[**ParamsT, ResultT]:
    """Create executable OSM tasks."""

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
        """Create an executable task."""
        return partial(
            self._task,
            *args,
            **kwargs,
        )
