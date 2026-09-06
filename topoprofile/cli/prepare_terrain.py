import argparse
from pathlib import Path

from topoprofile.config import load_region_config
from topoprofile.geo.regions import create_region
from topoprofile.terrain.task_factory import create_terrain_task_managers
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

    # Resolve config path relative to the project root.
    config_path = args.config
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    config = load_region_config(config_path)

    # Build the geographic region and resolve its covering XYZ chunks
    # at the configured minimum zoom.
    region = create_region(
        center=config.center,
        radius_km=config.radius_km,
        zoom=config.terrain.min_zoom,
    )

    # Configure terrain preparation tasks.
    prepare_dem_manager, generate_tiles_manager = (
        create_terrain_task_managers(
            terrain_root=PROJECT_ROOT / "data" / "terrain",
            resolution=config.terrain.resolution,
        )
    )

    worker = SequentialWorker()

    # Prepare one Terrarium DEM for every XYZ chunk.
    prepare_dem_tasks = [
        prepare_dem_manager.create_task(
            name=f"{chunk.z}/{chunk.x}/{chunk.y}/dem_terrarium",
            bounds=chunk.bounds,
        )
        for chunk in region.tiles
    ]
    worker.execute(prepare_dem_tasks)

    # Generate the final XYZ tile pyramid from each prepared DEM.
    generate_tiles_tasks = [
        generate_tiles_manager.create_task(
            name=f"{chunk.z}/{chunk.x}/{chunk.y}/dem_terrarium",
            bounds=chunk.bounds,
            min_zoom=chunk.z,
            max_zoom=config.terrain.max_zoom,
        )
        for chunk in region.tiles
    ]
    worker.execute(generate_tiles_tasks)


if __name__ == "__main__":
    main()
