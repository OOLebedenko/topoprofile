import {
    addContourLabels,
} from "./labels.js";

import {
    addContourLines,
} from "./lines.js";

export {
    loadContours,
} from "./source.js";

export function addContourLayers(map) {
    addContourLabels(map);
    addContourLines(map);
}