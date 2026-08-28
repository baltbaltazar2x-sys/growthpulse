from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.video import VideoBrief, VideoOrchestrator

router = APIRouter(prefix="/v1/video", tags=["video"])
service = VideoOrchestrator()


class VideoPlanRequest(BaseModel):
    topic: str
    script: str
    visual_prompts: list[str] = Field(default_factory=list)
    duration_seconds: int = 30
    aspect_ratio: str = "9:16"


@router.get("/status")
def video_status():
    return service.status()


@router.post("/plan")
def video_plan(request: VideoPlanRequest):
    return service.plan(VideoBrief(**request.model_dump()))
