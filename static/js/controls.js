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

function updateViewToggleButton(button, is3D) {
    const targetView = is3D ? "2D" : "3D";
    button.textContent = targetView;
    button.dataset.tooltip = `Switch to ${targetView}`;
    button.setAttribute("aria-label", `Switch to ${targetView} view`);
}

function animatePitch(map, targetPitch, duration) {
    const startPitch = map.getPitch();
    const pitchDifference = targetPitch - startPitch;
    const startTime = performance.now();

    function animate(currentTime) {
        const progress = Math.min(
            (currentTime - startTime) / duration,
            1,
        );

        const easedProgress =
            progress < 0.5
                ? 4 * progress ** 3
                : 1 - Math.pow(-2 * progress + 2, 3) / 2;

        map.setPitch(
            startPitch + pitchDifference * easedProgress,
        );

        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }

    requestAnimationFrame(animate);
}

export function setupViewToggle(map) {
    const viewToggleButton = document.getElementById("view-toggle");

    let is3D = false;

    viewToggleButton.addEventListener("click", () => {
        if (is3D) {
            animatePitch(
                map,
                MAP_CONFIG.pitch,
                MAP_CONFIG.viewTransitionDuration,
            );

            disableTerrain(map);
        } else {
            enableTerrain(map);

            animatePitch(
                map,
                MAP_CONFIG.pitch3D,
                MAP_CONFIG.viewTransitionDuration,
            );
        }

        is3D = !is3D;
        updateViewToggleButton(viewToggleButton, is3D);
    });
}