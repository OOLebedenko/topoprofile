from dataclasses import dataclass
from pathlib import Path

from topoprofile.geo.models import XYZTile


@dataclass(frozen=True, slots=True)
class TerrainBuildPaths:
    raw_dem: Path
    terrarium_dem: Path
    terrain_tiles: Path
    completion_marker: Path


@dataclass(frozen=True, slots=True)
class TerrainStore:
    """Terrain data storage layout."""

    root: Path

    @property
    def tiles_root(self) -> Path:
        return self.root / "tiles"

    def chunk_paths(
        self,
        chunk: XYZTile,
    ) -> TerrainBuildPaths:
        chunk_root = (
            self.root
            / "chunks"
            / str(chunk.z)
            / str(chunk.x)
            / str(chunk.y)
        )

        return TerrainBuildPaths(
            raw_dem=chunk_root / "raw" / "dem.tif",
            terrarium_dem=chunk_root / "prepared" / "dem_terrarium.tif",
            terrain_tiles=self.tiles_root,
            completion_marker=chunk_root / ".complete",
        )