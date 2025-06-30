@echo off

REM venv path
set VENV_PATH=_pyenv

REM activate
call %VENV_PATH%\Scripts\activate.bat

REM uvicorn server run
python -m tool.import_csv simple
