from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, PositiveFloat, NonNegativeFloat, PositiveInt


class ItemIn(BaseModel):
    sku: str = Field(min_length=1)
    qty: PositiveInt
    length: PositiveFloat
    width: PositiveFloat
    height: PositiveFloat
    weight: NonNegativeFloat = 0.0


class BoxTypeIn(BaseModel):
    code: str = Field(min_length=1)
    inner_length: PositiveFloat
    inner_width: PositiveFloat
    inner_height: PositiveFloat
    max_weight: NonNegativeFloat = 0.0


class OptimizeRequest(BaseModel):
    items: List[ItemIn] = Field(default_factory=list)
    box_types: List[BoxTypeIn] = Field(default_factory=list)


class PackedItemOut(BaseModel):
    sku: str
    length: float
    width: float
    height: float
    weight: float


class PackedBoxOut(BaseModel):
    box_code: str
    inner_length: float
    inner_width: float
    inner_height: float
    items: List[PackedItemOut]


class OptimizeResponse(BaseModel):
    boxes: List[PackedBoxOut]
    errors: List[str] = Field(default_factory=list)


class OptimizationRunOut(BaseModel):
    id: int
    created_at: str
    request_json: dict
    response_json: dict

