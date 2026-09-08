/**
 * Application entry point.
 * Initializes the map, controls, and map features.
 */

import {
    createMapLoadingIndicator,
} from "./controls/loading.js";
import { setupNavigationControls } from "./controls/navigation.js";
import { setupViewToggle } from "./controls/view-toggle.js";

import { addAtmosphere } from "./features/atmosphere.js";
import { addContours } from "./features/contours/contours.js";
import { addHikingRoutes } from "./features/hiking-routes/hiking-routes.js";
import { addHillshade } from "./features/hillshade.js";
import {
    addMountainInfrastructure,
} from "./features/mountain-infrastructure/mountain-infrastructure.js";
import { addPeaks } from "./features/peaks/peaks.js";
import { addTerrainSource } from "./features/terrain.js";
import { addTerrainFeatures } from "./features/terrain-features/terrain-features.js";

import { createMap } from "./map.js";

// Create the main MapLibre map instance.
const map = createMap("map");
const loading = createMapLoadingIndicator();

// Navigation controls can be connected immediately after map creation.
setupNavigationControls(map);

// Add map features after the base style has finished loading.
map.on("load", async () => {
    addTerrainSource(map);
    addHillshade(map);

    await addTerrainFeatures(map);
    loading.setProgress(25);

    await addHikingRoutes(map);
    loading.setProgress(50);

    await addContours(map);
    loading.setProgress(75);

    await addMountainInfrastructure(map);
    loading.setProgress(100);

    addAtmosphere(map);
    addPeaks(map);
    setupViewToggle(map);

    map.once("idle", () => {
        loading.hide();
    });
});