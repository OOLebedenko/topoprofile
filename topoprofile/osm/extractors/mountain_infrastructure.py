import logging
from typing import Any

from shapely.geometry import mapping, shape

from topoprofile.geo.models import Bounds
from topoprofile.osm.extractors.base import OverpassExtractor
from topoprofile.osm.geojson import geometry_type, is_valid_geometry

logger = logging.getLogger(__name__)

HUT_TYPES = {
    "alpine_hut",
    "wilderness_hut",
}

SHELTER_TYPES = {
    "weather_shelter",
}

OVERPASS_QUERY_TIMEOUT_SECONDS = 180


class MountainInfrastructureExtractor(OverpassExtractor):
    """Extract renderable mountain huts and shelters from OSM."""

    def _build_query(self, bounds: Bounds) -> str:
        """Build an Overpass query for mountain infrastructure."""
        bbox = (
            f"{bounds.south},"
            f"{bounds.west},"
            f"{bounds.north},"
            f"{bounds.east}"
        )

        hut_values = "|".join(sorted(HUT_TYPES))
        shelter_values = "|".join(sorted(SHELTER_TYPES))

        return f"""
[out:json][timeout:{OVERPASS_QUERY_TIMEOUT_SECONDS}];

(
  node
    ["tourism"~"^({hut_values})$"]
    ({bbox});

  nwr
    ["amenity"="shelter"]
    ["shelter_type"~"^({shelter_values})$"]
    ({bbox});
);

out body geom;
""".strip()

    def _process(self, geojson: dict[str, Any]) -> dict[str, Any]:
        """Keep and normalize renderable mountain infrastructure."""
        features = []

        for feature in geojson["features"]:
            normalized = self._normalize_feature(feature)

            if normalized is not None:
                features.append(normalized)

        logger.info(
            "Mountain infrastructure: total=%d, kept=%d, rejected=%d",
            len(geojson["features"]),
            len(features),
            len(geojson["features"]) - len(features),
        )

        return {
            "type": "FeatureCollection",
            "features": features,
        }

    @staticmethod
    def _normalize_feature(
            feature: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Normalize mountain infrastructure to point geometry."""
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return None

        feature_geometry = geometry_type(geometry)

        if properties.get("tourism") in HUT_TYPES:
            if feature_geometry != "Point":
                return None

            return feature

        if (
                properties.get("amenity") == "shelter"
                and properties.get("shelter_type") in SHELTER_TYPES
        ):
            if feature_geometry == "Point":
                return feature

            centroid = shape(geometry).centroid

            if centroid.is_empty:
                return None

            return {
                **feature,
                "geometry": mapping(centroid),
            }

        return None
