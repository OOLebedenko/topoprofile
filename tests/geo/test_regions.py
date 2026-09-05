import geopandas as gpd
import pytest
from shapely.geometry import box

from topoprofile.geo.models import GeoPoint
from topoprofile.geo.projections import get_utm_epsg
from topoprofile.geo.regions import create_region


@pytest.mark.parametrize(
    ("point", "expected"),
    [
        (GeoPoint(lon=42.4361, lat=43.3538), "EPSG:32638"),
        (GeoPoint(lon=42.4361, lat=-43.3538), "EPSG:32738"),
        (GeoPoint(lon=-122.4194, lat=37.7749), "EPSG:32610"),
    ],
)
def test_get_utm_epsg(
        point: GeoPoint,
        expected: str,
) -> None:
    """Test UTM EPSG code computation for various coordinates."""
    assert get_utm_epsg(point) == expected


def test_create_region_bounds_contain_center() -> None:
    """Test that region bounds contain the center point."""
    center = GeoPoint(
        lon=42.4361,
        lat=43.3538,
    )

    region = create_region(
        center=center,
        radius_km=70,
        zoom=8,
    )

    assert region.bounds.west <= center.lon <= region.bounds.east
    assert region.bounds.south <= center.lat <= region.bounds.north


@pytest.mark.parametrize(
    ("center", "radius_km", "utm_epsg"),
    [
        (GeoPoint(42.4361, 43.3538), 70, "EPSG:32638"),
        (GeoPoint(42.4361, -43.3538), 50, "EPSG:32738"),
        (GeoPoint(-122.4194, 37.7749), 30, "EPSG:32610"),
    ],
)
def test_create_region_bounds_area(
        center: GeoPoint,
        radius_km: float,
        utm_epsg: str,
) -> None:
    """
    Test that region bounding box area matches expected square area
    (2 * radius)^2 within a 5% relative tolerance after UTM projection.
    """
    region = create_region(
        center=center,
        radius_km=radius_km,
        zoom=8,
    )

    bounds_geometry = gpd.GeoSeries(
        [
            box(
                region.bounds.west,
                region.bounds.south,
                region.bounds.east,
                region.bounds.north,
            )
        ],
        crs="EPSG:4326",
    )

    bounds_utm = bounds_geometry.to_crs(utm_epsg)

    actual_area = bounds_utm.area.iloc[0]
    expected_area = (2 * radius_km * 1000) ** 2

    assert actual_area == pytest.approx(expected_area, rel=0.05)


@pytest.mark.parametrize(
    "point",
    [
        GeoPoint(lon=-180.1, lat=0.0),
        GeoPoint(lon=180.1, lat=0.0),
    ],
)
def test_get_utm_epsg_rejects_invalid_longitude(
        point: GeoPoint,
) -> None:
    """Test that longitude outside [-180, 180] is rejected."""
    with pytest.raises(
            ValueError,
            match="Longitude must be in the range",
    ):
        get_utm_epsg(point)


@pytest.mark.parametrize(
    "point",
    [
        GeoPoint(lon=0.0, lat=-80.1),
        GeoPoint(lon=0.0, lat=84.1),
    ],
)
def test_get_utm_epsg_rejects_latitude_outside_utm_range(
        point: GeoPoint,
) -> None:
    """Test that points outside the UTM latitude range are rejected."""
    with pytest.raises(
            ValueError,
            match="Latitude must be in the UTM range",
    ):
        get_utm_epsg(point)