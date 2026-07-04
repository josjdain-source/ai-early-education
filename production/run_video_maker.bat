@echo off
chcp 65001 >nul
title Video Auto Maker
echo ============================================
echo   Illustrated Video Auto Maker (topic -^> video)
echo   Local: Ollama(11435) + ComfyUI(8188) required
echo ============================================
echo.
set /p TOPIC="Enter topic (Korean OK): "
if "%TOPIC%"=="" (echo No topic entered. & pause & exit /b)
echo.
echo Generating... about 5 min ^(SDXL 18 images^). Please wait.
echo.
python "%~dp0make_illust_video.py" "%TOPIC%"
echo.
echo Done. Output: ai-craft-kids\assets\world-ai-education-5min\render\auto-*.mp4
pause
