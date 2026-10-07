from fastapi import FastAPI

from app.slots.router import router as slots_router

app = FastAPI(title="Booking API")
app.include_router(slots_router)


@app.get("/health")
def health_check():
    """รองรับ FR-BKG-01: endpoint health check สำหรับ smoke test"""
    return {"status": "ok"}
