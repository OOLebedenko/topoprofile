/**
 * Adds terrain contour vector tiles to the map.
 */

import {
    CONTOURS_CONFIG,
    CONTOURS_SOURCE_ID,
} from "../../config.js";

import {
    addContourLayers,
} from "./layers/index.js";

export function addContours(map) {
    const {
        dataPath,
        bounds,
        chunkZoom,
    } = CONTOURS_CONFIG;

    const tileUrl = (
        `${window.location.origin}`
        + `${dataPath}/{z}/{x}/{y}/contours.pbf`
    );

    map.addSource(CONTOURS_SOURCE_ID, {
        type: "vector",
        tiles: [
            tileUrl,
        ],
        bounds,
        minzoom: chunkZoom,
        maxzoom: chunkZoom,
    });

    addContourLayers(map);
}