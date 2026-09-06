from pathlib import Path

import numpy as np
import pytest
from affine import Affine
from rasterio.crs import CRS

from topoprofile.geo.models import XYZTile
from topoprofile.terrain.models import DEM, RasterTile
from topoprofile.terrain.store import GeoTIFFDEMStore, PNGXYZTileStore


def test_geotiff_dem_store(
        tmp_path: Path,
) -> None:
    store = GeoTIFFDEMStore(
        root=tmp_path,
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
        name="elbrus",
        dem=dem,
    )

    assert output_path == tmp_path / "elbrus.tif"
    assert store.exists("elbrus")

    loaded_dem = store.load("elbrus")

    np.testing.assert_array_equal(
        loaded_dem.values,
        dem.values,
    )

    assert loaded_dem.transform == dem.transform
    assert loaded_dem.crs == dem.crs
    assert loaded_dem.nodata == dem.nodata


@pytest.mark.filterwarnings(
    "ignore::rasterio.errors.NotGeoreferencedWarning"
)
def test_png_xyz_tile_store(
        tmp_path: Path,
) -> None:
    store = PNGXYZTileStore(
        root=tmp_path,
    )

    tile = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    raster_tile = RasterTile(
        tile=tile,
        values=np.array(
            [
                [
                    [10, 20],
                    [30, 40],
                ],
                [
                    [50, 60],
                    [70, 80],
                ],
                [
                    [90, 100],
                    [110, 120],
                ],
            ],
            dtype=np.uint8,
        ),
    )

    output_path = store.save(raster_tile)

    assert output_path == (
            tmp_path
            / "8"
            / "158"
            / "93.png"
    )

    assert store.exists(tile)

    loaded_tile = store.load(tile)

    assert loaded_tile.tile == tile

    np.testing.assert_array_equal(
        loaded_tile.values,
        raster_tile.values,
    )
