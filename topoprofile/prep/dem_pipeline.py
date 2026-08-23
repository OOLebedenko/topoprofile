import logging

from topoprofile.domain.terrain import Bounds, TerrainRequest
from topoprofile.prep.dem_utils.download import get_region_bounds
from topoprofile.prep.dem_utils.load import load_region_config
from topoprofile.prep.region_paths import get_region_paths
from topoprofile.prep.settings import REGION_ID
from topoprofile.prep.terrain_paths import TerrainPaths
from topoprofile.prep.terrain_pipeline import prepare_terrain

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def prepare_region(region_id: str) -> None:
    """Prepare terrain using the legacy region configuration."""
    region_paths = get_region_paths(region_id)
    region = load_region_config(region_paths.dem_config)

    min_lon, min_lat, max_lon, max_lat = get_region_bounds(
        center_lon=float(region["center"]["lon"]),
        center_lat=float(region["center"]["lat"]),
        radius_m=float(region["radius_m"]),
    )

    request = TerrainRequest(
        bounds=Bounds(
            west=min_lon,
            south=min_lat,
            east=max_lon,
            north=max_lat,
        ),
        resolution=str(region["dem"]["resolution"]),
        min_zoom=int(region["tiles"]["min_zoom"]),
        max_zoom=int(region["tiles"]["max_zoom"]),
    )

    terrain_paths = TerrainPaths(
        raw_dem=region_paths.raw / str(region["dem"]["filename"]),
        terrarium_dem=region_paths.prepared / "dem_terrarium.tif",
        terrain_tiles=region_paths.terrain_tiles,
    )

    prepare_terrain(
        request=request,
        paths=terrain_paths,
    )


def main() -> None:
    prepare_region(REGION_ID)


if __name__ == "__main__":
    main()
