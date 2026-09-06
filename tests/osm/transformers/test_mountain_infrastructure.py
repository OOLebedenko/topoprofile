from topoprofile.geo.models import Bounds
from topoprofile.osm.transformers.terrain_surface import TerrainSurfaceTransformer


def test_transform_keeps_renderable_features(
        osm_geojson: dict,
        bounds: Bounds,
) -> None:
    transformer = TerrainSurfaceTransformer()

    result = transformer.transform(
        osm_geojson,
        bounds,
    )

    assert len(result["features"]) == 2
    assert result["features"][0]["properties"]["natural"] == "glacier"
    assert result["features"][1]["properties"]["natural"] == "cliff"
