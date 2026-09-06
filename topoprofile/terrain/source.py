from typing import Protocol, TypeVar

import pygmt

from topoprofile.geo.models import Bounds
from topoprofile.terrain.models import DEM

KeyT_contra = TypeVar(
    "KeyT_contra",
    contravariant=True,
)
DataT_co = TypeVar(
    "DataT_co",
    covariant=True,
)


class Source(Protocol[KeyT_contra, DataT_co]):
    """Source of processing data."""

    def load(
            self,
            key: KeyT_contra,
            /,
    ) -> DataT_co:
        """Load data by key."""
        ...


class EarthReliefSource:
    """Load DEM data from GMT Earth Relief."""

    def __init__(
            self,
            resolution: str,
    ) -> None:
        self._resolution = resolution

    def load(
            self,
            bounds: Bounds,
    ) -> DEM:
        data = pygmt.datasets.load_earth_relief(
            resolution=self._resolution,
            region=[
                bounds.west,
                bounds.east,
                bounds.south,
                bounds.north,
            ],
        )

        data.rio.write_crs(
            "EPSG:4326",
            inplace=True,
        )

        return DEM(
            values=data.values,
            transform=data.rio.transform(),
            crs=data.rio.crs,
            nodata=data.rio.nodata,
        )
