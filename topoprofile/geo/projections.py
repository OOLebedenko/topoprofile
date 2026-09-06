from topoprofile.geo.models import LonLat


def get_utm_epsg(point: LonLat) -> str:
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
