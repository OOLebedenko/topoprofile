from pathlib import Path

import numpy as np
from affine import Affine
from rasterio.crs import CRS

from topoprofile.geo.models import XYZTile
from topoprofile.terrain.models import DEM
from topoprofile.terrain.store import XYZGeoTIFFDEMStore


def test_geotiff_dem_store(
        tmp_path: Path,
) -> None:
    store = XYZGeoTIFFDEMStore(
        root=tmp_path,
    )

    tile = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    dem = DEM(
        values=np.array(
            [
                [100, 200],
                [300, 400],
            ],
            dtype=np.int16,
        ),
        transform=Affine(
            0.5,
            0.0,
            42.0,
            0.0,
            -0.5,
            44.0,
        ),
        crs=CRS.from_epsg(4326),
        nodata=-32768,
    )

    output_path = store.save(
        tile=tile,
        dem=dem,
    )

    assert output_path == (
            tmp_path
            / "8"
            / "158"
            / "93"
            / "dem_terrarium.tif"
    )
    assert store.exists(tile)

    loaded = store.load(tile)

    np.testing.assert_array_equal(
        loaded.values,
        dem.values,
    )
    assert loaded.transform == dem.transform
    assert loaded.crs == dem.crs
    assert loaded.nodata == dem.nodata
