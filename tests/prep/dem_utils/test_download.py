from pathlib import Path
from unittest.mock import Mock

import geopandas as gpd
import pytest
from shapely.geometry import box

from topoprofile.prep.dem_utils import download


@pytest.mark.parametrize(
    ("lon", "lat", "expected"),
    [
        (42.4361, 43.3538, "EPSG:32638"),
        (42.4361, -43.3538, "EPSG:32738"),
        (-122.4194, 37.7749, "EPSG:32610"),
    ],
)
def test_get_utm_epsg(
    lon: float,
    lat: float,
    expected: str,
) -> None:
    """Test UTM EPSG code computation for various coordinates."""
    assert download.get_utm_epsg(lon, lat) == expected


def test_get_region_bounds_contains_center() -> None:
    """Test that computed bounds contain the center point."""
    center_lon = 42.4361
    center_lat = 43.3538

    min_lon, min_lat, max_lon, max_lat = download.get_region_bounds(
        center_lon=center_lon,
        center_lat=center_lat,
        radius_m=70_000,
    )

    assert min_lon <= center_lon <= max_lon
    assert min_lat <= center_lat <= max_lat


@pytest.mark.parametrize(
    "center_lon, center_lat, radius_m, utm_epsg",
    [
        (42.4361, 43.3538, 70_000, "EPSG:32638"),
        (42.4361, -43.3538, 50_000, "EPSG:32738"),
        (-122.4194, 37.7749, 30_000, "EPSG:32610"),
    ],
)
def test_get_region_bounds_area(
    center_lon: float,
    center_lat: float,
    radius_m: float,
    utm_epsg: str,
) -> None:
    """
    Test that bounding box area matches expected square area (2*radius)^2
    within a 5% relative tolerance after UTM projection.
    """
    min_lon, min_lat, max_lon, max_lat = download.get_region_bounds(
        center_lon=center_lon,
        center_lat=center_lat,
        radius_m=radius_m,
    )

    bounds = gpd.GeoSeries(
        [box(min_lon, min_lat, max_lon, max_lat)],
        crs="EPSG:4326",
    )

    bounds_utm = bounds.to_crs(utm_epsg)

    actual_area = bounds_utm.area.iloc[0]
    expected_area = (2 * radius_m) ** 2

    assert actual_area == pytest.approx(expected_area, rel=0.05)


def test_download_dem_by_bounds(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Test that download_dem_by_bounds calls pygmt with correct parameters,
    creates parent directories, sets CRS, and saves the raster.
    """
    output_path = tmp_path / "nested" / "dem.tif"

    fake_dem = Mock()
    fake_dem.rio = Mock()

    load_earth_relief_mock = Mock(return_value=fake_dem)

    monkeypatch.setattr(
        download.pygmt.datasets,
        "load_earth_relief",
        load_earth_relief_mock,
    )

    download.download_dem_by_bounds(
        bounds=(42.0, 43.0, 43.0, 44.0),
        resolution="01s",
        output_path=output_path,
    )

    assert output_path.parent.exists()

    load_earth_relief_mock.assert_called_once_with(
        resolution="01s",
        region=[
            42.0,
            43.0,
            43.0,
            44.0,
        ],
    )

    fake_dem.rio.write_crs.assert_called_once_with(
        "EPSG:4326",
        inplace=True,
    )

    fake_dem.rio.to_raster.assert_called_once_with(output_path)


def test_download_region_dem_uses_existing_file(tmp_path, monkeypatch):
    """Test that existing DEM file is reused when force_download=False."""
    region = {
        "center": {"lon": 42.4361, "lat": 43.3538},
        "radius_m": 70_000,
        "dem": {"resolution": "01s", "filename": "dem.tif"},
    }
    output_path = tmp_path / "dem.tif"
    output_path.touch()

    mock_download = Mock()
    monkeypatch.setattr(download, "download_dem_by_bounds", mock_download)

    result = download.download_region_dem(region, tmp_path, force_download=False)

    assert result == output_path
    mock_download.assert_not_called()
