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

    def write(
            path: Path,
            data: dict,
    ) -> None:
        path.write_text(
            "",
            encoding="utf-8",
        )

    writer.write.side_effect = write

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

    expected_data = {
        "type": "FeatureCollection",
        "features": list(features.features),
    }

    assert result == expected_path
    assert expected_path.is_file()

    writer.write.assert_called_once()

    temporary_path, data = writer.write.call_args.args

    assert temporary_path != expected_path
    assert temporary_path.parent == expected_path.parent
    assert data == expected_data
