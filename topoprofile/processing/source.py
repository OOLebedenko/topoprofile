from typing import Protocol, TypeVar

KeyT_contra = TypeVar(
    "KeyT_contra",
    contravariant=True,
)
DataT_co = TypeVar(
    "DataT_co",
    covariant=True,
)


class Source(Protocol[KeyT_contra, DataT_co]):
    """Source of input data."""

    def load(
            self,
            key: KeyT_contra,
            /,
    ) -> DataT_co:
        """Load data for the given key."""
        ...
