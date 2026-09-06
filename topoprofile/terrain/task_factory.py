from pathlib import Path

from topoprofile.terrain.source import EarthReliefSource
from topoprofile.terrain.store import GeoTIFFDEMStore, PNGXYZTileStore
from topoprofile.terrain.task import GenerateTilesTask, PrepareDEMTask
from topoprofile.terrain.task_manager import TerrainTaskManager
from topoprofile.terrain.transforms import (
    Compose,
    ConvertToInt16,
    TerrariumTransform,
)


def create_terrain_task_managers(
        terrain_root: Path,
        resolution: str,
) -> tuple[TerrainTaskManager, TerrainTaskManager]:
    """Create configured terrain task managers."""

    # Intermediate DEM rasters are stored by XYZ coordinates:
    # dem/{z}/{x}/{y}/dem_terrarium.tif
    dem_store = GeoTIFFDEMStore(
        root=terrain_root / "dem",
    )

    # Final terrain tiles form a global XYZ tile pyramid:
    # tiles/{z}/{x}/{y}.png
    tile_store = PNGXYZTileStore(
        root=terrain_root / "tiles",
    )

    # Download DEM, convert elevations to int16 and then
    # encode the raster using Terrarium representation.
    prepare_dem_manager = TerrainTaskManager(
        task=PrepareDEMTask(
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
        ),
    )

    # Generate PNG XYZ tiles from the prepared Terrarium DEM.
    generate_tiles_manager = TerrainTaskManager(
        task=GenerateTilesTask(
            source=dem_store,
            store=tile_store,
        ),
    )

    return prepare_dem_manager, generate_tiles_manager
