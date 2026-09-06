from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class OverpassData:
    """Raw OSM data returned by the Overpass API."""

    elements: tuple[dict[str, Any], ...]


@dataclass(frozen=True, slots=True)
class OSMFeatureCollection:
    """Collection of OSM features."""

    features: tuple[dict[str, Any], ...]
