from pathlib import Path

from topoprofile.processing.transforms import Compose
from topoprofile.terrain.source import EarthReliefSource
from topoprofile.terrain.store import (
    WebPXYZTileStore,
    XYZContourStore,
    XYZGeoTIFFDEMStore,
)
from topoprofile.terrain.task import (
    GenerateTilesTask,
    PrepareContoursTask,
    PrepareDEMTask,
)
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

    tile_store = WebPXYZTileStore(
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

    return (
        prepare_dem_task,
        generate_tiles_task,
    )


def create_contours_task(
        terrain_root: Path,
        contour_interval: int,
        simplify_tolerance: float = 0.0001,
        resolution: str = "03s",
) -> PrepareContoursTask:
    """Create terrain contour preparation task."""
    contour_store = XYZContourStore(
        root=terrain_root / "contours",
    )

    return PrepareContoursTask(
        source=EarthReliefSource(
            resolution=resolution,
        ),
        store=contour_store,
        transform=ConvertToInt16(),
        interval=contour_interval,
        simplify_tolerance=simplify_tolerance,
    )
