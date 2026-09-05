import logging
from typing import Any

from topoprofile.geo.models import Bounds
from topoprofile.osm.geojson import (
    LINE_GEOMETRY_TYPES,
    GeoJSON,
    clip_to_bounds,
    geometry_type,
    is_valid_geometry,
)
from topoprofile.osm.tags import (
    HIKING_ROUTE_TYPES,
    HIKING_TRAIL_TYPES,
)
from topoprofile.osm.transformers.base import OSMFeatureTransformer

logger = logging.getLogger(__name__)


class HikingRouteTransformer(OSMFeatureTransformer):
    """Transform hiking route GeoJSON into renderable features."""

    def transform(
            self,
            geojson: GeoJSON,
            bounds: Bounds,
    ) -> GeoJSON:
        features = geojson["features"]

        filtered = [
            feature
            for feature in features
            if self._is_renderable(feature)
        ]

        result = {
            "type": "FeatureCollection",
            "features": filtered,
        }

        result = clip_to_bounds(
            result,
            bounds,
        )

        logger.info(
            "Hiking routes: total=%d, kept=%d, rejected=%d",
            len(features),
            len(result["features"]),
            len(features) - len(filtered),
        )

        return result

    @staticmethod
    def _is_renderable(
            feature: dict[str, Any],
    ) -> bool:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return False

        feature_geometry = geometry_type(geometry)

        if feature_geometry not in LINE_GEOMETRY_TYPES:
            return False

        route = properties.get("route")
        highway = properties.get("highway")
        aerialway = properties.get("aerialway")

        return (
                route in HIKING_ROUTE_TYPES
                or highway in HIKING_TRAIL_TYPES
                or aerialway is not None
        )
