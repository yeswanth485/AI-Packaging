from __future__ import annotations


def validate_positive_dimensions(*, length: float, width: float, height: float, weight: float) -> None:
    if length <= 0 or width <= 0 or height <= 0 or weight <= 0:
        raise ValueError("Invalid inputs: length/width/height/weight must be > 0")

