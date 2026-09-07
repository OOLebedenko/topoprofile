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
            "line-color": "#ad5548",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                8, 1.2,
                11, 1.8,
                14, 2.6,
            ],
            "line-dasharray": [5, 2.5],
            "line-opacity": 0.95,
        },
    });
}