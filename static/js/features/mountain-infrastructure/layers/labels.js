/**
 * Mountain infrastructure label layer.
 */

import {
    MOBILE_LAYER_CONFIG,
} from "../../../responsive/config.js";

import {
    getResponsiveScale,
} from "../../../responsive/viewport.js";

import {
    NAME_FIELD,
    NAMED_FEATURE_FILTER,
    SOURCE_ID,
    SOURCE_LAYER,
} from "./shared.js";

const LABEL_SCALE = getResponsiveScale(
    MOBILE_LAYER_CONFIG.mountainInfrastructure.labelScale,
);

export function addMountainInfrastructureLabels(map) {
    map.addLayer({
        id: "mountain-infrastructure-labels",
        type: "symbol",
        source: SOURCE_ID,
        "source-layer": SOURCE_LAYER,
        minzoom: 10,
        filter: NAMED_FEATURE_FILTER,

        layout: {
            "text-field": NAME_FIELD,
            "text-font": [
                "Noto Sans Regular",
            ],

            "text-size": [
                "interpolate",
                ["linear"],
                ["zoom"],
                10,
                10.5 * LABEL_SCALE,
                12,
                12 * LABEL_SCALE,
                14,
                13.5 * LABEL_SCALE,
            ],

            // Place labels above the hut marker.
            "text-anchor": "bottom",
            "text-offset": [0, -1.1],
            "text-max-width": 10,
            "text-padding": 2,

            // Let MapLibre suppress overlapping labels.
            "text-allow-overlap": false,
            "text-ignore-placement": false,
        },

        paint: {
            "text-color": "#672525",
            "text-halo-color": "rgba(255,255,255,0.97)",
            "text-halo-width": 2,
            "text-halo-blur": 0.2,
        },
    });
}