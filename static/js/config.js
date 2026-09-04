/**
 * Shared configuration for the map, terrain tiles,
 * and 3D atmosphere.
 */

// Geographic area currently available as local terrain tiles.
const TERRAIN_AREA = {
    center: [42.4361, 43.3538],

    // Bounds in MapLibre order: west, south, east, north.
    bounds: [
        40.78125,
        42.03297433244139,
        45.0,
        45.089035564831015,
    ],

    dataPath: "/data/terrain/tiles",
};

// Slightly inset bounds used only by raster DEM sources.
// This prevents MapLibre from requesting neighboring tiles
// that only touch the exact terrain boundary.
const SOURCE_BOUNDS_EPSILON = 1e-9;

const TERRAIN_SOURCE_BOUNDS = [
    TERRAIN_AREA.bounds[0] + SOURCE_BOUNDS_EPSILON,
    TERRAIN_AREA.bounds[1] + SOURCE_BOUNDS_EPSILON,
    TERRAIN_AREA.bounds[2] - SOURCE_BOUNDS_EPSILON,
    TERRAIN_AREA.bounds[3] - SOURCE_BOUNDS_EPSILON,
];

// Base map and camera settings.
export const MAP_CONFIG = {
    style: "https://tiles.openfreemap.org/styles/liberty",
    center: TERRAIN_AREA.center,
    zoom: 10,
    minPitch: 0,
    maxPitch: 85,
    pitchStep: 10,
    pitch: 0,
    pitch3D: 60,
    rotationStep: 20,
    viewTransitionDuration: 1000,
};

// Local terrain DEM source settings.
export const TERRAIN_SOURCE_ID = "terrain-dem";

// Local hillshade DEM source settings.
export const HILLSHADE_SOURCE_ID = "hillshade-dem";

export const TERRAIN_CONFIG = {
    tiles: [
        `${TERRAIN_AREA.dataPath}/{z}/{x}/{y}.png`,
    ],

    minZoom: 8,
    maxZoom: 14,
    tileSize: 256,
    encoding: "terrarium",
    bounds: TERRAIN_SOURCE_BOUNDS,
};

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

// Local hillshade settings.
export const HILLSHADE_LAYER_ID = "terrain-hillshade";

export const HILLSHADE_CONFIG = {
    exaggeration: 0.15,
};

// Local mountain infrastructure source settings.
export const MOUNTAIN_INFRASTRUCTURE_SOURCE_ID =
    "mountain-infrastructure";

export const MOUNTAIN_INFRASTRUCTURE_CONFIG = {
    dataPath: "/data/osm/chunks",
    chunkZoom: TERRAIN_CONFIG.minZoom,
    bounds: TERRAIN_AREA.bounds,
};

// Sky and fog settings used in the 3D terrain view.
export const ATMOSPHERE_CONFIG = {
    skyColor: "#88c6fc",
    horizonColor: "#ffffff",
    fogColor: "#ffffff",
    skyHorizonBlend: 0.8,
    horizonFogBlend: 0.2,
    fogGroundBlend: 0.05,
};