import json
from pathlib import Path

import pytest

from topoprofile.config import load_region_config
from topoprofile.geo.models import LonLat


def test_load_region_config(
        tmp_path: Path,
) -> None:
    config_path = tmp_path / "elbrus.json"

    config_path.write_text(
        json.dumps(
            {
                "region_id": "elbrus",
                "name": "Elbrus",
                "center": {
                    "lon": 42.4361,
                    "lat": 43.3538,
                },
                "radius_km": 70,
                "terrain": {
                    "resolution": "01s",
                    "min_zoom": 8,
                    "max_zoom": 14,
                },
            }
        ),
        encoding="utf-8",
    )

    config = load_region_config(config_path)

    assert config.region_id == "elbrus"
    assert config.name == "Elbrus"
    assert config.center == LonLat(
        lon=42.4361,
        lat=43.3538,
    )
    assert config.radius_km == 70

    assert config.terrain.resolution == "01s"
    assert config.terrain.min_zoom == 8
    assert config.terrain.max_zoom == 14


def test_load_region_config_raises_if_file_missing(
        tmp_path: Path,
) -> None:
    config_path = tmp_path / "missing.json"

    with pytest.raises(
            FileNotFoundError,
            match="Region config not found",
    ):
        load_region_config(config_path)
