from typing import Any

POLYGON_GEOMETRY_TYPES = {
    "Polygon",
    "MultiPolygon",
}

LINE_GEOMETRY_TYPES = {
    "LineString",
    "MultiLineString",
}


def geometry_type(
        geometry: Any,
) -> str | None:
    """Return the GeoJSON geometry type."""
    if not isinstance(geometry, dict):
        return None

    value = geometry.get("type")

    return value if isinstance(value, str) else None


def has_coordinates(
        geometry: Any,
) -> bool:
    """Return whether a GeoJSON geometry has non-empty coordinates."""
    if not isinstance(geometry, dict):
        return False

    coordinates = geometry.get("coordinates")

    return (
            isinstance(coordinates, (list, tuple))
            and bool(coordinates)
    )


def is_valid_geometry(
        geometry: Any,
) -> bool:
    """Return whether a GeoJSON geometry has a type and coordinates."""
    return (
            geometry_type(geometry) is not None
            and has_coordinates(geometry)
    )
