#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""로컬 영상 자동 정리 — 유튜브에 백업된(youtube_url 또는 youtube_id 있음) + N일 지난 렌더 mp4 삭제.
★안전 규칙:
  - youtube_url/youtube_id 둘 다 없으면 절대 삭제 안 함(업로드 실패/URL 미기록/검수 전 보존).
  - dry-run 및 실제 삭제 내역을 logs/video_cleanup.log 에 타임스탬프와 함께 기록.
사용: python cleanup_local_videos.py [--dry] [--days N]"""
import json, os, time, sys
from datetime import datetime
from pathlib import Path
HERE=Path(__file__).resolve().parent; REPO=HERE.parent
QUEUE=HERE/"upload_queue.json"
LOGDIR=REPO/"logs"; LOG=LOGDIR/"video_cleanup.log"

def _yt_ref(it):
    """youtube_url 또는 youtube_id 중 하나라도 있으면 백업된 것으로 간주."""
    if it.get("youtube_id"): return it["youtube_id"]
    u=it.get("youtube_url") or ""
    return u.rstrip("/").split("/")[-1] if u else ""

def log(lines):
    LOGDIR.mkdir(exist_ok=True)
    ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG,"a",encoding="utf-8") as f:
        for ln in lines: f.write(f"[{ts}] {ln}\n")

def main(dry=False, days=1):
    q=json.load(open(QUEUE,encoding="utf-8")); now=time.time(); thresh=days*86400
    freed=0; deleted=[]; kept=[]; out=[]
    mode="DRY-RUN" if dry else "DELETE"
    for it in q["queue"]:
        mp4=REPO/it["mp4_path"]; ref=_yt_ref(it)
        if not ref:                                   # ★유튜브 백업 없음 → 절대 삭제 안 함
            if mp4.exists(): kept.append(f"{it['video_id']}: 유튜브 백업 없음(url/id 미기록) → 보존")
            continue
        if not mp4.exists(): continue
        age=now-mp4.stat().st_mtime
        if age>=thresh:
            sz=mp4.stat().st_size
            if dry:
                deleted.append(f"{it['video_id']} {os.path.basename(it['mp4_path'])} (yt={ref}, {age/86400:.1f}일, {sz/1e6:.1f}MB) [삭제예정]")
            else:
                try:
                    mp4.unlink(); it["local_deleted"]=True
                    deleted.append(f"{it['video_id']} {os.path.basename(it['mp4_path'])} (yt={ref}, {age/86400:.1f}일, {sz/1e6:.1f}MB) [삭제됨]")
                except Exception as e:
                    kept.append(f"{it['video_id']}: 삭제실패 {e}"); continue
            freed+=sz
        else:
            kept.append(f"{it['video_id']}: {age/3600:.1f}시간 경과(1일 미만) → 보존")
    if not dry: json.dump(q,open(QUEUE,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    out.append(f"=== {mode} · 삭제 {len(deleted)}개 · {freed/1e6:.1f}MB (유튜브 백업+{days}일 경과분만) ===")
    out+= [f"  🗑 {d}" for d in deleted] + [f"  · {k}" for k in kept]
    print("\n".join(out)); log(out)

if __name__=="__main__":
    dry="--dry" in sys.argv
    days=int(sys.argv[sys.argv.index("--days")+1]) if "--days" in sys.argv else 1
    main(dry,days)
