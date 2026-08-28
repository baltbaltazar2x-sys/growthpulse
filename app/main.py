from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from app.services.research import ResearchService

app = FastAPI(title="GrowthPulse", version="0.1.0")
research = ResearchService()


class ResearchRequest(BaseModel):
    url: HttpUrl
    query: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "growthpulse"}


@app.post("/v1/research")
def run_research(request: ResearchRequest):
    try:
        return research.run(str(request.url), request.query)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
