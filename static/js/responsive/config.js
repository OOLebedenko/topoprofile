/**
 * Responsive map view and layer settings.
 */

export const MOBILE_VIEWPORT_CONFIG = {
    maxWidth: 700,
};

// Camera settings for desktop and mobile viewports.
export const CAMERA_CONFIG = {
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

    pitchStep: 10,
    rotationStep: 20,
    viewTransitionDuration: 1400,
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