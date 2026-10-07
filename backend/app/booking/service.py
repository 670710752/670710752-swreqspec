# บันทึกการจองและตัดที่นั่ง (T-03)
# รองรับ FR-BKG-04
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import AuditLog, Booking, Slot


class SlotFullError(Exception):
    """ช่วงเวลาที่เลือกไม่มีที่นั่งเหลือแล้ว"""


def next_queue_no(db: Session, slot_date) -> str:
    """ออกหมายเลขคิวที่เป็นตัวแทนจริงของการจอง และไม่สมมติรูปแบบโรงพยาบาลจนกว่าจะมีคำตอบ Q-02"""
    latest = db.scalar(select(func.max(Booking.id)))
    return f"Q-{(latest or 0) + 1:04d}"


def record_booking_access(db: Session, actor_id: str, hn: str) -> None:
    """บันทึก audit log เมื่อมีการเข้าถึงข้อมูลการจอง"""
    db.add(AuditLog(actor_id=actor_id, action="READ_BOOKING", hn=hn))
    db.commit()


def get_booking(db: Session, booking_id: int, hn: str) -> Booking:
    """อ่านข้อมูลการจองของผู้รับบริการที่ยืนยันตัวตนแล้ว"""
    booking = db.get(Booking, booking_id)
    if booking is None or booking.hn != hn:
        raise ValueError("ไม่พบการจอง")
    return booking


def create_booking(db: Session, hn: str, slot_id: int) -> Booking:
    """ยืนยันการจอง: ตรวจที่นั่ง ตัดที่นั่ง บันทึกการจอง ออกหมายเลขคิว (FR-BKG-04)"""
    slot = db.get(Slot, slot_id)
    if slot is None:
        raise ValueError("ไม่พบช่วงเวลา")
    if slot.remaining <= 0:
        raise SlotFullError(slot_id)

    slot.remaining -= 1
    booking = Booking(
        hn=hn,
        slot_id=slot.id,
        booking_date=slot.slot_date,
        queue_no=next_queue_no(db, slot.slot_date),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
