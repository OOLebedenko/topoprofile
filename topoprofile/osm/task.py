from pathlib import Path
from typing import Protocol

from topoprofile.geo.models import Bounds, XYZTile
from topoprofile.osm.models import OverpassData
from topoprofile.osm.source import Source
from topoprofile.osm.store import OSMStore
from topoprofile.osm.transforms.osm import (
    ClipToBounds,
    Compose,
    OSMTransform,
)
from topoprofile.osm.transforms.overpass import OverpassTransform


class Task[**ParamsT, ResultT](Protocol):
    """Executable processing task."""

    def __call__(
            self,
            *args: ParamsT.args,
            **kwargs: ParamsT.kwargs,
    ) -> ResultT:
        """Execute the task."""
        ...


class PrepareOSMTask:
    """Download, transform, and store OSM features."""

    def __init__(
            self,
            source: Source[Bounds, OverpassData],
            store: OSMStore,
            overpass_transform: OverpassTransform,
            osm_transform: OSMTransform,
    ) -> None:
        self._source = source
        self._store = store
        self._overpass_transform = overpass_transform
        self._osm_transform = osm_transform

    def __call__(
            self,
            chunk: XYZTile,
    ) -> Path:
        if self._store.exists(chunk):
            return self._store.path(chunk)

        data = self._source.load(chunk.bounds)
        features = self._overpass_transform(data)

        transform = Compose(
            transforms=(
                self._osm_transform,
                ClipToBounds(chunk.bounds),
            ),
        )
        features = transform(features)

        return self._store.save(
            chunk,
            features,
        )
