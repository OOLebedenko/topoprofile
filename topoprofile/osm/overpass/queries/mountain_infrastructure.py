from topoprofile.geo.models import Bounds
from topoprofile.osm.overpass.config import QUERY_TIMEOUT_SECONDS
from topoprofile.osm.overpass.queries.base import OverpassQuery
from topoprofile.osm.tags import (
    MOUNTAIN_HUT_TYPES,
    MOUNTAIN_SHELTER_TYPES,
)


class MountainInfrastructureQuery(OverpassQuery):
    """Build Overpass queries for mountain infrastructure."""

    def build(
            self,
            bounds: Bounds,
    ) -> str:
        """Build an Overpass query for mountain infrastructure."""
        bbox = (
            f"{bounds.south},"
            f"{bounds.west},"
            f"{bounds.north},"
            f"{bounds.east}"
        )

        hut_values = "|".join(
            sorted(MOUNTAIN_HUT_TYPES)
        )
        shelter_values = "|".join(
            sorted(MOUNTAIN_SHELTER_TYPES)
        )

        return f"""
[out:json][timeout:{QUERY_TIMEOUT_SECONDS}];

(
  node
    ["tourism"~"^({hut_values})$"]
    ({bbox});

  nwr
    ["amenity"="shelter"]
    ["shelter_type"~"^({shelter_values})$"]
    ({bbox});
);

out body geom;
""".strip()
