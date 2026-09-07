import { MAP_CONFIG } from "../config.js";
import {
    disableTerrain,
    enableTerrain,
} from "../features/terrain.js";

function updateViewToggleButton(button, is3D) {
    const targetView = is3D ? "2D" : "3D";

    button.textContent = targetView;
    button.dataset.tooltip = `Switch to ${targetView}`;
    button.setAttribute(
        "aria-label",
        `Switch to ${targetView} view`,
    );
}

function animateView(
    map,
    targetPitch,
    targetZoom,
    duration,
) {
    const startPitch = map.getPitch();
    const pitchDifference = targetPitch - startPitch;

    const startZoom = map.getZoom();
    const zoomDifference = targetZoom - startZoom;

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

        map.setZoom(
            startZoom + zoomDifference * easedProgress,
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
            animateView(
                map,
                MAP_CONFIG.pitch,
                MAP_CONFIG.zoom,
                MAP_CONFIG.viewTransitionDuration,
            );

            disableTerrain(map);
        } else {
            enableTerrain(map);

            animateView(
                map,
                MAP_CONFIG.pitch3D,
                MAP_CONFIG.zoom3D,
                MAP_CONFIG.viewTransitionDuration,
            );
        }

        is3D = !is3D;
        updateViewToggleButton(viewToggleButton, is3D);
    });
}