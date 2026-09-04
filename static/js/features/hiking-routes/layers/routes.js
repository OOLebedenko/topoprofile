import {
    LINE_LAYOUT,
    SOURCE_ID,
} from "./shared.js";

const ROUTE_LAYER_ID = "hiking-route";

const ROUTE_FILTER = [
    "match",
    ["get", "route"],
    ["hiking", "foot", "walking"],
    true,
    false,
];

export function addRouteLayers(map) {
    map.addLayer({
        id: ROUTE_LAYER_ID,
        type: "line",
        source: SOURCE_ID,
        filter: ROUTE_FILTER,
        layout: LINE_LAYOUT,

        paint: {
            "line-color": "#945f55",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 0.9,
                11, 1.2,
                14, 1.8,
            ],
            "line-dasharray": [5, 2.5],
            "line-opacity": 0.95,
        },
    });
}