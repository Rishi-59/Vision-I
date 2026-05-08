"""
Scene description service.
"""

import base64

import cv2

from src.scene.describer import SceneDescriber


scene_describer = SceneDescriber(
    provider="stub",
    debug=True,
)


def run_describe(
    frame,
    mode: str = "safety"
):

    _, buffer = cv2.imencode(
        ".jpg",
        frame
    )

    image_bytes = buffer.tobytes()

    b64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    original = scene_describer._read_image_b64

    def _patched(_):
        return b64, "image/jpeg"

    scene_describer._read_image_b64 = _patched

    try:

        description = scene_describer.describe(
            "memory.jpg",
            mode
        )

    finally:

        scene_describer._read_image_b64 = original

    return description