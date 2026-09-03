import logging
from typing import Any

import requests

from topoprofile.osm.geojson import GeoJSONConverter

logger = logging.getLogger(__name__)

OVERPASS_ENDPOINTS = (
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
)

REQUEST_TIMEOUT_SECONDS = 240


class OverpassClient:
    """Client for downloading OSM data from the Overpass API."""

    def __init__(
        self,
        endpoints: tuple[str, ...] = OVERPASS_ENDPOINTS,
        timeout: int = REQUEST_TIMEOUT_SECONDS,
    ) -> None:
        self.endpoints = endpoints
        self.timeout = timeout
        self._headers = {
            "User-Agent": "topoprofile",
            "Accept": "application/json",
        }

    def download(self, query: str) -> dict[str, Any]:
        """Download OSM data from the first available Overpass endpoint."""
        errors: list[str] = []

        for endpoint in self.endpoints:
            try:
                return self._download_from_endpoint(endpoint, query)
            except (requests.RequestException, TypeError) as error:
                message = f"{endpoint}: {error}"
                errors.append(message)
                logger.warning("Overpass request failed: %s", message)

        raise RuntimeError(
            "All Overpass endpoints failed:\n"
            + "\n".join(errors)
        )

    def _download_from_endpoint(
        self,
        endpoint: str,
        query: str,
    ) -> dict[str, Any]:
        """Download and validate data from a single Overpass endpoint."""
        logger.info("Requesting OSM data from %s", endpoint)

        raw_data = self._fetch(endpoint, query)
        elements = self._extract_elements(raw_data)

        logger.info(
            "Received %d elements from %s",
            len(elements),
            endpoint,
        )

        return raw_data

    def _fetch(
        self,
        endpoint: str,
        query: str,
    ) -> Any:
        """Perform an HTTP request to a single Overpass endpoint."""
        response = requests.post(
            endpoint,
            data={"data": query},
            headers=self._headers,
            timeout=self.timeout,
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


class OverpassGeoJSONClient:
    """Client for loading OSM data as normalized GeoJSON."""

    def __init__(
            self,
            overpass_client: OverpassClient,
            converter: GeoJSONConverter,
    ) -> None:
        self.overpass_client = overpass_client
        self.converter = converter

    def fetch(
            self,
            query: str,
    ) -> dict[str, Any]:
        """Fetch OSM data and convert it to normalized GeoJSON."""
        osm_json = self.overpass_client.download(query)
        return self.converter.convert(osm_json)
