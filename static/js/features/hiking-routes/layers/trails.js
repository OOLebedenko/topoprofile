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
            "line-color": "#9a7564",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 0.7,
                11, 1.0,
                14, 1.5,
            ],
            "line-dasharray": [3, 2],
            "line-opacity": 0.75,
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
            "line-color": "#a66f60",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 0.8,
                11, 1.1,
                14, 1.6,
            ],
            "line-dasharray": [4, 2.5],
            "line-opacity": 0.9,
        },
    });
}