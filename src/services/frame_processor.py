"""
Frame processing utilities.
"""

import base64

import cv2
import numpy as np


def decode_base64_frame(b64_string: str):

    image_bytes = base64.b64decode(b64_string)

    np_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    frame = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if frame is None:
        raise ValueError(
            "Invalid image frame"
        )

    return frame