/**
 * Adds mountain peak markers and labels to the map.
 */

import {
    PEAK_LAYERS,
    PEAKS_SOURCE_ID,
} from "./layers/index.js";

// Adds a layer only if it has not already been added to the map.
function addLayer(map, layer) {
    if (map.getLayer(layer.id)) {
        return;
    }

    map.addLayer(layer);
}

// Adds all peak-related layers using the existing OpenMapTiles source.
export function addPeaks(map) {
    if (!map.getSource(PEAKS_SOURCE_ID)) {
        throw new Error(
            `Map source "${PEAKS_SOURCE_ID}" is not available.`,
        );
    }

    for (const layer of PEAK_LAYERS) {
        addLayer(map, layer);
    }
}