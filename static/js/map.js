/**
 * Creates the MapLibre map instance using the shared map configuration.
 */

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
    const map = new maplibregl.Map({
        container,
        style: MAP_CONFIG.style,
        center: MAP_CONFIG.center,
        zoom: MAP_CONFIG.zoom,
        pitch: MAP_CONFIG.pitch,
        maxPitch: MAP_CONFIG.maxPitch,
    });

    setupMissingImageFallback(map);

    return map;
}