from functools import partial

from topoprofile.geo.models import Region, XYZTile
from topoprofile.osm.overpass.loader import OSMFeatureLoader
from topoprofile.osm.store import OSMStore
from topoprofile.osm.transformers.base import OSMFeatureTransformer
from topoprofile.workers.worker import (
    Task,
    TaskExecutionError,
)


class OSMTaskManager:
    """Create tasks for processing OSM feature data."""

    def __init__(
            self,
            loader: OSMFeatureLoader,
            response_transformer: OSMFeatureTransformer,
            store: OSMStore,
    ) -> None:
        self._loader = loader
        self._response_transformer = response_transformer
        self._store = store

    def create_tasks(
            self,
            region: Region,
    ) -> list[Task[None]]:
        """Create processing tasks for a geographic region."""
        return [
            partial(
                self._process,
                tile,
            )
            for tile in region.tiles
            if not self._store.exists(tile)
        ]

    def _process(
            self,
            tile: XYZTile,
    ) -> None:
        """Process OSM feature data for an XYZ tile."""
        try:
            response = self._loader.load(
                tile.bounds,
            )

            response = self._response_transformer.transform(
                response,
                tile.bounds,
            )

            self._store.save(
                tile,
                response,
            )
        except Exception as error:
            raise TaskExecutionError(
                f"OSM processing failed for tile "
                f"{tile.z}/{tile.x}/{tile.y}."
            ) from error
