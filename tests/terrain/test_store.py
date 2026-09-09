from pathlib import Path

import numpy as np
from affine import Affine
from rasterio.crs import CRS

from topoprofile.geo.models import XYZTile
from topoprofile.terrain.models import DEM, RasterTile
from topoprofile.terrain.store import (
    WebPXYZTileStore,
    XYZContourStore,
    XYZGeoTIFFDEMStore,
)


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


def test_geotiff_dem_store_multiband(
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
                [
                    [1, 2],
                    [3, 4],
                ],
                [
                    [5, 6],
                    [7, 8],
                ],
                [
                    [9, 10],
                    [11, 12],
                ],
            ],
            dtype=np.uint8,
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
        nodata=None,
    )

    store.save(
        tile=tile,
        dem=dem,
    )

    loaded = store.load(tile)

    np.testing.assert_array_equal(
        loaded.values,
        dem.values,
    )
    assert loaded.count == 3
    assert loaded.transform == dem.transform
    assert loaded.crs == dem.crs


def test_webp_xyz_tile_store_rgb_roundtrip(
        tmp_path: Path,
) -> None:
    store = WebPXYZTileStore(
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
            / "93.webp"
    )
    assert store.exists(tile)

    loaded = store.load(tile)

    assert loaded.tile == tile

    np.testing.assert_array_equal(
        loaded.values,
        raster_tile.values,
    )


def test_contour_store_path_and_exists(
        tmp_path: Path,
) -> None:
    store = XYZContourStore(
        root=tmp_path,
    )

    chunk = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    expected_path = (
            tmp_path
            / "8"
            / "158"
            / "93"
            / "contours.pbf"
    )

    assert store.path(chunk) == expected_path
    assert not store.exists(chunk)

    expected_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    expected_path.touch()

    assert store.exists(chunk)
