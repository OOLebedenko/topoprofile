from abc import ABC, abstractmethod

from topoprofile.geo.models import Bounds


class OverpassQuery(ABC):
    """Base interface for Overpass queries."""

    @abstractmethod
    def build(
            self,
            bounds: Bounds,
    ) -> str:
        """Build the query for geographic bounds."""
