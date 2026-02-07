"""
Scene description stub for Vision I.

This module will later integrate with a vision API.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SceneDescriber:
    def describe(self, image_path: str, mode: str) -> str:
        mode = mode.lower()
        if mode == "safety":
            return "Safety check complete. No immediate hazards detected."
        if mode == "awareness":
            return "You are in an open area with clear space ahead."
        if mode == "companion":
            return "It feels calm and open around you, with a quiet atmosphere."

        return "Scene description mode not recognized."
