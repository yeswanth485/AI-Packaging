from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User
from app.schemas.prediction_schema import PredictionRequest, PredictionResponse
from app.services.prediction_service import predict_packaging

router = APIRouter(tags=["prediction"])


@router.post("/predict-packaging", response_model=PredictionResponse)
def predict_packaging_endpoint(
    payload: PredictionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PredictionResponse:
    result = predict_packaging(
        db=db,
        user=user,
        length=payload.length,
        width=payload.width,
        height=payload.height,
        weight=payload.weight,
    )
    return PredictionResponse(
        recommended_box=result.recommended_box,
        confidence_score=result.confidence_score,
        efficiency_score=result.efficiency_score,
    )

