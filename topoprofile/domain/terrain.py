from dataclasses import dataclass

from topoprofile.geo.models import Bounds


@dataclass(frozen=True, slots=True)
class TerrainRequest:
    """Parameters describing terrain data to prepare."""

    bounds: Bounds
    resolution: str
    min_zoom: int
    max_zoom: int


@dataclass(frozen=True, slots=True)
class XYZTile:
    """XYZ terrain tile coordinates."""

    z: int
    x: int
    y: int
