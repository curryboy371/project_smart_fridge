@echo off

REM venv path
set VENV_PATH=_pyenv

REM activate
call %VENV_PATH%\Scripts\activate.bat

REM uvicorn server run
uvicorn main:app --host 0.0.0.0 --port 8000
