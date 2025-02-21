from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..core.detector import Detector

app = FastAPI(title="VerifiedX API")
detector = Detector()

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    result: str

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest) -> AnalysisResponse:
    try:
        result = await detector.analyze(request.text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 