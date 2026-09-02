import geopandas as gpd
from shapely.geometry import Point

from topoprofile.geo.models import Bounds, GeoPoint

WGS84_CRS = "EPSG:4326"

def get_utm_epsg(point: GeoPoint) -> str:
    """
    Return the EPSG code of the UTM CRS containing the given point.

    The UTM zone is determined from longitude:
    - zones are numbered from 1 to 60;
    - each zone spans 6 degrees of longitude;
    - longitude 180° is assigned to zone 60.

    The hemisphere is determined from latitude:
    - northern hemisphere uses EPSG:326xx;
    - southern hemisphere uses EPSG:327xx.

    UTM is supported only between 80°S and 84°N. Points outside this
    latitude range are not supported by this function.

    Args:
        point: Geographic point in longitude/latitude coordinates
            (EPSG:4326).

    Returns:
        UTM CRS identifier in EPSG form, for example ``"EPSG:32638"``.

    Raises:
        ValueError: If longitude is outside [-180, 180].
        ValueError: If latitude is outside the UTM range [-80, 84].
    """
    if not -180 <= point.lon <= 180:
        raise ValueError(
            "Longitude must be in the range [-180, 180]."
        )

    if not -80 <= point.lat <= 84:
        raise ValueError(
            "Latitude must be in the UTM range [-80, 84]."
        )

    if point.lon == 180:
        zone = 60
    else:
        zone = int((point.lon + 180) / 6) + 1

    epsg_base = 326 if point.lat >= 0 else 327

    return f"EPSG:{epsg_base}{zone:02d}"


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
