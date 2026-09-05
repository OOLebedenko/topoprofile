from pathlib import Path

from topoprofile.osm.geojson import GeoJSONConverter
from topoprofile.osm.overpass.client import OverpassClient
from topoprofile.osm.overpass.loader import OverpassFeatureLoader
from topoprofile.osm.overpass.queries.base import OverpassQuery
from topoprofile.osm.store import OSMStore
from topoprofile.osm.task_manager import OSMTaskManager
from topoprofile.osm.transformers.base import OSMFeatureTransformer
from topoprofile.osm.writer import CompactGeoJSONWriter


def create_osm_task_manager(
        query: OverpassQuery,
        response_transformer: OSMFeatureTransformer,
        output_root: Path,
        filename: str,
) -> OSMTaskManager:
    """Create a configured OSM task manager."""
    loader = OverpassFeatureLoader(
        query=query,
        client=OverpassClient(),
        converter=GeoJSONConverter(),
    )

    store = OSMStore(
        root=output_root,
        filename=filename,
        writer=CompactGeoJSONWriter(),
    )

    return OSMTaskManager(
        loader=loader,
        response_transformer=response_transformer,
        store=store,
    )
