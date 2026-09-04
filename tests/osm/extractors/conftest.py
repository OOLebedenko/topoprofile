from unittest.mock import Mock

import pytest

from topoprofile.geo.models import Bounds
from topoprofile.osm.client import OverpassGeoJSONClient


@pytest.fixture
def bounds() -> Bounds:
    return Bounds(
        west=42.0,
        south=43.0,
        east=44.0,
        north=45.0,
    )


@pytest.fixture
def overpass_geojson_client() -> Mock:
    return Mock(spec=OverpassGeoJSONClient)


@pytest.fixture
def osm_geojson() -> dict:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "properties": {"natural": "glacier"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[42.0, 43.0]]],
                },
            },
            {
                "properties": {"natural": "cliff"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[42.0, 43.0]],
                },
            },
            {
                "properties": {"route": "hiking"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[42.0, 43.0], [42.1, 43.1]],
                },
            },
            {
                "properties": {"route": "foot"},
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [
                            [42.0, 43.0],
                            [42.1, 43.1],
                        ],
                    ],
                },
            },
            {
                "properties": {"natural": "forest"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[42.0, 43.0]]],
                },
            },
            {
                "properties": {"route": "bicycle"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[42.0, 43.0], [42.1, 43.1]],
                },
            },
        ],
    }
