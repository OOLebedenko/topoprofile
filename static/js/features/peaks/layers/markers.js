/**
 * Defines marker layers for important peaks and volcanoes.
 */

import {
    PEAKS_SOURCE_ID,
    PEAKS_SOURCE_LAYER,
    POINT_GEOMETRY_FILTER,
    RANK1_FILTER,
    VALID_NAME_FILTER,
} from "./shared.js";

// Visual style of peak and volcano markers.
const MARKER_PAINT = {
    "circle-radius": [
        "interpolate",
        ["linear"],
        ["zoom"],
        7, 3.4,
        11, 4.6,
        14, 5.9,
        17, 6.6,
    ],
    "circle-color": "#263238",
    "circle-stroke-color": "#ffffff",
    "circle-stroke-width": [
        "interpolate",
        ["linear"],
        ["zoom"],
        7, 1.5,
        14, 2.2,
        17, 2.4,
    ],
    "circle-opacity": 0.98,
};

// Marks important rank 1 peaks and volcanoes with circles.
export const PEAK_MARKER_LAYER = {
    id: "mountain_peak_points",
    type: "circle",
    source: PEAKS_SOURCE_ID,
    "source-layer": PEAKS_SOURCE_LAYER,
    minzoom: 7,
    filter: [
        "all",
        POINT_GEOMETRY_FILTER,
        [
            "match",
            ["get", "class"],
            ["peak", "volcano"],
            true,
            false,
        ],
        RANK1_FILTER,
        VALID_NAME_FILTER,
    ],
    paint: MARKER_PAINT,
};