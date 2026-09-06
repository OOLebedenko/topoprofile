from dataclasses import dataclass

import numpy as np
from affine import Affine
from rasterio.crs import CRS
from rasterio.transform import array_bounds

from topoprofile.geo.models import Bounds, XYZTile


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


@dataclass(frozen=True, slots=True)
class RasterTile:
    """Raster data associated with an XYZ tile."""

    tile: XYZTile
    values: np.ndarray

    def __post_init__(self) -> None:
        if self.values.ndim != 3:
            raise ValueError(
                "RasterTile values must have shape "
                "(bands, height, width)."
            )

    @property
    def nbands(self) -> int:
        return self.values.shape[0]

    @property
    def height(self) -> int:
        return self.values.shape[1]

    @property
    def width(self) -> int:
        return self.values.shape[2]
