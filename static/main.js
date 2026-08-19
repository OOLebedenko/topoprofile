const map = new maplibregl.Map({
    container: "map",

    style: {
        version: 8,
        sources: {},
        layers: [
            {
                id: "background",
                type: "background",
                paint: {
                    "background-color": "#e8edf2",
                },
            },
        ],
    },

    center: [0, 0],
    zoom: 1,
});