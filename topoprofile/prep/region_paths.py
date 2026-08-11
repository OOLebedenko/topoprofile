from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"


@dataclass(frozen=True, slots=True)
class RegionPaths:
    dem_config: Path
    raw: Path
    prepared: Path
    tiles: Path
    terrain_tiles: Path


def get_region_paths(region_id: str) -> RegionPaths:
    region_config_dir = CONFIG_DIR / "regions" / region_id
    region_data_dir = DATA_DIR / "regions" / region_id
    tiles_dir = region_data_dir / "tiles"

    return RegionPaths(
        dem_config=region_config_dir / "dem.json",
        raw=region_data_dir / "raw",
        prepared=region_data_dir / "prepared",
        tiles=tiles_dir,
        terrain_tiles=tiles_dir / "terrain",
    )
