from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

from topoprofile.geo.models import XYZTile
from topoprofile.processing.atomic import atomic_path
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

        with atomic_path(output_path) as temporary_path, rasterio.open(
                temporary_path,
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
                dataset.write(
                    dem.values,
                )

        return output_path


class WebPXYZTileStore:
    """Store raster XYZ tiles as lossless WebP."""

    def __init__(
            self,
            root: Path,
    ) -> None:
        self._root = root

    def path(
            self,
            tile: XYZTile,
    ) -> Path:
        """Return the path of a stored WebP tile."""
        return (
                self._root
                / str(tile.z)
                / str(tile.x)
                / f"{tile.y}.webp"
        )

    def exists(
            self,
            tile: XYZTile,
    ) -> bool:
        """Return whether a WebP tile already exists."""
        return self.path(tile).is_file()

    def load(
            self,
            tile: XYZTile,
    ) -> RasterTile:
        """Load a WebP tile."""
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
        """Save a raster XYZ tile as lossless WebP."""
        output_path = self.path(
            raster_tile.tile,
        )

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

        image = Image.fromarray(
            values,
        )

        with atomic_path(output_path) as temporary_path:
            image.save(
                temporary_path,
                format="WEBP",
                lossless=True,
            )

        return output_path


class XYZContourStore:
    """Store terrain contours as GeoJSON in XYZ chunk structure."""

    def __init__(
            self,
            root: Path,
            filename: str = "contours.pbf",
    ) -> None:
        self._root = root
        self._filename = filename

    def path(
            self,
            chunk: XYZTile,
    ) -> Path:
        return (
                self._root
                / str(chunk.z)
                / str(chunk.x)
                / str(chunk.y)
                / self._filename
        )

    def exists(
            self,
            chunk: XYZTile,
    ) -> bool:
        return self.path(chunk).is_file()
