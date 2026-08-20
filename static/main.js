import { addAtmosphere } from "./js/atmosphere.js";
import { createMap } from "./js/map.js";
import {
    setupNavigationControls,
    setupViewToggle,
} from "./js/controls.js";
import { addTerrainSource } from "./js/terrain.js";

const map = createMap("map");

setupNavigationControls(map);

map.on("load", () => {
    addTerrainSource(map);
    addAtmosphere(map);
    setupViewToggle(map);
});