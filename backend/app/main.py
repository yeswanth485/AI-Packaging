from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.api.auth_routes import router as auth_router
from app.api.orders_routes import router as orders_router
from app.api.prediction_routes import router as prediction_router
from app.core.database import Base, engine
from app.models import __all_models  # noqa: F401
from app.services.prediction_service import load_model

app = FastAPI(title="AI Packaging Automation Platform")


@app.on_event("startup")
def on_startup() -> None:
    # Create tables on startup (v1). Switch to Alembic later.
    Base.metadata.create_all(bind=engine)

    # Preload ML model for <200ms response target.
    # Missing model is handled at request-time too, but preloading catches it early.
    try:
        load_model()
    except FileNotFoundError:
        pass


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the AI Packaging Automation Platform API.",
        "docs": "Visit /docs for the API documentation.",
        "health": "Visit /health to check API status."
    }


@app.exception_handler(OperationalError)
def db_operational_error_handler(_, __):
    return JSONResponse(status_code=503, content={"detail": "Database connection failure"})


app.include_router(auth_router)
app.include_router(orders_router)
app.include_router(prediction_router)

