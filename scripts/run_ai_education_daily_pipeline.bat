@echo off
REM AI Early Education - Daily Watch pipeline runner (pure ASCII)
REM Runs: python scripts/ai_education_daily_pipeline.py --write
REM Logs to ops/ai-early-education/pipeline_runs/logs/
REM Does NOT edit site HTML / sitemap / deploy / upload. Auto-observe only.

setlocal
set "ROOT=%~dp0.."
set "PY=C:\Users\admin\AppData\Local\Programs\Python\Python313\python.exe"
set "LOGDIR=%ROOT%\ops\ai-early-education\pipeline_runs\logs"

if not exist "%LOGDIR%" mkdir "%LOGDIR%"

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set "TS=%%i"
set "RUNLOG=%LOGDIR%\run_%TS%.log"
set "ERRLOG=%LOGDIR%\error_%TS%.log"

cd /d "%ROOT%"
if not exist "%PY%" set "PY=python"

echo [%TS%] start daily pipeline --write > "%RUNLOG%"
"%PY%" scripts\ai_education_daily_pipeline.py --write 1>> "%RUNLOG%" 2> "%ERRLOG%"

if errorlevel 1 (
  echo [exit nonzero] >> "%RUNLOG%"
  echo pipeline failed, see "%ERRLOG%"
  endlocal
  exit /b 1
)

echo [exit 0] >> "%RUNLOG%"
REM Keep error log only if it has content
for %%A in ("%ERRLOG%") do if %%~zA==0 del "%ERRLOG%"
echo pipeline ok, log: "%RUNLOG%"
endlocal
