/**
 * Adapts the external base-map style for TopoProfile.
 */

const ROAD_SHIELD_LAYER_IDS = new Set([
    "highway-shield-non-us",
    "highway-shield-us-interstate",
    "road_shield_us",
]);

const TRANSPORTATION_SOURCE_LAYERS = new Set([
    "transportation",
    "transportation_name",
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

const HIDE_TRAILS_FILTER = [
    "!=",
    ["get", "class"],
    "path",
];

function addFilter(
        layer,
        filter,
) {
    return {
        ...layer,

        filter: layer.filter
            ? [
                "all",
                filter,
                layer.filter,
            ]
            : filter,
    };
}

// Adapts base-map transportation layers and filters
// invalid road shield features.
export function transformBaseMapStyle(previousStyle, nextStyle) {
    return {
        ...nextStyle,

        layers: nextStyle.layers.map(layer => {
            let transformedLayer = layer;

            if (
                TRANSPORTATION_SOURCE_LAYERS.has(
                    layer["source-layer"]
                )
            ) {
                transformedLayer = addFilter(
                    transformedLayer,
                    HIDE_TRAILS_FILTER,
                );
            }

            if (
                ROAD_SHIELD_LAYER_IDS.has(
                    layer.id
                )
            ) {
                transformedLayer = addFilter(
                    transformedLayer,
                    VALID_REF_LENGTH_FILTER,
                );
            }

            return transformedLayer;
        }),
    };
}