import json
from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path

import mapbox_vector_tile
from pyproj import Transformer
from shapely.geometry import GeometryCollection, shape
from shapely.geometry.base import BaseGeometry

from topoprofile.geo.models import Bounds
from topoprofile.osm.models import GeoJSON

WGS84_TO_WEB_MERCATOR = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:3857",
    always_xy=True,
)


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


class MVTWriter:
    """Write GeoJSON features as a Mapbox Vector Tile."""

    def __init__(
            self,
            layer_name: str,
    ) -> None:
        self._layer_name = layer_name

    def write(
            self,
            path: Path,
            geojson: GeoJSON,
            bounds: Bounds,
    ) -> None:
        features = []

        for feature in geojson["features"]:
            geometry = feature.get("geometry")

            if geometry is None:
                continue

            for part in self._iter_geometries(
                    shape(geometry),
            ):
                features.append({
                    "geometry": part,
                    "properties": feature.get(
                        "properties",
                        {},
                    ),
                })

        west, south = WGS84_TO_WEB_MERCATOR.transform(
            bounds.west,
            bounds.south,
        )
        east, north = WGS84_TO_WEB_MERCATOR.transform(
            bounds.east,
            bounds.north,
        )

        tile = mapbox_vector_tile.encode(
            {
                "name": self._layer_name,
                "features": features,
            },
            default_options={
                "transformer": WGS84_TO_WEB_MERCATOR.transform,
                "quantize_bounds": (
                    west,
                    south,
                    east,
                    north,
                ),
            },
        )

        path.write_bytes(tile)

    @classmethod
    def _iter_geometries(
            cls,
            geometry: BaseGeometry,
    ) -> Iterator[BaseGeometry]:
        if geometry.is_empty:
            return

        if isinstance(geometry, GeometryCollection):
            for part in geometry.geoms:
                yield from cls._iter_geometries(part)

            return

        yield geometry
