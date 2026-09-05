import argparse
from pathlib import Path

from topoprofile.config import load_region_config
from topoprofile.geo.regions import create_region
from topoprofile.osm.overpass.queries.hiking_routes import HikingRouteQuery
from topoprofile.osm.task_factory import create_osm_task_manager
from topoprofile.osm.transformers.hiking_routes import HikingRouteTransformer
from topoprofile.workers.worker import SequentialWorker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OSM_CHUNKS_ROOT = PROJECT_ROOT / "data" / "osm" / "chunks"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare hiking routes from Overpass.",
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

    task_manager = create_osm_task_manager(
        query=HikingRouteQuery(),
        response_transformer=HikingRouteTransformer(),
        output_root=OSM_CHUNKS_ROOT,
        filename="hiking_routes.geojson",
    )

    tasks = task_manager.create_tasks(region)
    worker = SequentialWorker()
    worker.execute(tasks)


if __name__ == "__main__":
    main()
