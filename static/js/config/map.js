/**
 * Base map, camera, responsive layer, and atmosphere configuration.
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

// Base map settings independent of viewport size.
export const MAP_CONFIG = {
    style: "https://tiles.openfreemap.org/styles/liberty",
};

// Viewport breakpoint shared by responsive JavaScript behavior.
export const MOBILE_VIEWPORT_CONFIG = {
    maxWidth: 700,
};

// Camera settings shared by and specialized for each viewport.
export const CAMERA_CONFIG = {
    common: {
        center: TERRAIN_AREA.center,
        minZoom: 10,
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

// Scale factors applied to the existing desktop layer styles.
export const MOBILE_LAYER_CONFIG = {
    mountainInfrastructure: {
        iconScale: 0.72,
        labelScale: 0.8,
    },

    peaks: {
        markerScale: 0.8,
        labelScale: 0.78,
    },

    contours: {
        labelScale: 0.82,
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