import { MAP_CONFIG } from "../config.js";

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