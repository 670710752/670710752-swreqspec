# Plan: จองคิวตรวจสุขภาพ

## 1. สรุปแนวทาง
- ฟีเจอร์นี้ให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ เพื่อรับหมายเลขคิว และยืนยันการจองผ่านระบบแจ้งเตือน ตาม FR-BKG-01 ถึง FR-BKG-06
- ผู้ใช้หลักคือ ผู้รับบริการที่มีสถานะยืนยันตัวตนแล้ว และทีมงานที่ดูแลช่องทางแจ้งเตือน/เวชระเบียนตาม IF-IDP-01 และ IF-HIS-01
- แนวทางคือแยกการค้นหาช่วงว่าง การป้องกันการจองซ้ำ การยืนยันการจอง และการจัดการส่งข้อความยืนยันแบบ asynchronous ให้แยกชัดเพื่อให้ระบบยังคงบันทึก booking แม้ส่งข้อความไม่สำเร็จ
- การออกแบบจะใช้ข้อมูล booking แบบอ้างอิง HN และไม่เก็บเลขบัตรประชาชนเพื่อให้ตรงตาม IF-HIS-01 และ DOM-PDPA-01
- การตรวจสอบความสมบูรณ์จะอาศัย AC-BKG-01 ถึง AC-BKG-06 เป็นเกณฑ์หลัก โดยเน้นการทดสอบ concurrency, retry queue และ audit log

## 2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| MySQL | CON-TECH-01 | ใช้เป็นฐานข้อมูลหลักสำหรับข้อมูลการจองและ audit log |
| React (Vite) | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับหน้าเลือกแพ็กเกจ/วัน/ช่วงเวลา และผลลัพธ์การจอง |
| Python FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับ REST API สำหรับค้นหาช่วงว่างและยืนยันการจอง |
| ระบบแจ้งเตือนแบบ asynchronous (SMS/LINE) | IF-NOT-01 | การจองต้องไม่รอผลการส่งข้อความ และต้องมีสถานะ retry queue |
| Audit log | DOM-PDPA-01 | บันทึกผู้เข้าถึง เวลา และรหัสผู้รับบริการอย่างน้อย 1 ปี |
| HN เป็นข้อมูลอ้างอิงผู้รับบริการ | IF-HIS-01 | ไม่เก็บเลขบัตรประชาชนในตารางการจอง |
| ผู้ยืนยันตัวตนภายนอก | IF-IDP-01 | ต้องมีผลยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ |

## 3. โมเดลข้อมูล

| Entity | ฟิลด์หลัก | รองรับ FR/Constraint |
|---|---|---|
| PatientProfile | patient_id, hn, verified_at, status | รองรับ IF-IDP-01, IF-HIS-01; ไม่เก็บเลขบัตรประชาชนในตารางการจอง |
| Booking | booking_id, hn, package_id, booking_date, slot_id, status, queue_number, created_at, confirmed_at, last_updated_at | รองรับ FR-BKG-02, FR-BKG-04, FR-BKG-05, DOM-PDPA-01 |
| BookingSlot | slot_id, date, start_time, end_time, capacity, remaining_capacity, package_id | รองรับ FR-BKG-01, FR-BKG-03, FR-BKG-06 |
| QueueNumberPolicy | policy_id, date, prefix, sequence_start, sequence_current | รองรับ FR-BKG-04 และ Q-02 (Open Questions) |
| NotificationRequest | notification_id, booking_id, channel, payload, status, retry_count, next_retry_at, created_at | รองรับ FR-BKG-05, NFR-REL-02, IF-NOT-01 |
| AuditLog | audit_id, actor_user_id, access_time, hn, action_type, target_record_id | รองรับ DOM-PDPA-01, AC-BKG-06 |

หมายเหตุ: ตารางการจองจะเก็บ HN เพื่ออ้างอิงผู้รับบริการ แต่จะไม่เก็บเลขบัตรประชาชน ตาม IF-HIS-01

## 4. API / หน้าจอ

### หน้าจอ
- UI-01: หน้าเลือกแพ็กเกจ/วัน/ช่วงเวลา — รองรับ FR-BKG-01, FR-BKG-06
- UI-02: หน้าแสดงผลการจองสำเร็จ — รองรับ FR-BKG-04
- UI-03: หน้าแจ้ง “ช่วงเวลาเต็ม” พร้อม 3 ตัวเลือกใกล้เคียง — รองรับ FR-BKG-03
- UI-04: หน้าแจ้ง “คิวเดิม” เมื่อมีคิวในวันเดียวกัน — รองรับ FR-BKG-02
- UI-05: หน้าดูสถานะส่งข้อความยืนยันและ retry queue — รองรับ FR-BKG-05, NFR-REL-02

### API
- GET /api/booking/availability?dateFrom=YYYY-MM-DD&dateTo=YYYY-MM-DD&packageId=... — คืนค่า slot ว่างและจำนวนที่นั่งคงเหลือ — รองรับ FR-BKG-01
- POST /api/booking/validate — ตรวจว่าผู้ใช้มีคิวที่ยังไม่ได้ใช้ในวันเดียวกันหรือไม่ — รองรับ FR-BKG-02
- POST /api/booking/confirm — ยืนยันการจอง สร้าง booking และออกหมายเลขคิว — รองรับ FR-BKG-04, AC-BKG-01
- POST /api/booking/alternative-slots — ส่ง 3 ตัวเลือกช่วงเวลาใกล้เคียงเมื่อ slot เต็ม — รองรับ FR-BKG-03, AC-BKG-03
- POST /api/booking/notify/retry — ส่งซ้ำข้อความแจ้งเตือนตาม queue — รองรับ FR-BKG-05, NFR-REL-02
- GET /api/audit-log/{hn} — ดึง audit log เพื่อเช็ค tracking — รองรับ DOM-PDPA-01, AC-BKG-06

## 5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | ใช้ MySQL ในส่วนโมเดลข้อมูลและ API backend | ใช้แล้ว |
| DOM-PDPA-01 | audit log มี actor_user_id, access_time, hn, target_record_id และระบุ 1 ปี | ใช้แล้ว |
| IF-IDP-01 | PatientProfile/validation flow บังคับให้มีผลยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ | ใช้แล้ว |
| IF-HIS-01 | Booking อ้างอิง hn จาก HIS และแยกออกจากเลขบัตรประชาชนในตารางการจอง | ใช้แล้ว |
| IF-NOT-01 | NotificationRequest และ API retry queue สำหรับ SMS/LINE แบบ asynchronous | ใช้แล้ว |

## 6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_booking_success_decrements_capacity | Mock/seed slot 09.00 มี capacity = 1 และยืนยัน booking แล้วตรวจว่าบันทึก booking สำเร็จ และ remaining_capacity = 0 และมี queue_number |
| AC-BKG-02 | test_AC_BKG_02_block_duplicate_booking_same_day | Seed คิวที่ยังไม่ได้ใช้ของผู้รับบริการในวันเดียวกัน แล้วลองจองใหม่ในวันเดียวกัน ตรวจว่า API ปฏิเสธ และแสดงหมายเลขคิวเดิม |
| AC-BKG-03 | test_AC_BKG_03_show_alternatives_when_slot_full | Seed slot ที่เหลือ 1 ที่ แล้วมีผู้ใช้ยืนยันก่อน จัดการ race condition ตรวจว่าแสดง “ช่วงเวลาเต็ม” และ 3 ตัวเลือกใกล้เคียง โดยไม่มี double booking |
| AC-BKG-04 | test_AC_BKG_04_booking_persists_when_notification_fails | Simulate notification service timeout แล้วตรวจว่าการจองยังถูกบันทึก พร้อม queue retry ภายใน 5 นาที |
| AC-BKG-05 | test_AC_BKG_05_booking_availability_latency_p95 | Load test 200 concurrent users เพื่อวัด p95 ของการค้นหาช่วงว่างให้ <= 2 วินาที |
| AC-BKG-06 | test_AC_BKG_06_audit_log_written_on_access | Simulate การเข้าถึงข้อมูล booking ของผู้รับบริการ แล้วตรวจว่า audit log มี actor_user_id, access_time, hn |

## 7. ลำดับงาน

1. กำหนดสถาปัตยกรรมข้อมูล booking และ slot รวมถึงการเชื่อมข้อมูล HN จาก HIS ตาม IF-HIS-01 และ IF-IDP-01 — เกี่ยวกับ FR-BKG-01, FR-BKG-02, DOM-PDPA-01
2. สร้าง API เพื่อค้นหาช่วงว่างและจำนวนที่นั่งคงเหลือภายใน 30 วัน — เกี่ยวกับ FR-BKG-01, AC-BKG-05
3. สร้าง flow ตรวจสอบคิวที่ยังไม่ได้ใช้ในวันเดียวกันก่อนยืนยันการจอง — เกี่ยวกับ FR-BKG-02, AC-BKG-02
4. สร้าง flow แสดง 3 ตัวเลือกใกล้เคียงเมื่อ slot เต็ม และบล็อก race condition — เกี่ยวกับ FR-BKG-03, AC-BKG-03
5. สร้าง flow บันทึกการจองและออกหมายเลขคิว พร้อมลด remaining_capacity — เกี่ยวกับ FR-BKG-04, AC-BKG-01
6. สร้าง queue สำหรับส่งข้อความยืนยันแบบ asynchronous และ retry ภายใน 5 นาที — เกี่ยวกับ FR-BKG-05, NFR-REL-02, AC-BKG-04
7. สร้าง audit log และหน้าแสดงผลการจองที่ติดตามการเข้าถึงข้อมูลผู้รับบริการ — เกี่ยวกับ DOM-PDPA-01, AC-BKG-06
8. ทดสอบ end-to-end และ load test ตาม AC-BKG-01 ถึง AC-BKG-06 — เกี่ยวกับทุก AC

## 8. สิ่งที่ยังไม่ทำ

- Q-01 “ช่วงเวลาใกล้เคียง” นับเฉพาะวันเดียวกัน หรือรวมวันถัดไปด้วย? -> ถามพยาบาลคัดกรอง  
  ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง? -> ถามเจ้าหน้าที่เวชระเบียน  
  ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ

> หมายเหตุ: spec ณ ปัจจุบันยังอยู่ที่ Status: Draft v1 และยังไม่ได้ผ่านขั้น clarify จึงควรยืนยันคำตอบของ Open Questions ก่อนเริ่มพัฒนาเต็มรูปแบบ
