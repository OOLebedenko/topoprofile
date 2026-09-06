import argparse
from functools import partial
from pathlib import Path

from topoprofile.config import load_region_config
from topoprofile.geo.regions import create_region
from topoprofile.terrain.task_factory import create_terrain_tasks
from topoprofile.workers.worker import SequentialWorker

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare terrain tiles for a configured region.",
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the terrain region config.",
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

    prepare_dem_task, generate_tiles_task = create_terrain_tasks(
        terrain_root=PROJECT_ROOT / "data" / "terrain",
        resolution=config.terrain.resolution,
    )

    worker = SequentialWorker()

    prepare_dem_tasks = [
        partial(
            prepare_dem_task,
            chunk,
        )
        for chunk in region.tiles
    ]
    worker.execute(prepare_dem_tasks)

    generate_tiles_tasks = [
        partial(
            generate_tiles_task,
            chunk,
            max_zoom=config.terrain.max_zoom,
        )
        for chunk in region.tiles
    ]
    worker.execute(generate_tiles_tasks)


if __name__ == "__main__":
    main()
