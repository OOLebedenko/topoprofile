/**
 * Shared identifiers, expressions, and filters
 * for mountain infrastructure layers.
 */

import {
    MOUNTAIN_INFRASTRUCTURE_SOURCE_ID,
} from "../../../config.js";

export const SOURCE_ID = MOUNTAIN_INFRASTRUCTURE_SOURCE_ID;

// Registered MapLibre image used for mountain huts.
export const HUT_ICON_ID = "mountain-hut";

// Icon size for infrastructure loaded from local GeoJSON.
export const HUT_ICON_SIZE = [
    "interpolate",
    ["linear"],
    ["zoom"],
    10,
    0.45,
    12,
    0.55,
    14,
    0.7,
];

// Base-map POIs use a slightly smaller icon
// to visually match the locally prepared markers.
export const BASE_HUT_ICON_SIZE = [
    "interpolate",
    ["linear"],
    ["zoom"],
    10,
    0.43,
    12,
    0.53,
    14,
    0.68,
];

// Prefer a localized Russian name when available.
export const NAME_FIELD = [
    "coalesce",
    ["get", "name:ru"],
    ["get", "name"],
    ["get", "name:en"],
    "",
];

// Labels are rendered only for named infrastructure objects.
export const NAMED_FEATURE_FILTER = [
    "!=",
    NAME_FIELD,
    "",
];