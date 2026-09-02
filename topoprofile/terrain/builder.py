from topoprofile.geo.tiles import XYZTile, xyz_to_bounds
from topoprofile.prep.terrain_pipeline import prepare_terrain
from topoprofile.terrain.models import TerrainRequest
from topoprofile.terrain.paths import TerrainStore


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