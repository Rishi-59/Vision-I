"""
Description route.
"""

from fastapi import APIRouter

from src.api.models.schemas import (
    DescribeRequest,
    DescribeResponse,
)
from src.services.describe_service import (
    run_describe,
)
from src.services.frame_processor import (
    decode_base64_frame,
)

router = APIRouter()


@router.post(
    "/describe",
    response_model=DescribeResponse,
)
async def describe(
    request: DescribeRequest
):

    frame = decode_base64_frame(
        request.frame_b64
    )

    description = run_describe(
        frame=frame,
        mode=request.mode,
    )

    return DescribeResponse(
        description=description,
        mode=request.mode,
    )