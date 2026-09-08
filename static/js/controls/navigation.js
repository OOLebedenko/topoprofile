import {
    getCameraConfig,
} from "../viewport.js";

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
        const cameraConfig = getCameraConfig();

        map.easeTo({
            bearing: (
                map.getBearing()
                - cameraConfig.rotationStep
            ),
        });
    });

    rotateRightButton.addEventListener("click", () => {
        const cameraConfig = getCameraConfig();

        map.easeTo({
            bearing: (
                map.getBearing()
                + cameraConfig.rotationStep
            ),
        });
    });

    tiltUpButton.addEventListener("click", () => {
        const cameraConfig = getCameraConfig();

        map.easeTo({
            pitch: Math.min(
                map.getPitch() + cameraConfig.pitchStep,
                cameraConfig.maxPitch,
            ),
        });
    });

    tiltDownButton.addEventListener("click", () => {
        const cameraConfig = getCameraConfig();

        map.easeTo({
            pitch: Math.max(
                map.getPitch() - cameraConfig.pitchStep,
                cameraConfig.minPitch,
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