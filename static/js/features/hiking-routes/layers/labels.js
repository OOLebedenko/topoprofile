import {
    SOURCE_ID,
} from "./shared.js";

const HIKING_LABELS_LAYER_ID = "hiking-route-labels";
const AERIALWAY_LABELS_LAYER_ID = "hiking-aerialway-labels";

const HIKING_LABEL_FILTER = [
    "all",
    ["!", ["has", "aerialway"]],
    [
        "any",
        ["has", "name:ru"],
        ["has", "name"],
        ["has", "ref"],
    ],
];

const AERIALWAY_LABEL_FILTER = [
    "all",
    ["has", "aerialway"],
    [
        "any",
        ["has", "name:ru"],
        ["has", "name"],
        ["has", "ref"],
    ],
];

const TEXT_FIELD = [
    "coalesce",
    ["get", "name:ru"],
    ["get", "name"],
    ["get", "ref"],
];

const TEXT_SIZE = [
    "interpolate",
    ["linear"],
    ["zoom"],
    10, 12,
    16, 17,
];

const LABEL_LAYOUT = {
    "symbol-placement": "line",
    "text-field": TEXT_FIELD,
    "text-size": TEXT_SIZE,
    "text-rotation-alignment": "map",
    "text-pitch-alignment": "viewport",
    "text-max-angle": 60,
    "text-padding": 1,
    "symbol-spacing": 250,
};

export function addHikingRouteLabels(map) {
    map.addLayer({
        id: HIKING_LABELS_LAYER_ID,
        type: "symbol",
        source: SOURCE_ID,
        filter: HIKING_LABEL_FILTER,
        layout: LABEL_LAYOUT,

        paint: {
            "text-color": "#89584f",
            "text-halo-color": "#f7f4ef",
            "text-halo-width": 1.2,
        },
    });

    map.addLayer({
        id: AERIALWAY_LABELS_LAYER_ID,
        type: "symbol",
        source: SOURCE_ID,
        filter: AERIALWAY_LABEL_FILTER,
        layout: LABEL_LAYOUT,

        paint: {
            "text-color": "#60439a",
            "text-halo-color": "#ffffff",
            "text-halo-width": 1.2,
        },
    });
}