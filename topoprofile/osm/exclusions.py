import json
from pathlib import Path

type OSMFeatureKey = tuple[str, str]


def load_hiking_exclusions(
        path: Path,
) -> frozenset[OSMFeatureKey]:
    """Load manually excluded hiking features."""
    with path.open(
            encoding="utf-8",
    ) as file:
        data = json.load(file)

    return frozenset(
        (
            str(item["osm_type"]),
            str(item["osm_id"]),
        )
        for item in data["excluded"]
    )
