import { MAP_CONFIG } from "./config.js";

export function createMap(container) {
    const map = new maplibregl.Map({
        container,
        style: MAP_CONFIG.style,
        center: MAP_CONFIG.center,
        zoom: MAP_CONFIG.zoom,
    });

    map.addControl(
        new maplibregl.NavigationControl(),
        "top-right",
    );

    return map;
}
