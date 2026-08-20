export const PEAKS_SOURCE_ID = "openmaptiles";

export const PEAKS_SOURCE_LAYER = "mountain_peak";


// Mountain features used by peak layers are represented as points.
export const POINT_GEOMETRY_FILTER = [
    "match",
    ["geometry-type"],
    ["Point", "MultiPoint"],
    true,
    false,
];


// Selects the most important mountain features.
export const RANK1_FILTER = [
    "<=",
    [
        "coalesce",
        ["get", "rank"],
        99,
    ],
    1,
];


// Selects the preferred localized name for a mountain feature.
export const PEAK_NAME = [
    "coalesce",
    ["get", "name:ru"],
    ["get", "name_ru"],
    ["get", "name"],
    ["get", "name:latin"],
    ["get", "name_en"],
    "",
];


// Excludes empty and generic placeholder names.
export const VALID_NAME_FILTER = [
    "all",
    [
        "!=",
        PEAK_NAME,
        "",
    ],
    [
        "!",
        [
            "in",
            [
                "downcase",
                PEAK_NAME,
            ],
            [
                "literal",
                [
                    "peak",
                    "volcano",
                    "summit",
                    "pass",
                    "saddle",
                    "unknown",
                    "unknown peak",
                    "unnamed",
                    "unnamed peak",
                    "безымянная вершина",
                    "неизвестная вершина",
                    "вершина",
                    "вулкан",
                    "перевал",
                    "седловина",
                ],
            ],
        ],
    ],
];


// Builds the displayed label from the feature name and elevation.
export const PEAK_LABEL = [
    "case",
    ["has", "ele"],
    [
        "concat",
        PEAK_NAME,
        "\n",
        [
            "to-string",
            [
                "round",
                [
                    "to-number",
                    ["get", "ele"],
                ],
            ],
        ],
        " m",
        "\n│",
    ],
    [
        "concat",
        PEAK_NAME,
        "\n│",
    ],
];