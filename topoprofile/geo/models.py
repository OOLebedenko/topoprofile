import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GeoPoint:
    lon: float
    lat: float


@dataclass(frozen=True, slots=True)
class Bounds:
    """Geographic bounds in west, south, east, north order."""

    west: float
    south: float
    east: float
    north: float


@dataclass(frozen=True, slots=True)
class XYZTile:
    """XYZ tile coordinates."""

    z: int
    x: int
    y: int

    @property
    def bounds(self) -> Bounds:
        """Return geographic bounds of the XYZ tile."""
        n = 2 ** self.z

        west = self.x / n * 360.0 - 180.0
        east = (self.x + 1) / n * 360.0 - 180.0

        north = math.degrees(
            math.atan(
                math.sinh(
                    math.pi * (1 - 2 * self.y / n)
                )
            )
        )

        south = math.degrees(
            math.atan(
                math.sinh(
                    math.pi * (1 - 2 * (self.y + 1) / n)
                )
            )
        )

        return Bounds(
            west=west,
            south=south,
            east=east,
            north=north,
        )

    def parent(
            self,
            target_zoom: int,
    ) -> "XYZTile":
        """Return the ancestor XYZ tile at the target zoom."""
        if target_zoom > self.z:
            raise ValueError(
                "Target zoom must not exceed tile zoom."
            )

        scale = 2 ** (self.z - target_zoom)

        return XYZTile(
            z=target_zoom,
            x=self.x // scale,
            y=self.y // scale,
        )
