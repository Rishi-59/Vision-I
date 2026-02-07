"""
Scene capture utilities for on-demand scene descriptions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import cv2


@dataclass
class SceneCapture: # type: ignore
    cache_dir: Path

    def ensure_cache_dir(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def capture(self, frame) -> Optional[Path]:
        if frame is None:
            return None

        self.ensure_cache_dir()
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        image_path = self.cache_dir / f"scene_{timestamp}.jpg"

        saved = cv2.imwrite(str(image_path), frame)
        if not saved:
            return None

        return image_path
