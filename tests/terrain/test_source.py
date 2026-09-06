from unittest.mock import MagicMock

import numpy as np
import pygmt
from affine import Affine
from rasterio.crs import CRS

from topoprofile.geo.models import Bounds
from topoprofile.terrain.models import DEM
from topoprofile.terrain.source import EarthReliefDEMSource


def test_earth_relief_source_load(
        monkeypatch,
) -> None:
    bounds = Bounds(
        west=42.4,
        south=43.3,
        east=42.5,
        north=43.4,
    )

    values = np.array(
        [
            [100, 200],
            [300, 400],
        ],
        dtype=np.int16,
    )

    transform = Affine(
        0.05,
        0.0,
        42.4,
        0.0,
        -0.05,
        43.4,
    )

    crs = CRS.from_epsg(4326)

    data = MagicMock()
    data.values = values
    data.rio.transform.return_value = transform
    data.rio.crs = crs
    data.rio.nodata = None

    load_earth_relief = MagicMock(
        return_value=data,
    )

    monkeypatch.setattr(
        pygmt.datasets,
        "load_earth_relief",
        load_earth_relief,
    )

    source = EarthReliefDEMSource(
        resolution="01s",
    )

    dem = source.load(bounds)

    assert isinstance(dem, DEM)
    assert dem.values is values
    assert dem.transform == transform
    assert dem.crs == crs
    assert dem.nodata is None

    load_earth_relief.assert_called_once_with(
        resolution="01s",
        region=[
            bounds.west,
            bounds.east,
            bounds.south,
            bounds.north,
        ],
    )

    data.rio.write_crs.assert_called_once_with(
        "EPSG:4326",
        inplace=True,
    )
