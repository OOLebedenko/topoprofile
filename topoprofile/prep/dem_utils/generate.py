import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_terrain_tiles(
    input_path: Path,
    output_dir: Path,
    min_zoom: int = 8,
    max_zoom: int = 14,
    force_generate: bool = False,
) -> Path:
    """
    Generate terrain tiles from a Terrarium-encoded GeoTIFF.

    Args:
        input_path: Source Terrarium GeoTIFF.
        output_dir: Directory where generated tiles will be saved.
        min_zoom: Minimum zoom level.
        max_zoom: Maximum zoom level.
        force_generate: Regenerate tiles even if the output directory
            already contains files.

    Returns:
        Path to the directory containing generated tiles.

    Raises:
        FileNotFoundError: If the source GeoTIFF does not exist.
        ValueError: If the zoom range is invalid.
        RuntimeError: If gdal2tiles fails.
    """
    if not input_path.is_file():
        raise FileNotFoundError(f"Terrarium DEM not found: {input_path}")

    if min_zoom < 0:
        raise ValueError("min_zoom must be non-negative")

    if max_zoom < min_zoom:
        raise ValueError("max_zoom must be greater than or equal to min_zoom")

    if output_dir.is_dir() and any(output_dir.iterdir()):
        if not force_generate:
            logger.info(
                "Using existing terrain tiles: %s",
                output_dir,
            )
            return output_dir

        logger.info(
            "Regenerating terrain tiles: %s",
            output_dir,
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "gdal2tiles.py",
        "--xyz",
        "--resampling=near",
        "-z",
        f"{min_zoom}-{max_zoom}",
        str(input_path),
        str(output_dir),
    ]

    logger.info(
        "Generating terrain tiles: zoom=%d-%d, output=%s",
        min_zoom,
        max_zoom,
        output_dir,
    )

    try:
        subprocess.run(
            command,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        logger.exception(
            "Failed to generate terrain tiles in %s",
            output_dir,
        )
        raise RuntimeError(
            f"gdal2tiles failed with exit code {error.returncode}"
        ) from error

    logger.info(
        "Terrain tiles generated: %s",
        output_dir,
    )

    return output_dir
