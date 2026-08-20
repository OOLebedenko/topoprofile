export function setupNavigationControls(map) {
    const zoomInButton = document.getElementById("zoom-in");
    const zoomOutButton = document.getElementById("zoom-out");
    const resetNorthButton = document.getElementById("reset-north");

    zoomInButton.addEventListener("click", () => {
        map.zoomIn();
    });

    zoomOutButton.addEventListener("click", () => {
        map.zoomOut();
    });

    resetNorthButton.addEventListener("click", () => {
        map.resetNorth();
    });
}