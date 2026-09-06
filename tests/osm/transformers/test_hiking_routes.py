from topoprofile.geo.models import Bounds
from topoprofile.osm.transformers.hiking_routes import HikingRouteTransformer


def test_transform_keeps_renderable_routes(
        osm_geojson: dict,
        bounds: Bounds,
) -> None:
    transformer = HikingRouteTransformer()

    result = transformer.transform(
        osm_geojson,
        bounds,
    )

    assert len(result["features"]) == 2
    assert result["features"][0]["properties"]["route"] == "hiking"
    assert result["features"][1]["properties"]["route"] == "foot"
