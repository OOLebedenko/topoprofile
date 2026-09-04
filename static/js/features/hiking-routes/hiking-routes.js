/**
 * Loads and renders local hiking route data.
 */

import {
    HIKING_ROUTES_CONFIG,
    HIKING_ROUTES_SOURCE_ID,
} from "../../config.js";
import {
    addHikingRouteLayers,
} from "./layers/index.js";

function lonToTileX(lon, zoom) {
    return (lon + 180) / 360 * 2 ** zoom;
}

function latToTileY(lat, zoom) {
    const latRad = lat * Math.PI / 180;

    return (
        1
        - Math.asinh(Math.tan(latRad)) / Math.PI
    ) / 2 * 2 ** zoom;
}

function getChunks(bounds, zoom) {
    const [west, south, east, north] = bounds;

    const minX = Math.floor(lonToTileX(west, zoom));
    const maxX = Math.ceil(lonToTileX(east, zoom)) - 1;
    const minY = Math.floor(latToTileY(north, zoom));
    const maxY = Math.ceil(latToTileY(south, zoom)) - 1;

    const chunks = [];

    for (let x = minX; x <= maxX; x++) {
        for (let y = minY; y <= maxY; y++) {
            chunks.push({ z: zoom, x, y });
        }
    }

    return chunks;
}

async function loadChunk(chunk) {
    const { dataPath } = HIKING_ROUTES_CONFIG;
    const { z, x, y } = chunk;

    const response = await fetch(
        `${dataPath}/${z}/${x}/${y}/hiking_routes.geojson`
    );

    if (response.status === 404) {
        return [];
    }

    if (!response.ok) {
        throw new Error(
            `Failed to load hiking routes ${z}/${x}/${y}: `
            + `${response.status}`
        );
    }

    const geojson = await response.json();

    return geojson.features;
}

async function loadHikingRoutes() {
    const {
        bounds,
        chunkZoom,
    } = HIKING_ROUTES_CONFIG;

    const chunks = getChunks(
        bounds,
        chunkZoom,
    );

    const results = await Promise.all(
        chunks.map(loadChunk)
    );

    return {
        type: "FeatureCollection",
        features: results.flat(),
    };
}

export async function addHikingRoutes(map) {
    const geojson = await loadHikingRoutes();

    map.addSource(HIKING_ROUTES_SOURCE_ID, {
        type: "geojson",
        data: geojson,
    });

    addHikingRouteLayers(map);
}