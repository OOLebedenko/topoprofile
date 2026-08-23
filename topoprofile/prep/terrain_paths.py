from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TerrainPaths:
    """Paths used by the terrain preparation pipeline."""

    raw_dem: Path
    terrarium_dem: Path
    terrain_tiles: Path
