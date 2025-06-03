
from fastapi import HTTPException
from core.tflog import TFLoggerManager as TFLog



# 400 Bad Request (잘못된 요청)
def raise_bad_request(detail: str = "Bad request"):
    TFLog().get_instance().logger.error(f'HTTP_EXCEPTION 400 {detail}')   
    raise HTTPException(status_code=400, detail=detail)

# 401 Unauthorized (인증 실패)
def raise_unauthorized(detail: str = "Unauthorized"):
    TFLog().get_instance().logger.error(f'HTTP_EXCEPTION 401 {detail}')   
    raise HTTPException(status_code=401, detail=detail)

# 403 Forbidden (권한 없음)
def raise_forbidden(detail: str = "Forbidden"):
    TFLog().get_instance().logger.error(f'HTTP_EXCEPTION 403 {detail}')   
    raise HTTPException(status_code=403, detail=detail)

# 404 Not Found (자원 없음)
def raise_not_found(detail: str = "Resource not found"):
    TFLog().get_instance().logger.error(f'HTTP_EXCEPTION 404 {detail}')   
    raise HTTPException(status_code=404, detail=detail)

# 409 Conflict (중복 등 충돌)
def raise_conflict(detail: str = "Conflict"):
    TFLog().get_instance().logger.error(f'HTTP_EXCEPTION 409 {detail}')   
    raise HTTPException(status_code=409, detail=detail)

# 500 Internal Server Error (서버 오류)
def raise_internal_error(detail: str = "Internal server error"):
    TFLog().get_instance().logger.error(f'HTTP_EXCEPTION 500 {detail}')   
    raise HTTPException(status_code=500, detail=detail)