/**
 * Mountain infrastructure marker layer.
 */

import {
    HUT_ICON_ID,
    HUT_ICON_SIZE,
    SOURCE_ID,
} from "./shared.js";

export function addMountainInfrastructureMarkers(map) {
    map.addLayer({
        id: "mountain-infrastructure-markers",
        type: "symbol",
        source: SOURCE_ID,
        minzoom: 10,

        layout: {
            "icon-image": HUT_ICON_ID,
            "icon-size": HUT_ICON_SIZE,

            // Keep hut markers visible even in dense infrastructure areas.
            "icon-allow-overlap": true,
            "icon-ignore-placement": true,
        },
    });
}