from topoprofile.geo.models import Bounds
from topoprofile.osm.overpass.config import QUERY_TIMEOUT_SECONDS
from topoprofile.osm.overpass.queries.base import OverpassQuery
from topoprofile.osm.tags import (
    TERRAIN_AREA_TYPES,
    TERRAIN_LINE_TYPES,
)


class TerrainSurfaceQuery(OverpassQuery):
    """Build Overpass queries for terrain surface features."""

    def build(
            self,
            bounds: Bounds,
    ) -> str:
        """Build an Overpass query for terrain surface features."""
        bbox = (
            f"{bounds.south},"
            f"{bounds.west},"
            f"{bounds.north},"
            f"{bounds.east}"
        )

        area_values = "|".join(
            sorted(TERRAIN_AREA_TYPES)
        )
        line_values = "|".join(
            sorted(TERRAIN_LINE_TYPES)
        )

        return f"""
[out:json][timeout:{QUERY_TIMEOUT_SECONDS}];

(
  way["natural"~"^({area_values})$"]({bbox});
  relation["natural"~"^({area_values})$"]({bbox});
  way["natural"~"^({line_values})$"]({bbox});
  relation["natural"~"^({line_values})$"]({bbox});
);

out body geom;
""".strip()
