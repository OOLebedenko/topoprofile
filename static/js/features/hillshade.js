/**
 * Adds hillshade rendering based on the local DEM source.
 */

import {
    HILLSHADE_CONFIG,
    HILLSHADE_LAYER_ID,
    TERRAIN_SOURCE_ID,
} from "../config.js";

// Adds a hillshade layer using the existing terrain DEM source.
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