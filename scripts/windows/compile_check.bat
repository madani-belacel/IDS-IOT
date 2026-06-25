@echo off
REM Quick PDF compile check (Windows CMD wrapper)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0compile_check.ps1"
exit /b %ERRORLEVEL%
