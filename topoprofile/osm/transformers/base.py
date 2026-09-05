from abc import ABC, abstractmethod

from topoprofile.geo.models import Bounds
from topoprofile.osm.geojson import GeoJSON


class OSMFeatureTransformer(ABC):
    """Base interface for transforming OSM feature data."""

    @abstractmethod
    def transform(
            self,
            geojson: GeoJSON,
            bounds: Bounds,
    ) -> GeoJSON:
        """Transform OSM features for the given geographic bounds."""
