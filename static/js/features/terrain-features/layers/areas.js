/**
 * Defines fill layers for terrain surface areas.
 */

import { createAreaLayer } from "./shared.js";

// Glacier areas use a very light cold blue fill.
export const GLACIER_LAYER = createAreaLayer(
    "terrain-glacier",
    "glacier",
    "#edf5f9",
    0.82,
);

// Snowfields use a bright neutral white fill.
export const SNOWFIELD_LAYER = createAreaLayer(
    "terrain-snowfield",
    "snowfield",
    "#ffffff",
    0.78,
);

// Bare rock areas use a warm earthy rock tone.
export const BARE_ROCK_LAYER = createAreaLayer(
    "terrain-bare-rock",
    "bare_rock",
    "#b79f86",
    0.56,
);

// Scree areas use a slightly cooler stone tone.
export const SCREE_LAYER = createAreaLayer(
    "terrain-scree",
    "scree",
    "#ad9a86",
    0.48,
);

// Shingle areas use a lighter sandy stone tone.
export const SHINGLE_LAYER = createAreaLayer(
    "terrain-shingle",
    "shingle",
    "#c0ad95",
    0.48,
);

// Blockfields use a slightly darker rocky tone.
export const BLOCKFIELD_LAYER = createAreaLayer(
    "terrain-blockfield",
    "blockfield",
    "#9f8d7a",
    0.52,
);