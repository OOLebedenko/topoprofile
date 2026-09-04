from typing import Any

import osm2geojson
from shapely.geometry import box, mapping, shape

from topoprofile.geo.models import Bounds


def geometry_type(
    geometry: Any,
) -> str | None:
    """Return the GeoJSON geometry type."""
    if not isinstance(geometry, dict):
        return None

    value = geometry.get("type")
    return value if isinstance(value, str) else None


def has_coordinates(
    geometry: Any,
) -> bool:
    """Return whether a GeoJSON geometry has non-empty coordinates."""
    if not isinstance(geometry, dict):
        return False

    coordinates = geometry.get("coordinates")
    return isinstance(coordinates, list) and bool(coordinates)


def is_valid_geometry(
        geometry: Any,
) -> bool:
    """Return whether a GeoJSON geometry has a type and coordinates."""
    return geometry_type(geometry) is not None and has_coordinates(geometry)


class GeoJSONConverter:
    """Convert Overpass JSON to normalized GeoJSON."""

    def __init__(
        self,
        log_level: str = "WARNING",
    ) -> None:
        self.log_level = log_level

    def convert(
        self,
        osm_json: dict[str, Any],
    ) -> dict[str, Any]:
        """Convert Overpass JSON to a normalized GeoJSON FeatureCollection."""
        geojson = osm2geojson.json2geojson(
            osm_json,
            raise_on_failure=False,
            log_level=self.log_level,
        )
        self._flatten_tags(geojson)
        return geojson

    @staticmethod
    def _flatten_tags(geojson: dict[str, Any]) -> None:
        """Flatten OSM tags into feature properties."""
        for feature in geojson["features"]:
            properties = feature.get("properties", {})

            if not isinstance(properties, dict):
                feature["properties"] = {}
                continue

            # Extract service fields first.
            osm_type = properties.pop("type", None)
            osm_id = properties.pop("id", None)

            # Extract and flatten OSM tags.
            tags = properties.pop("tags", {})
            if isinstance(tags, dict):
                properties.update(tags)

            # Restore service fields with explicit names.
            if osm_type is not None:
                properties["osm_type"] = osm_type
            if osm_id is not None:
                properties["osm_id"] = osm_id


def clip_to_bounds(
        geojson: dict[str, Any],
        bounds: Bounds,
) -> dict[str, Any]:
    """Clip GeoJSON features to geographic bounds."""
    clip_geometry = box(
        bounds.west,
        bounds.south,
        bounds.east,
        bounds.north,
    )

    features = []

    for feature in geojson["features"]:
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            continue

        clipped_geometry = shape(geometry).intersection(clip_geometry)

        if clipped_geometry.is_empty:
            continue

        features.append({
            **feature,
            "geometry": mapping(clipped_geometry),
        })

    return {
        **geojson,
        "features": features,
    }
