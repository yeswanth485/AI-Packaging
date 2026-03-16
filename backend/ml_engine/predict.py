from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np

from app.core.config import settings
from app.utils.validators import validate_positive_dimensions


@lru_cache(maxsize=1)
def _load_model():
    """
    Load the trained model from packaging_model.pkl (or path from settings).
    Cached in memory for fast predictions.
    """
    model_path = Path(settings.ml_model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Missing ML model: {model_path}")
    return joblib.load(model_path)


def predict_packaging(length: float, width: float, height: float, weight: float) -> Tuple[str, float]:
    """
    Validate inputs and run model prediction.

    Returns:
        recommended_box (str)
        confidence_score (float)
    """
    validate_positive_dimensions(length=length, width=width, height=height, weight=weight)

    model = _load_model()

    features = np.array([[length, width, height, weight]], dtype=float)
    pred = model.predict(features)[0]
    recommended_box = str(pred)

    confidence = 1.0
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        confidence = float(np.max(proba))

    return recommended_box, confidence

