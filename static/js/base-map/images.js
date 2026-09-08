/**
 * Handles missing images in the external base-map style.
 */

// Registers a transparent fallback for missing base-map icons.
export function setupMissingImageFallback(map) {
    map.on("styleimagemissing", event => {
        const imageId = event.id;

        if (map.hasImage(imageId)) {
            return;
        }

        const size = 16;
        const data = new Uint8Array(size * size * 4);

        map.addImage(imageId, {
            width: size,
            height: size,
            data,
        });
    });
}