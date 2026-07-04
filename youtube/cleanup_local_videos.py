#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""로컬 영상 자동 정리 — 유튜브에 백업(youtube_url 있음)되고 1일 지난 렌더 mp4를 삭제.
로컬 용량 안 늘리면서 영상은 유튜브에 계속 쌓기 위한 청소부.
★안전: youtube_url 없는 항목은 절대 삭제 안 함. --dry 로 미리보기.
사용: python cleanup_local_videos.py [--dry] [--days N]"""
import json, os, time, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; REPO=HERE.parent
QUEUE=HERE/"upload_queue.json"
def main(dry=False, days=1):
    q=json.load(open(QUEUE,encoding="utf-8")); now=time.time(); thresh=days*86400
    freed=0; deleted=[]; kept=[]
    for it in q["queue"]:
        mp4=REPO/it["mp4_path"]
        if not it.get("youtube_url"):
            if mp4.exists(): kept.append((it["video_id"],"유튜브 업로드 전 → 보존"))
            continue
        if not mp4.exists(): continue
        age=now-mp4.stat().st_mtime
        if age>=thresh:
            sz=mp4.stat().st_size
            if not dry:
                try: mp4.unlink(); it["local_deleted"]=True
                except Exception as e: kept.append((it["video_id"],f"삭제실패 {e}")); continue
            freed+=sz; deleted.append((it["video_id"], os.path.basename(it["mp4_path"]), round(age/86400,1), round(sz/1e6,1)))
        else:
            kept.append((it["video_id"], f"{round(age/3600,1)}시간 경과(1일 미만) → 보존"))
    if not dry: json.dump(q,open(QUEUE,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    tag="[미리보기] " if dry else ""
    print(f"{tag}로컬 영상 정리 — 삭제 {len(deleted)}개 · {freed/1e6:.1f}MB 회수 (유튜브 백업+{days}일 경과분만)")
    for vid,fn,d,mb in deleted: print(f"  🗑 {vid} {fn} ({d}일, {mb}MB)")
    for vid,why in kept: print(f"  · {vid}: {why}")
    if not deleted and not kept: print("  대상 없음")

if __name__=="__main__":
    dry="--dry" in sys.argv
    days=1
    if "--days" in sys.argv: days=int(sys.argv[sys.argv.index("--days")+1])
    main(dry,days)
