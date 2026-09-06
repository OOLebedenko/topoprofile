from abc import ABC, abstractmethod

import osm2geojson

from topoprofile.osm.models import (
    GeoJSON,
    OSMFeatureCollection,
    OverpassData,
)


class OverpassTransform(ABC):
    """Transform raw Overpass data into OSM features."""

    @abstractmethod
    def __call__(
            self,
            data: OverpassData,
    ) -> OSMFeatureCollection:
        """Transform Overpass data."""


class GeoJSONTransformError(RuntimeError):
    """Raised when Overpass data cannot be converted to GeoJSON."""


class GeoJSONTransform(OverpassTransform):
    """Convert Overpass data to normalized OSM features."""

    def __call__(
            self,
            data: OverpassData,
    ) -> OSMFeatureCollection:
        try:
            geojson = osm2geojson.json2geojson(
                {
                    "elements": list(data.elements),
                },
                raise_on_failure=False,
            )
            self._flatten_tags(geojson)

            return OSMFeatureCollection(
                features=tuple(geojson["features"]),
            )
        except Exception as error:
            raise GeoJSONTransformError(
                "Failed to convert Overpass data to GeoJSON."
            ) from error

    @staticmethod
    def _flatten_tags(
            geojson: GeoJSON,
    ) -> None:
        """Flatten OSM tags into feature properties."""
        for feature in geojson["features"]:
            properties = feature.get("properties", {})

            if not isinstance(properties, dict):
                feature["properties"] = {}
                continue

            osm_type = properties.pop("type", None)
            osm_id = properties.pop("id", None)

            tags = properties.pop("tags", {})

            if isinstance(tags, dict):
                properties.update(tags)

            if osm_type is not None:
                properties["osm_type"] = osm_type

            if osm_id is not None:
                properties["osm_id"] = osm_id
