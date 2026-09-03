/**
 * Loads terrain surface features from local OSM chunks
 * and adds them to the map.
 */

import {
    TERRAIN_FEATURES_CONFIG,
    TERRAIN_FEATURES_SOURCE_ID,
} from "../../config.js";
import { addTerrainFeatureLayers } from "./layers/index.js";

// Converts longitude to an XYZ tile X coordinate.
function lonToTileX(lon, zoom) {
    return ((lon + 180) / 360) * 2 ** zoom;
}

// Converts latitude to an XYZ tile Y coordinate.
function latToTileY(lat, zoom) {
    const latRad = lat * Math.PI / 180;

    return (
        1
        - Math.asinh(Math.tan(latRad)) / Math.PI
    )
    / 2
    * 2 ** zoom;
}

// Returns all OSM chunks intersecting the configured terrain bounds.
function getChunks(bounds, zoom) {
    const [west, south, east, north] = bounds;

    const minX = Math.floor(lonToTileX(west, zoom));
    const maxX = Math.ceil(lonToTileX(east, zoom)) - 1;
    const minY = Math.floor(latToTileY(north, zoom));
    const maxY = Math.ceil(latToTileY(south, zoom)) - 1;

    const chunks = [];

    for (let x = minX; x <= maxX; x += 1) {
        for (let y = minY; y <= maxY; y += 1) {
            chunks.push({ z: zoom, x, y });
        }
    }

    return chunks;
}

// Loads terrain surface features for a single OSM chunk.
async function loadChunk(chunk) {
    const { dataPath } = TERRAIN_FEATURES_CONFIG;
    const { z, x, y } = chunk;

    const response = await fetch(
        `${dataPath}/${z}/${x}/${y}/terrain_surface.geojson`,
    );

    if (!response.ok) {
        return [];
    }

    const geojson = await response.json();
    return geojson.features;
}

// Loads and combines terrain surface features from all configured chunks.
async function loadTerrainFeatures() {
    const chunks = getChunks(
        TERRAIN_FEATURES_CONFIG.bounds,
        TERRAIN_FEATURES_CONFIG.chunkZoom,
    );

    const results = await Promise.all(
        chunks.map(loadChunk),
    );

    return {
        type: "FeatureCollection",
        features: results.flat(),
    };
}

// Adds the terrain feature source and its rendering layers.
export async function addTerrainFeatures(map) {
    const geojson = await loadTerrainFeatures();

    map.addSource(TERRAIN_FEATURES_SOURCE_ID, {
        type: "geojson",
        data: geojson,
    });

    addTerrainFeatureLayers(map);
}