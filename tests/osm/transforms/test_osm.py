from topoprofile.geo.models import XYZTile
from topoprofile.osm.models import (
    OSMFeatureChunkCollection,
    OSMFeatureCollection,
)
from topoprofile.osm.transforms.osm import (
    ClipToBounds,
    FilterHikingRoutes,
    FilterTerrainSurface,
    PrepareMountainInfrastructure,
)
from topoprofile.processing.transforms import Compose


def test_filter_hiking_routes_keeps_renderable_routes(
        osm_features: OSMFeatureCollection,
) -> None:
    result = FilterHikingRoutes()(osm_features)

    assert len(result.features) == 1
    assert result.features[0]["properties"]["route"] == "hiking"


def test_filter_terrain_surface_keeps_renderable_features(
        osm_features: OSMFeatureCollection,
) -> None:
    result = FilterTerrainSurface()(osm_features)

    assert len(result.features) == 2
    assert result.features[0]["properties"]["natural"] == "glacier"
    assert result.features[1]["properties"]["natural"] == "cliff"


def test_prepare_mountain_infrastructure_keeps_renderable_features(
        osm_features: OSMFeatureCollection,
) -> None:
    result = PrepareMountainInfrastructure()(osm_features)

    assert len(result.features) == 2
    assert result.features[0]["properties"]["tourism"] == "alpine_hut"
    assert result.features[1]["properties"]["amenity"] == "shelter"


def test_prepare_mountain_infrastructure_converts_polygon_to_point() -> None:
    features = OSMFeatureCollection(
        features=(
            {
                "properties": {
                    "amenity": "shelter",
                    "shelter_type": "weather_shelter",
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [42.0, 43.0],
                        [42.2, 43.0],
                        [42.2, 43.2],
                        [42.0, 43.2],
                        [42.0, 43.0],
                    ]],
                },
            },
        ),
    )

    result = PrepareMountainInfrastructure()(features)

    assert len(result.features) == 1
    assert result.features[0]["geometry"]["type"] == "Point"


def test_clip_to_bounds_splits_feature_between_adjacent_tiles() -> None:
    left_chunk = XYZTile(
        z=8,
        x=157,
        y=93,
    )
    right_chunk = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    feature = {
        "type": "Feature",
        "properties": {
            "osm_type": "relation",
            "osm_id": 15394285,
            "route": "hiking",
        },
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [42.0, 43.5],
                [42.4, 43.5],
            ],
        },
    }

    left_features = OSMFeatureChunkCollection(
        features=(feature,),
        chunk=left_chunk,
    )

    right_features = OSMFeatureChunkCollection(
        features=(feature,),
        chunk=right_chunk,
    )

    left = ClipToBounds()(left_features)
    right = ClipToBounds()(right_features)

    assert left.features[0]["geometry"]["coordinates"] == (
        (42.0, 43.5),
        (42.1875, 43.5),
    )
    assert right.features[0]["geometry"]["coordinates"] == (
        (42.1875, 43.5),
        (42.4, 43.5),
    )


def test_compose_applies_transforms_sequentially() -> None:
    chunk = XYZTile(
        z=8,
        x=158,
        y=93,
    )

    features = OSMFeatureChunkCollection(
        chunk=chunk,
        features=(
            {
                "properties": {
                    "route": "hiking",
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [42.0, 43.5],
                        [42.4, 43.5],
                    ],
                },
            },
            {
                "properties": {
                    "route": "bicycle",
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [42.0, 43.5],
                        [42.4, 43.5],
                    ],
                },
            },
        ),
    )

    transform = Compose(
        transforms=(
            FilterHikingRoutes(),
            ClipToBounds(),
        ),
    )

    result = transform(features)

    assert isinstance(
        result,
        OSMFeatureChunkCollection,
    )
    assert result.chunk == chunk
    assert len(result.features) == 1
    assert result.features[0]["properties"]["route"] == "hiking"
