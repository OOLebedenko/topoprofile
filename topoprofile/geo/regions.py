import math

import geopandas as gpd
from shapely.geometry import Point as ShapelyPoint

from topoprofile.geo.models import (
    Bounds,
    LonLat,
    Region,
    XYZTile,
)
from topoprofile.geo.projections import get_utm_epsg

WGS84_CRS = "EPSG:4326"
WEB_MERCATOR_MAX_LAT = 85.05112878


def create_region(
        center: LonLat,
        radius_km: float,
        zoom: int,
) -> Region:
    """Create a geographic region covered by XYZ tiles."""
    bounds = _calculate_region_bounds(
        center=center,
        radius_km=radius_km,
    )

    tiles = RegionToXYZTiles.resolve(
        bounds=bounds,
        zoom=zoom,
    )

    return Region(
        bounds=bounds,
        tiles=tuple(tiles),
    )


def _calculate_region_bounds(
        center: LonLat,
        radius_km: float,
) -> Bounds:
    """
    Calculate geographic bounds for a region around a center point.

    The input point is interpreted as WGS84 longitude/latitude coordinates.
    To construct a region with a radius expressed in kilometers, the center
    point is projected to its local UTM CRS, where distances are measured
    in meters.

    A circular buffer is created around the projected point and then
    transformed back to WGS84. The returned bounds are the bounding box
    of that buffered region.

    Args:
        center: Region center in WGS84 longitude/latitude coordinates.
        radius_km: Region radius in kilometers.

    Returns:
        Geographic bounds in WGS84 longitude/latitude coordinates.

    Raises:
        ValueError: If radius_km is not positive.
        ValueError: If the center point cannot be represented by a
            supported UTM CRS.
    """
    if radius_km <= 0:
        raise ValueError("Radius must be positive.")

    center_geometry = gpd.GeoDataFrame(
        geometry=[
            ShapelyPoint(
                center.lon,
                center.lat,
            )
        ],
        crs=WGS84_CRS,
    )

    buffered_geometry = (
        center_geometry
        .to_crs(get_utm_epsg(center))
        .geometry.buffer(radius_km * 1000)
        .to_crs(WGS84_CRS)
    )

    west, south, east, north = buffered_geometry.total_bounds

    return Bounds(
        west=float(west),
        south=float(south),
        east=float(east),
        north=float(north),
    )


class RegionToXYZTiles:
    """Resolve geographic bounds into covering XYZ tiles."""

    @classmethod
    def resolve(
            cls,
            bounds: Bounds,
            zoom: int,
    ) -> list[XYZTile]:
        """
        Return all XYZ regions required to cover geographic bounds.

        The input bounds are expected in WGS84 longitude/latitude
        coordinates. They are mapped to the Web Mercator XYZ tile grid
        at the specified zoom level.

        Args:
            bounds: Geographic bounds in WGS84 coordinates.
            zoom: Zoom level of the XYZ grid.

        Returns:
            XYZ regions covering the entire geographic region.

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
            cls._longitude_to_x(bounds.west, tile_count)
        )
        x_max = math.ceil(
            cls._longitude_to_x(bounds.east, tile_count)
        ) - 1

        y_min = math.floor(
            cls._latitude_to_y(bounds.north, tile_count)
        )
        y_max = math.ceil(
            cls._latitude_to_y(bounds.south, tile_count)
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
