from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any


@dataclass
class VideoBrief:
    topic: str
    script: str
    visual_prompts: list[str]
    duration_seconds: int = 30
    aspect_ratio: str = "9:16"


class VideoOrchestrator:
    """Provider-neutral video orchestration layer.

    Heavy model runtimes stay outside the GrowthPulse process. Adapters can be
    connected to ComfyUI, Wan, LTX or LiveTalking through their deployed APIs.
    """

    def __init__(self) -> None:
        self.comfyui_url = os.getenv("COMFYUI_URL", "").rstrip("/")
        self.wan_url = os.getenv("WAN_URL", "").rstrip("/")
        self.ltx_url = os.getenv("LTX_URL", "").rstrip("/")
        self.livetalking_url = os.getenv("LIVETALKING_URL", "").rstrip("/")

    def status(self) -> dict[str, Any]:
        return {
            "comfyui": bool(self.comfyui_url),
            "wan": bool(self.wan_url),
            "ltx": bool(self.ltx_url),
            "livetalking": bool(self.livetalking_url),
            "assembly": "moviepy/ffmpeg",
        }

    def plan(self, brief: VideoBrief) -> dict[str, Any]:
        return {
            "status": "planned",
            "brief": {
                "topic": brief.topic,
                "script": brief.script,
                "visual_prompts": brief.visual_prompts,
                "duration_seconds": brief.duration_seconds,
                "aspect_ratio": brief.aspect_ratio,
            },
            "steps": [
                "generate_visuals",
                "generate_voice_or_audio",
                "optional_avatar",
                "assemble",
                "captions",
                "export",
            ],
            "runtime": self.status(),
        }
