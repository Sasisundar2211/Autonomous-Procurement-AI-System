from fastapi import APIRouter, File, HTTPException, UploadFile
import pandas as pd

from app.models.schema import AnalyzeResponse
from app.services.llm import generate_explanation
from app.services.scoring import rank_vendors
from app.utils.preprocess import preprocess_vendor_data

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...)) -> AnalyzeResponse:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file")

    try:
        df = pd.read_csv(file.file)
        cleaned = preprocess_vendor_data(df)
        ranked = rank_vendors(cleaned)

        top = ranked.iloc[0]
        explanation = generate_explanation(top["vendor"], top)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Failed to analyze vendor data: {exc}") from exc

    return AnalyzeResponse(
        top_vendor=str(top["vendor"]),
        ranking=ranked.to_dict(orient="records"),
        explanation=explanation,
    )
