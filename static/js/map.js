/**
 * Creates the MapLibre map instance using the shared map configuration.
 */

import { Map as MapLibreMap } from
    "https://unpkg.com/maplibre-gl@6.0.0/dist/maplibre-gl.mjs";

import { setupMissingImageFallback } from "./base-map/images.js";
import { transformBaseMapRequest } from "./base-map/requests.js";
import { transformBaseMapStyle } from "./base-map/style.js";
import { MAP_CONFIG } from "./config.js";

import {
    getCameraConfig,
} from "./viewport.js";

// Creates and returns the main application map.
export function createMap(container) {
    const cameraConfig = getCameraConfig();

    const map = new MapLibreMap({
        container,
        center: cameraConfig.center,
        zoom: cameraConfig.zoom,
        minZoom: cameraConfig.minZoom,
        maxBounds: cameraConfig.maxBounds,
        pitch: cameraConfig.pitch,
        minPitch: cameraConfig.minPitch,
        maxPitch: cameraConfig.maxPitch,
        transformRequest: transformBaseMapRequest,
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