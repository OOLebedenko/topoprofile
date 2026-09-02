import pytest

from topoprofile.geo.models import Bounds
from topoprofile.geo.region_chunks import RegionChunkResolver
from topoprofile.geo.tiles import XYZTile, xyz_to_bounds


def test_resolve_single_chunk() -> None:
    """Test that exact bounds of one XYZ tile resolve to that tile only."""
    resolver = RegionChunkResolver()

    tile = XYZTile(z=8, x=158, y=93)
    bounds = xyz_to_bounds(tile)

    chunks = resolver.resolve(
        bounds=bounds,
        zoom=8,
    )

    assert chunks == [tile]


def test_resolve_multiple_chunks() -> None:
    """Test that bounds spanning several tiles resolve to all of them."""
    resolver = RegionChunkResolver()

    northwest = xyz_to_bounds(
        XYZTile(z=8, x=158, y=93)
    )
    southeast = xyz_to_bounds(
        XYZTile(z=8, x=159, y=94)
    )

    bounds = Bounds(
        west=northwest.west,
        south=southeast.south,
        east=southeast.east,
        north=northwest.north,
    )

    chunks = resolver.resolve(
        bounds=bounds,
        zoom=8,
    )

    assert set(chunks) == {
        XYZTile(z=8, x=158, y=93),
        XYZTile(z=8, x=158, y=94),
        XYZTile(z=8, x=159, y=93),
        XYZTile(z=8, x=159, y=94),
    }


def test_resolve_rejects_negative_zoom() -> None:
    """Test that negative zoom is rejected."""
    resolver = RegionChunkResolver()

    bounds = Bounds(
        west=42.0,
        south=43.0,
        east=43.0,
        north=44.0,
    )

    with pytest.raises(
            ValueError,
            match="Zoom must be non-negative",
    ):
        resolver.resolve(
            bounds=bounds,
            zoom=-1,
        )


def test_resolve_rejects_bounds_outside_web_mercator() -> None:
    """Test that bounds outside Web Mercator latitude limits are rejected."""
    resolver = RegionChunkResolver()

    bounds = Bounds(
        west=0.0,
        south=84.0,
        east=1.0,
        north=86.0,
    )

    with pytest.raises(
            ValueError,
            match="Web Mercator",
    ):
        resolver.resolve(
            bounds=bounds,
            zoom=8,
        )
