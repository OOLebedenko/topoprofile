/**
 * Responsive viewport helpers.
 */

import {
    CAMERA_CONFIG,
    MOBILE_VIEWPORT_CONFIG,
} from "./config.js";

export function isMobileViewport() {
    return window.matchMedia(
        `(max-width: ${MOBILE_VIEWPORT_CONFIG.maxWidth}px)`,
    ).matches;
}

export function getCameraConfig() {
    const viewportConfig = isMobileViewport()
        ? CAMERA_CONFIG.mobile
        : CAMERA_CONFIG.desktop;

    return {
        ...CAMERA_CONFIG.common,
        ...viewportConfig,
    };
}

export function getResponsiveScale(mobileScale) {
    return isMobileViewport()
        ? mobileScale
        : 1;
}