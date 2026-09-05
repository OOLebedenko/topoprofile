from topoprofile.geo.models import Bounds
from topoprofile.osm.overpass.config import QUERY_TIMEOUT_SECONDS
from topoprofile.osm.overpass.queries.base import OverpassQuery
from topoprofile.osm.tags import (
    HIKING_ROUTE_TYPES,
    HIKING_TRAIL_TYPES,
)


class HikingRouteQuery(OverpassQuery):
    """Build Overpass queries for hiking routes."""

    def build(
            self,
            bounds: Bounds,
    ) -> str:
        """Build an Overpass query for hiking routes."""
        bbox = (
            f"{bounds.south},"
            f"{bounds.west},"
            f"{bounds.north},"
            f"{bounds.east}"
        )

        route_values = "|".join(
            sorted(HIKING_ROUTE_TYPES)
        )
        trail_values = "|".join(
            sorted(HIKING_TRAIL_TYPES)
        )

        return f"""
[out:json][timeout:{QUERY_TIMEOUT_SECONDS}];

(
  relation
    ["type"="route"]
    ["route"~"^({route_values})$"]
    ({bbox});

  way
    ["highway"~"^({trail_values})$"]
    ({bbox});

  way
    ["aerialway"]
    ({bbox});
);

out body geom;
""".strip()
