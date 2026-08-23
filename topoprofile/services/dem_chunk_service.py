from pathlib import Path

from topoprofile.domain.terrain import TerrainRequest, XYZTile
from topoprofile.geo.tiles import parent_tile, xyz_to_bounds
from topoprofile.prep.terrain_paths import get_dem_chunk_paths
from topoprofile.prep.terrain_pipeline import prepare_terrain


class DEMChunkService:
    """Manage DEM chunks used for terrain generation."""

    def __init__(
        self,
        chunks_root: Path,
        tiles_root: Path,
        chunk_zoom: int,
        resolution: str,
        max_zoom: int,
    ) -> None:
        self._chunks_root = chunks_root
        self._tiles_root = tiles_root
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
        return self._completion_marker(chunk).is_file()

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

        paths = get_dem_chunk_paths(
            chunks_root=self._chunks_root,
            tiles_root=self._tiles_root,
            chunk=chunk,
        )

        prepare_terrain(
            request=request,
            paths=paths,
        )

        marker = self._completion_marker(chunk)
        marker.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        marker.touch()

    def _completion_marker(
        self,
        chunk: XYZTile,
    ) -> Path:
        return (
            self._chunks_root / str(chunk.z) / str(chunk.x) / str(chunk.y) / ".complete"
        )
