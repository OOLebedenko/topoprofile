/**
 * Mountain infrastructure label layer.
 */

import {
    NAME_FIELD,
    NAMED_FEATURE_FILTER,
    SOURCE_ID,
} from "./shared.js";

export function addMountainInfrastructureLabels(map) {
    map.addLayer({
        id: "mountain-infrastructure-labels",
        type: "symbol",
        source: SOURCE_ID,
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
                10,
                12,
                11.5,
                14,
                13,
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