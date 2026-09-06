from dataclasses import dataclass

import numpy as np
from affine import Affine
from rasterio.crs import CRS
from rasterio.transform import array_bounds

from topoprofile.geo.models import Bounds


@dataclass(frozen=True, slots=True)
class DEM:
    """Digital elevation model raster."""

    values: np.ndarray
    transform: Affine
    crs: CRS
    nodata: float | int | None = None

    @property
    def height(self) -> int:
        return self.values.shape[0]

    @property
    def width(self) -> int:
        return self.values.shape[1]

    @property
    def bounds(self) -> Bounds:
        west, south, east, north = array_bounds(
            self.height,
            self.width,
            self.transform,
        )

        return Bounds(
            west=west,
            south=south,
            east=east,
            north=north,
        )
