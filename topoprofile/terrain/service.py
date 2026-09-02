from topoprofile.geo.regions import get_region_bounds
from topoprofile.geo.tiles import XYZTile, parent_tile
from topoprofile.terrain.builder import TerrainChunkBuilder
from topoprofile.terrain.chunks import RegionChunkResolver
from topoprofile.terrain.config import TerrainRegionConfig
from topoprofile.workers.worker import Worker


class TerrainChunkManager:

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


class RegionTerrainProcessor:

    def __init__(
        self,
        chunk_resolver: RegionChunkResolver,
        chunk_manager: TerrainChunkManager,
        worker: Worker,
    ) -> None:
        self._chunk_resolver = chunk_resolver
        self._chunk_manager = chunk_manager
        self._worker = worker

    def prepare_region(
        self,
        config: TerrainRegionConfig,
    ) -> None:
        bounds = get_region_bounds(
            center=config.center,
            radius_km=config.radius_km,
        )

        chunks = self._chunk_resolver.resolve(
            bounds=bounds,
            zoom=config.chunk_zoom,
        )

        self._worker.process(
            self._chunk_manager.prepare_chunk,
            chunks,
        )