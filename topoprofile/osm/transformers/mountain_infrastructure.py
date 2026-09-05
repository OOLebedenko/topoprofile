import logging
from typing import Any

from shapely.geometry import mapping, shape

from topoprofile.geo.models import Bounds
from topoprofile.osm.geojson import (
    POLYGON_GEOMETRY_TYPES,
    GeoJSON,
    clip_to_bounds,
    geometry_type,
    is_valid_geometry,
)
from topoprofile.osm.tags import (
    MOUNTAIN_HUT_TYPES,
    MOUNTAIN_SHELTER_TYPES,
)
from topoprofile.osm.transformers.base import OSMFeatureTransformer

logger = logging.getLogger(__name__)


class MountainInfrastructureTransformer(OSMFeatureTransformer):
    """Transform mountain infrastructure into renderable point features."""

    def transform(
            self,
            geojson: GeoJSON,
            bounds: Bounds,
    ) -> GeoJSON:
        features = geojson["features"]

        transformed = []

        for feature in features:
            result = self._transform_feature(feature)

            if result is not None:
                transformed.append(result)

        result = {
            "type": "FeatureCollection",
            "features": transformed,
        }

        result = clip_to_bounds(
            result,
            bounds,
        )

        logger.info(
            "Mountain infrastructure: total=%d, kept=%d, rejected=%d",
            len(features),
            len(result["features"]),
            len(features) - len(transformed),
        )

        return result

    @staticmethod
    def _transform_feature(
            feature: dict[str, Any],
    ) -> dict[str, Any] | None:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return None

        feature_geometry = geometry_type(geometry)

        if properties.get("tourism") in MOUNTAIN_HUT_TYPES:
            if feature_geometry == "Point":
                return feature

            return None

        if (
                properties.get("amenity") == "shelter"
                and properties.get("shelter_type")
                in MOUNTAIN_SHELTER_TYPES
        ):
            if feature_geometry == "Point":
                return feature

            if feature_geometry in POLYGON_GEOMETRY_TYPES:
                transformed = dict(feature)
                transformed["geometry"] = mapping(
                    shape(geometry).centroid
                )

                return transformed

        return None
