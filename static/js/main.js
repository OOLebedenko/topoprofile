import { setupNavigationControls } from "./controls/navigation.js";
import { setupViewToggle } from "./controls/view-toggle.js";

import { addAtmosphere } from "./features/atmosphere.js";
import { addPeaks } from "./features/peaks/peaks.js";
import { addTerrainSource } from "./features/terrain.js";

import { createMap } from "./map.js";

const map = createMap("map");

setupNavigationControls(map);

map.on("load", () => {
    addTerrainSource(map);
    addAtmosphere(map);
    addPeaks(map);
    setupViewToggle(map);
});