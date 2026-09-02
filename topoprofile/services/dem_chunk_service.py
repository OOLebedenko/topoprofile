from topoprofile.geo.tiles import XYZTile, parent_tile, xyz_to_bounds
from topoprofile.prep.terrain_pipeline import prepare_terrain
from topoprofile.terrain.models import TerrainRequest
from topoprofile.terrain.paths import TerrainStore


class DEMChunkService:
    """Manage DEM chunks used for terrain generation."""

    def __init__(
        self,
        terrain_store: TerrainStore,
        chunk_zoom: int,
        resolution: str,
        max_zoom: int,
    ) -> None:
        self._terrain_store = terrain_store
        self._chunk_zoom = chunk_zoom
        self._resolution = resolution
        self._max_zoom = max_zoom

    def get_chunk_for_tile(
        self,
        tile: XYZTile,
    ) -> XYZTile:
        """Return the DEM chunk containing the requested tile."""
        return parent_tile(
            tile=tile,
            target_zoom=self._chunk_zoom,
        )

    def is_chunk_prepared(
        self,
        chunk: XYZTile,
    ) -> bool:
        """Return whether terrain tiles for the DEM chunk are prepared."""
        paths = self._terrain_store.chunk_paths(chunk)

        return paths.completion_marker.is_file()

    def prepare_chunk(
        self,
        chunk: XYZTile,
    ) -> None:
        """Prepare terrain data for a DEM chunk."""
        if self.is_chunk_prepared(chunk):
            return

        request = TerrainRequest(
            bounds=xyz_to_bounds(chunk),
            resolution=self._resolution,
            min_zoom=chunk.z,
            max_zoom=self._max_zoom,
        )

        paths = self._terrain_store.chunk_paths(chunk)

        prepare_terrain(
            request=request,
            paths=paths,
        )

        paths.completion_marker.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        paths.completion_marker.touch()