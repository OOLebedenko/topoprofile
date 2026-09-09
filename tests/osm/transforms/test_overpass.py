from unittest.mock import patch

import pytest

from topoprofile.osm.models import OverpassData
from topoprofile.osm.transforms.overpass import (
    GeoJSONTransform,
    GeoJSONTransformError,
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
                    "coordinates": [[
                        [42.0, 43.0],
                        [42.1, 43.0],
                        [42.1, 43.1],
                        [42.0, 43.0],
                    ]],
                },
                "properties": {
                    "type": "way",
                    "id": 12345,
                    "tags": {
                        "natural": "glacier",
                        "name": "Some Glacier",
                    },
                },
            },
        ],
    }


def test_geojson_transform_flattens_tags(
        glacier_geojson: dict,
) -> None:
    with patch(
            "topoprofile.osm.transforms.overpass.osm2geojson.json2geojson",
            return_value=glacier_geojson,
    ):
        result = GeoJSONTransform()(
            OverpassData(
                elements=(),
            ),
        )

    properties = result.features[0]["properties"]

    assert properties["natural"] == "glacier"
    assert properties["name"] == "Some Glacier"
    assert properties["osm_type"] == "way"
    assert properties["osm_id"] == 12345
    assert "tags" not in properties


def test_geojson_transform_raises_conversion_error() -> None:
    with patch(
            "topoprofile.osm.transforms.overpass.osm2geojson.json2geojson",
            side_effect=ValueError("conversion failed"),
    ), pytest.raises(
        GeoJSONTransformError,
        match="Failed to convert Overpass data to GeoJSON",
    ):
        GeoJSONTransform()(
            OverpassData(
                elements=(),
            ),
        )


def test_geojson_transform_propagates_normalization_error(
        glacier_geojson: dict,
) -> None:
    transform = GeoJSONTransform()

    with patch(
            "topoprofile.osm.transforms.overpass.osm2geojson.json2geojson",
            return_value=glacier_geojson,
    ), patch.object(
        transform,
        "_flatten_tags",
        side_effect=RuntimeError("normalization failed"),
    ), pytest.raises(
        RuntimeError,
        match="normalization failed",
    ):
        transform(
            OverpassData(
                elements=(),
            ),
        )
