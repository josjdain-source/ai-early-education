#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""미국 편 롱폼1+쇼츠5를 upload_queue.json에 등록(status=ready_to_upload, private).
메타데이터(production/us_ai_education_metadata.json) 기반. 멱등(있으면 갱신 안 함). 포스터도 생성."""
import os, json, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent; REPO=HERE.parent
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
META=json.load(open(REPO/"production/us_ai_education_metadata.json",encoding="utf-8"))
QF=HERE/"upload_queue.json"; Q=json.load(open(QF,encoding="utf-8"))
POST=REPO/"assets/us-ai-education/poster"; POST.mkdir(parents=True,exist_ok=True)
def have(vid): return any(it["video_id"]==vid for it in Q["queue"])
def poster(mp4,out,ss):
    if Path(mp4).exists() and not Path(out).exists():
        subprocess.run([FF,"-hide_banner","-loglevel","error","-ss",str(ss),"-i",str(mp4),"-frames:v","1","-y",str(out)],check=False)
added=[]
# 롱폼
lf=META["longform"]; lf_mp4="assets/us-ai-education/render/us-ai-education-longform.mp4"; lf_th="assets/us-ai-education/poster/longform.jpg"
poster(REPO/lf_mp4, REPO/lf_th, 30)
if not have(lf["video_id"]):
    Q["queue"].append({"video_id":lf["video_id"],"title":lf["title"],"description":lf["description"],"tags":lf["tags"],
        "category":lf["category"],"mp4_path":lf_mp4,"thumbnail_path":lf_th,"status":"ready_to_upload","visibility_target":"private",
        "shorts":False,"youtube_url":"","detail_page":"/videos/us-ai-education.html","on_video_hub":True,
        "created_at":"2026-07-04","updated_at":"2026-07-04","notes":"미국 편 롱폼 심층다큐(6~8분). 홈페이지 /world-cases/china.html 임베드. private→사람 검수→공개."})
    added.append(lf["video_id"])
# 쇼츠 5
for s in META["shorts"]:
    mp4=f"assets/us-ai-education/render/shorts/china-{s['key']}.mp4"
    # 파일명 규칙: build_china_ai_shorts는 us-short-<key>.mp4 로 출력
    mp4=f"assets/us-ai-education/render/shorts/us-short-{s['key']}.mp4"
    th=f"assets/us-ai-education/poster/short-{s['key']}.jpg"
    poster(REPO/mp4, REPO/th, 10)
    if not have(s["video_id"]):
        Q["queue"].append({"video_id":s["video_id"],"title":s["title"],"description":s["description"],"tags":s["tags"],
            "category":"27","mp4_path":mp4,"thumbnail_path":th,"status":"ready_to_upload","visibility_target":"private",
            "shorts":True,"youtube_url":"","detail_page":"/videos/us-ai-education.html","on_video_hub":True,
            "created_at":"2026-07-04","updated_at":"2026-07-04","notes":f"미국 편 쇼츠 {s['key']}. 독립 후킹구조. private→사람 공개."})
        added.append(s["video_id"])
json.dump(Q,open(QF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("큐 등록:",added if added else "이미 전부 등록됨")
print("총 대기열:",len(Q["queue"]),"편")
