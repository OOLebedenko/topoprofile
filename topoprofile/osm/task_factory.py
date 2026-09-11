from pathlib import Path

from topoprofile.osm.client.overpass import OverpassClient
from topoprofile.osm.client.queries.base import UnionQuery
from topoprofile.osm.client.queries.hiking_routes import HikingRouteQuery
from topoprofile.osm.client.queries.mountain_infrastructure import (
    MountainInfrastructureQuery,
)
from topoprofile.osm.client.queries.terrain_surface import TerrainSurfaceQuery
from topoprofile.osm.exclusions import load_hiking_exclusions
from topoprofile.osm.source import OverpassFeatureSource
from topoprofile.osm.store import MVTStore
from topoprofile.osm.task import PrepareOSMChunkTask, PrepareOSMTask
from topoprofile.osm.transforms.osm import (
    ClipToBounds,
    FilterExcludedHikingRoutes,
    FilterHikingRoutes,
    FilterTerrainSurface,
    PrepareMountainInfrastructure,
    RemoveNodeReferences,
)
from topoprofile.osm.transforms.overpass import GeoJSONTransform
from topoprofile.osm.writer import MVTWriter
from topoprofile.processing.transforms import Compose


def create_osm_task(
        osm_root: Path,
        hiking_exclusions_path: Path,
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

    hiking_exclusions = load_hiking_exclusions(
        hiking_exclusions_path,
    )

    hiking_routes_task = PrepareOSMTask(
        store=MVTStore(
            root=osm_root,
            filename="hiking_routes.pbf",
            writer=MVTWriter(
                layer_name="hiking_routes",
            ),
        ),
        transform=Compose(
            transforms=(
                FilterHikingRoutes(),
                FilterExcludedHikingRoutes(
                    exclusions=hiking_exclusions,
                ),
                RemoveNodeReferences(),
                ClipToBounds(),
            ),
        ),
    )

    mountain_infrastructure_task = PrepareOSMTask(
        store=MVTStore(
            root=osm_root,
            filename="mountain_infrastructure.pbf",
            writer=MVTWriter(
                layer_name="mountain_infrastructure",
            ),
        ),
        transform=Compose(
            transforms=(
                PrepareMountainInfrastructure(),
                RemoveNodeReferences(),
                ClipToBounds(),
            ),
        ),
    )

    terrain_surface_task = PrepareOSMTask(
        store=MVTStore(
            root=osm_root,
            filename="terrain_surface.pbf",
            writer=MVTWriter(
                layer_name="terrain_surface",
            ),
        ),
        transform=Compose(
            transforms=(
                FilterTerrainSurface(),
                RemoveNodeReferences(),
                ClipToBounds(),
            ),
        ),
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
