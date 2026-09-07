import {
    CONTOURS_SOURCE_ID,
} from "../../../config.js";

export function addContourLines(map) {
    map.addLayer({
        id: "terrain-contours",
        type: "line",
        source: CONTOURS_SOURCE_ID,
        minzoom: 9,

        paint: {
            "line-color": "#7f8987",
            "line-width": [
                "interpolate",
                ["linear"],
                ["zoom"],
                9, 0.4,
                12, 0.7,
                15, 1.0,
            ],
            "line-opacity": 0.4,
        },
    });
}