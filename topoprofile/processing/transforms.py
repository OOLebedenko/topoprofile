from collections.abc import Callable
from typing import Protocol


class Transform[T](Protocol):
    """Transform data of a given type."""

    def __call__(
            self,
            value: T,
            /,
    ) -> T:
        """Transform and return data."""
        ...


class Compose[T]:
    """Apply transformations sequentially."""

    def __init__(
            self,
            transforms: tuple[Callable[[T], T], ...],
    ) -> None:
        self._transforms = transforms

    def __call__(
            self,
            value: T,
            /,
    ) -> T:
        for transform in self._transforms:
            value = transform(value)

        return value
