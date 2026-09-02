from pathlib import Path
from tempfile import TemporaryDirectory

from topoprofile.domain.terrain import TerrainRequest
from topoprofile.prep.dem_utils.convert import convert_dem_to_terrarium
from topoprofile.prep.dem_utils.download import download_dem
from topoprofile.prep.dem_utils.generate import generate_terrain_tiles
from topoprofile.prep.dem_utils.publish import publish_terrain_tiles
from topoprofile.prep.terrain_paths import TerrainPaths


def prepare_terrain(
    request: TerrainRequest,
    paths: TerrainPaths,
) -> None:
    """Prepare terrain data for arbitrary geographic bounds."""
    raw_dem = download_dem(
        bounds=request.bounds,
        resolution=request.resolution,
        output_path=paths.raw_dem,
    )

    terrarium_dem = convert_dem_to_terrarium(
        input_path=raw_dem,
        output_path=paths.terrarium_dem,
    )

    with TemporaryDirectory(
        prefix="topoprofile-terrain-",
    ) as temp_dir:
        generated_tiles = Path(temp_dir)

        generate_terrain_tiles(
            input_path=terrarium_dem,
            output_dir=generated_tiles,
            min_zoom=request.min_zoom,
            max_zoom=request.max_zoom,
        )

        publish_terrain_tiles(
            source_dir=generated_tiles,
            output_dir=paths.terrain_tiles,
            bounds=request.bounds,
            min_zoom=request.min_zoom,
            max_zoom=request.max_zoom,
        )