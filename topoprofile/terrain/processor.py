# topoprofile/terrain/processor.py

from pathlib import Path

from topoprofile.geo.models import Bounds
from topoprofile.terrain.source import DEMSource
from topoprofile.terrain.store import GeoTIFFDEMStore


class DEMProcessor:
    """Process and store digital elevation model data."""

    def __init__(
            self,
            source: DEMSource,
            store: GeoTIFFDEMStore,
    ) -> None:
        self._source = source
        self._store = store

    def process(
            self,
            name: str,
            bounds: Bounds,
    ) -> Path:
        if self._store.exists(name):
            return self._store.path(name)

        dem = self._source.load(bounds)

        return self._store.save(
            name=name,
            dem=dem,
        )
