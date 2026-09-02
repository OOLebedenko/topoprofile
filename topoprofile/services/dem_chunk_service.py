from topoprofile.geo.tiles import XYZTile, parent_tile
from topoprofile.terrain.builder import TerrainChunkBuilder


class DEMChunkService:
    """Manage DEM chunks used for terrain generation."""

    def __init__(
        self,
        builder: TerrainChunkBuilder,
        chunk_zoom: int,
    ) -> None:
        self._builder = builder
        self._chunk_zoom = chunk_zoom

    def get_chunk_for_tile(
        self,
        tile: XYZTile,
    ) -> XYZTile:
        return parent_tile(
            tile=tile,
            target_zoom=self._chunk_zoom,
        )

    def is_chunk_prepared(
        self,
        chunk: XYZTile,
    ) -> bool:
        return self._builder.is_built(chunk)

    def prepare_chunk(
        self,
        chunk: XYZTile,
    ) -> None:
        if self.is_chunk_prepared(chunk):
            return

        self._builder.build(chunk)