from pathlib import Path
from tempfile import TemporaryDirectory

from topoprofile.geo.tiles import XYZTile, xyz_to_bounds
from topoprofile.prep.dem_utils.convert import convert_dem_to_terrarium
from topoprofile.prep.dem_utils.download import download_dem
from topoprofile.prep.dem_utils.generate import generate_terrain_tiles
from topoprofile.prep.dem_utils.publish import publish_terrain_tiles
from topoprofile.terrain.models import TerrainRequest
from topoprofile.terrain.paths import TerrainBuildPaths, TerrainStore


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
        paths = self._terrain_store.chunk_paths(chunk)

        request = TerrainRequest(
            bounds=xyz_to_bounds(chunk),
            resolution=self._resolution,
            min_zoom=chunk.z,
            max_zoom=self._max_zoom,
        )

        prepare_terrain(
            request=request,
            paths=paths,
        )

        paths.completion_marker.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        paths.completion_marker.touch()


def prepare_terrain(
    request: TerrainRequest,
    paths: TerrainBuildPaths,
) -> None:
    """Prepare terrain data for arbitrary geographic bounds."""
    raw_dem = download_dem(
        bounds=request.bounds,
        resolution=request.resolution,
        output_path=paths.raw_dem,
    )

    terrarium_dem = convert_dem_to_terrarium(
        input_path=raw_dem,
        output_path=paths.terrarium_dem,
    )

    with TemporaryDirectory(
        prefix="topoprofile-terrain-",
    ) as temp_dir:
        generated_tiles = Path(temp_dir)

        generate_terrain_tiles(
            input_path=terrarium_dem,
            output_dir=generated_tiles,
            min_zoom=request.min_zoom,
            max_zoom=request.max_zoom,
        )

        publish_terrain_tiles(
            source_dir=generated_tiles,
            output_dir=paths.terrain_tiles,
            bounds=request.bounds,
            min_zoom=request.min_zoom,
            max_zoom=request.max_zoom,
        )
