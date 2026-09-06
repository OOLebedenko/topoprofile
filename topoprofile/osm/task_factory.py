from pathlib import Path

from topoprofile.osm.client.overpass import OverpassClient
from topoprofile.osm.client.queries.base import Query
from topoprofile.osm.source import OverpassFeatureSource
from topoprofile.osm.store import OSMStore
from topoprofile.osm.task import PrepareOSMTask
from topoprofile.osm.transforms.osm import OSMTransform
from topoprofile.osm.transforms.overpass import GeoJSONTransform
from topoprofile.osm.writer import CompactGeoJSONWriter


def create_osm_task(
        query: Query,
        transform: OSMTransform,
        osm_root: Path,
        filename: str,
) -> PrepareOSMTask:
    """Create a configured OSM processing task."""
    store = OSMStore(
        root=osm_root,
        filename=filename,
        writer=CompactGeoJSONWriter(),
    )

    return PrepareOSMTask(
        source=OverpassFeatureSource(
            query=query,
            client=OverpassClient(),
        ),
        store=store,
        overpass_transform=GeoJSONTransform(),
        osm_transform=transform,
    )
