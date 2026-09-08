/**
 * Creates the MapLibre map instance using the shared map configuration.
 */

import { Map as MapLibreMap } from
    "https://unpkg.com/maplibre-gl@6.0.0/dist/maplibre-gl.mjs";

import { setupMissingImageFallback } from "./base-map/images.js";
import { transformBaseMapStyle } from "./base-map/style.js";
import { MAP_CONFIG } from "./config.js";

// Registers a transparent fallback for missing base-map icons.
function setupMissingImageFallback(map) {
    map.on("styleimagemissing", event => {
        const imageId = event.id;

        if (map.hasImage(imageId)) {
            return;
        }

        const size = 16;
        const data = new Uint8Array(size * size * 4);

        map.addImage(imageId, {
            width: size,
            height: size,
            data,
        });
    });
}

// Creates and returns the main application map.
export function createMap(container) {
    const map = new MapLibreMap({
        container,
        style: MAP_CONFIG.style,
        center: MAP_CONFIG.center,
        zoom: MAP_CONFIG.zoom,
        minZoom: MAP_CONFIG.minZoom,
        maxBounds: MAP_CONFIG.maxBounds,
        pitch: MAP_CONFIG.pitch,
        minPitch: MAP_CONFIG.minPitch,
        maxPitch: MAP_CONFIG.maxPitch,
    });

    setupMissingImageFallback(map);

    return map;
}