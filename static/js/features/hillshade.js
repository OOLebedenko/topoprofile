/**
 * Adds hillshade rendering based on the local DEM source.
 */

import {
    HILLSHADE_CONFIG,
    HILLSHADE_LAYER_ID,
    TERRAIN_SOURCE_ID,
} from "../config.js";

/**
 * Adds a MapLibre hillshade layer using the terrain DEM source.
 * @param {maplibregl.Map} map
 */
export function addHillshade(map) {
    map.addLayer({
        id: HILLSHADE_LAYER_ID,
        type: "hillshade",
        source: TERRAIN_SOURCE_ID,

        paint: {
            "hillshade-exaggeration": HILLSHADE_CONFIG.exaggeration,
        },
    });
}