/**
 * Handles images missing from the base-map style.
 */

export function setupMissingImageFallback(map) {
    map.setMissingStyleImageResolver(id => {
        if (map.hasImage(id)) {
            return;
        }

        const size = 16;
        const data = new Uint8Array(size * size * 4);

        map.addImage(id, {
            width: size,
            height: size,
            data,
        });
    });
}