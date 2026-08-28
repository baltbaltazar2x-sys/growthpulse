# GrowthPulse Video Stack

## Open-source components

- Wan2.1 — text-to-video / image-to-video generation
- LTX-Video / LTX-2 — video generation with audio/video capabilities
- ComfyUI — workflow orchestration for supported diffusion/video models
- LiveTalking — talking-avatar / lip-sync runtime
- MoviePy — Python video assembly and post-processing
- Shotcut — desktop editing reference/tool; not a backend dependency

## Target architecture

Base44 UI -> GrowthPulse API -> Content/Research Orchestrator

Research/insights can produce a structured video brief:
- topic
- hook
- script
- scenes
- visual prompts
- voiceover text
- captions
- aspect ratio
- duration

Generation adapters:
- Wan adapter for T2V/I2V
- LTX adapter for audio+video workflows
- ComfyUI adapter for reusable workflows
- LiveTalking adapter for avatar scenes
- MoviePy/FFmpeg adapter for assembly, captions and final export

## Runtime policy

The Git repository stores adapters, configuration and orchestration only. Large model weights are NOT committed to Git. Models should be pulled into a GPU runtime/volume during deployment.

Shotcut remains an optional desktop tool and is not required for the server pipeline.

## Environment variables

See `.env.example`. Keep secrets and provider credentials outside Git.
