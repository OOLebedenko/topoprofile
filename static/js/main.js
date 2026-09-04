/**
 * Application entry point.
 * Initializes the map, controls, and map features.
 */

import { setupNavigationControls } from "./controls/navigation.js";
import { setupViewToggle } from "./controls/view-toggle.js";

import { addAtmosphere } from "./features/atmosphere.js";
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

// Navigation controls can be connected immediately after map creation.
setupNavigationControls(map);

// Add map features after the base style has finished loading.
map.on("load", async () => {
    addTerrainSource(map);
    addHillshade(map);
    await addTerrainFeatures(map);
    await addHikingRoutes(map);
    await addMountainInfrastructure(map);
    addAtmosphere(map);
    addPeaks(map);
    setupViewToggle(map);
});