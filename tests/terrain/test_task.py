import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Protocol

from topoprofile.geo.models import Bounds
from topoprofile.geo.regions import RegionToXYZTiles
from topoprofile.processing.source import Source
from topoprofile.terrain.models import DEM
from topoprofile.terrain.store import GeoTIFFDEMStore, PNGXYZTileStore
from topoprofile.terrain.transforms import DEMTransform, TerrainTileTransform


class Task[**ParamsT, ResultT](Protocol):
    """Executable processing task."""

    def __call__(
            self,
            *args: ParamsT.args,
            **kwargs: ParamsT.kwargs,
    ) -> ResultT:
        """Execute the task."""
        ...


class PrepareDEMTask:
    """Prepare and store digital elevation model data."""

    def __init__(
            self,
            source: Source[Bounds, DEM],
            store: GeoTIFFDEMStore,
            transform: DEMTransform | None = None,
    ) -> None:
        self._source = source
        self._store = store
        self._transform = transform

    def __call__(
            self,
            name: str,
            bounds: Bounds,
    ) -> Path:
        if self._store.exists(name):
            return self._store.path(name)

        dem = self._source.load(bounds)

        if self._transform is not None:
            dem = self._transform(dem)

        return self._store.save(
            name=name,
            dem=dem,
        )


class GenerateTilesTask:
    """Generate and store terrain XYZ tiles using GDAL."""

    def __init__(
            self,
            source: GeoTIFFDEMStore,
            store: PNGXYZTileStore,
            transform: TerrainTileTransform | None = None,
    ) -> None:
        self._source = source
        self._store = store
        self._transform = transform

    def __call__(
            self,
            name: str,
            bounds: Bounds,
            min_zoom: int,
            max_zoom: int,
    ) -> None:
        if self._tiles_exist(
                bounds=bounds,
                min_zoom=min_zoom,
                max_zoom=max_zoom,
        ):
            return

        input_path = self._source.path(name)

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
                min_zoom=min_zoom,
                max_zoom=max_zoom,
            )
            self._publish_tiles(
                source_dir=generated_tiles,
                bounds=bounds,
                min_zoom=min_zoom,
                max_zoom=max_zoom,
            )

        if self._transform is not None:
            raise NotImplementedError(
                "Terrain tile transformations are not implemented yet."
            )

    def _tiles_exist(
            self,
            bounds: Bounds,
            min_zoom: int,
            max_zoom: int,
    ) -> bool:
        for zoom in range(min_zoom, max_zoom + 1):
            tiles = RegionToXYZTiles.resolve(
                bounds=bounds,
                zoom=zoom,
            )

            if not all(
                    self._store.exists(tile)
                    for tile in tiles
            ):
                return False

        return True

    def _generate_tiles(
            self,
            input_path: Path,
            output_dir: Path,
            min_zoom: int,
            max_zoom: int,
    ) -> None:
        command = [
            "gdal2tiles.py",
            "--xyz",
            "--resampling=near",
            "--processes=4",
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
            bounds: Bounds,
            min_zoom: int,
            max_zoom: int,
    ) -> None:
        for zoom in range(min_zoom, max_zoom + 1):
            tiles = RegionToXYZTiles.resolve(
                bounds=bounds,
                zoom=zoom,
            )

            for tile in tiles:
                source_path = (
                        source_dir
                        / str(tile.z)
                        / str(tile.x)
                        / f"{tile.y}.png"
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
