from unittest.mock import Mock

from topoprofile.geo.models import Bounds
from topoprofile.osm.models import OverpassData
from topoprofile.osm.source import OverpassFeatureSource


def test_overpass_source_loads_data() -> None:
    bounds = Bounds(
        west=42.0,
        south=43.0,
        east=43.0,
        north=44.0,
    )

    query = Mock()
    query.build.return_value = "overpass query"

    client = Mock()
    client.fetch.return_value = {
        "elements": [
            {
                "type": "way",
                "id": 123,
            },
        ],
    }

    source = OverpassFeatureSource(
        query=query,
        client=client,
    )

    result = source.load(bounds)

    assert result == OverpassData(
        elements=(
            {
                "type": "way",
                "id": 123,
            },
        ),
    )

    query.build.assert_called_once_with(bounds)
    client.fetch.assert_called_once_with("overpass query")
