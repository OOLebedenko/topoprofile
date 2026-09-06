import logging
from pathlib import Path

import rasterio
from click.testing import CliRunner
from rio_rgbify.scripts.cli import rgbify

from topoprofile.geo.models import Bounds
from topoprofile.terrain.source import Source

logger = logging.getLogger(__name__)


def download_dem_by_bounds(
    bounds: Bounds,
    source: Source,
    output_path: Path,
) -> None:
    """
    Download a DEM for the given geographic bounds and save it as GeoTIFF.

    Args:
        bounds: Geographic bounds.
        source: DEM data source.
        output_path: Destination GeoTIFF path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dem = source.load(bounds)

    with rasterio.open(
        output_path,
        "w",
        driver="GTiff",
        height=dem.height,
        width=dem.width,
        count=1,
        dtype=dem.values.dtype,
        crs=dem.crs,
        transform=dem.transform,
        nodata=dem.nodata,
    ) as dataset:
        dataset.write(
            dem.values,
            1,
        )


def download_dem(
    bounds: Bounds,
    source: Source,
    output_path: Path,
    force_download: bool = False,
) -> Path:
    """Download DEM for geographic bounds or reuse an existing file."""
    if output_path.is_file() and not force_download:
        logger.info("Using existing DEM: %s", output_path)
        return output_path

    logger.info(
        "Downloading DEM: bounds=%s",
        bounds,
    )

    try:
        download_dem_by_bounds(
            bounds=bounds,
            source=source,
            output_path=output_path,
        )
    except Exception:
        logger.exception("Failed to download DEM to %s", output_path)
        raise

    logger.info("DEM saved: %s", output_path)

    return output_path


class ConversionError(RuntimeError):
    """Raised when rio-rgbify conversion fails."""


def convert_dem_to_terrarium(
    input_path: Path,
    output_path: Path,
    force_convert: bool = False,
) -> Path:
    """
    Convert a DEM GeoTIFF to Terrarium encoding.

    Args:
        input_path: Source DEM GeoTIFF.
        output_path: Destination Terrarium GeoTIFF.
        force_convert: Recreate the output file even if it already exists.

    Returns:
        Path to the Terrarium-encoded GeoTIFF.

    Raises:
        FileNotFoundError: If the source DEM does not exist.
        ConversionError: If rio-rgbify fails or does not create the output file.
    """
    if not input_path.is_file():
        raise FileNotFoundError(f"Input DEM not found: {input_path}")

    if output_path.is_file():
        if not force_convert:
            logger.info(
                "Using existing Terrarium DEM: %s",
                output_path,
            )
            return output_path

        logger.info(
            "Recreating Terrarium DEM: %s",
            output_path,
        )
        output_path.unlink()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(
        "Converting DEM to Terrarium: input=%s, output=%s",
        input_path,
        output_path,
    )

    runner = CliRunner()

    result = runner.invoke(
        rgbify,
        [
            "--base-val",
            "-32768",
            "--interval",
            "0.00390625",
            "--co",
            "TILED=YES",
            "--co",
            "BLOCKXSIZE=256",
            "--co",
            "BLOCKYSIZE=256",
            str(input_path),
            str(output_path),
        ],
    )

    if result.exit_code != 0:
        logger.error(
            "rio-rgbify failed with exit code %d:\n%s",
            result.exit_code,
            result.output,
        )
        raise ConversionError(
            f"rio-rgbify failed with exit code {result.exit_code}"
        ) from result.exception

    if not output_path.is_file():
        raise ConversionError(
            "rio-rgbify completed successfully, but the output file "
            f"was not created: {output_path}"
        )

    logger.info(
        "Terrarium DEM saved: %s",
        output_path,
    )

    return output_path
