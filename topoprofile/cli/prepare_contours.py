import argparse
from functools import partial
from pathlib import Path

from topoprofile.config import load_region_config
from topoprofile.geo.regions import create_region
from topoprofile.terrain.task_factory import create_contours_task
from topoprofile.workers.worker import SequentialWorker

# Project root used to resolve config and data paths.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Vertical distance between neighboring contour lines, in meters.
CONTOUR_INTERVAL = 100

# Geometry simplification tolerance in geographic coordinate units.
SIMPLIFY_TOLERANCE = 0.0002

# Earth relief DEM resolution used for contour generation.
RESOLUTION = "03s"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare terrain contours for a configured region.",
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

    prepare_contours_task = create_contours_task(
        terrain_root=PROJECT_ROOT / "data" / "terrain",
        contour_interval=CONTOUR_INTERVAL,
        simplify_tolerance=SIMPLIFY_TOLERANCE,
        resolution=RESOLUTION,
    )

    tasks = [
        partial(
            prepare_contours_task,
            chunk,
        )
        for chunk in region.tiles
    ]

    worker = SequentialWorker()
    worker.execute(tasks)


if __name__ == "__main__":
    main()
