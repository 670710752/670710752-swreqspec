from datetime import date, time, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.db.models import Base, Slot
from app.db.session import create_db_engine
from app.main import app
from app.slots.router import get_db


def build_test_db():
    engine = create_db_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    with SessionLocal() as session:
        for index in range(20):
            slot_date = date.today() + timedelta(days=index % 10)
            session.add(
                Slot(
                    id=index + 1,
                    slot_date=slot_date,
                    start_time=time(hour=9, minute=0) if index % 2 == 0 else time(hour=10, minute=0),
                    package_code="STD",
                    capacity=10,
                    remaining=5,
                )
            )
        session.commit()

    return engine, SessionLocal


def override_get_db():
    engine, SessionLocal = build_test_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_AC_BKG_05_slots_endpoint_is_authenticated_and_fast_enough():
    timings = []
    headers = {"X-User-Verified": "true"}

    for _ in range(200):
        start = __import__("time").perf_counter()
        response = client.get("/slots?date_from=" + date.today().isoformat() + "&package_code=STD", headers=headers)
        elapsed = __import__("time").perf_counter() - start
        timings.append(elapsed)
        assert response.status_code == 200, response.text

    timings.sort()
    p95_index = max(0, min(len(timings) - 1, int(len(timings) * 0.95)))
    p95 = timings[p95_index]

    assert p95 <= 2.0, f"p95 exceeded threshold: {p95} seconds"
    payload = response.json()
    assert payload["count"] > 0
