const TERRAIN_REGION = {
    id: "elbrus",
    center: [42.4361, 43.3538],
    bounds: [
        41.5706944,
        42.7206944,
        43.3001389,
        43.9876389,
    ],
    dataPath: "../data/regions/elbrus",
};

export const MAP_CONFIG = {
    style: "https://tiles.openfreemap.org/styles/liberty",
    center: TERRAIN_REGION.center,
    zoom: 10,
    minPitch: 0,
    maxPitch: 85,
    pitchStep: 10,
    pitch: 0,
    pitch3D: 60,
    rotationStep: 20,
    viewTransitionDuration: 1000,
};

export const TERRAIN_CONFIG = {
    tiles: [
        `${TERRAIN_REGION.dataPath}/tiles/terrain/{z}/{x}/{y}.png`,
    ],
    minZoom: 8,
    maxZoom: 14,
    tileSize: 256,
    encoding: "terrarium",
    bounds: TERRAIN_REGION.bounds,
};

export const ATMOSPHERE_CONFIG = {
    skyColor: "#88c6fc",
    horizonColor: "#ffffff",
    fogColor: "#ffffff",
    skyHorizonBlend: 0.8,
    horizonFogBlend: 0.8,
    fogGroundBlend: 0.5,
};