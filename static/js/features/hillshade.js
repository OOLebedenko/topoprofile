/**
 * Adds hillshade rendering based on the local DEM source.
 */

import {
    HILLSHADE_CONFIG,
    HILLSHADE_LAYER_ID,
    HILLSHADE_SOURCE_ID,
    TERRAIN_CONFIG,
} from "../config.js";

/**
 * Adds a MapLibre hillshade layer using the terrain DEM source.
 * @param {maplibregl.Map} map
 */
export function addHillshade(map) {
    map.addSource(HILLSHADE_SOURCE_ID, {
        type: "raster-dem",
        tiles: TERRAIN_CONFIG.tiles,
        minzoom: TERRAIN_CONFIG.minZoom,
        maxzoom: TERRAIN_CONFIG.maxZoom,
        tileSize: TERRAIN_CONFIG.tileSize,
        encoding: TERRAIN_CONFIG.encoding,
        bounds: TERRAIN_CONFIG.bounds,
    });

    map.addLayer({
        id: HILLSHADE_LAYER_ID,
        type: "hillshade",
        source: HILLSHADE_SOURCE_ID,

        paint: {
            "hillshade-exaggeration": HILLSHADE_CONFIG.exaggeration,
        },
    });
}