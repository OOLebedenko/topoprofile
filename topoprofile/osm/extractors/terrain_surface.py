import logging
from typing import Any

from topoprofile.geo.models import Bounds
from topoprofile.osm.extractors.base import OverpassExtractor
from topoprofile.osm.geojson import geometry_type, is_valid_geometry

logger = logging.getLogger(__name__)

AREA_TYPES = {
    "bare_rock",
    "blockfield",
    "glacier",
    "scree",
    "shingle",
    "snowfield",
}
LINE_TYPES = {"cliff"}

AREA_GEOMETRIES = {"Polygon", "MultiPolygon"}
LINE_GEOMETRIES = {"LineString", "MultiLineString"}

OVERPASS_QUERY_TIMEOUT_SECONDS = 180


class TerrainSurfaceExtractor(OverpassExtractor):
    """Extract renderable terrain surface features from OSM."""

    def _build_query(
        self,
        bounds: Bounds,
    ) -> str:
        """Build an Overpass query for terrain surface features."""
        bbox = (
            f"{bounds.south},"
            f"{bounds.west},"
            f"{bounds.north},"
            f"{bounds.east}"
        )
        area_values = "|".join(sorted(AREA_TYPES))
        line_values = "|".join(sorted(LINE_TYPES))

        return f"""
[out:json][timeout:{OVERPASS_QUERY_TIMEOUT_SECONDS}];

(
  way["natural"~"^({area_values})$"]({bbox});
  relation["natural"~"^({area_values})$"]({bbox});
  way["natural"~"^({line_values})$"]({bbox});
  relation["natural"~"^({line_values})$"]({bbox});
);

out body geom;
""".strip()

    def _process(
        self,
        geojson: dict[str, Any],
    ) -> dict[str, Any]:
        """Keep only renderable terrain surface features."""
        features = geojson["features"]
        filtered = [
            feature
            for feature in features
            if self._is_renderable(feature)
        ]

        logger.info(
            "Terrain surface features: total=%d, kept=%d, rejected=%d",
            len(features),
            len(filtered),
            len(features) - len(filtered),
        )

        return {
            "type": "FeatureCollection",
            "features": filtered,
        }

    @staticmethod
    def _is_renderable(
            feature: dict[str, Any],
    ) -> bool:
        """Return whether a terrain surface feature can be rendered."""
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return False

        natural = properties.get("natural")
        feature_geometry = geometry_type(geometry)

        if natural in AREA_TYPES:
            return feature_geometry in AREA_GEOMETRIES

        if natural in LINE_TYPES:
            return feature_geometry in LINE_GEOMETRIES

        return False