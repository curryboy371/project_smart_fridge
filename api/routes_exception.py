
from fastapi import HTTPException

# 400 Bad Request (잘못된 요청)
def raise_bad_request(detail: str = "Bad request"):
    raise HTTPException(status_code=400, detail=detail)

# 401 Unauthorized (인증 실패)
def raise_unauthorized(detail: str = "Unauthorized"):
    raise HTTPException(status_code=401, detail=detail)

# 403 Forbidden (권한 없음)
def raise_forbidden(detail: str = "Forbidden"):
    raise HTTPException(status_code=403, detail=detail)

# 404 Not Found (자원 없음)
def raise_not_found(detail: str = "Resource not found"):
    raise HTTPException(status_code=404, detail=detail)

# 409 Conflict (중복 등 충돌)
def raise_conflict(detail: str = "Conflict"):
    raise HTTPException(status_code=409, detail=detail)

# 500 Internal Server Error (서버 오류)
def raise_internal_error(detail: str = "Internal server error"):
    raise HTTPException(status_code=500, detail=detail)