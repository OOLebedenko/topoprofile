from pathlib import Path
from unittest.mock import MagicMock

import numpy as np
import pytest
from affine import Affine
from rasterio.crs import CRS

from topoprofile.geo.models import XYZTile
from topoprofile.terrain.models import DEM
from topoprofile.terrain.task import (
    GenerateTilesTask,
    PrepareContoursTask,
    PrepareDEMTask,
)


@pytest.fixture
def chunk() -> XYZTile:
    return XYZTile(
        z=8,
        x=158,
        y=93,
    )


@pytest.fixture
def dem() -> DEM:
    return DEM(
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
        nodata=None,
    )


def test_prepare_dem_task_skips_existing_chunk(
        chunk: XYZTile,
) -> None:
    source = MagicMock()
    store = MagicMock()
    transform = MagicMock()

    output_path = Path("dem_terrarium.tif")
    store.exists.return_value = True
    store.path.return_value = output_path

    task = PrepareDEMTask(
        source=source,
        store=store,
        transform=transform,
    )

    result = task(chunk)

    store.exists.assert_called_once_with(chunk)
    store.path.assert_called_once_with(chunk)
    source.load.assert_not_called()
    transform.assert_not_called()
    store.save.assert_not_called()

    assert result == output_path


def test_prepare_dem_task_loads_transforms_and_saves(
        chunk: XYZTile,
        dem: DEM,
) -> None:
    source = MagicMock()
    source.load.return_value = dem

    store = MagicMock()
    store.exists.return_value = False
    store.save.return_value = Path("dem_terrarium.tif")

    transformed_dem = MagicMock(spec=DEM)
    transform = MagicMock(
        return_value=transformed_dem,
    )

    task = PrepareDEMTask(
        source=source,
        store=store,
        transform=transform,
    )

    result = task(chunk)

    source.load.assert_called_once_with(chunk.bounds)
    transform.assert_called_once_with(dem)
    store.save.assert_called_once_with(
        tile=chunk,
        dem=transformed_dem,
    )

    assert result == Path("dem_terrarium.tif")


def test_prepare_dem_task_saves_without_transform(
        chunk: XYZTile,
        dem: DEM,
) -> None:
    source = MagicMock()
    source.load.return_value = dem

    store = MagicMock()
    store.exists.return_value = False
    store.save.return_value = Path("dem.tif")

    task = PrepareDEMTask(
        source=source,
        store=store,
    )

    result = task(chunk)

    source.load.assert_called_once_with(chunk.bounds)
    store.save.assert_called_once_with(
        tile=chunk,
        dem=dem,
    )

    assert result == Path("dem.tif")


def test_prepare_contours_task_skips_existing_chunk(
        chunk: XYZTile,
) -> None:
    source = MagicMock()
    store = MagicMock()
    store.exists.return_value = True
    transform = MagicMock()

    task = PrepareContoursTask(
        source=source,
        store=store,
        interval=20,
        simplify_tolerance=0.0001,
        transform=transform,
    )

    task(chunk)

    store.exists.assert_called_once_with(chunk)
    source.load.assert_not_called()
    transform.assert_not_called()


def test_prepare_contours_task_runs_processing_pipeline(
        monkeypatch: pytest.MonkeyPatch,
        chunk: XYZTile,
        dem: DEM,
) -> None:
    source = MagicMock()
    source.load.return_value = dem

    store = MagicMock()
    store.exists.return_value = False

    transformed_dem = MagicMock(spec=DEM)
    transform = MagicMock(
        return_value=transformed_dem,
    )

    task = PrepareContoursTask(
        source=source,
        store=store,
        interval=20,
        simplify_tolerance=0.0001,
        transform=transform,
    )

    write_dem = MagicMock()
    generate_contours = MagicMock()
    generate_mvt = MagicMock()
    publish_mvt_tile = MagicMock()

    monkeypatch.setattr(task, "_write_dem", write_dem)
    monkeypatch.setattr(task, "_generate_contours", generate_contours)
    monkeypatch.setattr(task, "_generate_mvt", generate_mvt)
    monkeypatch.setattr(task, "_publish_mvt_tile", publish_mvt_tile)

    task(chunk)

    source.load.assert_called_once_with(chunk.bounds)
    transform.assert_called_once_with(dem)

    write_call = write_dem.call_args.kwargs
    contour_call = generate_contours.call_args.kwargs
    mvt_call = generate_mvt.call_args.kwargs
    publish_call = publish_mvt_tile.call_args.kwargs

    assert write_call["dem"] is transformed_dem
    assert write_call["output_path"].name == "dem.tif"

    assert contour_call["input_path"] == write_call["output_path"]
    assert contour_call["output_path"].name == "contours.geojson"

    assert mvt_call["input_path"] == contour_call["output_path"]
    assert mvt_call["output_dir"].name == "mvt"
    assert mvt_call["zoom"] == chunk.z

    assert publish_call["source_dir"] == mvt_call["output_dir"]
    assert publish_call["chunk"] == chunk


def test_generate_tiles_task_skips_existing_tiles(
        monkeypatch: pytest.MonkeyPatch,
        chunk: XYZTile,
) -> None:
    source = MagicMock()
    store = MagicMock()

    task = GenerateTilesTask(
        source=source,
        store=store,
    )

    tiles_exist = MagicMock(
        return_value=True,
    )

    monkeypatch.setattr(
        task,
        "_tiles_exist",
        tiles_exist,
    )

    task(
        chunk,
        max_zoom=10,
        processes=2,
    )

    tiles_exist.assert_called_once_with(
        chunk=chunk,
        max_zoom=10,
    )
    source.path.assert_not_called()


def test_generate_tiles_task_raises_if_dem_is_missing(
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        chunk: XYZTile,
) -> None:
    source = MagicMock()
    source.path.return_value = tmp_path / "missing.tif"

    store = MagicMock()

    task = GenerateTilesTask(
        source=source,
        store=store,
    )

    tiles_exist = MagicMock(
        return_value=False,
    )

    monkeypatch.setattr(
        task,
        "_tiles_exist",
        tiles_exist,
    )

    with pytest.raises(
            FileNotFoundError,
            match="Terrain raster not found",
    ):
        task(chunk)

    source.path.assert_called_once_with(chunk)


def test_generate_tiles_task_runs_generation_and_publish(
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        chunk: XYZTile,
) -> None:
    input_path = tmp_path / "dem_terrarium.tif"
    input_path.touch()

    source = MagicMock()
    source.path.return_value = input_path

    store = MagicMock()

    task = GenerateTilesTask(
        source=source,
        store=store,
    )

    tiles_exist = MagicMock(
        return_value=False,
    )
    generate_tiles = MagicMock()
    publish_tiles = MagicMock()

    monkeypatch.setattr(
        task,
        "_tiles_exist",
        tiles_exist,
    )
    monkeypatch.setattr(
        task,
        "_generate_tiles",
        generate_tiles,
    )
    monkeypatch.setattr(
        task,
        "_publish_tiles",
        publish_tiles,
    )

    task(
        chunk,
        max_zoom=10,
        processes=2,
    )

    generate_call = generate_tiles.call_args.kwargs
    publish_call = publish_tiles.call_args.kwargs

    assert generate_call["input_path"] == input_path
    assert generate_call["output_dir"].name.startswith(
        "topoprofile-terrain-"
    )
    assert generate_call["min_zoom"] == chunk.z
    assert generate_call["max_zoom"] == 10
    assert generate_call["processes"] == 2

    assert publish_call["source_dir"] == generate_call["output_dir"]
    assert publish_call["chunk"] == chunk
    assert publish_call["max_zoom"] == 10


def test_generate_tiles_task_raises_if_generated_tile_is_missing(
        tmp_path: Path,
        chunk: XYZTile,
) -> None:
    source = MagicMock()
    store = MagicMock()

    task = GenerateTilesTask(
        source=source,
        store=store,
    )

    with pytest.raises(
            FileNotFoundError,
            match="Generated terrain tile not found",
    ):
        task._publish_tiles(
            source_dir=tmp_path,
            chunk=chunk,
            max_zoom=chunk.z,
        )
