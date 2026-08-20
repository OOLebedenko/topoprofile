import { MAP_CONFIG } from "./config.js";

export function createMap(container) {
    return new maplibregl.Map({
        container,
        style: MAP_CONFIG.style,
        center: MAP_CONFIG.center,
        zoom: MAP_CONFIG.zoom,
        pitch: MAP_CONFIG.pitch,
    });
}