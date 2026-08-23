from dataclasses import dataclass
from pathlib import Path

from topoprofile.domain.terrain import XYZTile


@dataclass(frozen=True, slots=True)
class TerrainPaths:
    """Paths used by the terrain preparation pipeline."""

    raw_dem: Path
    terrarium_dem: Path
    terrain_tiles: Path


def get_dem_chunk_paths(
        chunks_root: Path,
        tiles_root: Path,
        chunk: XYZTile,
) -> TerrainPaths:
    """Build terrain preparation paths for one DEM chunk."""
    chunk_root = (
            chunks_root
            / str(chunk.z)
            / str(chunk.x)
            / str(chunk.y)
    )

    return TerrainPaths(
        raw_dem=chunk_root / "raw" / "dem.tif",
        terrarium_dem=chunk_root / "prepared" / "dem_terrarium.tif",
        terrain_tiles=tiles_root,
    )
