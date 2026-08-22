from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Bounds:
    """Geographic bounds in west, south, east, north order."""

    west: float
    south: float
    east: float
    north: float


@dataclass(frozen=True, slots=True)
class TerrainRequest:
    """Parameters describing terrain data to prepare."""

    bounds: Bounds
    resolution: str
    min_zoom: int
    max_zoom: int
