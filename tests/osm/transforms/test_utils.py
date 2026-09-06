from topoprofile.osm.transforms.utils import (
    geometry_type,
    has_coordinates,
    is_valid_geometry,
)


def test_geometry_helpers() -> None:
    geometry = {
        "type": "Polygon",
        "coordinates": [[
            [42.0, 43.0],
            [42.1, 43.0],
            [42.1, 43.1],
            [42.0, 43.0],
        ]],
    }

    assert geometry_type(geometry) == "Polygon"
    assert has_coordinates(geometry)
    assert is_valid_geometry(geometry)


def test_invalid_geometry() -> None:
    geometry = {
        "type": "Polygon",
        "coordinates": [],
    }

    assert geometry_type(geometry) == "Polygon"
    assert not has_coordinates(geometry)
    assert not is_valid_geometry(geometry)
