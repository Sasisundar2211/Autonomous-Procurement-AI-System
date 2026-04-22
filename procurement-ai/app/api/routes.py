from fastapi import APIRouter, File, HTTPException, UploadFile
import pandas as pd

from app.models.schema import AnalyzeResponse
from app.services.agent_controller import run_pipeline

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...)) -> AnalyzeResponse:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    try:
        df = pd.read_csv(file.file)
        result = run_pipeline(df)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Failed to analyze vendor data: {exc}") from exc

    return AnalyzeResponse(**result)
