from topoprofile.geo.models import Bounds
from topoprofile.osm.client.overpass import OverpassClient
from topoprofile.osm.client.queries.base import Query
from topoprofile.osm.models import OverpassData


class OverpassFeatureSource:
    """Load OSM data from the Overpass API."""

    def __init__(
            self,
            query: Query,
            client: OverpassClient,
    ) -> None:
        self._query = query
        self._client = client

    def load(
            self,
            bounds: Bounds,
    ) -> OverpassData:
        query = self._query.build(bounds)
        data = self._client.fetch(query)

        return OverpassData(
            elements=tuple(data["elements"]),
        )