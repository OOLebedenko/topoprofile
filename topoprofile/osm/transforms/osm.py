import logging
from dataclasses import replace
from typing import Any, TypeVar

from shapely.geometry import box, mapping, shape

from topoprofile.osm.models import (
    OSMFeatureChunkCollection,
    OSMFeatureCollection,
)
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
from topoprofile.processing.transforms import Transform

logger = logging.getLogger(__name__)

OSMFeatureCollectionT = TypeVar(
    "OSMFeatureCollectionT",
    bound=OSMFeatureCollection,
)

type OSMTransform = Transform[OSMFeatureCollection]
type OSMChunkTransform = Transform[OSMFeatureChunkCollection]


# OSM feature collection transforms.


class RemoveNodeReferences:
    """Remove source OSM node references not required for rendering."""

    def __call__(
            self,
            features: OSMFeatureCollectionT,
            /,
    ) -> OSMFeatureCollectionT:
        transformed = []

        for feature in features.features:
            properties = dict(feature.get("properties", {}))
            properties.pop("nodes", None)

            transformed.append({
                **feature,
                "properties": properties,
            })

        return replace(
            features,
            features=tuple(transformed),
        )


class FilterHikingRoutes:
    """Keep renderable hiking route features."""

    def __call__(
            self,
            features: OSMFeatureCollectionT,
    ) -> OSMFeatureCollectionT:
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

        return replace(
            features,
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


class PrepareMountainInfrastructure:
    """Convert mountain infrastructure to renderable point features."""

    def __call__(
            self,
            features: OSMFeatureCollectionT,
    ) -> OSMFeatureCollectionT:
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

        return replace(
            features,
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


class FilterTerrainSurface:
    """Keep renderable terrain surface features."""

    def __call__(
            self,
            features: OSMFeatureCollectionT,
    ) -> OSMFeatureCollectionT:
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

        return replace(
            features,
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


# OSM feature chunk collection transforms.


class ClipToBounds:
    """Clip OSM features to geographic bounds."""

    def __call__(
            self,
            features: OSMFeatureChunkCollection,
    ) -> OSMFeatureChunkCollection:
        bounds = features.chunk.bounds

        clip_geometry = box(
            bounds.west,
            bounds.south,
            bounds.east,
            bounds.north,
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

        return replace(
            features,
            features=tuple(clipped_features),
        )
