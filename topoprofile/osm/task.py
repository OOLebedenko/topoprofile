from pathlib import Path

from topoprofile.geo.models import Bounds, XYZTile
from topoprofile.osm.models import OSMFeatureCollection, OverpassData
from topoprofile.osm.store import MVTStore, OSMStore
from topoprofile.osm.transforms.osm import ClipToBounds, OSMTransform
from topoprofile.osm.transforms.overpass import OverpassTransform
from topoprofile.processing.source import Source
from topoprofile.processing.transforms import Compose


class PrepareOSMTask:
    """Transform and store one OSM dataset."""

    def __init__(
            self,
            store: OSMStore | MVTStore,
            transform: OSMTransform,
    ) -> None:
        self._store = store
        self._transform = transform

    def exists(
            self,
            chunk: XYZTile,
    ) -> bool:
        return self._store.exists(chunk)

    def __call__(
            self,
            chunk: XYZTile,
            features: OSMFeatureCollection,
    ) -> Path:
        transform = Compose(
            transforms=(
                self._transform,
                ClipToBounds(chunk.bounds),
            ),
        )

        features = transform(features)

        return self._store.save(
            chunk,
            features,
        )


class PrepareOSMChunkTask:
    """Load OSM data once and prepare all datasets for a chunk."""

    def __init__(
            self,
            source: Source[Bounds, OverpassData],
            overpass_transform: OverpassTransform,
            tasks: tuple[PrepareOSMTask, ...],
    ) -> None:
        self._source = source
        self._overpass_transform = overpass_transform
        self._tasks = tasks

    def __call__(
            self,
            chunk: XYZTile,
    ) -> None:
        tasks = [
            task
            for task in self._tasks
            if not task.exists(chunk)
        ]

        if not tasks:
            return

        data = self._source.load(chunk.bounds)
        features = self._overpass_transform(data)

        for task in tasks:
            task(
                chunk,
                features,
            )
