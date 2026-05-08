"""
Optimized detection route.
"""

import asyncio

from fastapi import APIRouter

from src.api.models.schemas import (
    DetectResponse,
    DetectedObject,
    FrameRequest,
)
from src.services.detection_service import (
    run_detection,
)
from src.services.executor import (
    executor,
)
from src.services.frame_processor import (
    decode_base64_frame,
)

router = APIRouter()


@router.post(
    "/detect",
    response_model=DetectResponse,
)
async def detect(
    request: FrameRequest
):

    frame = decode_base64_frame(
        request.frame_b64
    )

    loop = asyncio.get_running_loop()

    result = await loop.run_in_executor(
        executor,
        lambda: run_detection(
            frame=frame,
            frame_width=request.frame_width,
        )
    )

    objects = [
        DetectedObject(**obj)
        for obj in result["detections"]
    ]

    return DetectResponse(
        objects=objects,
        object_count=len(objects),
        scene_context=result["scene_context"],
    )