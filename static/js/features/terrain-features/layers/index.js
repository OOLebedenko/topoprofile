/**
 * Adds all terrain surface feature layers to the map.
 */

import {
    BARE_ROCK_LAYER,
    BLOCKFIELD_LAYER,
    GLACIER_LAYER,
    SCREE_LAYER,
    SHINGLE_LAYER,
    SNOWFIELD_LAYER,
} from "./areas.js";
import { CLIFF_LAYER } from "./cliffs.js";

// Area layers are ordered from broad surface fills to smaller details.
const AREA_LAYERS = [
    BARE_ROCK_LAYER,
    SCREE_LAYER,
    SHINGLE_LAYER,
    BLOCKFIELD_LAYER,
    GLACIER_LAYER,
    SNOWFIELD_LAYER,
];

// Adds terrain area fills followed by cliff lines.
export function addTerrainFeatureLayers(map) {
    for (const layer of AREA_LAYERS) {
        map.addLayer(layer);
    }

    map.addLayer(CLIFF_LAYER);
}