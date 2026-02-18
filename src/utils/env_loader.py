"""
Minimal .env loader for local development.
"""

from __future__ import annotations

import os
from pathlib import Path


def load_env(path: str | Path = ".env", verbose: bool = False) -> None:
    env_path = Path(path)
    if not env_path.exists():
        if verbose:
            print(f"[ENV] .env not found at: {env_path.resolve()}")
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        current = os.environ.get(key)
        if current:
            continue
        os.environ[key] = value

    if verbose:
        resolved = env_path.resolve()
        key_state = "SET" if os.environ.get("GEMINI_API_KEY") else "MISSING"
        print(f"[ENV] Loaded .env from: {resolved}")
        print(f"[ENV] GEMINI_API_KEY is {key_state}")
