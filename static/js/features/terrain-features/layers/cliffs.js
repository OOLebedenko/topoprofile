/**
 * Defines line layers for terrain cliffs.
 */

import { TERRAIN_FEATURES_SOURCE_ID } from "../../../config.js";
import { createNaturalFilter } from "./shared.js";

// Cliffs are rendered as distinct dark terrain lines.
export const CLIFF_LAYER = {
    id: "terrain-cliffs",
    type: "line",
    source: TERRAIN_FEATURES_SOURCE_ID,
    filter: createNaturalFilter("cliff"),
    paint: {
        "line-color": "#8f8175",
        "line-width": [
            "interpolate",
            ["linear"],
            ["zoom"],
            8, 0.8,
            11, 1.5,
            14, 2.5,
            17, 3.5,
        ],
        "line-opacity": 0.4,
    },
};