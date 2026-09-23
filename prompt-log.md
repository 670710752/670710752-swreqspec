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
