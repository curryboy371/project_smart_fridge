import re
from datetime import datetime
import utils.exceptions

#  날짜/정규표현식 딕셔너리
DATETIME_REGEX_FORMATS = {
    "date": r"^\d{4}-\d{2}-\d{2}$",
    "hour": r"^\d{4}-\d{2}-\d{2} \d{2}$",
    "minute": r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$",
    "second": r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
    "micro": r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{1,6}$",
    "iso": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{1,6}$",
}
# 날짜/포맷 딕셔너리
DATETIME_FORMAT_STRFTIME = {
    "date": "%Y-%m-%d",
    "hour": "%Y-%m-%d %H",
    "minute": "%Y-%m-%d %H:%M",
    "second": "%Y-%m-%d %H:%M:%S",
}


#  문자열이 지정된 날짜 포맷에 맞는지 정규표현식으로 검증
def format_datetime(dt: datetime, fmt: str = "second") -> str:
    pattern = DATETIME_FORMAT_STRFTIME.get(fmt)
    if not pattern:
        utils.exceptions.raise_bad_request(detail=f"Unsupported format type: {fmt}")
    return dt.strftime(pattern)

#  datetime 객체를 지정한 문자열 포맷으로 변환
def validate_datetime_string(value: str, fmt: str = "second") -> str:
    if not value or not isinstance(value, str):
        utils.exceptions.raise_bad_request(detail=f"Empty or invalid datetime string: {value!r}")
    
    regex = DATETIME_REGEX_FORMATS.get(fmt)
    if not regex:
        utils.exceptions.raise_bad_request(detail=f"Unsupported format type: {fmt}")
    
    if not re.match(regex, value):
        utils.exceptions.raise_bad_request(detail=f"Invalid format: {value!r} (expected: {fmt})")
    
    return value

#  문자열을 datetime 객체로 파싱
def strptime_datetime(value: str, fmt: str = "second") -> datetime:
    pattern = DATETIME_FORMAT_STRFTIME.get(fmt)
    if not pattern:
        utils.exceptions.raise_bad_request(detail=f"Unsupported format type: {fmt}")
    return datetime.strptime(value, pattern)
