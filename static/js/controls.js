import { MAP_CONFIG } from "./config.js";
import {
    disableTerrain,
    enableTerrain,
} from "./terrain.js";

export function setupNavigationControls(map) {
    const resetNorthButton = document.getElementById("reset-north");

    const rotateLeftButton = document.getElementById("rotate-left");
    const rotateRightButton = document.getElementById("rotate-right");

    const tiltUpButton = document.getElementById("tilt-up");
    const tiltDownButton = document.getElementById("tilt-down");

    const zoomInButton = document.getElementById("zoom-in");
    const zoomOutButton = document.getElementById("zoom-out");

    resetNorthButton.addEventListener("click", () => {
        map.resetNorth();
    });

    rotateLeftButton.addEventListener("click", () => {
        map.easeTo({
            bearing: map.getBearing() - MAP_CONFIG.rotationStep,
        });
    });

    rotateRightButton.addEventListener("click", () => {
        map.easeTo({
            bearing: map.getBearing() + MAP_CONFIG.rotationStep,
        });
    });

    tiltUpButton.addEventListener("click", () => {
        map.easeTo({
            pitch: Math.min(
                map.getPitch() + MAP_CONFIG.pitchStep,
                MAP_CONFIG.maxPitch,
            ),
        });
    });

    tiltDownButton.addEventListener("click", () => {
        map.easeTo({
            pitch: Math.max(
                map.getPitch() - MAP_CONFIG.pitchStep,
                MAP_CONFIG.minPitch,
            ),
        });
    });

    zoomInButton.addEventListener("click", () => {
        map.zoomIn();
    });

    zoomOutButton.addEventListener("click", () => {
        map.zoomOut();
    });
}

export function setupViewToggle(map) {
    const viewToggleButton = document.getElementById("view-toggle");

    let is3D = false;

    viewToggleButton.addEventListener("click", () => {
        if (is3D) {
            disableTerrain(map);

            map.easeTo({
                pitch: MAP_CONFIG.pitch,
            });

            viewToggleButton.textContent = "3D";
            viewToggleButton.dataset.tooltip = "Switch to 3D";
            viewToggleButton.setAttribute(
                "aria-label",
                "Switch to 3D view",
            );
        } else {
            enableTerrain(map);

            map.easeTo({
                pitch: MAP_CONFIG.pitch3D,
            });

            viewToggleButton.textContent = "2D";
            viewToggleButton.dataset.tooltip = "Switch to 2D";
            viewToggleButton.setAttribute(
                "aria-label",
                "Switch to 2D view",
            );
        }

        is3D = !is3D;
    });
}