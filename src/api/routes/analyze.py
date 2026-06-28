"""
Optimized full pipeline route.
"""

import asyncio

from fastapi import APIRouter

from src.api.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    DetectedObject,
)
from src.services.decision_service import (
    run_decision,
)
from src.services.describe_service import (
    run_describe,
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
    "/analyze",
    response_model=AnalyzeResponse,
)
async def analyze(
    request: AnalyzeRequest
):

    frame = decode_base64_frame(
        request.frame_b64
    )

    loop = asyncio.get_running_loop()

    # =====================================================
    # DETECTION
    # =====================================================

    detection_result = await loop.run_in_executor(
        executor,
        lambda: run_detection(
            frame=frame,
            frame_width=request.frame_width,
        )
    )

    # =====================================================
    # DECISION
    # =====================================================

    decision_task = loop.run_in_executor(
        executor,
        lambda: run_decision(
            detections=detection_result["detections"],
            frame_width=request.frame_width,
            user_mode=request.user_mode,
        )
    )

    # =====================================================
    # DESCRIPTION
    # =====================================================

    description_task = None

    if request.include_description:

        description_task = loop.run_in_executor(
            executor,
            lambda: run_describe(
                frame=frame,
                mode=request.describe_mode,
            )
        )

    # =====================================================
    # WAIT FOR TASKS
    # =====================================================

    decision_result = await decision_task

    description = None

    if description_task:

        description = await description_task

    objects = [
        DetectedObject(**obj)
        for obj in detection_result["detections"]
    ]

    return AnalyzeResponse(
        objects=objects,
        object_count=len(objects),
        scene_context=detection_result["scene_context"],
        guidance=decision_result["guidance"],
        severity=decision_result["severity"],
        speak=decision_result["speak"],
        description=description,
    )