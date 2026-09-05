from topoprofile.config import RegionConfig
from topoprofile.geo.models import XYZTile
from topoprofile.geo.regions import RegionToXYZTiles, create_region
from topoprofile.terrain.builder import TerrainChunkBuilder
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
        chunk_resolver: RegionToXYZTiles,
        chunk_manager: TerrainChunkManager,
        worker: Worker,
    ) -> None:
        self._chunk_resolver = chunk_resolver
        self._chunk_manager = chunk_manager
        self._worker = worker

    def process(
        self,
        config: RegionConfig,
    ) -> None:
        region = create_region(
            center=config.center,
            radius_km=config.radius_km,
            zoom=config.terrain.min_zoom,
        )

        chunks = self._chunk_resolver.resolve(
            bounds=region.bounds,
            zoom=config.min_zoom,
        )

        self._worker.process(
            self._chunk_manager.prepare,
            chunks,
        )