from dataclasses import dataclass
from pathlib import Path

from topoprofile.geo.models import XYZTile
from topoprofile.osm.geojson import GeoJSON
from topoprofile.osm.writer import CompactGeoJSONWriter


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
            geojson: GeoJSON,
    ) -> Path:
        """Save GeoJSON data for a chunk."""
        output_path = self.path(chunk)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.writer.write(
            output_path,
            geojson,
        )

        return output_path
