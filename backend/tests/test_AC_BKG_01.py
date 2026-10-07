# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่ จองแล้วต้องบันทึกและลดที่นั่ง"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    payload = res.json()
    assert payload["booking_id"]
    assert payload["queue_no"]
    assert payload["slot_id"] == slot.id

    slot_after = client.get("/slots", params={"package_code": "BASIC"}, headers=AUTH)
    assert slot_after.status_code == 200
    items = slot_after.json()
    target = next(item for item in items if item["slot_id"] == slot.id)
    assert target["remaining"] == 0
