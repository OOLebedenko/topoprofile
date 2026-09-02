import pytest

from topoprofile.geo.tiles import XYZTile, parent_tile, xyz_to_bounds


def test_xyz_to_bounds_world_tile() -> None:
    """Test bounds of the root XYZ tile covering the whole Web Mercator world."""
    tile = XYZTile(
        z=0,
        x=0,
        y=0,
    )

    bounds = xyz_to_bounds(tile)

    assert bounds.west == pytest.approx(-180.0)
    assert bounds.south == pytest.approx(-85.05112878)
    assert bounds.east == pytest.approx(180.0)
    assert bounds.north == pytest.approx(85.05112878)


def test_xyz_to_bounds_southeast_quarter() -> None:
    """Test bounds of a tile in the south-eastern world quadrant."""
    tile = XYZTile(
        z=1,
        x=1,
        y=1,
    )

    bounds = xyz_to_bounds(tile)

    assert bounds.west == pytest.approx(0.0)
    assert bounds.south == pytest.approx(-85.05112878)
    assert bounds.east == pytest.approx(180.0)
    assert bounds.north == pytest.approx(0.0)


def test_parent_tile() -> None:
    """Test finding an ancestor tile at a lower zoom level."""
    tile = XYZTile(
        z=11,
        x=1265,
        y=742,
    )

    parent = parent_tile(
        tile=tile,
        target_zoom=8,
    )

    assert parent == XYZTile(
        z=8,
        x=158,
        y=92,
    )


def test_parent_tile_at_same_zoom() -> None:
    """Test that a tile is its own ancestor at the same zoom level."""
    tile = XYZTile(
        z=8,
        x=158,
        y=92,
    )

    parent = parent_tile(
        tile=tile,
        target_zoom=8,
    )

    assert parent == tile


def test_parent_tile_rejects_higher_target_zoom() -> None:
    """Test that an ancestor cannot have a higher zoom than the source tile."""
    tile = XYZTile(
        z=8,
        x=158,
        y=92,
    )

    with pytest.raises(
        ValueError,
        match="Target zoom must not exceed tile zoom",
    ):
        parent_tile(
            tile=tile,
            target_zoom=9,
        )
