from __future__ import annotations

from typing import List, Literal, Optional, Tuple

from pydantic import BaseModel, Field


# =========================================================
# REQUEST MODELS
# =========================================================

class FrameRequest(BaseModel):

    frame_b64: str = Field(
        ...,
        description="Base64 encoded image frame"
    )

    user_mode: Literal[
        "cautious",
        "normal",
        "fast"
    ] = "normal"

    frame_width: int = 640


class DescribeRequest(FrameRequest):

    mode: Literal[
        "safety",
        "awareness",
        "companion"
    ] = "safety"


class AnalyzeRequest(FrameRequest):

    include_description: bool = False

    describe_mode: Literal[
        "safety",
        "awareness",
        "companion"
    ] = "safety"


# =========================================================
# RESPONSE MODELS
# =========================================================

class DetectedObject(BaseModel):

    label: str

    confidence: float

    bbox: Tuple[float, float, float, float]

    distance: Optional[float] = None

    direction: Optional[str] = None

    motion: Optional[str] = None


class DetectResponse(BaseModel):

    objects: List[DetectedObject]

    object_count: int

    scene_context: str


class DecisionResponse(BaseModel):

    guidance: Optional[str]

    severity: str

    scene_context: str

    speak: bool


class DescribeResponse(BaseModel):

    description: str

    mode: str


class AnalyzeResponse(BaseModel):

    objects: List[DetectedObject]

    object_count: int

    scene_context: str

    guidance: Optional[str]

    severity: str

    speak: bool

    description: Optional[str] = None