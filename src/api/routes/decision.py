"""
Optimized decision route.
"""

import asyncio

from fastapi import APIRouter

from src.api.models.schemas import (
    DecisionResponse,
    FrameRequest,
)
from src.services.decision_service import (
    run_decision,
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
    "/decision",
    response_model=DecisionResponse,
)
async def decision(
    request: FrameRequest
):

    frame = decode_base64_frame(
        request.frame_b64
    )

    loop = asyncio.get_running_loop()

    detection_result = await loop.run_in_executor(
        executor,
        lambda: run_detection(
            frame=frame,
            frame_width=request.frame_width,
        )
    )

    decision_result = await loop.run_in_executor(
        executor,
        lambda: run_decision(
            detections=detection_result["detections"],
            frame_width=request.frame_width,
            user_mode=request.user_mode,
        )
    )

    return DecisionResponse(
        guidance=decision_result["guidance"],
        severity=decision_result["severity"],
        scene_context=detection_result["scene_context"],
        speak=decision_result["speak"],
    )