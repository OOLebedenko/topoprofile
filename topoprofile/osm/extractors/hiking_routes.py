import logging
from typing import Any

from topoprofile.geo.models import Bounds
from topoprofile.osm.extractors.base import OverpassExtractor
from topoprofile.osm.geojson import geometry_type, is_valid_geometry

logger = logging.getLogger(__name__)

ROUTE_TYPES = {
    "foot",
    "hiking",
}

ROUTE_GEOMETRIES = {
    "LineString",
    "MultiLineString",
}

OVERPASS_QUERY_TIMEOUT_SECONDS = 180


class HikingRouteExtractor(OverpassExtractor):
    """Extract renderable hiking routes from OSM."""

    def _build_query(self, bounds: Bounds) -> str:
        """Build an Overpass query for hiking routes."""
        bbox = (
            f"{bounds.south},"
            f"{bounds.west},"
            f"{bounds.north},"
            f"{bounds.east}"
        )
        route_values = "|".join(sorted(ROUTE_TYPES))

        return f"""
[out:json][timeout:{OVERPASS_QUERY_TIMEOUT_SECONDS}];

relation
  ["type"="route"]
  ["route"~"^({route_values})$"]
  ({bbox});

out body geom;
""".strip()

    def _process(self, geojson: dict[str, Any]) -> dict[str, Any]:
        """Keep only renderable hiking routes."""
        features = geojson["features"]

        filtered = [
            feature
            for feature in features
            if self._is_renderable(feature)
        ]

        logger.info(
            "Hiking routes: total=%d, kept=%d, rejected=%d",
            len(features),
            len(filtered),
            len(features) - len(filtered),
        )

        return {
            "type": "FeatureCollection",
            "features": filtered,
        }

    @staticmethod
    def _is_renderable(feature: dict[str, Any]) -> bool:
        """Return whether a hiking route can be rendered."""
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return False

        route = properties.get("route")
        feature_geometry = geometry_type(geometry)

        return (
                route in ROUTE_TYPES
                and feature_geometry in ROUTE_GEOMETRIES
        )
