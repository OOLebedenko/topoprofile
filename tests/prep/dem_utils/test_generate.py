from pathlib import Path

import pytest

from topoprofile.prep.dem_utils import generate


def test_generate_terrain_tiles_raises_if_input_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        generate.generate_terrain_tiles(
            input_path=tmp_path / "missing.tif",
            output_dir=tmp_path / "tiles",
            min_zoom=8,
            max_zoom=14,
        )


@pytest.mark.parametrize(("min_zoom", "max_zoom"), [(-1, 14), (15, 14)])
def test_generate_terrain_tiles_rejects_invalid_zoom(
    tmp_path: Path,
    min_zoom: int,
    max_zoom: int,
) -> None:
    input_path = tmp_path / "dem_terrarium.tif"
    input_path.touch()

    with pytest.raises(ValueError):
        generate.generate_terrain_tiles(
            input_path=input_path,
            output_dir=tmp_path / "tiles",
            min_zoom=min_zoom,
            max_zoom=max_zoom,
        )
