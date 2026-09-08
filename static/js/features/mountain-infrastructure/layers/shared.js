/**
 * Shared identifiers, expressions, and filters
 * for mountain infrastructure layers.
 */

import {
    MOUNTAIN_INFRASTRUCTURE_SOURCE_ID,
} from "../../../config.js";

import {
    MOBILE_LAYER_CONFIG,
} from "../../../responsive/config.js";

import {
    getResponsiveScale,
} from "../../../responsive/viewport.js";

export const SOURCE_ID = MOUNTAIN_INFRASTRUCTURE_SOURCE_ID;
export const SOURCE_LAYER = "mountain_infrastructure";

// Registered MapLibre image used for mountain huts.
export const HUT_ICON_ID = "mountain-hut";

const HUT_ICON_SCALE = getResponsiveScale(
    MOBILE_LAYER_CONFIG.mountainInfrastructure.iconScale,
);

// Icon size for local mountain infrastructure.
export const HUT_ICON_SIZE = [
    "interpolate",
    ["linear"],
    ["zoom"],
    10,
    0.45 * HUT_ICON_SCALE,
    12,
    0.55 * HUT_ICON_SCALE,
    14,
    0.7 * HUT_ICON_SCALE,
];

// Base-map POIs use a slightly smaller icon
// to visually match the locally prepared markers.
export const BASE_HUT_ICON_SIZE = [
    "interpolate",
    ["linear"],
    ["zoom"],
    10,
    0.5 * HUT_ICON_SCALE,
    12,
    0.6 * HUT_ICON_SCALE,
    14,
    0.75 * HUT_ICON_SCALE,
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