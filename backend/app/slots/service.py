from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Slot


def list_available_slots(session: Session, package_code: str | None = None, date_from: date | None = None):
    """รองรับ FR-BKG-01 และ FR-BKG-06: คืนช่วงเวลาว่างภายใน 30 วันพร้อมจำนวนที่นั่งคงเหลือ"""
    if date_from is None:
        date_from = date.today()

    date_to = date_from + timedelta(days=30)
    query = select(Slot).where(Slot.slot_date >= date_from, Slot.slot_date <= date_to)

    if package_code:
        query = query.where(Slot.package_code == package_code)

    rows = session.execute(query).scalars().all()
    rows = sorted(rows, key=lambda item: (item.slot_date, item.start_time, item.package_code))

    return [
        {
            "id": row.id,
            "slot_date": row.slot_date.isoformat(),
            "start_time": row.start_time.isoformat(),
            "package_code": row.package_code,
            "capacity": row.capacity,
            "remaining": row.remaining,
        }
        for row in rows
        if row.remaining > 0
    ]
