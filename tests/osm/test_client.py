from unittest.mock import Mock, patch

import pytest
import requests

from topoprofile.osm.overpass.client import OverpassClient


def test_download_returns_data_from_first_endpoint() -> None:
    response = Mock()
    response.json.return_value = {
        "elements": [{"type": "way", "id": 1}],
    }

    client = OverpassClient(
        endpoints=("https://first.example",),
    )

    with patch(
        "topoprofile.osm.overpass.client.requests.post",
        return_value=response,
    ) as post:
        result = client.download("test query")

    assert result["elements"][0]["id"] == 1
    assert post.call_count == 1


def test_download_uses_next_endpoint_after_request_error() -> None:
    response = Mock()
    response.json.return_value = {
        "elements": [{"type": "way", "id": 2}],
    }

    client = OverpassClient(
        endpoints=(
            "https://first.example",
            "https://second.example",
        ),
    )

    with patch(
        "topoprofile.osm.overpass.client.requests.post",
        side_effect=[
            requests.ConnectionError("Connection failed"),
            response,
        ],
    ) as post:
        result = client.download("test query")

    assert result["elements"][0]["id"] == 2
    assert post.call_count == 2


def test_download_raises_if_all_endpoints_fail() -> None:
    client = OverpassClient(
        endpoints=(
            "https://first.example",
            "https://second.example",
        ),
    )

    with patch(
        "topoprofile.osm.overpass.client.requests.post",
        side_effect=requests.ConnectionError("Connection failed"),
    ), pytest.raises(
        RuntimeError,
        match="All Overpass endpoints failed",
    ):
        client.download("test query")