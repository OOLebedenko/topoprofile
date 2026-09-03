from topoprofile.geo.chunks import RegionChunkResolver
from topoprofile.geo.regions import get_region_bounds
from topoprofile.geo.tiles import XYZTile
from topoprofile.terrain.builder import TerrainChunkBuilder
from topoprofile.terrain.config import TerrainRegionConfig
from topoprofile.terrain.resolver import RegionChunkResolver
from topoprofile.workers.worker import Worker


class TerrainChunkManager:

    def __init__(
        self,
        builder: TerrainChunkBuilder,
    ) -> None:
        self._builder = builder


    def is_prepared(
        self,
        chunk: XYZTile,
    ) -> bool:
        return self._builder.is_built(chunk)

    def prepare(
        self,
        chunk: XYZTile,
    ) -> None:
        if self.is_prepared(chunk):
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

    def process(
        self,
        config: TerrainRegionConfig,
    ) -> None:
        bounds = get_region_bounds(
            center=config.center,
            radius_km=config.radius_km,
        )

        chunks = self._chunk_resolver.resolve(
            bounds=bounds,
            zoom=config.min_zoom,
        )

        self._worker.process(
            self._chunk_manager.prepare,
            chunks,
        )