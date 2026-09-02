import geopandas as gpd
from shapely.geometry import Point

from topoprofile.geo.models import Bounds, GeoPoint
from topoprofile.geo.projections import get_utm_epsg

WGS84_CRS = "EPSG:4326"


def get_region_bounds(
        center: GeoPoint,
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
        geometry=[Point(center.lon, center.lat)],
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
