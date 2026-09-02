from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GeoPoint:
    lon: float
    lat: float


@dataclass(frozen=True, slots=True)
class Bounds:
    """Geographic bounds in west, south, east, north order."""

    west: float
    south: float
    east: float
    north: float
