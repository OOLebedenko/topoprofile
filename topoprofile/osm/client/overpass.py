import logging
import time
from typing import Any

import requests

from topoprofile.osm.client.config import (
    MAX_ATTEMPTS,
    OVERPASS_ENDPOINTS,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_DELAY_SECONDS,
)
from topoprofile.osm.geojson import OverpassJSON

logger = logging.getLogger(__name__)


class OverpassClientError(RuntimeError):
    """Raised when data cannot be fetched from the Overpass API."""


class OverpassClient:
    """Client for fetching OSM data from the Overpass API."""

    def __init__(
            self,
            endpoints: tuple[str, ...] = OVERPASS_ENDPOINTS,
            timeout: int = REQUEST_TIMEOUT_SECONDS,
            max_attempts: int = MAX_ATTEMPTS,
            retry_delay: int = RETRY_DELAY_SECONDS,
    ) -> None:
        self._endpoints = endpoints
        self._timeout = timeout
        self._max_attempts = max_attempts
        self._retry_delay = retry_delay
        self._headers = {
            "User-Agent": "topoprofile",
            "Accept": "application/json",
        }

    def fetch(
            self,
            query: str,
    ) -> OverpassJSON:
        """Fetch OSM data from the available Overpass endpoints."""
        for attempt in range(1, self._max_attempts + 1):
            try:
                return self._fetch_from_endpoints(
                    query,
                )
            except OverpassClientError:
                if attempt == self._max_attempts:
                    raise

                delay = self._retry_delay * attempt

                logger.warning(
                    "Overpass attempt %d/%d failed. Retrying in %ds.",
                    attempt,
                    self._max_attempts,
                    delay,
                )

                time.sleep(delay)

    def _fetch_from_endpoints(
            self,
            query: str,
    ) -> OverpassJSON:
        """Fetch data from the first available Overpass endpoint."""
        errors = []
        last_error = None

        for endpoint in self._endpoints:
            try:
                return self._fetch_from_endpoint(
                    endpoint,
                    query,
                )
            except (
                    requests.RequestException,
                    TypeError,
            ) as error:
                last_error = error

                message = f"{endpoint}: {error}"
                errors.append(message)

                logger.debug(
                    "Overpass endpoint failed: %s",
                    message,
                )

        raise OverpassClientError(
            "All Overpass endpoints failed:\n"
            + "\n".join(errors)
        ) from last_error

    def _fetch_from_endpoint(
            self,
            endpoint: str,
            query: str,
    ) -> OverpassJSON:
        """Fetch and validate data from a single Overpass endpoint."""
        logger.info(
            "Requesting OSM data from %s",
            endpoint,
        )

        data = self._request(
            endpoint,
            query,
        )

        elements = self._extract_elements(
            data,
        )

        logger.info(
            "Received %d elements from %s",
            len(elements),
            endpoint,
        )

        return data

    def _request(
            self,
            endpoint: str,
            query: str,
    ) -> Any:
        """Perform an HTTP request to a single Overpass endpoint."""
        response = requests.post(
            endpoint,
            data={"data": query},
            headers=self._headers,
            timeout=self._timeout,
        )

        response.raise_for_status()

        return response.json()

    @staticmethod
    def _extract_elements(
            data: Any,
    ) -> list[Any]:
        """Extract and validate the elements list from an Overpass response."""
        if not isinstance(data, dict):
            raise TypeError(
                "Overpass response is not a JSON object."
            )

        elements = data.get("elements")

        if not isinstance(elements, list):
            raise TypeError(
                "Overpass response has no elements list."
            )

        return elements
