import logging

from topoprofile.prep.dem_utils.convert import convert_dem_to_terrarium
from topoprofile.prep.dem_utils.download import (
    download_region_dem,
)
from topoprofile.prep.dem_utils.generate import generate_terrain_tiles
from topoprofile.prep.dem_utils.load import load_region_config
from topoprofile.prep.region_paths import get_region_paths
from topoprofile.prep.settings import REGION_ID

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def prepare_region(region_id: str) -> None:
    """Run the complete DEM preparation pipeline for one region."""
    paths = get_region_paths(region_id)
    region = load_region_config(paths.dem_config)

    raw_dem_path = download_region_dem(
        region=region,
        output_dir=paths.raw,
    )

    terrarium_path = convert_dem_to_terrarium(
        input_path=raw_dem_path,
        output_path=paths.prepared / "dem_terrarium.tif",
    )

    generate_terrain_tiles(
        input_path=terrarium_path,
        output_dir=paths.terrain_tiles,
        min_zoom=region["tiles"]["min_zoom"],
        max_zoom=region["tiles"]["max_zoom"],
    )


def main() -> None:
    prepare_region(REGION_ID)


if __name__ == "__main__":
    main()
