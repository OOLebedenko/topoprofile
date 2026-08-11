import json
from pathlib import Path
from typing import Any


def load_region_config(config_path: Path) -> dict[str, Any]:
    """Load region configuration from a JSON file."""
    if not config_path.is_file():
        raise FileNotFoundError(f"Region config not found: {config_path}")

    with config_path.open(encoding="utf-8") as file:
        return json.load(file)
