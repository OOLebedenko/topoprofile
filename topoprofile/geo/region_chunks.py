import math

from topoprofile.domain.terrain import XYZTile
from topoprofile.geo.models import Bounds

WEB_MERCATOR_MAX_LAT = 85.05112878


class RegionChunkResolver:
    """Resolve geographic bounds into XYZ DEM chunks."""

    def resolve(
            self,
            bounds: Bounds,
            zoom: int,
    ) -> list[XYZTile]:
        """
        Return all XYZ chunks required to cover geographic bounds.

        The input bounds are expected in WGS84 longitude/latitude
        coordinates. They are mapped to the Web Mercator XYZ tile grid
        at the specified zoom level.

        Args:
            bounds: Geographic bounds in WGS84 coordinates.
            zoom: Zoom level of the DEM chunk grid.

        Returns:
            XYZ tiles covering the entire geographic region.

        Raises:
            ValueError: If zoom is negative.
            ValueError: If latitude exceeds Web Mercator limits.
        """
        if zoom < 0:
            raise ValueError("Zoom must be non-negative.")

        if (
                bounds.south < -WEB_MERCATOR_MAX_LAT
                or bounds.north > WEB_MERCATOR_MAX_LAT
        ):
            raise ValueError(
                "Bounds exceed Web Mercator latitude limits."
            )

        tile_count = 2 ** zoom

        x_min = math.floor(
            self._longitude_to_x(bounds.west, tile_count)
        )
        x_max = math.ceil(
            self._longitude_to_x(bounds.east, tile_count)
        ) - 1

        y_min = math.floor(
            self._latitude_to_y(bounds.north, tile_count)
        )
        y_max = math.ceil(
            self._latitude_to_y(bounds.south, tile_count)
        ) - 1

        return [
            XYZTile(
                z=zoom,
                x=x,
                y=y,
            )
            for x in range(x_min, x_max + 1)
            for y in range(y_min, y_max + 1)
        ]

    @staticmethod
    def _longitude_to_x(
            lon: float,
            tile_count: int,
    ) -> float:
        return (lon + 180.0) / 360.0 * tile_count

    @staticmethod
    def _latitude_to_y(
            lat: float,
            tile_count: int,
    ) -> float:
        lat_rad = math.radians(lat)

        return (
                1.0
                - math.asinh(math.tan(lat_rad)) / math.pi
        ) / 2.0 * tile_count
