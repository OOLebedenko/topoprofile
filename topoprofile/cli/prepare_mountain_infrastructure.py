import argparse
import json
import time
from pathlib import Path
from typing import Any

from tqdm import tqdm

from topoprofile.config import load_region_config
from topoprofile.geo.chunks import RegionChunkResolver
from topoprofile.geo.models import Bounds
from topoprofile.geo.regions import get_region_bounds
from topoprofile.geo.tiles import xyz_to_bounds
from topoprofile.osm.extractors.mountain_infrastructure import (
    MountainInfrastructureExtractor,
)
from topoprofile.osm.geojson import GeoJSONConverter, clip_to_bounds
from topoprofile.osm.overpass.client import OverpassClient, OverpassGeoJSONClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OSM_CHUNKS_ROOT = PROJECT_ROOT / "data" / "osm" / "chunks"

MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare mountain infrastructure from Overpass.",
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the region config.",
    )
    return parser.parse_args()


def extract_with_retry(
        extractor: MountainInfrastructureExtractor,
        bounds: Bounds,
) -> dict[str, Any] | None:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return extractor.extract(bounds)
        except (RuntimeError, TypeError, ValueError) as error:
            if attempt == MAX_ATTEMPTS:
                tqdm.write(
                    f"Failed after {MAX_ATTEMPTS} attempts: {error}"
                )
                return None

            delay = RETRY_DELAY_SECONDS * attempt
            tqdm.write(
                f"Attempt {attempt}/{MAX_ATTEMPTS} failed: {error}. "
                f"Retrying in {delay}s."
            )
            time.sleep(delay)

    return None


def main() -> None:
    args = parse_args()

    config_path = args.config
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    config = load_region_config(config_path)
    bounds = get_region_bounds(
        center=config.center,
        radius_km=config.radius_km,
    )

    chunks = RegionChunkResolver().resolve(
        bounds=bounds,
        zoom=config.terrain.min_zoom,
    )

    client = OverpassGeoJSONClient(
        overpass_client=OverpassClient(),
        converter=GeoJSONConverter(),
    )
    extractor = MountainInfrastructureExtractor(client)

    with tqdm(
            chunks,
            desc="Mountain infrastructure",
            unit="chunk",
    ) as progress:
        for chunk in progress:
            progress.set_postfix_str(
                f"{chunk.z}/{chunk.x}/{chunk.y}"
            )

            output_path = (
                    OSM_CHUNKS_ROOT
                    / str(chunk.z)
                    / str(chunk.x)
                    / str(chunk.y)
                    / "mountain_infrastructure.geojson"
            )

            if output_path.is_file():
                continue

            chunk_bounds = xyz_to_bounds(chunk)

            geojson = extract_with_retry(
                extractor,
                chunk_bounds,
            )
            if geojson is None:
                continue

            geojson = clip_to_bounds(
                geojson,
                chunk_bounds,
            )

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(
                    geojson,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )


if __name__ == "__main__":
    main()
