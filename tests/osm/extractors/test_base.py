from typing import Any
from unittest.mock import Mock

from topoprofile.geo.models import Bounds
from topoprofile.osm.extractors.base import OverpassExtractor


class StubExtractor(OverpassExtractor):
    def _build_query(self, bounds: Bounds) -> str:
        return (
            f"{bounds.south},"
            f"{bounds.west},"
            f"{bounds.north},"
            f"{bounds.east}"
        )

    def _process(self, geojson: dict[str, Any]) -> dict[str, Any]:
        return geojson


def test_extract_fetches_and_processes_features(
        bounds: Bounds,
        overpass_geojson_client: Mock,
) -> None:
    geojson = {
        "type": "FeatureCollection",
        "features": [],
    }
    overpass_geojson_client.fetch.return_value = geojson
    extractor = StubExtractor(overpass_geojson_client)

    result = extractor.extract(bounds)

    overpass_geojson_client.fetch.assert_called_once_with(
        "43.0,42.0,45.0,44.0"
    )
    assert result == geojson
