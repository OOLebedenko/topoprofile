from abc import ABC, abstractmethod
from typing import Any

from topoprofile.geo.models import Bounds
from topoprofile.osm.overpass.client import OverpassGeoJSONClient


class OverpassExtractor(ABC):
    """Base class for extracting features through Overpass."""

    def __init__(
            self,
            client: OverpassGeoJSONClient,
    ) -> None:
        self.client = client

    def extract(
            self,
            bounds: Bounds,
    ) -> dict[str, Any]:
        """Fetch and process Overpass features for geographic bounds."""
        query = self._build_query(bounds)
        geojson = self.client.fetch(query)
        return self._process(geojson)

    @abstractmethod
    def _build_query(
            self,
            bounds: Bounds,
    ) -> str:
        """Build an Overpass query."""

    @abstractmethod
    def _process(
            self,
            geojson: dict[str, Any],
    ) -> dict[str, Any]:
        """Process fetched GeoJSON features."""
