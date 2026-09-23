# Feature: จองคิวตรวจสุขภาพ (Booking)
Spec ID: SPEC-BKG-001
อ้างอิง: plan.md v1 (2569-09-22)
วันที่: 2569-09-23

สรุป: ทำ 11 task ในลำดับพึ่งพา และมี 0 task ที่ต้องรอ Open Questions
สรุป: งานที่เปิดไว้ตาม spec ยังไม่มี task ที่ต้องรอ Q-02 เนื่องจากระบุชัดว่าห้ามเดาวิธีออกเลขคิวก่อนได้รับคำตอบ

### T-01 สร้าง schema และ migration ฐานข้อมูล
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง slots, bookings และ audit_logs ใน PostgreSQL พร้อมใช้งานสำหรับ test SQLite ในหน่วยความจำ
- สถานะ: พร้อมทำ

### T-02 สร้าง auth guard และ API ดึงช่วงเวลาว่าง
- รองรับ: IF-IDP-01, FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/auth/idp.py, backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /slots คืนช่วงเวลาที่ว่างพร้อม remaining ภายใต้ auth guard และผล load test ย่อส่วนแสดง p95 ไม่เกิน 2 วินาทีที่ 200 คน
- สถานะ: พร้อมทำ

### T-03 สร้าง API จองคิวพื้นฐาน
- รองรับ: FR-BKG-04
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py, backend/tests/test_AC_BKG_01.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: POST /bookings บันทึก booking, ตัด remaining, และส่งกลับ queue_no พร้อมยืนยันว่าการจองสำเร็จในสถานการณ์ที่มีที่นั่งว่าง
- สถานะ: พร้อมทำ

### T-04 ป้องกันการจองซ้ำวันเดียวกัน
- รองรับ: FR-BKG-02
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/tests/test_AC_BKG_02.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test_AC_BKG_02 ผ่าน และเมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ระบบปฏิเสธพร้อมแสดงหมายเลขคิวเดิม
- สถานะ: พร้อมทำ

### T-05 จัดการช่วงเวลาที่เต็มและเสนอ 3 ตัวเลือก
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/service.py, backend/tests/test_AC_BKG_03.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: เมื่อ slot เต็ม ระบบคืน 409 พร้อม 3 ตัวเลือกที่ใกล้ที่สุดในวันเดียวกันและวันถัดไป และไม่มีการจองซ้อนเกิดขึ้น
- สถานะ: พร้อมทำ

### T-06 สร้างคิวส่งข้อความและการส่งซ้ำ
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py, backend/tests/test_AC_BKG_04.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: การจองถูกบันทึกแม้การส่งข้อความยืนยันล้มเหลว และมีงานส่งซ้ำอยู่ภายใน 5 นาทีตามเงื่อนไข ASM-03
- สถานะ: พร้อมทำ

### T-07 บันทึก audit log ทุกการเข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/main.py, backend/tests/test_AC_BKG_06.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: audit log เก็บ actor_id, accessed_at และ hn เมื่อผู้ใช้เข้าดูข้อมูลการจองและให้ตรงตามข้อกำหนดความเป็นส่วนตัว
- สถานะ: พร้อมทำ

### T-08 ค้น HN จาก HIS ก่อนบันทึกการจอง
- รองรับ: IF-HIS-01, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/booking/service.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ระบบค้น HN จาก HIS ด้วยเลขบัตรประชาชน แล้วเก็บเฉพาะ HN ใน booking และไม่เก็บเลขบัตรประชาชนในตารางการจอง
- สถานะ: พร้อมทำ

### T-09 สร้างหน้าเลือกแพ็กเกจและเวลาแบบ mock
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/api/client.js, frontend/src/App.jsx
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: หน้าแสดงแพ็กเกจและช่วงเวลาว่าง และเมื่อเปลี่ยนแพ็กเกจจะโหลดช่วงเวลาใหม่จาก mock API ตามสัญญา API ใน plan
- สถานะ: พร้อมทำ

### T-10 สร้างหน้ายืนยันการจองและจัดการช่วงเต็ม
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-09
- เสร็จเมื่อ: เมื่อ mock API คืน 409 ระบบแสดง “ช่วงเวลาเต็ม” พร้อม 3 ตัวเลือกในวันเดียวกันและวันถัดไป โดยคงสภาพแวดล้อมแนวคิดจาก spec
- สถานะ: พร้อมทำ

### T-11 แสดงผลการจองและต่อหน้าจอกับ API จริง
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/src/api/client.js, frontend/src/App.jsx
- ต้องทำหลัง: T-02, T-05, T-06, T-09, T-10
- เสร็จเมื่อ: หน้าแสดงหมายเลขคิวและผลการจองจาก API จริง พร้อมทั้งแสดงผลแม้การส่งข้อความยืนยันไม่สำเร็จ
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ AC
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03, T-11 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-10 |
| AC-BKG-04 | T-06, T-11 |
| AC-BKG-05 | T-02 |
| AC-BKG-06 | T-07 |

## ตารางตรวจความครบ Constraint
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01, T-07 |
| IF-IDP-01 | T-02 |
| IF-HIS-01 | T-01, T-08 |
| IF-NOT-01 | T-06 |

## สิ่งที่ยังไม่ทำ
- Q-02 หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)?
  -> ถามเจ้าหน้าที่เวชระเบียน (ยังไม่ได้คำตอบ)
  -> ไม่มี task ที่สร้างไว้รอ Q-02 เนื่องจาก plan และ spec ระบุชัดว่าห้ามเดาและชะลองานที่เกี่ยวข้องกับเลขคิวจนกว่าจะได้รับคำตอบ
