import { addAtmosphere } from "./js/atmosphere.js";
import { setupViewToggle } from "./js/controls.js";
import { createMap } from "./js/map.js";
import { setupNavigationControls } from "./js/navigation.js";
import { addTerrainSource } from "./js/terrain.js";
import { addPeaks } from "./js/peaks.js";

const map = createMap("map");

setupNavigationControls(map);

map.on("load", () => {
    addTerrainSource(map);
    addAtmosphere(map);
    addPeaks(map);
    setupViewToggle(map);
});