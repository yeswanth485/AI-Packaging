from __future__ import annotations

import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Tuple

import joblib
import numpy as np
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.order_model import Order
from app.models.packaging_result_model import PackagingResult
from app.models.user_model import User
from app.utils.validators import validate_positive_dimensions


# Example internal box volume map for efficiency scoring.
# Replace/extend with your real box catalog later (or store in DB).
BOX_CATALOG: Dict[str, Tuple[float, float, float]] = {
    "Box_A": (20.0, 15.0, 10.0),
    "Box_B": (30.0, 20.0, 10.0),
    "Box_C": (40.0, 30.0, 20.0),
}


def _volume(l: float, w: float, h: float) -> float:
    return l * w * h


@lru_cache(maxsize=1)
def load_model() -> Any:
    model_path = Path(settings.ml_model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Missing ML model: {model_path}")
    return joblib.load(model_path)


def _predict(model: Any, features: np.ndarray) -> Tuple[str, float]:
    pred = model.predict(features)[0]
    recommended = str(pred)

    confidence = 1.0
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        confidence = float(np.max(proba))

    return recommended, confidence


def predict_packaging(
    *,
    db: Session,
    user: User,
    length: float,
    width: float,
    height: float,
    weight: float,
) -> PackagingResult:
    """
    End-to-end prediction flow used by the API:
    1) validate inputs
    2) calculate product volume
    3) run ML prediction
    4) calculate packaging efficiency
    5) create an Order (quantity=1) for traceability
    6) store PackagingResult linked to that order
    """
    try:
        validate_positive_dimensions(
            length=float(length),
            width=float(width),
            height=float(height),
            weight=float(weight),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    try:
        model = load_model()
    except FileNotFoundError as e:
        # Surface as API error with clear message
        raise HTTPException(status_code=500, detail=str(e)) from e

    start = time.perf_counter()

    features = np.array([[length, width, height, weight, 1.0]], dtype=float)
    recommended_box, confidence = _predict(model, features)

    product_volume = _volume(length, width, height)
    dims = BOX_CATALOG.get(recommended_box)
    if dims:
        box_volume = _volume(*dims)
        efficiency = max(0.0, min(1.0, product_volume / box_volume)) if box_volume > 0 else 0.0
    else:
        efficiency = 0.0

    elapsed_ms = (time.perf_counter() - start) * 1000.0
    if elapsed_ms > 200.0:
        # Not fatal; could log for monitoring.
        pass

    # Create a lightweight Order record to maintain the schema requirement
    order = Order(
        user_id=user.id,
        product_name="Ad-hoc prediction",
        length=length,
        width=width,
        height=height,
        weight=weight,
        quantity=1,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    result = PackagingResult(
        order_id=order.id,
        recommended_box=recommended_box,
        confidence_score=confidence,
        efficiency_score=efficiency,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

