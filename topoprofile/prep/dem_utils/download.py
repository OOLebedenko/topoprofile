import logging
from pathlib import Path
from typing import Any

import geopandas as gpd
import pygmt
from shapely.geometry import Point

from topoprofile.domain.terrain import Bounds

logger = logging.getLogger(__name__)


def get_utm_epsg(lon: float, lat: float) -> str:
    """
    Return the UTM EPSG code for the given coordinates.

    Args:
        lon: Longitude in decimal degrees.
        lat: Latitude in decimal degrees.

    Returns:
        EPSG string such as "EPSG:32638" for the Northern Hemisphere
        or "EPSG:32738" for the Southern Hemisphere.
    """
    zone = int((lon + 180) / 6) + 1

    if lat >= 0:
        return f"EPSG:326{zone:02d}"

    return f"EPSG:327{zone:02d}"


def get_region_bounds(
    center_lon: float,
    center_lat: float,
    radius_m: float,
) -> tuple[float, float, float, float]:
    """
    Compute the bounding box around a circular region.

    The center point is converted to a local UTM projection, buffered by
    the specified radius, and converted back to EPSG:4326.

    Args:
        center_lon: Center longitude in decimal degrees.
        center_lat: Center latitude in decimal degrees.
        radius_m: Region radius in meters.

    Returns:
        Bounding box as:
        (min_lon, min_lat, max_lon, max_lat).
    """
    center = gpd.GeoDataFrame(
        geometry=[Point(center_lon, center_lat)],
        crs="EPSG:4326",
    )

    buffered_geometry = (
        center.to_crs(get_utm_epsg(center_lon, center_lat))
        .geometry.buffer(radius_m)
        .to_crs("EPSG:4326")
    )

    min_lon, min_lat, max_lon, max_lat = buffered_geometry.total_bounds

    return (
        float(min_lon),
        float(min_lat),
        float(max_lon),
        float(max_lat),
    )


def download_dem_by_bounds(
    bounds: tuple[float, float, float, float],
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
    min_lon, min_lat, max_lon, max_lat = bounds

    output_path.parent.mkdir(parents=True, exist_ok=True)

    dem = pygmt.datasets.load_earth_relief(
        resolution=resolution,
        region=[
            min_lon,
            max_lon,
            min_lat,
            max_lat,
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
            bounds=(
                bounds.west,
                bounds.south,
                bounds.east,
                bounds.north,
            ),
            resolution=resolution,
            output_path=output_path,
        )
    except Exception:
        logger.exception("Failed to download DEM to %s", output_path)
        raise

    logger.info("DEM saved: %s", output_path)

    return output_path


def download_region_dem(
    region: dict[str, Any],
    output_dir: Path,
    force_download: bool = False,
) -> Path:
    center_lon = float(region["center"]["lon"])
    center_lat = float(region["center"]["lat"])
    radius_m = float(region["radius_m"])
    resolution = str(region["dem"]["resolution"])
    filename = str(region["dem"]["filename"])

    min_lon, min_lat, max_lon, max_lat = get_region_bounds(
        center_lon=center_lon,
        center_lat=center_lat,
        radius_m=radius_m,
    )

    bounds = Bounds(
        west=min_lon,
        south=min_lat,
        east=max_lon,
        north=max_lat,
    )

    return download_dem(
        bounds=bounds,
        resolution=resolution,
        output_path=output_dir / filename,
        force_download=force_download,
    )
