/**
 * Responsive viewport and layer configuration.
 */

export const MOBILE_VIEWPORT_CONFIG = {
    maxWidth: 700,
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