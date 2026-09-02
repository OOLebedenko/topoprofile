import math
from dataclasses import dataclass

from topoprofile.geo.models import Bounds


@dataclass(frozen=True, slots=True)
class XYZTile:
    """XYZ terrain tile coordinates."""

    z: int
    x: int
    y: int


def xyz_to_bounds(tile: XYZTile) -> Bounds:
    """Convert XYZ tile coordinates to geographic bounds."""
    n = 2**tile.z

    west = tile.x / n * 360.0 - 180.0
    east = (tile.x + 1) / n * 360.0 - 180.0

    north = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * tile.y / n))))

    south = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (tile.y + 1) / n))))

    return Bounds(
        west=west,
        south=south,
        east=east,
        north=north,
    )


def parent_tile(
    tile: XYZTile,
    target_zoom: int,
) -> XYZTile:
    """Return the ancestor of an XYZ tile at the target zoom."""
    if target_zoom > tile.z:
        raise ValueError("Target zoom must not exceed tile zoom.")

    scale = 2 ** (tile.z - target_zoom)

    return XYZTile(
        z=target_zoom,
        x=tile.x // scale,
        y=tile.y // scale,
    )
