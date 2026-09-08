from unittest.mock import Mock, patch

import pytest
import requests

from topoprofile.osm.client.overpass import (
    OverpassClient,
    OverpassClientError,
)


@pytest.fixture
def overpass_client() -> OverpassClient:
    return OverpassClient(
        endpoints=(
            "https://first.example",
            "https://second.example",
        ),
        max_attempts=1,
    )


def make_response(
        element_id: int,
) -> Mock:
    response = Mock()
    response.json.return_value = {
        "elements": [
            {
                "type": "way",
                "id": element_id,
            }
        ],
    }
    return response


def test_fetch_returns_data_from_first_endpoint(
        overpass_client: OverpassClient,
) -> None:
    response = make_response(1)

    with patch(
        "topoprofile.osm.client.overpass.requests.post",
        return_value=response,
    ) as post:
        result = overpass_client.fetch("test query")

    assert result["elements"][0]["id"] == 1
    assert post.call_count == 1


def test_fetch_uses_next_endpoint_after_request_error(
        overpass_client: OverpassClient,
) -> None:
    response = make_response(2)

    with patch(
        "topoprofile.osm.client.overpass.requests.post",
        side_effect=[
            requests.ConnectionError("Connection failed"),
            response,
        ],
    ) as post:
        result = overpass_client.fetch("test query")

    assert result["elements"][0]["id"] == 2
    assert post.call_count == 2


def test_fetch_raises_if_all_endpoints_fail(
        overpass_client: OverpassClient,
) -> None:
    with patch(
        "topoprofile.osm.client.overpass.requests.post",
        side_effect=requests.ConnectionError("Connection failed"),
    ), pytest.raises(
        OverpassClientError,
        match="All Overpass endpoints failed",
    ):
        overpass_client.fetch("test query")
