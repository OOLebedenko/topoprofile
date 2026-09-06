from pathlib import Path

from topoprofile.processing.transforms import Compose
from topoprofile.terrain.source import EarthReliefSource
from topoprofile.terrain.store import PNGXYZTileStore, XYZGeoTIFFDEMStore
from topoprofile.terrain.task import GenerateTilesTask, PrepareDEMTask
from topoprofile.terrain.transforms import (
    ConvertToInt16,
    TerrariumTransform,
)


def create_terrain_tasks(
        terrain_root: Path,
        resolution: str,
) -> tuple[PrepareDEMTask, GenerateTilesTask]:
    """Create configured terrain processing tasks."""

    dem_store = XYZGeoTIFFDEMStore(
        root=terrain_root / "dem",
    )

    tile_store = PNGXYZTileStore(
        root=terrain_root / "tiles",
    )

    prepare_dem_task = PrepareDEMTask(
        source=EarthReliefSource(
            resolution=resolution,
        ),
        store=dem_store,
        transform=Compose(
            transforms=(
                ConvertToInt16(),
                TerrariumTransform(),
            ),
        ),
    )

    generate_tiles_task = GenerateTilesTask(
        source=dem_store,
        store=tile_store,
    )

    return prepare_dem_task, generate_tiles_task
