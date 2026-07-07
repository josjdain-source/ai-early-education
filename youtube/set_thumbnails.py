#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""업로드된 영상에 커스텀 썸네일 일괄 설정(채널 전화인증 후 사용).
큐에서 youtube_id/url + poster_path 있는 항목을 찾아 thumbnails().set.
사용: python set_thumbnails.py            (전체 백필)
      python set_thumbnails.py <video_id> (한 편만)"""
import io, sys, json, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
import upload_to_aiclassroom as UA   # YU 설정(토큰·채널) 자동 구성
import youtube_upload as YU
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def ytid(it):
    y = it.get("youtube_id") or ""
    if y: return y
    u = it.get("youtube_url") or ""
    m = re.search(r"(?:youtu\.be/|shorts/|watch\?v=)([A-Za-z0-9_-]{11})", u)
    return m.group(1) if m else ""

only = sys.argv[1] if len(sys.argv) > 1 else None
q = json.load(open(os.path.join(HERE, "upload_queue.json"), encoding="utf-8"))["queue"]
creds = YU._creds(); yt = build("youtube", "v3", credentials=creds)
done = skip = fail = 0
for it in q:
    if only and it.get("video_id") != only: continue
    vid = ytid(it)
    tp = it.get("thumbnail_path") or it.get("poster_path") or ""
    fp = os.path.join(REPO, tp) if tp else ""
    if not vid or not tp or not os.path.exists(fp):
        skip += 1; continue
    try:
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(fp)).execute()
        print(f"  ✓ {it['video_id']} ({vid}) ← {os.path.basename(fp)}"); done += 1
    except Exception as e:
        print(f"  ✗ {it['video_id']}: {str(e)[:90]}"); fail += 1
print(f"완료 {done} · 건너뜀 {skip} · 실패 {fail}")
