@echo off

REM 가상환경 경로
set VENV_PATH=_pyenv

REM 가상환경 활성화
call %VENV_PATH%\Scripts\activate.bat

REM uvicorn 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000
