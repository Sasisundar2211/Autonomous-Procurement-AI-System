from typing import Any

from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    top_vendor: str
    ranking: list[dict[str, Any]]
    explanation: str
