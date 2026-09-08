/**
 * Defines marker layers for important peaks and volcanoes.
 */

import {
    MOBILE_LAYER_CONFIG,
} from "../../../config.js";

import {
    getResponsiveScale,
} from "../../../viewport.js";

import {
    PEAKS_SOURCE_ID,
    PEAKS_SOURCE_LAYER,
    POINT_GEOMETRY_FILTER,
    RANK1_FILTER,
    VALID_NAME_FILTER,
} from "./shared.js";

const MARKER_SCALE = getResponsiveScale(
    MOBILE_LAYER_CONFIG.peaks.markerScale,
);

// Visual style of peak and volcano markers.
const MARKER_PAINT = {
    "circle-radius": [
        "interpolate",
        ["linear"],
        ["zoom"],
        7,
        3.4 * MARKER_SCALE,
        11,
        4.6 * MARKER_SCALE,
        14,
        5.9 * MARKER_SCALE,
        17,
        6.6 * MARKER_SCALE,
    ],

    "circle-color": "#263238",
    "circle-stroke-color": "#ffffff",

    "circle-stroke-width": [
        "interpolate",
        ["linear"],
        ["zoom"],
        7,
        1.5 * MARKER_SCALE,
        14,
        2.2 * MARKER_SCALE,
        17,
        2.4 * MARKER_SCALE,
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