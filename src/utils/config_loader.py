"""
Configuration loader for Vision I.
"""

import yaml
from pathlib import Path


class Config:
    def __init__(self, path="config/config.yaml"):
        config_path = Path(path)

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(config_path, "r") as f:
            self.data = yaml.safe_load(f)

    def get(self, *keys, default=None):
        value = self.data
        for key in keys:
            value = value.get(key, {})
        return value if value else default
