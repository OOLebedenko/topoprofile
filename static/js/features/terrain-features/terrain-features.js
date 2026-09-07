/**
 * Loads terrain surface features from local OSM vector tiles
 * and adds them to the map.
 */

import {
    TERRAIN_FEATURES_CONFIG,
    TERRAIN_FEATURES_SOURCE_ID,
} from "../../config.js";
import { addTerrainFeatureLayers } from "./layers/index.js";

// Adds the terrain feature source and its rendering layers.
export async function addTerrainFeatures(map) {
    const {
        dataPath,
        bounds,
        chunkZoom,
    } = TERRAIN_FEATURES_CONFIG;

    const tileUrl = (
        `${window.location.origin}`
        + `${dataPath}/{z}/{x}/{y}/terrain_surface.pbf`
    );

    map.addSource(TERRAIN_FEATURES_SOURCE_ID, {
        type: "vector",
        tiles: [
            tileUrl,
        ],
        bounds,
        minzoom: chunkZoom,
        maxzoom: chunkZoom,
    });

    addTerrainFeatureLayers(map);
}