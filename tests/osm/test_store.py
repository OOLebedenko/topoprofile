from pathlib import Path
from unittest.mock import Mock

from topoprofile.geo.models import XYZTile
from topoprofile.osm.models import OSMFeatureCollection
from topoprofile.osm.store import OSMStore


def test_store_returns_tile_path(
        tmp_path: Path,
) -> None:
    store = OSMStore(
        root=tmp_path,
        filename="hiking_routes.geojson",
        writer=Mock(),
    )

    tile = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    assert store.path(tile) == (
            tmp_path
            / "8"
            / "158"
            / "93"
            / "hiking_routes.geojson"
    )
    assert not store.exists(tile)

    store.path(tile).parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    store.path(tile).touch()

    assert store.exists(tile)


def test_store_saves_feature_collection(
        tmp_path: Path,
) -> None:
    writer = Mock()

    store = OSMStore(
        root=tmp_path,
        filename="hiking_routes.geojson",
        writer=writer,
    )

    tile = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    features = OSMFeatureCollection(
        features=(
            {
                "type": "Feature",
                "properties": {
                    "route": "hiking",
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [42.3, 43.3],
                        [42.4, 43.4],
                    ],
                },
            },
        ),
    )

    result = store.save(
        tile,
        features,
    )

    expected_path = (
            tmp_path
            / "8"
            / "158"
            / "93"
            / "hiking_routes.geojson"
    )

    assert result == expected_path
    assert expected_path.parent.is_dir()

    writer.write.assert_called_once_with(
        expected_path,
        {
            "type": "FeatureCollection",
            "features": list(features.features),
        },
    )
