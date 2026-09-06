import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from topoprofile.geo.models import Bounds, XYZTile
from topoprofile.geo.regions import RegionToXYZTiles
from topoprofile.processing.source import Source
from topoprofile.terrain.models import DEM
from topoprofile.terrain.store import PNGXYZTileStore, XYZGeoTIFFDEMStore
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


class GenerateTilesTask:
    """Generate and store terrain XYZ tiles using GDAL."""

    def __init__(
            self,
            source: XYZGeoTIFFDEMStore,
            store: PNGXYZTileStore,
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
