import argparse
from functools import partial
from pathlib import Path

from topoprofile.config import load_region_config
from topoprofile.geo.regions import create_region
from topoprofile.osm.client.queries.hiking_routes import HikingRouteQuery
from topoprofile.osm.client.queries.mountain_infrastructure import (
    MountainInfrastructureQuery,
)
from topoprofile.osm.client.queries.terrain_surface import TerrainSurfaceQuery
from topoprofile.osm.task_factory import create_osm_task
from topoprofile.osm.transforms.osm import (
    FilterHikingRoutes,
    FilterTerrainSurface,
    PrepareMountainInfrastructure,
)
from topoprofile.workers.worker import SequentialWorker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OSM_CHUNKS_ROOT = PROJECT_ROOT / "data" / "osm" / "chunks"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare OSM features for a configured region.",
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the region config.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config_path = args.config
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    config = load_region_config(config_path)

    region = create_region(
        center=config.center,
        radius_km=config.radius_km,
        zoom=config.terrain.min_zoom,
    )

    hiking_task = create_osm_task(
        query=HikingRouteQuery(),
        transform=FilterHikingRoutes(),
        osm_root=OSM_CHUNKS_ROOT,
        filename="hiking_routes.geojson",
    )

    infrastructure_task = create_osm_task(
        query=MountainInfrastructureQuery(),
        transform=PrepareMountainInfrastructure(),
        osm_root=OSM_CHUNKS_ROOT,
        filename="mountain_infrastructure.geojson",
    )

    terrain_surface_task = create_osm_task(
        query=TerrainSurfaceQuery(),
        transform=FilterTerrainSurface(),
        osm_root=OSM_CHUNKS_ROOT,
        filename="terrain_surface.geojson",
    )

    osm_tasks = (
        hiking_task,
        infrastructure_task,
        terrain_surface_task,
    )

    tasks = [
        partial(task, chunk)
        for chunk in region.tiles
        for task in osm_tasks
    ]

    worker = SequentialWorker()
    worker.execute(tasks)


if __name__ == "__main__":
    main()
