/**
 * Loads local mountain infrastructure data
 * and integrates hut markers with the base map.
 */

import {
    MOUNTAIN_INFRASTRUCTURE_CONFIG,
    MOUNTAIN_INFRASTRUCTURE_SOURCE_ID,
} from "../../config.js";

import {
    addMountainInfrastructureLayers,
} from "./layers/index.js";

import {
    BASE_HUT_ICON_SIZE,
    HUT_ICON_ID,
} from "./layers/shared.js";

// Custom layer used to replace hut icons from the base map.
const BASE_INFRASTRUCTURE_LAYER_ID =
    "base-mountain-infrastructure-markers";

// Infrastructure categories provided by the base POI layer.
const BASE_INFRASTRUCTURE_SUBCLASSES = [
    "alpine_hut",
    "wilderness_hut",
    "shelter",
];

function lonToTileX(lon, zoom) {
    return ((lon + 180) / 360) * 2 ** zoom;
}

function latToTileY(lat, zoom) {
    const latRad = lat * Math.PI / 180;

    return (
        (1 - Math.asinh(Math.tan(latRad)) / Math.PI)
        / 2
        * 2 ** zoom
    );
}

// Return all XYZ chunks intersecting the configured terrain area.
function getChunks(bounds, zoom) {
    const [west, south, east, north] = bounds;

    const minX = Math.floor(lonToTileX(west, zoom));
    const maxX = Math.ceil(lonToTileX(east, zoom)) - 1;
    const minY = Math.floor(latToTileY(north, zoom));
    const maxY = Math.ceil(latToTileY(south, zoom)) - 1;

    const chunks = [];

    for (let x = minX; x <= maxX; x += 1) {
        for (let y = minY; y <= maxY; y += 1) {
            chunks.push({
                z: zoom,
                x,
                y,
            });
        }
    }

    return chunks;
}

// Load mountain infrastructure prepared for one XYZ chunk.
async function loadChunk(chunk) {
    const { dataPath } = MOUNTAIN_INFRASTRUCTURE_CONFIG;

    const url = (
        `${dataPath}/${chunk.z}/${chunk.x}/${chunk.y}`
        + "/mountain_infrastructure.geojson"
    );

    const response = await fetch(url);

    if (response.status === 404) {
        return null;
    }

    if (!response.ok) {
        throw new Error(
            `Failed to load mountain infrastructure: ${url}`
        );
    }

    return response.json();
}

// Load and register a custom map icon.
function loadIcon(map, id, url) {
    return new Promise((resolve, reject) => {
        const image = new Image();

        image.onload = () => {
            if (!map.hasImage(id)) {
                map.addImage(id, image);
            }

            resolve();
        };

        image.onerror = () => {
            reject(
                new Error(`Failed to load map icon: ${url}`)
            );
        };

        image.src = url;
    });
}

// Remove hut and shelter POIs from the original base-map symbol layers
// and render them with the same custom hut icon used by local data.
function customizeBaseInfrastructure(map) {
    const poiLayers = map.getStyle().layers.filter(
        layer => (
            layer.type === "symbol"
            && layer["source-layer"] === "poi"
        )
    );

    if (poiLayers.length === 0) {
        return;
    }

    const infrastructureFilter = [
        "in",
        ["get", "subclass"],
        ["literal", BASE_INFRASTRUCTURE_SUBCLASSES],
    ];

    const excludeInfrastructureFilter = [
        "!",
        infrastructureFilter,
    ];

    // Exclude infrastructure objects from the original POI layers
    // to avoid duplicate icons and labels.
    for (const layer of poiLayers) {
        const currentFilter = map.getFilter(layer.id);

        if (currentFilter) {
            map.setFilter(
                layer.id,
                [
                    "all",
                    currentFilter,
                    excludeInfrastructureFilter,
                ],
            );
        } else {
            map.setFilter(
                layer.id,
                excludeInfrastructureFilter,
            );
        }
    }

    if (map.getLayer(BASE_INFRASTRUCTURE_LAYER_ID)) {
        return;
    }

    // Render base-map huts and shelters with the custom hut icon.
    map.addLayer({
        id: BASE_INFRASTRUCTURE_LAYER_ID,
        type: "symbol",
        source: poiLayers[0].source,
        "source-layer": "poi",
        minzoom: 10,
        filter: infrastructureFilter,

        layout: {
            "icon-image": HUT_ICON_ID,
            "icon-size": BASE_HUT_ICON_SIZE,
            "icon-allow-overlap": true,
            "icon-ignore-placement": true,
        },
    });
}

// Load prepared infrastructure chunks and add all related map layers.
export async function addMountainInfrastructure(map) {
    const {
        bounds,
        chunkZoom,
    } = MOUNTAIN_INFRASTRUCTURE_CONFIG;

    const chunks = getChunks(bounds, chunkZoom);

    const collections = await Promise.all(
        chunks.map(loadChunk)
    );

    const features = collections
        .filter(collection => collection !== null)
        .flatMap(collection => collection.features);

    map.addSource(MOUNTAIN_INFRASTRUCTURE_SOURCE_ID, {
        type: "geojson",
        data: {
            type: "FeatureCollection",
            features,
        },
    });

    await loadIcon(
        map,
        HUT_ICON_ID,
        "/static/icons/mountain-hut.svg",
    );

    customizeBaseInfrastructure(map);

    addMountainInfrastructureLayers(map);
}