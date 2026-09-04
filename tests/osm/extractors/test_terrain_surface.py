from unittest.mock import Mock

from topoprofile.geo.models import Bounds
from topoprofile.osm.extractors.terrain_surface import TerrainSurfaceExtractor


def test_build_query(
    bounds: Bounds,
    overpass_geojson_client: Mock,
) -> None:
    extractor = TerrainSurfaceExtractor(overpass_geojson_client)

    query = extractor._build_query(bounds)

    assert "(43.0,42.0,45.0,44.0)" in query
    assert "glacier" in query
    assert "cliff" in query
    assert "way" in query
    assert "relation" in query


def test_process_keeps_renderable_features(
    osm_geojson: dict,
    overpass_geojson_client: Mock,
) -> None:
    extractor = TerrainSurfaceExtractor(overpass_geojson_client)

    result = extractor._process(osm_geojson)

    assert len(result["features"]) == 2
    assert result["features"][0]["properties"]["natural"] == "glacier"
    assert result["features"][1]["properties"]["natural"] == "cliff"