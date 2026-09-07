import {
    CONTOURS_SOURCE_ID,
} from "../../../config.js";

export function addContourLabels(map) {
    map.addLayer({
        id: "terrain-contour-labels",
        type: "symbol",
        source: CONTOURS_SOURCE_ID,
        minzoom: 10,

        layout: {
            "symbol-placement": "line",
            "symbol-spacing": 180,

            "text-field": [
                "concat",
                [
                    "to-string",
                    ["get", "elevation"],
                ],
                " m",
            ],

            "text-size": [
                "interpolate",
                ["linear"],
                ["zoom"],
                10, 10,
                12, 12,
                15, 14,
            ],

            "text-rotation-alignment": "map",
            "text-pitch-alignment": "map",
            "text-keep-upright": true,
            "text-allow-overlap": false,
            "text-ignore-placement": true,
        },

        paint: {
            "text-color": "#5f5043",
            "text-halo-color": "#ffffff",
            "text-halo-width": 1.5,
            "text-opacity": 0.9,
        },
    });
}