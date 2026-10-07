from fastapi import Header, HTTPException, status


def require_verified_identity(
    x_user_verified: str | None = Header(default=None, alias="X-User-Verified")
):
    """รองรับ IF-IDP-01: ต้องยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการ"""
    if x_user_verified is None or x_user_verified.lower() not in {"true", "1", "yes"}:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identity verification required before accessing booking data",
        )
    return True
