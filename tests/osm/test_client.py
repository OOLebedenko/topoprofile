from unittest.mock import Mock, patch

import pytest
import requests

from topoprofile.osm.client.overpass import (
    OverpassClient,
    OverpassClientError,
)

TEST_ENDPOINTS = (
    "https://first.example",
    "https://second.example",
)


@pytest.fixture
def overpass_client() -> OverpassClient:
    return OverpassClient(
        endpoints=TEST_ENDPOINTS,
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


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        (
                {"endpoints": ()},
                "At least one Overpass endpoint is required.",
        ),
        (
                {"timeout": 0},
                "Request timeout must be greater than zero.",
        ),
        (
                {"max_attempts": 0},
                "Maximum attempts must be at least one.",
        ),
        (
                {"retry_delay": -1},
                "Retry delay cannot be negative.",
        ),
    ],
)
def test_overpass_client_validates_config(
        kwargs: dict,
        message: str,
) -> None:
    with pytest.raises(
            ValueError,
            match=message,
    ):
        OverpassClient(**kwargs)


def test_fetch_does_not_retry_http_400() -> None:
    client = OverpassClient(
        endpoints=TEST_ENDPOINTS,
        max_attempts=3,
        retry_delay=0,
    )

    response = Mock()
    response.status_code = 400
    response.raise_for_status.side_effect = requests.HTTPError(
        response=response,
    )

    with patch(
            "topoprofile.osm.client.overpass.requests.post",
            return_value=response,
    ) as post, pytest.raises(
        OverpassClientError,
        match="HTTP 400",
    ):
        client.fetch("test query")

    assert post.call_count == 1


def test_fetch_retries_http_429() -> None:
    client = OverpassClient(
        endpoints=(
            "https://first.example",
        ),
        max_attempts=2,
        retry_delay=0,
    )

    rate_limit_response = Mock()
    rate_limit_response.status_code = 429
    rate_limit_response.raise_for_status.side_effect = requests.HTTPError(
        response=rate_limit_response,
    )

    response = make_response(1)

    with patch(
            "topoprofile.osm.client.overpass.requests.post",
            side_effect=[
                rate_limit_response,
                response,
            ],
    ) as post:
        result = client.fetch("test query")

    assert result["elements"][0]["id"] == 1
    assert post.call_count == 2
