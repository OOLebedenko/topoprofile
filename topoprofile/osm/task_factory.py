from pathlib import Path

from topoprofile.osm.client.overpass import OverpassClient
from topoprofile.osm.client.queries.base import Query
from topoprofile.osm.source import OverpassFeatureSource
from topoprofile.osm.store import OSMStore
from topoprofile.osm.task import PrepareOSMTask
from topoprofile.osm.task_manager import OSMTaskManager
from topoprofile.osm.transforms.osm import OSMTransform
from topoprofile.osm.transforms.overpass import GeoJSONTransform
from topoprofile.osm.writer import CompactGeoJSONWriter


def create_osm_task_manager(
        query: Query,
        transform: OSMTransform,
        osm_root: Path,
        filename: str,
) -> OSMTaskManager:
    """Create a configured OSM processing task manager."""
    store = OSMStore(
        root=osm_root,
        filename=filename,
        writer=CompactGeoJSONWriter(),
    )

    task = PrepareOSMTask(
        source=OverpassFeatureSource(
            query=query,
            client=OverpassClient(),
        ),
        store=store,
        overpass_transform=GeoJSONTransform(),
        osm_transform=transform,
    )

    return OSMTaskManager(
        task=task,
    )
