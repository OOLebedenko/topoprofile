/**
 * Shared configuration for the map, terrain region,
 * local DEM tiles, and 3D atmosphere.
 */

// Terrain region currently available as local DEM tiles.
const TERRAIN_REGION = {
    id: "elbrus",
    center: [42.4361, 43.3538],

    // Bounds in MapLibre order: west, south, east, north.
    bounds: [
        41.5706944,
        42.7206944,
        43.3001389,
        43.9876389,
    ],

    dataPath: "../data/regions/elbrus",
};

// Base map and camera settings.
export const MAP_CONFIG = {
    style: "https://tiles.openfreemap.org/styles/liberty",
    center: TERRAIN_REGION.center,
    zoom: 10,
    minPitch: 0,
    maxPitch: 85,
    pitchStep: 10,
    pitch: 0,
    pitch3D: 60,
    rotationStep: 20,
    viewTransitionDuration: 1000,
};

// Local Terrarium DEM source settings.
export const TERRAIN_CONFIG = {
    tiles: [
        `${TERRAIN_REGION.dataPath}/tiles/terrain/{z}/{x}/{y}.png`,
    ],

    minZoom: 8,
    maxZoom: 14,
    tileSize: 256,
    encoding: "terrarium",
    bounds: TERRAIN_REGION.bounds,
};

// Sky and fog settings used in the 3D terrain view.
export const ATMOSPHERE_CONFIG = {
    skyColor: "#88c6fc",
    horizonColor: "#ffffff",
    fogColor: "#ffffff",
    skyHorizonBlend: 0.8,
    horizonFogBlend: 0.8,
    fogGroundBlend: 0.5,
};