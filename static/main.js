import { createMap } from "./js/map.js";
import { setupNavigationControls } from "./js/controls.js";
import { addTerrain } from "./js/terrain.js";

const map = createMap("map");

setupNavigationControls(map);

map.on("load", () => {
    addTerrain(map);
});