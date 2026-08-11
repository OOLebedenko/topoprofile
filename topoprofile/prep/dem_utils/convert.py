import logging
from pathlib import Path

from click.testing import CliRunner
from rio_rgbify.scripts.cli import rgbify

logger = logging.getLogger(__name__)


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
