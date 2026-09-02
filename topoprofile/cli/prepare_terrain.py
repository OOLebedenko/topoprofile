import argparse
from pathlib import Path

from topoprofile.terrain.builder import TerrainChunkBuilder
from topoprofile.terrain.chunks import RegionChunkResolver
from topoprofile.terrain.config import load_region_config
from topoprofile.terrain.paths import TerrainStore
from topoprofile.terrain.service import (
    RegionTerrainProcessor,
    TerrainChunkManager,
)
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

    terrain_store = TerrainStore(
        root=PROJECT_ROOT / "data" / "terrain",
    )

    chunk_builder = TerrainChunkBuilder(
        terrain_store=terrain_store,
        resolution=config.resolution,
        max_zoom=config.max_zoom,
    )

    chunk_manager = TerrainChunkManager(
        builder=chunk_builder,
    )

    terrain_processor = RegionTerrainProcessor(
        chunk_resolver=RegionChunkResolver(),
        chunk_manager=chunk_manager,
        worker=SequentialWorker(),
    )

    terrain_processor.process(config)


if __name__ == "__main__":
    main()