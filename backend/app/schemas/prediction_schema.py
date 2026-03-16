from __future__ import annotations

from pydantic import BaseModel, PositiveFloat


class PredictionRequest(BaseModel):
    length: PositiveFloat
    width: PositiveFloat
    height: PositiveFloat
    weight: PositiveFloat


class PredictionResponse(BaseModel):
    recommended_box: str
    confidence_score: float
    efficiency_score: float

