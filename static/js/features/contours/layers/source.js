/**
 * Loads terrain contour GeoJSON from local XYZ chunks.
 */

import {
    CONTOURS_CONFIG,
} from "../../../config.js";

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

async function loadChunk(chunk) {
    const { dataPath } = CONTOURS_CONFIG;

    const url = (
        `${dataPath}/${chunk.z}/${chunk.x}/${chunk.y}`
        + "/contours.geojson"
    );

    const response = await fetch(url);

    if (response.status === 404) {
        return [];
    }

    if (!response.ok) {
        throw new Error(
            `Failed to load terrain contours: ${url}`
        );
    }

    const geojson = await response.json();

    return geojson.features;
}

export async function loadContours() {
    const chunks = getChunks(
        CONTOURS_CONFIG.bounds,
        CONTOURS_CONFIG.chunkZoom,
    );

    const results = await Promise.all(
        chunks.map(loadChunk),
    );

    return {
        type: "FeatureCollection",
        features: results.flat(),
    };
}