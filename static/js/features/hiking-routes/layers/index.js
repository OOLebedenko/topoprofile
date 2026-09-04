import {
    addAerialwayLayers,
} from "./aerialways.js";
import {
    addHikingRouteLabels,
} from "./labels.js";
import {
    addRouteLayers,
} from "./routes.js";
import {
    addTrailLayers,
} from "./trails.js";

export function addHikingRouteLayers(map) {
    addTrailLayers(map);
    addRouteLayers(map);
    addAerialwayLayers(map);
    addHikingRouteLabels(map);
}