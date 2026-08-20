import {
    PEAK_LABEL,
    PEAKS_SOURCE_ID,
    PEAKS_SOURCE_LAYER,
    POINT_GEOMETRY_FILTER,
    RANK1_FILTER,
    VALID_NAME_FILTER,
} from "./shared.js";


// Higher peaks receive higher placement priority.
const ELEVATION_SORT_KEY = [
    "-",
    9000,
    [
        "to-number",
        ["get", "ele"],
        0,
    ],
];


// Shared visual style for all peak labels.
const LABEL_PAINT = {
    "text-color": "#6f5246",
    "text-halo-blur": 0.12,
    "text-halo-color": "rgba(250,247,242,0.97)",
    "text-halo-width": 2.4,
};


// Shared label placement rules.
// Individual layers override only properties that differ.
const BASE_LABEL_LAYOUT = {
    "text-field": PEAK_LABEL,
    "text-font": ["Noto Sans Bold"],
    "text-allow-overlap": false,
    "text-line-height": 1.0,
    "text-padding": 5,
    "text-ignore-placement": false,
    "text-pitch-alignment": "viewport",
    "text-rotation-alignment": "viewport",
    "symbol-z-order": "viewport-y",
    "symbol-avoid-edges": true,
    "text-anchor": "bottom",
    "symbol-sort-key": ELEVATION_SORT_KEY,
};


// Builds a filter for rank 1 features of a specific mountain class.
function createRank1Filter(peakClass) {
    return [
        "all",
        POINT_GEOMETRY_FILTER,
        [
            "==",
            ["get", "class"],
            peakClass,
        ],
        RANK1_FILTER,
        VALID_NAME_FILTER,
    ];
}


// Creates label layers with the same style for peaks and volcanoes.
function createRank1LabelLayer(id, peakClass) {
    return {
        id,
        type: "symbol",
        source: PEAKS_SOURCE_ID,
        "source-layer": PEAKS_SOURCE_LAYER,
        minzoom: 7,

        filter: createRank1Filter(peakClass),

        layout: {
            ...BASE_LABEL_LAYOUT,
            "text-max-width": 12,
            "text-letter-spacing": 0.015,
            "text-offset": [0, -0.15],

            "text-size": [
                "interpolate",
                ["linear"],
                ["zoom"],
                7, 12.0,
                11, 14.2,
                14, 16.0,
                17, 17.0,
            ],
        },

        paint: LABEL_PAINT,
    };
}


// Saddles use their own zoom threshold and slightly smaller labels.
export const SADDLE_LABEL_LAYER = {
    id: "poi_saddle_m",
    type: "symbol",
    source: PEAKS_SOURCE_ID,
    "source-layer": PEAKS_SOURCE_LAYER,
    minzoom: 13,

    filter: [
        "all",
        POINT_GEOMETRY_FILTER,
        [
            "==",
            ["get", "class"],
            "saddle",
        ],
        VALID_NAME_FILTER,
    ],

    layout: {
        ...BASE_LABEL_LAYOUT,
        "text-max-width": 10,
        "text-offset": [0, -0.1],

        "text-size": [
            "interpolate",
            ["linear"],
            ["zoom"],
            13, 12.4,
            15, 13.5,
            17, 14.5,
        ],
    },

    paint: LABEL_PAINT,
};


// Rank 1 peak and volcano layers share the same layout and paint rules.
export const PEAK_LABEL_LAYER = createRank1LabelLayer(
    "poi_peak_rank1_m",
    "peak",
);


export const VOLCANO_LABEL_LAYER = createRank1LabelLayer(
    "poi_volcano_rank1_m",
    "volcano",
);