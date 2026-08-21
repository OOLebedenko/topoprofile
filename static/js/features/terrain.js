/**
 * Manages the local DEM source and MapLibre terrain rendering.
 */

import { TERRAIN_CONFIG } from "../config.js";

// Internal MapLibre source ID for the local DEM.
const TERRAIN_SOURCE_ID = "terrain-dem";

// Adds the local Terrarium DEM source to the map.
export function addTerrainSource(map) {
    map.addSource(TERRAIN_SOURCE_ID, {
        type: "raster-dem",
        tiles: TERRAIN_CONFIG.tiles,
        minzoom: TERRAIN_CONFIG.minZoom,
        maxzoom: TERRAIN_CONFIG.maxZoom,
        tileSize: TERRAIN_CONFIG.tileSize,
        encoding: TERRAIN_CONFIG.encoding,
        bounds: TERRAIN_CONFIG.bounds,
    });
}

// Enables 3D terrain using the local DEM source.
export function enableTerrain(map) {
    map.setTerrain({
        source: TERRAIN_SOURCE_ID,
    });
}

// Disables 3D terrain while keeping the DEM source available.
export function disableTerrain(map) {
    map.setTerrain(null);
}