from abc import ABC, abstractmethod

from topoprofile.geo.models import Bounds
from topoprofile.osm.client.config import QUERY_TIMEOUT_SECONDS


class Query(ABC):
    """Base interface for Overpass queries."""

    @abstractmethod
    def build(
            self,
            bounds: Bounds,
    ) -> str:
        """Build the query for geographic bounds."""


class UnionQuery(Query):
    """Combine multiple Overpass queries into a single query."""

    def __init__(
            self,
            queries: tuple[Query, ...],
    ) -> None:
        self._queries = queries

    def build(
            self,
            bounds: Bounds,
    ) -> str:
        bodies = [
            self._extract_body(
                query.build(bounds)
            )
            for query in self._queries
        ]

        body = "\n".join(bodies)

        return f"""
[out:json][timeout:{QUERY_TIMEOUT_SECONDS}];

(
{body}
);

out body geom;
""".strip()

    @staticmethod
    def _extract_body(
            query: str,
    ) -> str:
        start = query.index("(\n") + 2
        end = query.index("\n);", start)

        return query[start:end]
