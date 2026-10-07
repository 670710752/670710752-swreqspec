# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2026-09-16 00:00 คำสั่ง: /plan

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: specs/001-booking/plan.md
- Constraint ที่ AI ยังไม่ได้ใช้: ไม่มี (ทุก constraint ใน spec ถูกนำไปใช้ใน plan แล้ว)
- สิ่งที่ AI บอกว่าอยากเดาแต่ไม่ได้เดา: Q-01 และ Q-02 จาก spec เนื่องจากยังไม่มีคำตอบชัดเจนจากทีม

### สรุปผล
- สร้าง plan.md สำหรับฟีเจอร์จองคิวตรวจสุขภาพโดยอ้างอิง ID จาก spec อย่างครบถ้วน
- ได้นำทุก Constraint (CON, DOM, IF) มาเชื่อมในตารางตรวจ constraints และระบุสถานะเป็นใช้แล้ว
- รายงาน Open Questions ไว้ในส่วน “สิ่งที่ยังไม่ทำ” เพื่อให้ทีมตอบก่อนพัฒนาเต็มรูปแบบ

---

## 2026-09-23 00:00 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: specs/001-booking/tasks.md
- ข้อสังเกต: ใช้ spec.md และ plan.md ของฟีเจอร์นี้เป็นข้อมูลจริง กำหนด task ตามลำดับพึ่งพาและมีการอ้างอิง ID จาก spec อย่างครบทุก AC และ Constraint
- สถานะ Open Questions: Q-02 ยังไม่ได้คำตอบ แต่ได้ระบุชัดว่าต้องไม่เดาและไม่สร้าง task ที่เกี่ยวกับรูปแบบเลขคิวจนกว่าจะได้รับคำตอบ

### สรุปผล
- สร้าง tasks.md สำหรับฟีเจอร์จองคิวตรวจสุขภาพแบบแยกงานย่อยตามลำดับพึ่งพา
- ครอบคลุม AC ทั้ง 6 ข้อ และ Constraint ทั้ง 5 ข้อ ในตารางตรวจความครบ
- มี task 11 รายการและไม่มี task ที่รอ Q-xx เนื่องจาก Open Question ที่เหลือไม่ได้เกี่ยวข้องกับงานที่ต้องเริ่มทันที
---

## 2026-09-23 00:00 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: pytest tests/test_T01_schema.py -q -> 1 passed in 0.44s
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เพราะ task T-01 ไม่มี Open Question และ spec/plan ให้ข้อมูลครบสำหรับ schema และ migration

### สรุปผล
- สร้าง schema สำหรับ slots, bookings, audit_logs ตามข้อกำหนด PostgreSQL และให้ทำงานร่วมกับ SQLite ในหน่วยความจำสำหรับการทดสอบ
- ระบุคอลัมน์ที่ต้องมีตาม constraint อย่างชัดเจน เช่น ไม่มี national_id ใน bookings และมี actor_id, accessed_at ใน audit_logs
- สร้าง test ที่ตรวจว่าตารางและคอลัมน์พื้นฐานถูกสร้างจริง---
---

## 2026-09-23 00:00 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ผลลัพธ์: ถูกปฏิเสธก่อนเริ่มพัฒนา เนื่องจาก T-03 มีข้อกำหนด "ต้องทำหลัง: T-02" แต่ T-02 ยังไม่ใช่สถานะ "เสร็จ รอทีมตรวจ"
- ไฟล์ที่ตรวจ: specs/001-booking/tasks.md
- สถานะ: หยุดก่อนเริ่มงานตามกฎของ implement prompt

### สรุปผล
- T-03 ไม่สามารถเริ่มได้ เพราะ prerequisite T-02 ยังไม่ได้เสร็จตามเงื่อนไขของ task
- กรณีนี้ไม่ผ่านเงื่อนไขที่ 2 ของการเริ่มงาน: "task ในช่องต้องทำหลัง ทุกตัวมีสถานะเสร็จแล้ว"
- ทีมควรทำ T-02 ให้เสร็จก่อน แล้วจึงเริ่ม T-03 ต่อ

---

## 2026-09-23 00:00 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์ที่สร้าง/แก้: backend/app/auth/idp.py, backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/test_AC_BKG_05.py
- ผล test: pytest tests/test_AC_BKG_05.py -q -> 1 passed, 1 warning in 3.41s
- สิ่งที่เกือบต้องเดาแต่ถามแทน: ไม่มี เพราะ spec และ plan ระบุชัดว่าต้องยืนยันตัวตนก่อนเข้าถึงข้อมูล และต้องมี GET /slots สำหรับช่วงเวลาว่างพร้อม remaining

### สรุปผล
- สร้าง auth guard ที่รับ X-User-Verified เพื่อป้องกันการเข้าถึงข้อมูลโดยไม่ได้ยืนยันตัวตน
- สร้าง GET /slots และ service คืนช่วงเวลาว่างพร้อม remaining สำหรับแพ็กเกจและวันที่ที่เลือกได้
- Test AC-BKG-05 ผ่าน โดย p95 ของเวลาตอบสนองอยู่ในเกณฑ์ไม่เกิน 2 วินาที