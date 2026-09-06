from pathlib import Path

from topoprofile.osm.client.overpass import OverpassClient
from topoprofile.osm.client.queries.base import UnionQuery
from topoprofile.osm.client.queries.hiking_routes import HikingRouteQuery
from topoprofile.osm.client.queries.mountain_infrastructure import (
    MountainInfrastructureQuery,
)
from topoprofile.osm.client.queries.terrain_surface import TerrainSurfaceQuery
from topoprofile.osm.source import OverpassFeatureSource
from topoprofile.osm.store import OSMStore
from topoprofile.osm.task import PrepareOSMChunkTask, PrepareOSMTask
from topoprofile.osm.transforms.osm import (
    FilterHikingRoutes,
    FilterTerrainSurface,
    PrepareMountainInfrastructure,
)
from topoprofile.osm.transforms.overpass import GeoJSONTransform
from topoprofile.osm.writer import CompactGeoJSONWriter


def create_osm_task(
        osm_root: Path,
) -> PrepareOSMChunkTask:
    """Create a configured OSM chunk processing task."""
    source = OverpassFeatureSource(
        query=UnionQuery(
            queries=(
                HikingRouteQuery(),
                MountainInfrastructureQuery(),
                TerrainSurfaceQuery(),
            ),
        ),
        client=OverpassClient(),
    )

    hiking_routes_task = PrepareOSMTask(
        store=OSMStore(
            root=osm_root,
            filename="hiking_routes.geojson",
            writer=CompactGeoJSONWriter(),
        ),
        transform=FilterHikingRoutes(),
    )

    mountain_infrastructure_task = PrepareOSMTask(
        store=OSMStore(
            root=osm_root,
            filename="mountain_infrastructure.geojson",
            writer=CompactGeoJSONWriter(),
        ),
        transform=PrepareMountainInfrastructure(),
    )

    terrain_surface_task = PrepareOSMTask(
        store=OSMStore(
            root=osm_root,
            filename="terrain_surface.geojson",
            writer=CompactGeoJSONWriter(),
        ),
        transform=FilterTerrainSurface(),
    )

    return PrepareOSMChunkTask(
        source=source,
        overpass_transform=GeoJSONTransform(),
        tasks=(
            hiking_routes_task,
            mountain_infrastructure_task,
            terrain_surface_task,
        ),
    )
