from abc import ABC, abstractmethod

from topoprofile.geo.models import Bounds
from topoprofile.osm.geojson import (
    GeoJSON,
    GeoJSONConverter,
)
from topoprofile.osm.overpass.client import OverpassClient
from topoprofile.osm.overpass.queries.base import OverpassQuery


class OSMFeatureSource(ABC):
    """Base interface for loading OSM feature data."""

    @abstractmethod
    def load(
            self,
            bounds: Bounds,
    ) -> GeoJSON:
        """Load OSM features for the given geographic bounds."""


class OverpassFeatureSource(OSMFeatureSource):
    """Load OSM features through the Overpass API."""

    def __init__(
            self,
            query: OverpassQuery,
            client: OverpassClient,
            converter: GeoJSONConverter,
    ) -> None:
        self._query = query
        self._client = client
        self._converter = converter

    def load(
            self,
            bounds: Bounds,
    ) -> GeoJSON:
        """Load OSM features for the given geographic bounds."""
        query = self._query.build(bounds)
        overpass_json = self._client.fetch(query)

        return self._converter.convert(
            overpass_json,
        )
