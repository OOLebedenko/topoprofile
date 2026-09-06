from pathlib import Path
from unittest.mock import Mock

from topoprofile.geo.models import XYZTile
from topoprofile.osm.models import (
    OSMFeatureCollection,
    OverpassData,
)
from topoprofile.osm.task import PrepareOSMTask


def test_prepare_osm_task_returns_existing_output(
        tmp_path: Path,
) -> None:
    tile = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    output_path = tmp_path / "hiking_routes.geojson"

    source = Mock()
    store = Mock()
    overpass_transform = Mock()
    osm_transform = Mock()

    store.exists.return_value = True
    store.path.return_value = output_path

    task = PrepareOSMTask(
        source=source,
        store=store,
        overpass_transform=overpass_transform,
        osm_transform=osm_transform,
    )

    result = task(tile)

    assert result == output_path

    store.exists.assert_called_once_with(tile)
    store.path.assert_called_once_with(tile)
    source.load.assert_not_called()
    overpass_transform.assert_not_called()
    osm_transform.assert_not_called()
    store.save.assert_not_called()


def test_prepare_osm_task_runs_processing_pipeline(
        tmp_path: Path,
) -> None:
    tile = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    output_path = tmp_path / "hiking_routes.geojson"

    data = OverpassData(
        elements=(
            {
                "type": "way",
                "id": 123,
            },
        ),
    )

    features = OSMFeatureCollection(
        features=(),
    )

    source = Mock()
    source.load.return_value = data

    store = Mock()
    store.exists.return_value = False
    store.save.return_value = output_path

    overpass_transform = Mock(
        return_value=features,
    )
    osm_transform = Mock(
        return_value=features,
    )

    task = PrepareOSMTask(
        source=source,
        store=store,
        overpass_transform=overpass_transform,
        osm_transform=osm_transform,
    )

    result = task(tile)

    assert result == output_path

    store.exists.assert_called_once_with(tile)
    source.load.assert_called_once_with(tile.bounds)
    overpass_transform.assert_called_once_with(data)
    osm_transform.assert_called_once_with(features)
    store.save.assert_called_once_with(
        tile,
        features,
    )
