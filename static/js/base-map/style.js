/**
 * Adapts the external base-map style for TopoProfile.
 */

const ROAD_SHIELD_LAYER_IDS = new Set([
    "highway-shield-non-us",
    "highway-shield-us-interstate",
    "road_shield_us",
]);

const VALID_REF_LENGTH_FILTER = [
    "all",
    ["has", "ref_length"],
    [
        "==",
        ["typeof", ["get", "ref_length"]],
        "number",
    ],
    [
        ">",
        ["get", "ref_length"],
        0,
    ],
];

// Filters invalid road shield features while preserving
// the original base-map filters.
export function transformBaseMapStyle(previousStyle, nextStyle) {
    return {
        ...nextStyle,

        layers: nextStyle.layers.map(layer => {
            if (!ROAD_SHIELD_LAYER_IDS.has(layer.id)) {
                return layer;
            }

            return {
                ...layer,

                filter: layer.filter
                    ? [
                        "all",
                        VALID_REF_LENGTH_FILTER,
                        layer.filter,
                    ]
                    : VALID_REF_LENGTH_FILTER,
            };
        }),
    };
}