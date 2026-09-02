import json
from dataclasses import dataclass
from pathlib import Path

from topoprofile.domain.geo import GeoPoint


@dataclass(frozen=True, slots=True)
class TerrainRegionConfig:
    region_id: str
    name: str
    center: GeoPoint
    radius_km: float
    resolution: str
    chunk_zoom: int
    max_zoom: int


def load_region_config(path: Path) -> TerrainRegionConfig:
    if not path.is_file():
        raise FileNotFoundError(f"Region config not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    return TerrainRegionConfig(
        region_id=data["region_id"],
        name=data["name"],
        center=GeoPoint(
            lon=data["center"]["lon"],
            lat=data["center"]["lat"],
        ),
        radius_km=data["radius_km"],
        resolution=data["dem"]["resolution"],
        chunk_zoom=data["terrain"]["chunk_zoom"],
        max_zoom=data["terrain"]["max_zoom"],
    )
