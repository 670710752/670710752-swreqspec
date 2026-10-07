# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:40 | test: ผ่าน 5 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | ไม่มี AC | T-02 | backend/app/slots/router.py:get_slots; backend/app/slots/service.py:list_available_slots | backend/tests/test_AC_BKG_05.py: ผ่าน (p95 <= 2.0) | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 (พร้อมทำ) | ไม่มี | ไม่มี | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05 (พร้อมทำ) | ไม่มี | ไม่มี | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/router.py:create_booking; backend/app/booking/service.py:create_booking; backend/app/booking/service.py:next_queue_no | backend/tests/test_AC_BKG_01.py: ผ่าน (status 201) แต่ตรวจอ่อน | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มี | ไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 | backend/app/slots/router.py:get_slots; backend/app/slots/service.py:list_available_slots | ไม่มี | ยังไม่ถึง |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py:list_available_slots | backend/tests/test_AC_BKG_05.py: ผ่าน | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มี | ไม่มี | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มี | ไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มี | ไม่มี | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py:DATABASE_URL; backend/app/db/session.py:engine | ไม่มี | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 (พร้อมทำ) | backend/app/db/models.py:AuditLog; ไม่มี middleware หรือ route ที่บันทึก log ในทุกการเข้าถึง | ไม่มี | ยังไม่ถึง |
| IF-IDP-01 | ไม่มี AC | T-03 | backend/app/auth/idp.py:get_verified_hn | backend/tests/test_AC_BKG_01.py: ผ่าน (Authorization header ถูกตรวจ) | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 (พร้อมทำ) | ไม่มี | ไม่มี | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มี | ไม่มี | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/router.py:get_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | กำหนด 14 วัน แทน 30 วัน และไม่มี test สำหรับ 30 วัน |
| backend/app/booking/router.py:create_booking | FR-BKG-04 | ไม่ครบ | คืน queue_no เป็นค่าที่สรุปเองโดยไม่มีรูปแบบที่ Q-02 กำหนด |
| backend/app/booking/service.py:next_queue_no | FR-BKG-04, Q-02 | ไม่ครบ | ใช้รูปแบบ A001 โดยไม่รอคำตอบจากเจ้าหน้าที่เวชระเบียน |
| backend/app/booking/service.py:create_booking | FR-BKG-04 | ไม่ครบ | ลด remaining ทีละการจอง แต่ไม่มีตรวจว่ามีคิวเดิมวันเดียวกัน (FR-BKG-02) |
| backend/app/auth/idp.py:get_verified_hn | IF-IDP-01 | ใช่ | ตรวจ Authorization header แบบ Bearer verified:<HN> ตามเงื่อนไข precondition |
| backend/app/db/models.py:AuditLog | DOM-PDPA-01 | ไม่ครบ | มีตาราง audit_logs แต่ไม่มีการบันทึก log จริงทุกครั้งที่เข้าถึงข้อมูลการจอง |
| backend/app/config.py:DATABASE_URL | CON-TECH-01 | ใช่ | ระบุ PostgreSQL ในระบบจริง แต่ค่า default สำหรับ dev เป็น SQLite |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | test อ่อน | backend/tests/test_AC_BKG_01.py:test_AC_BKG_01 | AC-BKG-01 | test assert แค่ status_code == 201 ไม่ตรวจว่า queue_no ถูกแสดง และ remaining ถูกลดจาก 1 เป็น 0 ตาม Then ที่ระบุใน AC |  |
| F-002 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py:DAYS_AHEAD = 14 | FR-BKG-01 | Spec ระบุ "ภายใน 30 วันข้างหน้า" แต่โค้ดจำกัดแค่ 14 วัน จึงไม่ตรงกับข้อกำหนด |  |
| F-003 | เดา Q-xx | backend/app/booking/service.py:next_queue_no | FR-BKG-04, Q-02 | code เลือกรูปแบบ A001 และนับต่อวันใหม่ โดยไม่รอคำตอบจากเจ้าหน้าที่เวชระเบียน จึงเป็นการเดาแทนทีม |  |
| F-004 | ละเมิด Constraint / โค้ดไม่มี FR | backend/app/db/models.py:AuditLog | DOM-PDPA-01 | มีตาราง audit_logs แต่ไม่มีฟังก์ชันหรือ middleware ที่บันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลการจอง จึงไม่ทำให้ requirement เป็นจริง |  |
| F-005 | FR ไม่มี AC | specs/001-booking/spec.md | FR-BKG-01, FR-BKG-06 | มี requirement ที่เกี่ยวกับช่วงว่างและการเปลี่ยนแพ็กเกจ แต่ไม่มี AC ที่ตรวจตรงกันจริงใน test-cases.md ทำให้ย้อนกลับจาก requirement สู่ test ไม่มีรอยชัด |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
