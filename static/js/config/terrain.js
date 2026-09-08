/**
 * Terrain, hillshade, and contour configuration.
 */

// Geographic area currently available as local terrain tiles.
export const TERRAIN_AREA = {
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

// Local terrain DEM source settings.
export const TERRAIN_SOURCE_ID = "terrain-dem";

export const TERRAIN_CONFIG = {
    tiles: [
        `${TERRAIN_AREA.dataPath}/{z}/{x}/{y}.webp`,
    ],

    minZoom: 8,
    maxZoom: 12,
    tileSize: 256,
    encoding: "terrarium",
    bounds: TERRAIN_SOURCE_BOUNDS,
};

// Local hillshade layer settings.
export const HILLSHADE_LAYER_ID = "terrain-hillshade";

export const HILLSHADE_CONFIG = {
    exaggeration: 0.15,
};

// Local terrain contour source settings.
export const CONTOURS_SOURCE_ID = "terrain-contours";

export const CONTOURS_CONFIG = {
    dataPath: "/data/terrain/contours",
    chunkZoom: TERRAIN_CONFIG.minZoom,
    bounds: TERRAIN_AREA.bounds,
};