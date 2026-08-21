import {
    PEAK_MARKER_LAYER,
} from "./markers.js";

import {
    PEAK_LABEL_LAYER,
    SADDLE_LABEL_LAYER,
    VOLCANO_LABEL_LAYER,
} from "./labels.js";


// Re-export the shared source ID so external modules can use
// the peaks package through this single entry point.
export {
    PEAKS_SOURCE_ID,
} from "./shared.js";


// Collect all peak-related MapLibre layers in rendering order.
export const PEAK_LAYERS = [
    PEAK_MARKER_LAYER,
    SADDLE_LABEL_LAYER,
    PEAK_LABEL_LAYER,
    VOLCANO_LABEL_LAYER,
];