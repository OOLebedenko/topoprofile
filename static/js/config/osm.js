/**
 * OpenStreetMap vector source configuration.
 */

import {
    TERRAIN_AREA,
    TERRAIN_CONFIG,
} from "./terrain.js";

// Local terrain feature source settings.
export const TERRAIN_FEATURES_SOURCE_ID = "terrain-features";

export const TERRAIN_FEATURES_CONFIG = {
    dataPath: "/data/osm/chunks",
    chunkZoom: TERRAIN_CONFIG.minZoom,
    bounds: TERRAIN_AREA.bounds,
};

// Local hiking route source settings.
export const HIKING_ROUTES_SOURCE_ID = "hiking-routes";

export const HIKING_ROUTES_CONFIG = {
    dataPath: "/data/osm/chunks",
    chunkZoom: TERRAIN_CONFIG.minZoom,
    bounds: TERRAIN_AREA.bounds,
};

// Local mountain infrastructure source settings.
export const MOUNTAIN_INFRASTRUCTURE_SOURCE_ID =
    "mountain-infrastructure";

export const MOUNTAIN_INFRASTRUCTURE_CONFIG = {
    dataPath: "/data/osm/chunks",
    chunkZoom: TERRAIN_CONFIG.minZoom,
    bounds: TERRAIN_AREA.bounds,
};