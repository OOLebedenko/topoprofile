from unittest.mock import Mock

from topoprofile.geo.models import Bounds
from topoprofile.osm.extractors.mountain_infrastructure import (
    MountainInfrastructureExtractor,
)


def test_build_query(
        bounds: Bounds,
        overpass_geojson_client: Mock,
) -> None:
    extractor = MountainInfrastructureExtractor(
        overpass_geojson_client
    )

    query = extractor._build_query(bounds)

    assert "(43.0,42.0,45.0,44.0)" in query
    assert "alpine_hut" in query
    assert "wilderness_hut" in query
    assert "shelter" in query
    assert "weather_shelter" in query
    assert "node" in query


def test_process_keeps_renderable_infrastructure(
        osm_geojson: dict,
        overpass_geojson_client: Mock,
) -> None:
    extractor = MountainInfrastructureExtractor(
        overpass_geojson_client
    )

    result = extractor._process(osm_geojson)

    assert len(result["features"]) == 2

    assert (
            result["features"][0]["properties"]["tourism"]
            == "alpine_hut"
    )

    assert (
            result["features"][1]["properties"]["shelter_type"]
            == "weather_shelter"
    )
