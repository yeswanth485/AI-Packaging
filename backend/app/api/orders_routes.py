from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User
from app.schemas.order_schema import OrderCreate, OrderOut
from app.services.order_service import create_order, list_orders

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut)
def create_order_endpoint(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OrderOut:
    order = create_order(db=db, user=user, data=payload.model_dump())
    return OrderOut.model_validate(order, from_attributes=True)


@router.get("", response_model=list[OrderOut])
def list_orders_endpoint(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[OrderOut]:
    orders = list_orders(db=db, user=user)
    return [OrderOut.model_validate(o, from_attributes=True) for o in orders]

