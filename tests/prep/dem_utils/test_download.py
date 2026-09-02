from pathlib import Path
from unittest.mock import Mock

from topoprofile.geo.models import Bounds
from topoprofile.prep.dem_utils import download


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

    bounds = Bounds(
        west=42.0,
        south=43.0,
        east=43.0,
        north=44.0,
    )

    download.download_dem_by_bounds(
        bounds=bounds,
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
