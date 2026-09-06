from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

from topoprofile.geo.models import XYZTile
from topoprofile.terrain.models import DEM, RasterTile


class XYZGeoTIFFDEMStore:
    """Store DEM chunks as GeoTIFF in XYZ tile structure."""

    def __init__(
            self,
            root: Path,
            filename: str = "dem_terrarium.tif",
    ) -> None:
        self._root = root
        self._filename = filename

    def path(
            self,
            tile: XYZTile,
    ) -> Path:
        return (
                self._root
                / str(tile.z)
                / str(tile.x)
                / str(tile.y)
                / self._filename
        )

    def exists(
            self,
            tile: XYZTile,
    ) -> bool:
        return self.path(tile).is_file()

    def load(
            self,
            tile: XYZTile,
    ) -> DEM:
        input_path = self.path(tile)

        with rasterio.open(input_path) as dataset:
            if dataset.count == 1:
                values = dataset.read(1)
            else:
                values = dataset.read()

            return DEM(
                values=values,
                transform=dataset.transform,
                crs=dataset.crs,
                nodata=dataset.nodata,
            )

    def save(
            self,
            tile: XYZTile,
            dem: DEM,
    ) -> Path:
        output_path = self.path(tile)
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
                count=dem.count,
                dtype=dem.values.dtype,
                crs=dem.crs,
                transform=dem.transform,
                nodata=dem.nodata,
        ) as dataset:
            if dem.count == 1:
                dataset.write(
                    dem.values,
                    1,
                )
            else:
                dataset.write(dem.values)

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
