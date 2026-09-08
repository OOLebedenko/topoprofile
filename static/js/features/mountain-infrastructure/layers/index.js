/**
 * Registers all mountain infrastructure layers.
 */

import {
    addMountainInfrastructureLabels,
} from "./labels.js";

import {
    addMountainInfrastructureMarkers,
} from "./markers.js";

export function addMountainInfrastructureLayers(map) {
    addMountainInfrastructureMarkers(map);
    addMountainInfrastructureLabels(map);
}