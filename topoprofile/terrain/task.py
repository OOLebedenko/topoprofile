import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import rasterio

from topoprofile.geo.models import Bounds, XYZTile
from topoprofile.geo.regions import RegionToXYZTiles
from topoprofile.processing.source import Source
from topoprofile.terrain.models import DEM
from topoprofile.terrain.store import (
    WebPXYZTileStore,
    XYZContourStore,
    XYZGeoTIFFDEMStore,
)
from topoprofile.terrain.transforms import DEMTransform


class PrepareDEMTask:
    """Prepare and store digital elevation model data."""

    def __init__(
            self,
            source: Source[Bounds, DEM],
            store: XYZGeoTIFFDEMStore,
            transform: DEMTransform | None = None,
    ) -> None:
        self._source = source
        self._store = store
        self._transform = transform

    def __call__(
            self,
            chunk: XYZTile,
    ) -> Path:
        if self._store.exists(chunk):
            return self._store.path(chunk)

        dem = self._source.load(chunk.bounds)

        if self._transform is not None:
            dem = self._transform(dem)

        return self._store.save(
            tile=chunk,
            dem=dem,
        )


class PrepareContoursTask:
    """Prepare and store terrain contour lines."""

    def __init__(
            self,
            source: Source[Bounds, DEM],
            store: XYZContourStore,
            interval: int,
            simplify_tolerance: float,
            transform: DEMTransform | None = None,
    ) -> None:
        self._source = source
        self._store = store
        self._interval = interval
        self._simplify_tolerance = simplify_tolerance
        self._transform = transform

    def __call__(
            self,
            chunk: XYZTile,
    ) -> Path:
        if self._store.exists(chunk):
            return self._store.path(chunk)

        dem = self._source.load(chunk.bounds)

        if self._transform is not None:
            dem = self._transform(dem)

        output_path = self._store.path(chunk)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with TemporaryDirectory(
                prefix="topoprofile-contours-",
        ) as temp_dir:
            input_path = Path(temp_dir) / "dem.tif"
            contours_path = Path(temp_dir) / "contours.geojson"

            self._write_dem(
                dem=dem,
                output_path=input_path,
            )
            self._generate_contours(
                input_path=input_path,
                output_path=contours_path,
            )
            self._simplify_contours(
                input_path=contours_path,
                output_path=output_path,
            )

        return output_path

    @staticmethod
    def _write_dem(
            dem: DEM,
            output_path: Path,
    ) -> None:
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

    def _generate_contours(
            self,
            input_path: Path,
            output_path: Path,
    ) -> None:
        command = [
            "gdal_contour",
            "-a",
            "elevation",
            "-i",
            str(self._interval),
            "-f",
            "GeoJSON",
            str(input_path),
            str(output_path),
        ]

        subprocess.run(
            command,
            check=True,
        )

    def _simplify_contours(
            self,
            input_path: Path,
            output_path: Path,
    ) -> None:
        command = [
            "ogr2ogr",
            "-simplify",
            str(self._simplify_tolerance),
            str(output_path),
            str(input_path),
        ]

        subprocess.run(
            command,
            check=True,
        )


class GenerateTilesTask:
    """Generate and store terrain XYZ tiles using GDAL."""

    def __init__(
            self,
            source: XYZGeoTIFFDEMStore,
            store: WebPXYZTileStore,
    ) -> None:
        self._source = source
        self._store = store

    def __call__(
            self,
            chunk: XYZTile,
            max_zoom: int,
            processes: int = 4,
    ) -> None:
        if self._tiles_exist(
                chunk=chunk,
                max_zoom=max_zoom,
        ):
            return

        input_path = self._source.path(chunk)

        if not input_path.is_file():
            raise FileNotFoundError(
                f"Terrain raster not found: {input_path}"
            )

        with TemporaryDirectory(
                prefix="topoprofile-terrain-",
        ) as temp_dir:
            generated_tiles = Path(temp_dir)

            self._generate_tiles(
                input_path=input_path,
                output_dir=generated_tiles,
                min_zoom=chunk.z,
                max_zoom=max_zoom,
                processes=processes,
            )
            self._publish_tiles(
                source_dir=generated_tiles,
                chunk=chunk,
                max_zoom=max_zoom,
            )

    def _tiles_exist(
            self,
            chunk: XYZTile,
            max_zoom: int,
    ) -> bool:
        for zoom in range(chunk.z, max_zoom + 1):
            tiles = RegionToXYZTiles.resolve(
                bounds=chunk.bounds,
                zoom=zoom,
            )

            if not all(
                    self._store.exists(tile)
                    for tile in tiles
            ):
                return False

        return True

    @staticmethod
    def _generate_tiles(
            input_path: Path,
            output_dir: Path,
            min_zoom: int,
            max_zoom: int,
            processes: int,
    ) -> None:
        command = [
            "gdal2tiles.py",
            "--xyz",
            "--resampling=near",
            "--tiledriver=WEBP",
            "--webp-lossless",
            f"--processes={processes}",
            "-z",
            f"{min_zoom}-{max_zoom}",
            str(input_path),
            str(output_dir),
        ]

        subprocess.run(
            command,
            check=True,
        )

    def _publish_tiles(
            self,
            source_dir: Path,
            chunk: XYZTile,
            max_zoom: int,
    ) -> None:
        for zoom in range(chunk.z, max_zoom + 1):
            tiles = RegionToXYZTiles.resolve(
                bounds=chunk.bounds,
                zoom=zoom,
            )

            for tile in tiles:
                source_path = (
                        source_dir
                        / str(tile.z)
                        / str(tile.x)
                        / f"{tile.y}.webp"
                )

                if not source_path.is_file():
                    continue

                output_path = self._store.path(tile)
                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                shutil.copy2(
                    source_path,
                    output_path,
                )
