"""
Shared thread executor for AI tasks.
"""

from concurrent.futures import ThreadPoolExecutor

# =========================================================
# GLOBAL EXECUTOR
# =========================================================

executor = ThreadPoolExecutor(
    max_workers=4
)