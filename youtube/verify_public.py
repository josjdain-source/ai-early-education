#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""홈페이지 임베드 영상의 공개상태 검증 — public/unlisted면 OK, private면 재생 불가 경고.
upload_queue.json에서 임베드 대상(on_video_hub + youtube_url) ID를 모아 YouTube API로 privacyStatus 조회."""
import os, sys, json
from pathlib import Path
HERE=Path(__file__).resolve().parent; REPO=HERE.parent
sys.path.insert(0, r"C:/Users/admin/Desktop/유튜브쇼츠/동영상제작")
import youtube_upload as YU
YU.TOKEN = HERE / "token_aiclassroom.json"
_ds = HERE / "client_secret_aiclassroom.json"
if _ds.exists(): YU.CLIENT_SECRET=_ds; YU.CLIENT_SECRET_WEB=HERE/"__no_web__.json"

def vid_of(it):
    if it.get("youtube_id"): return it["youtube_id"]
    u=it.get("youtube_url") or ""; return u.rstrip("/").split("/")[-1] if u else ""

def main():
    q=json.load(open(HERE/"upload_queue.json",encoding="utf-8"))
    targets={vid_of(it):it["video_id"] for it in q["queue"] if it.get("on_video_hub") and vid_of(it) and it.get("status")!="superseded"}
    if not targets: print("검증 대상 없음(임베드+URL)"); return
    yt=YU.build("youtube","v3",credentials=YU._creds())
    r=yt.videos().list(part="status,snippet",id=",".join(targets)).execute()
    found={}
    for v in r.get("items",[]):
        found[v["id"]]=v["status"]["privacyStatus"]
    print("=== 임베드 영상 공개상태 검증 ===")
    allok=True
    for vid,name in targets.items():
        st=found.get(vid,"조회안됨")
        ok = st in ("public","unlisted")
        allok = allok and ok
        mark = "✅ 임베드 재생 가능" if st=="public" else ("✅ 일부공개(링크재생)" if st=="unlisted" else ("⚠️ PRIVATE — 홈페이지 재생 불가! 공개/일부공개로 변경 필요" if st=="private" else f"⚠️ {st}"))
        print(f"  {name} ({vid}): {st}  → {mark}")
    print("종합:", "모두 재생 가능 ✅" if allok else "⚠️ 일부 private — 홈페이지에서 안 뜸")
    return 0 if allok else 2

if __name__=="__main__":
    sys.exit(main() or 0)
