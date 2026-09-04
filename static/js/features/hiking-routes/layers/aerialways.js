import {
    LINE_LAYOUT,
    SOURCE_ID,
} from "./shared.js";

const AERIALWAY_CASING_LAYER_ID = "hiking-aerialway-casing";
const AERIALWAY_LAYER_ID = "hiking-aerialway";

const AERIALWAY_FILTER = [
    "has",
    "aerialway",
];

export function addAerialwayLayers(map) {
    map.addLayer({
        id: AERIALWAY_CASING_LAYER_ID,
        type: "line",
        source: SOURCE_ID,
        filter: AERIALWAY_FILTER,
        layout: LINE_LAYOUT,

        paint: {
            "line-color": "#ffffff",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 1.8,
                11, 2.6,
                14, 3.6,
            ],
            "line-opacity": 0.7,
        },
    });

    map.addLayer({
        id: AERIALWAY_LAYER_ID,
        type: "line",
        source: SOURCE_ID,
        filter: AERIALWAY_FILTER,
        layout: LINE_LAYOUT,

        paint: {
            "line-color": "#60439a",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 0.9,
                11, 1.4,
                14, 2.0,
            ],
            "line-dasharray": [1.5, 1],
            "line-opacity": 0.9,
        },
    });
}