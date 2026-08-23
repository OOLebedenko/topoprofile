import logging
from pathlib import Path

import pygmt

from topoprofile.domain.terrain import Bounds

logger = logging.getLogger(__name__)


def download_dem_by_bounds(
    bounds: Bounds,
    resolution: str,
    output_path: Path,
) -> None:
    """
    Download a DEM for the given bounding box and save it as GeoTIFF.

    Args:
        bounds: Bounding box as
            (min_lon, min_lat, max_lon, max_lat).
        resolution: DEM resolution, for example "01s", "03s" or "15s".
        output_path: Destination GeoTIFF path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dem = pygmt.datasets.load_earth_relief(
        resolution=resolution,
        region=[
            bounds.west,
            bounds.east,
            bounds.south,
            bounds.north,
        ],
    )

    dem.rio.write_crs("EPSG:4326", inplace=True)
    dem.rio.to_raster(output_path)


def download_dem(
    bounds: Bounds,
    resolution: str,
    output_path: Path,
    force_download: bool = False,
) -> Path:
    """Download DEM for geographic bounds or reuse an existing file."""
    if output_path.is_file() and not force_download:
        logger.info("Using existing DEM: %s", output_path)
        return output_path

    logger.info(
        "Downloading DEM: bounds=%s, resolution=%s",
        bounds,
        resolution,
    )

    try:
        download_dem_by_bounds(
            bounds=bounds,
            resolution=resolution,
            output_path=output_path,
        )
    except Exception:
        logger.exception("Failed to download DEM to %s", output_path)
        raise

    logger.info("DEM saved: %s", output_path)

    return output_path
