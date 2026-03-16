from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order_model import Order
from app.models.user_model import User
from app.utils.validators import validate_positive_dimensions


def create_order(*, db: Session, user: User, data: dict) -> Order:
    try:
        validate_positive_dimensions(
            length=float(data["length"]),
            width=float(data["width"]),
            height=float(data["height"]),
            weight=float(data["weight"]),
        )
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    order = Order(user_id=user.id, **data)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_orders(*, db: Session, user: User) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user.id).order_by(Order.id.desc()).all()


def get_order_for_user(*, db: Session, user: User, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

