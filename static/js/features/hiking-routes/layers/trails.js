import {
    LINE_LAYOUT,
    SOURCE_ID,
} from "./shared.js";

const TRAILS_LAYER_ID = "hiking-trails";
const TRACKS_LAYER_ID = "hiking-tracks";

export function addTrailLayers(map) {
    map.addLayer({
        id: TRACKS_LAYER_ID,
        type: "line",
        source: SOURCE_ID,

        filter: [
            "==",
            ["get", "highway"],
            "track",
        ],

        layout: LINE_LAYOUT,

        paint: {
            "line-color": "#a86b5b",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 1.0,
                11, 1.5,
                14, 2.1,
            ],
            "line-dasharray": [3, 2],
            "line-opacity": 0.8,
        },
    });

    map.addLayer({
        id: TRAILS_LAYER_ID,
        type: "line",
        source: SOURCE_ID,

        filter: [
            "match",
            ["get", "highway"],
            ["path", "footway", "steps"],
            true,
            false,
        ],

        layout: LINE_LAYOUT,

        paint: {
            "line-color": "#b45f4f",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 1.1,
                11, 1.7,
                14, 2.4,
            ],
            "line-dasharray": [4, 2.5],
            "line-opacity": 0.9,
        },
    });
}