/**
 * Creates the MapLibre map instance using the shared map configuration.
 */

import { Map as MapLibreMap } from
    "https://unpkg.com/maplibre-gl@6.0.0/dist/maplibre-gl.mjs";

import { setupMissingImageFallback } from "./base-map/images.js";
import { transformBaseMapStyle } from "./base-map/style.js";
import { MAP_CONFIG } from "./config.js";

import {
    getCameraConfig,
} from "./responsive/viewport.js";

// Creates and returns the main application map.
export function createMap(container) {
    const cameraConfig = getCameraConfig();

    const map = new MapLibreMap({
        container,
        center: MAP_CONFIG.center,
        zoom: cameraConfig.zoom,
        minZoom: MAP_CONFIG.minZoom,
        maxBounds: MAP_CONFIG.maxBounds,
        pitch: cameraConfig.pitch,
        minPitch: MAP_CONFIG.minPitch,
        maxPitch: MAP_CONFIG.maxPitch,
    });

    map.setStyle(
        MAP_CONFIG.style,
        {
            transformStyle: transformBaseMapStyle,
        },
    );

    setupMissingImageFallback(map);

    return map;
}