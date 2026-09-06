from abc import ABC, abstractmethod

import numpy as np

from topoprofile.terrain.models import DEM, RasterTile


class DEMTransform(ABC):
    """Transform a digital elevation model."""

    @abstractmethod
    def __call__(
            self,
            dem: DEM,
    ) -> DEM:
        """Transform DEM data."""


class Compose(DEMTransform):
    """Apply DEM transformations sequentially."""

    def __init__(
            self,
            transforms: tuple[DEMTransform, ...],
    ) -> None:
        self._transforms = transforms

    def __call__(
            self,
            dem: DEM,
    ) -> DEM:
        for transform in self._transforms:
            dem = transform(dem)

        return dem


class ConvertToInt16(DEMTransform):
    """Round DEM elevations and convert them to int16."""

    def __call__(
            self,
            dem: DEM,
    ) -> DEM:
        values = np.rint(
            dem.values,
        ).astype(np.int16)

        return DEM(
            values=values,
            transform=dem.transform,
            crs=dem.crs,
            nodata=dem.nodata,
        )


class TerrainTileTransform(ABC):
    """Transform a terrain raster tile."""

    @abstractmethod
    def __call__(
            self,
            tile: RasterTile,
    ) -> RasterTile:
        """Transform terrain tile data."""
