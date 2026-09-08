/**
 * Shared constants and helpers for terrain feature layers.
 */

import { TERRAIN_FEATURES_SOURCE_ID } from "../../../config.js";

export const SOURCE_LAYER = "terrain_surface";

// Creates a filter for a specific OSM natural feature type.
export function createNaturalFilter(natural) {
    return [
        "==",
        ["get", "natural"],
        natural,
    ];
}

// Creates a common fill layer for terrain surface areas.
export function createAreaLayer(
    id,
    natural,
    color,
    opacity,
) {
    return {
        id,
        type: "fill",
        source: TERRAIN_FEATURES_SOURCE_ID,
        "source-layer": SOURCE_LAYER,
        filter: createNaturalFilter(natural),
        paint: {
            "fill-color": color,
            "fill-opacity": opacity,
        },
    };
}