from unittest.mock import patch

import pytest

from topoprofile.geo.tiles import XYZTile, xyz_to_bounds
from topoprofile.osm.geojson import (
    GeoJSONConverter,
    clip_to_bounds,
    geometry_type,
    has_coordinates,
    is_valid_geometry,
)


@pytest.fixture
def glacier_geojson() -> dict:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": 12345,
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [42.0, 43.0],
                            [42.1, 43.0],
                            [42.1, 43.1],
                            [42.0, 43.0],
                        ]
                    ],
                },
                "properties": {
                    "type": "way",
                    "id": 12345,
                    "tags": {
                        "natural": "glacier",
                        "name": "Some Glacier",
                    },
                },
            }
        ],
    }


def test_geometry_helpers(glacier_geojson: dict) -> None:
    geometry = glacier_geojson["features"][0]["geometry"]

    assert geometry_type(geometry) == "Polygon"
    assert has_coordinates(geometry)
    assert is_valid_geometry(geometry)


def test_invalid_geometry() -> None:
    geometry = {
        "type": "Polygon",
        "coordinates": [],
    }

    assert geometry_type(geometry) == "Polygon"
    assert not has_coordinates(geometry)
    assert not is_valid_geometry(geometry)


def test_converter_flattens_tags(glacier_geojson: dict) -> None:
    with patch(
            "topoprofile.osm.geojson.osm2geojson.json2geojson",
            return_value=glacier_geojson,
    ):
        result = GeoJSONConverter().convert({})

    properties = result["features"][0]["properties"]

    assert properties["natural"] == "glacier"
    assert properties["name"] == "Some Glacier"
    assert properties["osm_type"] == "way"
    assert properties["osm_id"] == 12345
    assert "tags" not in properties


def test_clip_to_bounds_splits_feature_between_adjacent_chunks() -> None:
    left_bounds = xyz_to_bounds(
        XYZTile(z=8, x=157, y=93),
    )
    right_bounds = xyz_to_bounds(
        XYZTile(z=8, x=158, y=93),
    )

    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "osm_type": "relation",
                    "osm_id": 15394285,
                    "route": "hiking",
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [42.0, 43.5],
                        [42.4, 43.5],
                    ],
                },
            },
        ],
    }

    left = clip_to_bounds(
        geojson,
        left_bounds,
    )
    right = clip_to_bounds(
        geojson,
        right_bounds,
    )

    assert left["features"][0]["geometry"]["coordinates"] == (
        (42.0, 43.5),
        (42.1875, 43.5),
    )

    assert right["features"][0]["geometry"]["coordinates"] == (
        (42.1875, 43.5),
        (42.4, 43.5),
    )
