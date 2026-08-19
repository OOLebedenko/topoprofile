import { TERRAIN_CONFIG } from "./config.js";

const TERRAIN_SOURCE_ID = "terrain-dem";

export function addTerrain(map) {
    map.addSource(TERRAIN_SOURCE_ID, {
        type: "raster-dem",
        tiles: TERRAIN_CONFIG.tiles,
        minzoom: TERRAIN_CONFIG.minZoom,
        maxzoom: TERRAIN_CONFIG.maxZoom,
        tileSize: TERRAIN_CONFIG.tileSize,
        encoding: TERRAIN_CONFIG.encoding,
        bounds: TERRAIN_CONFIG.bounds,
    });

    map.setTerrain({
        source: TERRAIN_SOURCE_ID,
    });
}