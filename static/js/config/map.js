/**
 * Base map, camera, and atmosphere configuration.
 */

import {
    TERRAIN_AREA,
} from "./terrain.js";

// Area available for map navigation.
const MAP_BOUNDS = [
    41.00,
    42.55,
    44.95,
    43.75,
];

// Base map settings.
export const MAP_CONFIG = {
    style: "https://tiles.openfreemap.org/styles/liberty",
};

// Camera settings shared by and specialized
// for desktop and mobile viewports.
export const CAMERA_CONFIG = {
    common: {
        center: TERRAIN_AREA.center,
        minZoom: 9,
        maxBounds: MAP_BOUNDS,
        minPitch: 0,
        maxPitch: 85,
        pitchStep: 10,
        rotationStep: 20,
        viewTransitionDuration: 1400,
    },

    desktop: {
        zoom: 10,
        zoom3D: 12,
        pitch: 0,
        pitch3D: 85,
    },

    mobile: {
        zoom: 10,
        zoom3D: 11,
        pitch: 0,
        pitch3D: 76,
    },
};

// Sky and fog settings used in the 3D terrain view.
export const ATMOSPHERE_CONFIG = {
    skyColor: "#88c6fc",
    horizonColor: "#ffffff",
    fogColor: "#ffffff",
    skyHorizonBlend: 0.5,
    horizonFogBlend: 0.2,
    fogGroundBlend: 0.02,
};