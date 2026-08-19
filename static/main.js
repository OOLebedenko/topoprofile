import { createMap } from "./js/map.js";
import { addTerrain } from "./js/terrain.js";

const map = createMap("map");

map.on("load", () => {
    addTerrain(map);
});
