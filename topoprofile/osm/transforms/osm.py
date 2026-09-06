import logging
from abc import ABC, abstractmethod
from typing import Any

from shapely.geometry import box, mapping, shape

from topoprofile.geo.models import Bounds
from topoprofile.osm.models import OSMFeatureCollection
from topoprofile.osm.tags import (
    HIKING_ROUTE_TYPES,
    HIKING_TRAIL_TYPES,
    MOUNTAIN_HUT_TYPES,
    MOUNTAIN_SHELTER_TYPES,
    TERRAIN_AREA_TYPES,
    TERRAIN_LINE_TYPES,
)
from topoprofile.osm.transforms.utils import (
    LINE_GEOMETRY_TYPES,
    POLYGON_GEOMETRY_TYPES,
    geometry_type,
    is_valid_geometry,
)

logger = logging.getLogger(__name__)


class OSMTransform(ABC):
    """Transform OSM feature data."""

    @abstractmethod
    def __call__(
            self,
            features: OSMFeatureCollection,
    ) -> OSMFeatureCollection:
        """Transform OSM features."""


class Compose(OSMTransform):
    """Apply OSM transformations sequentially."""

    def __init__(
            self,
            transforms: tuple[OSMTransform, ...],
    ) -> None:
        self._transforms = transforms

    def __call__(
            self,
            features: OSMFeatureCollection,
    ) -> OSMFeatureCollection:
        for transform in self._transforms:
            features = transform(features)

        return features


class ClipToBounds(OSMTransform):
    """Clip OSM features to geographic bounds."""

    def __init__(
            self,
            bounds: Bounds,
    ) -> None:
        self._bounds = bounds

    def __call__(
            self,
            features: OSMFeatureCollection,
    ) -> OSMFeatureCollection:
        clip_geometry = box(
            self._bounds.west,
            self._bounds.south,
            self._bounds.east,
            self._bounds.north,
        )

        clipped_features = []

        for feature in features.features:
            geometry = feature.get("geometry")

            if not is_valid_geometry(geometry):
                continue

            clipped_geometry = shape(geometry).intersection(
                clip_geometry,
            )

            if clipped_geometry.is_empty:
                continue

            clipped_features.append({
                **feature,
                "geometry": mapping(clipped_geometry),
            })

        return OSMFeatureCollection(
            features=tuple(clipped_features),
        )


class FilterHikingRoutes(OSMTransform):
    """Keep renderable hiking route features."""

    def __call__(
            self,
            features: OSMFeatureCollection,
    ) -> OSMFeatureCollection:
        filtered = [
            feature
            for feature in features.features
            if self._is_renderable(feature)
        ]

        logger.info(
            "Hiking routes: total=%d, kept=%d, rejected=%d",
            len(features.features),
            len(filtered),
            len(features.features) - len(filtered),
        )

        return OSMFeatureCollection(
            features=tuple(filtered),
        )

    @staticmethod
    def _is_renderable(
            feature: dict[str, Any],
    ) -> bool:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return False

        feature_geometry = geometry_type(geometry)

        if feature_geometry not in LINE_GEOMETRY_TYPES:
            return False

        route = properties.get("route")
        highway = properties.get("highway")
        aerialway = properties.get("aerialway")

        return (
                route in HIKING_ROUTE_TYPES
                or highway in HIKING_TRAIL_TYPES
                or aerialway is not None
        )


class PrepareMountainInfrastructure(OSMTransform):
    """Convert mountain infrastructure to renderable point features."""

    def __call__(
            self,
            features: OSMFeatureCollection,
    ) -> OSMFeatureCollection:
        transformed = []

        for feature in features.features:
            result = self._transform_feature(feature)

            if result is not None:
                transformed.append(result)

        logger.info(
            "Mountain infrastructure: total=%d, kept=%d, rejected=%d",
            len(features.features),
            len(transformed),
            len(features.features) - len(transformed),
        )

        return OSMFeatureCollection(
            features=tuple(transformed),
        )

    @staticmethod
    def _transform_feature(
            feature: dict[str, Any],
    ) -> dict[str, Any] | None:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return None

        feature_geometry = geometry_type(geometry)

        if properties.get("tourism") in MOUNTAIN_HUT_TYPES:
            if feature_geometry == "Point":
                return feature

            return None

        if (
                properties.get("amenity") == "shelter"
                and properties.get("shelter_type")
                in MOUNTAIN_SHELTER_TYPES
        ):
            if feature_geometry == "Point":
                return feature

            if feature_geometry in POLYGON_GEOMETRY_TYPES:
                transformed = dict(feature)
                transformed["geometry"] = mapping(
                    shape(geometry).centroid
                )

                return transformed

        return None


class FilterTerrainSurface(OSMTransform):
    """Keep renderable terrain surface features."""

    def __call__(
            self,
            features: OSMFeatureCollection,
    ) -> OSMFeatureCollection:
        filtered = [
            feature
            for feature in features.features
            if self._is_renderable(feature)
        ]

        logger.info(
            "Terrain surface features: total=%d, kept=%d, rejected=%d",
            len(features.features),
            len(filtered),
            len(features.features) - len(filtered),
        )

        return OSMFeatureCollection(
            features=tuple(filtered),
        )

    @staticmethod
    def _is_renderable(
            feature: dict[str, Any],
    ) -> bool:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry")

        if not is_valid_geometry(geometry):
            return False

        natural = properties.get("natural")
        feature_geometry = geometry_type(geometry)

        if natural in TERRAIN_AREA_TYPES:
            return feature_geometry in POLYGON_GEOMETRY_TYPES

        if natural in TERRAIN_LINE_TYPES:
            return feature_geometry in LINE_GEOMETRY_TYPES

        return False
