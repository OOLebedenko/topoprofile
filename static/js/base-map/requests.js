const OPENFREEMAP_URL = "https://tiles.openfreemap.org/";

const PROXY_HOSTS = new Set([
    "topoprofile.org",
    "www.topoprofile.org",
]);

// Rewrites OpenFreeMap requests through Nginx in production.
export function transformBaseMapRequest(url) {
    if (
        PROXY_HOSTS.has(window.location.hostname)
        && url.startsWith(OPENFREEMAP_URL)
    ) {
        const path = url.slice(OPENFREEMAP_URL.length);

        return {
            url: `${window.location.origin}/openfreemap/${path}`,
        };
    }

    return { url };
}