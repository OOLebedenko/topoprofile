import json
from dataclasses import dataclass
from pathlib import Path

from topoprofile.geo.models import GeoPoint


@dataclass(frozen=True, slots=True)
class RegionTerrainConfig:
    resolution: str
    min_zoom: int
    max_zoom: int


@dataclass(frozen=True, slots=True)
class RegionConfig:
    region_id: str
    name: str
    center: GeoPoint
    radius_km: float
    terrain: RegionTerrainConfig


def load_region_config(path: Path) -> RegionConfig:
    if not path.is_file():
        raise FileNotFoundError(f"Region config not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    return RegionConfig(
        region_id=data["region_id"],
        name=data["name"],
        center=GeoPoint(
            lon=data["center"]["lon"],
            lat=data["center"]["lat"],
        ),
        radius_km=data["radius_km"],
        terrain=RegionTerrainConfig(
            resolution=data["terrain"]["resolution"],
            min_zoom=data["terrain"]["min_zoom"],
            max_zoom=data["terrain"]["max_zoom"],
        ),
    )
