@echo off
chcp 65001 >nul
cd /d C:\Users\admin\Desktop\ai-craft-kids
python youtube\cleanup_local_videos.py >> youtube\_cleanup.log 2>&1
