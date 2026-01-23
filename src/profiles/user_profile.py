"""
User profile management for Vision I.
"""

import yaml
from pathlib import Path


class UserProfile:
    def __init__(self, config_path="config/user_profile.yaml"):
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"User profile config not found: {config_path}")

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        profile_name = data.get("profile", "normal")
        profiles = data.get("profiles", {})

        self.profile = profiles.get(profile_name, profiles.get("normal", {}))
        self.name = profile_name

    def cooldown(self):
        return self.profile.get("cooldown_seconds", 3.0)

    def center_offset(self):
        return self.profile.get("center_distance_offset", 0.0)

    def side_offset(self):
        return self.profile.get("side_distance_offset", 0.0)

    def verbosity(self):
        return self.profile.get("verbosity", "medium")
