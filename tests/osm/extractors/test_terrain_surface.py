from unittest.mock import Mock

import pytest

from topoprofile.geo.models import Bounds
from topoprofile.osm.client import OverpassGeoJSONClient
from topoprofile.osm.extractors.terrain_surface import TerrainSurfaceExtractor


@pytest.fixture
def terrain_surface_geojson() -> dict:
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
                "properties": {"natural": "glacier"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[42.0, 43.0]],
                },
            },
            {
                "properties": {"natural": "forest"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[42.0, 43.0]]],
                },
            },
        ],
    }


def test_build_query() -> None:
    bounds = Bounds(
        west=42.0,
        south=43.0,
        east=44.0,
        north=45.0,
    )
    extractor = TerrainSurfaceExtractor(
        Mock(spec=OverpassGeoJSONClient)
    )

    query = extractor._build_query(bounds)

    assert "(43.0,42.0,45.0,44.0)" in query
    assert "glacier" in query
    assert "cliff" in query
    assert "way" in query
    assert "relation" in query


def test_process_keeps_renderable_features(
    terrain_surface_geojson: dict,
) -> None:
    extractor = TerrainSurfaceExtractor(
        Mock(spec=OverpassGeoJSONClient)
    )

    result = extractor._process(terrain_surface_geojson)

    assert len(result["features"]) == 2
    assert result["features"][0]["properties"]["natural"] == "glacier"
    assert result["features"][1]["properties"]["natural"] == "cliff"


def test_extract_fetches_and_processes_features() -> None:
    client = Mock(spec=OverpassGeoJSONClient)
    client.fetch.return_value = {
        "type": "FeatureCollection",
        "features": [
            {
                "properties": {"natural": "snowfield"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[42.0, 43.0]]],
                },
            }
        ],
    }
    bounds = Bounds(
        west=42.0,
        south=43.0,
        east=44.0,
        north=45.0,
    )
    extractor = TerrainSurfaceExtractor(client)

    result = extractor.extract(bounds)

    client.fetch.assert_called_once()
    assert len(result["features"]) == 1
    assert result["features"][0]["properties"]["natural"] == "snowfield"