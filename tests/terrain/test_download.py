from pathlib import Path
from unittest.mock import Mock

import numpy as np
import rasterio
from affine import Affine
from rasterio.crs import CRS

from topoprofile.geo.models import Bounds
from topoprofile.terrain import dem
from topoprofile.terrain.models import DEM
from topoprofile.terrain.source import DEMSource


def test_download_dem_by_bounds(
        tmp_path: Path,
) -> None:
    """
    Test that download_dem_by_bounds loads DEM data from the source
    and saves it as a GeoTIFF.
    """
    output_path = tmp_path / "nested" / "dem.tif"

    bounds = Bounds(
        west=42.0,
        south=43.0,
        east=43.0,
        north=44.0,
    )

    values = np.array(
        [
            [100, 200],
            [300, 400],
        ],
        dtype=np.int16,
    )

    transform = Affine(
        0.5,
        0.0,
        42.0,
        0.0,
        -0.5,
        44.0,
    )

    crs = CRS.from_epsg(4326)

    source = Mock(spec=DEMSource)
    source.load.return_value = DEM(
        values=values,
        transform=transform,
        crs=crs,
    )

    dem.download_dem_by_bounds(
        bounds=bounds,
        source=source,
        output_path=output_path,
    )

    source.load.assert_called_once_with(bounds)

    assert output_path.parent.exists()
    assert output_path.is_file()

    with rasterio.open(output_path) as dataset:
        np.testing.assert_array_equal(
            dataset.read(1),
            values,
        )

        assert dataset.transform == transform
        assert dataset.crs == crs
