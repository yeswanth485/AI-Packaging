from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class OrderCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=255)
    length: PositiveFloat
    width: PositiveFloat
    height: PositiveFloat
    weight: PositiveFloat
    quantity: PositiveInt


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_name: str
    length: float
    width: float
    height: float
    weight: float
    quantity: int
    created_at: datetime

