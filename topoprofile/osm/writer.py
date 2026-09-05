import json
from abc import ABC, abstractmethod
from pathlib import Path

from topoprofile.osm.geojson import GeoJSON


class GeoJSONWriter(ABC):
    """Base interface for writing GeoJSON data."""

    @abstractmethod
    def write(
            self,
            path: Path,
            geojson: GeoJSON,
    ) -> None:
        """Write GeoJSON data to the given path."""


class CompactGeoJSONWriter(GeoJSONWriter):
    """Write GeoJSON data as compact JSON."""

    def write(
            self,
            path: Path,
            geojson: GeoJSON,
    ) -> None:
        path.write_text(
            json.dumps(
                geojson,
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
