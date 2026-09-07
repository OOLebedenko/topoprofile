/**
 * Loads and renders local hiking route data.
 */

import {
    HIKING_ROUTES_CONFIG,
    HIKING_ROUTES_SOURCE_ID,
} from "../../config.js";
import {
    addHikingRouteLayers,
} from "./layers/index.js";


export async function addHikingRoutes(map) {
    const {
        dataPath,
        bounds,
        chunkZoom,
    } = HIKING_ROUTES_CONFIG;

    const tileUrl = (
        `${window.location.origin}`
        + `${dataPath}/{z}/{x}/{y}/hiking_routes.pbf`
    );

    map.addSource(HIKING_ROUTES_SOURCE_ID, {
        type: "vector",
        tiles: [
            tileUrl,
        ],
        bounds,
        minzoom: chunkZoom,
        maxzoom: chunkZoom,
    });

    addHikingRouteLayers(map);
}