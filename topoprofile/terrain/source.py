from abc import ABC, abstractmethod

import pygmt

from topoprofile.geo.models import Bounds
from topoprofile.terrain.models import DEM


class DEMSource(ABC):
    """Source of digital elevation model data."""

    @abstractmethod
    def load(
            self,
            bounds: Bounds,
    ) -> DEM:
        """Load DEM data for geographic bounds."""


class EarthReliefDEMSource(DEMSource):
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
