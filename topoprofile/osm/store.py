from dataclasses import dataclass
from pathlib import Path

from topoprofile.geo.models import XYZTile
from topoprofile.osm.models import OSMFeatureCollection
from topoprofile.osm.writer import (
    CompactGeoJSONWriter,
    MVTWriter,
)
from topoprofile.processing.atomic import atomic_path


@dataclass(frozen=True, slots=True)
class OSMStore:
    """Store prepared OSM feature data."""

    root: Path
    filename: str
    writer: CompactGeoJSONWriter

    def path(
            self,
            chunk: XYZTile,
    ) -> Path:
        """Return the output path for a chunk."""
        return (
                self.root
                / str(chunk.z)
                / str(chunk.x)
                / str(chunk.y)
                / self.filename
        )

    def exists(
            self,
            chunk: XYZTile,
    ) -> bool:
        """Return whether data for a chunk already exists."""
        return self.path(chunk).is_file()

    def save(
            self,
            chunk: XYZTile,
            features: OSMFeatureCollection,
    ) -> Path:
        """Save OSM features for a chunk."""
        output_path = self.path(chunk)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with atomic_path(output_path) as temporary_path:
            self.writer.write(
                temporary_path,
                {
                    "type": "FeatureCollection",
                    "features": list(features.features),
                },
            )

        return output_path


@dataclass(frozen=True, slots=True)
class MVTStore:
    """Store prepared OSM feature data as a Mapbox Vector Tile."""

    root: Path
    filename: str
    writer: MVTWriter

    def path(
            self,
            chunk: XYZTile,
    ) -> Path:
        """Return the output path for a chunk."""
        return (
                self.root
                / str(chunk.z)
                / str(chunk.x)
                / str(chunk.y)
                / self.filename
        )

    def exists(
            self,
            chunk: XYZTile,
    ) -> bool:
        """Return whether data for a chunk already exists."""
        return self.path(chunk).is_file()

    def save(
            self,
            chunk: XYZTile,
            features: OSMFeatureCollection,
    ) -> Path:
        """Save OSM features for a chunk."""
        output_path = self.path(chunk)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with atomic_path(output_path) as temporary_path:
            self.writer.write(
                path=temporary_path,
                geojson={
                    "type": "FeatureCollection",
                    "features": list(features.features),
                },
                bounds=chunk.bounds,
            )

        return output_path
