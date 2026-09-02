from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GeoPoint:
    lon: float
    lat: float
