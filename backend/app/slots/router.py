from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.idp import require_verified_identity
from app.db.session import create_session_factory
from app.slots.service import list_available_slots

router = APIRouter(tags=["slots"])
SessionLocal = create_session_factory()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/slots", dependencies=[Depends(require_verified_identity)])
@router.get("/api/slots", dependencies=[Depends(require_verified_identity)])
def read_slots(
    date_from: date | None = Query(default=None),
    package_code: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """รองรับ FR-BKG-01 และ IF-IDP-01"""
    items = list_available_slots(db, package_code=package_code, date_from=date_from)
    return {"items": items, "count": len(items)}
