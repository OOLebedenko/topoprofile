from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

from topoprofile.geo.models import XYZTile
from topoprofile.terrain.models import DEM, RasterTile


class GeoTIFFDEMStore:
    """Store digital elevation models as GeoTIFF."""

    def __init__(
            self,
            root: Path,
    ) -> None:
        self._root = root

    def path(
            self,
            name: str,
    ) -> Path:
        """Return the path of a stored DEM."""
        return self._root / f"{name}.tif"

    def exists(
            self,
            name: str,
    ) -> bool:
        """Return whether a DEM already exists."""
        return self.path(name).is_file()

    def load(
            self,
            name: str,
    ) -> DEM:
        """Load a DEM from GeoTIFF."""
        input_path = self.path(name)

        with rasterio.open(input_path) as dataset:
            return DEM(
                values=dataset.read(1),
                transform=dataset.transform,
                crs=dataset.crs,
                nodata=dataset.nodata,
            )

    def save(
            self,
            name: str,
            dem: DEM,
    ) -> Path:
        """Save a DEM as GeoTIFF."""
        output_path = self.path(name)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with rasterio.open(
                output_path,
                "w",
                driver="GTiff",
                height=dem.height,
                width=dem.width,
                count=1,
                dtype=dem.values.dtype,
                crs=dem.crs,
                transform=dem.transform,
                nodata=dem.nodata,
        ) as dataset:
            dataset.write(
                dem.values,
                1,
            )

        return output_path


class PNGXYZTileStore:
    """Store raster XYZ tiles as PNG."""

    def __init__(
            self,
            root: Path,
    ) -> None:
        self._root = root

    def path(
            self,
            tile: XYZTile,
    ) -> Path:
        """Return the path of a stored PNG tile."""
        return (
                self._root
                / str(tile.z)
                / str(tile.x)
                / f"{tile.y}.png"
        )

    def exists(
            self,
            tile: XYZTile,
    ) -> bool:
        """Return whether a PNG tile already exists."""
        return self.path(tile).is_file()

    def load(
            self,
            tile: XYZTile,
    ) -> RasterTile:
        """Load a PNG tile."""
        input_path = self.path(tile)

        with Image.open(input_path) as image:
            values = np.array(image)

        if values.ndim == 2:
            values = values[np.newaxis, ...]
        else:
            values = np.moveaxis(
                values,
                -1,
                0,
            )

        return RasterTile(
            tile=tile,
            values=values,
        )

    def save(
            self,
            raster_tile: RasterTile,
    ) -> Path:
        """Save a raster XYZ tile as PNG."""
        output_path = self.path(raster_tile.tile)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if raster_tile.nbands == 1:
            values = raster_tile.values[0]
        else:
            values = np.moveaxis(
                raster_tile.values,
                0,
                -1,
            )

        image = Image.fromarray(values)
        image.save(
            output_path,
            format="PNG",
        )

        return output_path
