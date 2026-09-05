import logging
from typing import Any

from topoprofile.geo.models import Bounds
from topoprofile.osm.geojson import (
    LINE_GEOMETRY_TYPES,
    POLYGON_GEOMETRY_TYPES,
    GeoJSON,
    clip_to_bounds,
    geometry_type,
    is_valid_geometry,
)
from topoprofile.osm.tags import (
    TERRAIN_AREA_TYPES,
    TERRAIN_LINE_TYPES,
)
from topoprofile.osm.transformers.base import OSMFeatureTransformer

logger = logging.getLogger(__name__)


class TerrainSurfaceTransformer(OSMFeatureTransformer):
    """Transform terrain surface GeoJSON into renderable features."""

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
            "Terrain surface features: total=%d, kept=%d, rejected=%d",
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

        natural = properties.get("natural")
        feature_geometry = geometry_type(geometry)

        if natural in TERRAIN_AREA_TYPES:
            return feature_geometry in POLYGON_GEOMETRY_TYPES

        if natural in TERRAIN_LINE_TYPES:
            return feature_geometry in LINE_GEOMETRY_TYPES

        return False
