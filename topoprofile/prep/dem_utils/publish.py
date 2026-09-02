import shutil
from pathlib import Path

from topoprofile.domain.terrain import Bounds
from topoprofile.geo.region_chunks import RegionChunkResolver


def publish_terrain_tiles(
    source_dir: Path,
    output_dir: Path,
    bounds: Bounds,
    min_zoom: int,
    max_zoom: int,
) -> None:
    """Publish only XYZ tiles covering the requested bounds."""
    resolver = RegionChunkResolver()

    for zoom in range(min_zoom, max_zoom + 1):
        tiles = resolver.resolve(
            bounds=bounds,
            zoom=zoom,
        )

        for tile in tiles:
            source_path = (
                source_dir
                / str(tile.z)
                / str(tile.x)
                / f"{tile.y}.png"
            )

            if not source_path.is_file():
                continue

            output_path = (
                output_dir
                / str(tile.z)
                / str(tile.x)
                / f"{tile.y}.png"
            )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source_path,
                output_path,
            )