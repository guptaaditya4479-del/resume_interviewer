@echo off
echo Starting Resume Interviewer Backend...
cd /d %~dp0
call venv\Scripts\activate.bat
echo.
echo Backend starting on http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
