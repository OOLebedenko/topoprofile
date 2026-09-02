from topoprofile.geo.regions import get_region_bounds
from topoprofile.prep.dem_utils.load import TerrainRegionConfig
from topoprofile.services.dem_chunk_service import DEMChunkService
from topoprofile.terrain.chunks import RegionChunkResolver
from topoprofile.workers.worker import Worker


class TerrainPreparationService:
    def __init__(
            self,
            chunk_resolver: RegionChunkResolver,
            dem_chunk_service: DEMChunkService,
            worker: Worker,
    ) -> None:
        self.chunk_resolver = chunk_resolver
        self.dem_chunk_service = dem_chunk_service
        self.worker = worker

    def prepare_region(
            self,
            config: TerrainRegionConfig,
    ) -> None:
        bounds = get_region_bounds(
            center=config.center,
            radius_km=config.radius_km,
        )

        chunks = self.chunk_resolver.resolve(
            bounds=bounds,
            zoom=config.chunk_zoom,
        )

        self.worker.process(
            self.dem_chunk_service.prepare_chunk,
            chunks,
        )
