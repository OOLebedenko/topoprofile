from pathlib import Path
from unittest.mock import MagicMock

from topoprofile.geo.models import XYZTile
from topoprofile.osm.models import (
    OSMFeatureChunkCollection,
    OSMFeatureCollection,
    OverpassData,
)
from topoprofile.osm.task import PrepareOSMChunkTask, PrepareOSMTask


def test_prepare_osm_task_runs_processing_pipeline() -> None:
    chunk = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    features = OSMFeatureChunkCollection(
        features=(),
        chunk=chunk,
    )

    transformed_features = OSMFeatureChunkCollection(
        features=(),
        chunk=chunk,
    )

    store = MagicMock()
    store.save.return_value = Path("output.geojson")

    transform = MagicMock(
        return_value=transformed_features,
    )

    task = PrepareOSMTask(
        store=store,
        transform=transform,
    )

    output_path = task(features)

    transform.assert_called_once_with(features)
    store.save.assert_called_once_with(
        chunk,
        transformed_features,
    )

    assert output_path == Path("output.geojson")


def test_prepare_osm_chunk_task_skips_existing_outputs() -> None:
    chunk = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    source = MagicMock()
    overpass_transform = MagicMock()

    dataset_task = MagicMock()
    dataset_task.exists.return_value = True

    task = PrepareOSMChunkTask(
        source=source,
        overpass_transform=overpass_transform,
        tasks=(dataset_task,),
    )

    task(chunk)

    source.load.assert_not_called()
    overpass_transform.assert_not_called()
    dataset_task.assert_not_called()


def test_prepare_osm_chunk_task_loads_data_once() -> None:
    chunk = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    data = OverpassData(
        elements=(),
    )

    features = OSMFeatureCollection(
        features=(),
    )

    chunk_features = OSMFeatureChunkCollection(
        features=features.features,
        chunk=chunk,
    )

    source = MagicMock()
    source.load.return_value = data

    overpass_transform = MagicMock(
        return_value=features,
    )

    first_task = MagicMock()
    first_task.exists.return_value = False

    second_task = MagicMock()
    second_task.exists.return_value = False

    third_task = MagicMock()
    third_task.exists.return_value = False

    task = PrepareOSMChunkTask(
        source=source,
        overpass_transform=overpass_transform,
        tasks=(
            first_task,
            second_task,
            third_task,
        ),
    )

    task(chunk)

    source.load.assert_called_once_with(chunk.bounds)
    overpass_transform.assert_called_once_with(data)

    first_task.assert_called_once_with(chunk_features)
    second_task.assert_called_once_with(chunk_features)
    third_task.assert_called_once_with(chunk_features)


def test_prepare_osm_chunk_task_skips_existing_dataset() -> None:
    chunk = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    data = OverpassData(
        elements=(),
    )

    features = OSMFeatureCollection(
        features=(),
    )

    chunk_features = OSMFeatureChunkCollection(
        features=features.features,
        chunk=chunk,
    )

    source = MagicMock()
    source.load.return_value = data

    overpass_transform = MagicMock(
        return_value=features,
    )

    existing_task = MagicMock()
    existing_task.exists.return_value = True

    missing_task = MagicMock()
    missing_task.exists.return_value = False

    task = PrepareOSMChunkTask(
        source=source,
        overpass_transform=overpass_transform,
        tasks=(
            existing_task,
            missing_task,
        ),
    )

    task(chunk)

    source.load.assert_called_once_with(chunk.bounds)

    existing_task.assert_not_called()
    missing_task.assert_called_once_with(chunk_features)
