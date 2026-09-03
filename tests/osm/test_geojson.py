from unittest.mock import patch

import pytest

from topoprofile.osm.geojson import (
    GeoJSONConverter,
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