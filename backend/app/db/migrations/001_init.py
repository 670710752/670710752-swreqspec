from sqlalchemy import MetaData

from app.db.models import AuditLog, Base, Booking, Slot


def upgrade(engine):
    """รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01"""
    metadata = MetaData()
    metadata.reflect(bind=engine)
    Base.metadata.create_all(bind=engine)


def downgrade(engine):
    """ลบตารางทั้งหมดเมื่อ rollback migration"""
    Base.metadata.drop_all(bind=engine)
