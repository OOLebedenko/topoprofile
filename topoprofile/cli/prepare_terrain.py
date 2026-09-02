import argparse
from pathlib import Path

from topoprofile.prep.dem_utils.load import load_region_config
from topoprofile.services.dem_chunk_service import DEMChunkService
from topoprofile.services.terrain_service import TerrainPreparationService
from topoprofile.terrain.chunks import RegionChunkResolver
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

    dem_chunk_service = DEMChunkService(
        chunks_root=PROJECT_ROOT / "data" / "terrain" / "chunks",
        tiles_root=PROJECT_ROOT / "data" / "terrain" / "tiles",
        chunk_zoom=config.chunk_zoom,
        resolution=config.resolution,
        max_zoom=config.max_zoom,
    )

    terrain_service = TerrainPreparationService(
        chunk_resolver=RegionChunkResolver(),
        dem_chunk_service=dem_chunk_service,
        worker=SequentialWorker(),
    )

    terrain_service.prepare_region(config)


if __name__ == "__main__":
    main()