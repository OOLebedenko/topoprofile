from pathlib import Path
from tempfile import TemporaryDirectory

from topoprofile.geo.models import Bounds, XYZTile
from topoprofile.terrain.dem import convert_dem_to_terrarium, download_dem
from topoprofile.terrain.paths import TerrainBuildPaths, TerrainStore
from topoprofile.terrain.tiles import generate_terrain_tiles, publish_terrain_tiles


class TerrainChunkBuilder:
    """Build terrain data for one XYZ chunk."""

    def __init__(
        self,
        terrain_store: TerrainStore,
        resolution: str,
        max_zoom: int,
    ) -> None:
        self._terrain_store = terrain_store
        self._resolution = resolution
        self._max_zoom = max_zoom

    def is_built(
        self,
        chunk: XYZTile,
    ) -> bool:
        paths = self._terrain_store.chunk_paths(chunk)

        return paths.completion_marker.is_file()

    def build(
        self,
        chunk: XYZTile,
    ) -> None:
        paths = self._terrain_store.chunk_paths(chunk.bounds)

        raw_dem = self._download_dem(
            bounds=chunk.bounds,
            paths=paths,
        )

        terrarium_dem = self._convert_dem(
            raw_dem=raw_dem,
            paths=paths,
        )

        with TemporaryDirectory(
            prefix="topoprofile-terrain-",
        ) as temp_dir:
            generated_tiles = Path(temp_dir)

            self._generate_tiles(
                terrarium_dem=terrarium_dem,
                output_dir=generated_tiles,
                chunk=chunk,
            )

            self._publish_tiles(
                source_dir=generated_tiles,
                paths=paths,
                bounds=chunk.bounds,
                chunk=chunk,
            )

        self._mark_complete(paths)

    def _download_dem(
        self,
        bounds: Bounds,
        paths: TerrainBuildPaths,
    ) -> Path:
        return download_dem(
            bounds=bounds,
            resolution=self._resolution,
            output_path=paths.raw_dem,
        )

    def _convert_dem(
        self,
        raw_dem: Path,
        paths: TerrainBuildPaths,
    ) -> Path:
        return convert_dem_to_terrarium(
            input_path=raw_dem,
            output_path=paths.terrarium_dem,
        )

    def _generate_tiles(
        self,
        terrarium_dem: Path,
        output_dir: Path,
        chunk: XYZTile,
    ) -> None:
        generate_terrain_tiles(
            input_path=terrarium_dem,
            output_dir=output_dir,
            min_zoom=chunk.z,
            max_zoom=self._max_zoom,
        )

    def _publish_tiles(
        self,
        source_dir: Path,
        paths: TerrainBuildPaths,
        bounds: Bounds,
        chunk: XYZTile,
    ) -> None:
        publish_terrain_tiles(
            source_dir=source_dir,
            output_dir=paths.terrain_tiles,
            bounds=bounds,
            min_zoom=chunk.z,
            max_zoom=self._max_zoom,
        )

    def _mark_complete(
        self,
        paths: TerrainBuildPaths,
    ) -> None:
        paths.completion_marker.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        paths.completion_marker.touch()