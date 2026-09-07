/**
 * Loads terrain contours and adds them to the map.
 */

import {
    CONTOURS_SOURCE_ID,
} from "../../config.js";

import {
    addContourLayers,
    loadContours,
} from "./layers/index.js";

export async function addContours(map) {
    const geojson = await loadContours();

    map.addSource(CONTOURS_SOURCE_ID, {
        type: "geojson",
        data: geojson,
    });

    addContourLayers(map);
}