/**
 * Configures sky and fog for the 3D map view.
 */

import { ATMOSPHERE_CONFIG } from "../config.js";

// Applies atmospheric sky and fog settings to the map.
export function addAtmosphere(map) {
    map.setSky({
        "sky-color": ATMOSPHERE_CONFIG.skyColor,
        "horizon-color": ATMOSPHERE_CONFIG.horizonColor,
        "fog-color": ATMOSPHERE_CONFIG.fogColor,
        "sky-horizon-blend": ATMOSPHERE_CONFIG.skyHorizonBlend,
        "horizon-fog-blend": ATMOSPHERE_CONFIG.horizonFogBlend,
        "fog-ground-blend": ATMOSPHERE_CONFIG.fogGroundBlend,
    });
}