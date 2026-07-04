#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""아이와 AI교실 전용 업로드기 — upload_queue.json의 ready_to_upload를 API로 자동 업로드(private).
- 기존 youtube_upload.py 로직 재사용(채널 가드/재시도/썸네일).
- 채널 가드 = 아이와 AI교실(UCzCA_HXDHMVGvWpQv4PSZgw) 로 고정 → 다른 채널이면 거부.
- 토큰은 이 폴더 token_aiclassroom.json 에 별도 저장(IGS_AI 토큰 불침범).
- 공개(public)는 절대 안 함: 항상 private 업로드. 공개는 사람이 스튜디오에서.

사용:
  python upload_to_aiclassroom.py --auth-only      # ★최초 1회: OAuth 동의만(브라우저 URL 뜸)
  python upload_to_aiclassroom.py                  # 큐의 ready_to_upload 자동 업로드
  python upload_to_aiclassroom.py --id wae-illust-v2
"""
import os, sys, json, argparse
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CHANNEL_ID = "UCzCA_HXDHMVGvWpQv4PSZgw"   # 아이와 AI교실 (현재 브라우저 로그인 채널)
UPLOAD_TOOL_DIR = r"C:/Users/admin/Desktop/유튜브쇼츠/동영상제작"
QUEUE = HERE / "upload_queue.json"

sys.path.insert(0, UPLOAD_TOOL_DIR)
try:
    import youtube_upload as YU
except Exception as e:
    sys.exit(f"[준비 필요] youtube_upload.py 로드 실패: {e}\n  경로: {UPLOAD_TOOL_DIR}")

# ★이 채널로 고정 + 별도 토큰(IGS_AI 토큰 안 건드림).
YU.TARGET_CHANNEL_ID = CHANNEL_ID
YU.TOKEN = HERE / "token_aiclassroom.json"
# 데스크톱 OAuth 클라이언트 사용(매끄러운 loopback). 있으면 웹 클라이언트 대신 이걸로.
_desktop = HERE / "client_secret_aiclassroom.json"
if _desktop.exists():
    YU.CLIENT_SECRET = _desktop
    YU.CLIENT_SECRET_WEB = HERE / "__no_web__.json"   # 존재X → 데스크톱 플로우 강제(random localhost 포트)

def _load(): return json.load(open(QUEUE, encoding="utf-8"))
def _save(q): json.dump(q, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def auth_only():
    print("[인증] 아이와 AI교실 채널 OAuth 동의를 시작합니다.")
    print("  ▶ 곧 출력되는 URL을 '아이와 AI교실' 계정으로 로그인된 브라우저에 붙여넣고 '허용' 하세요.")
    creds = YU._creds()                       # run_local_server(open_browser=False) → URL 출력
    yt = YU.build("youtube", "v3", credentials=creds)
    r = yt.channels().list(part="snippet", mine=True).execute()
    it = r.get("items", [])
    if it:
        cid, ctitle = it[0]["id"], it[0]["snippet"]["title"]
        ok = "✅ 일치" if cid == CHANNEL_ID else "❌ 채널 불일치(다른 계정으로 동의함)"
        print(f"[확인] 인증된 채널: {ctitle} ({cid}) {ok}")
    print(f"[완료] 토큰 저장: {YU.TOKEN}")

def do_upload(vid_id=None):
    q = _load(); items = q["queue"]
    cand = [it for it in items if (vid_id is None and it["status"] == "ready_to_upload") or it["video_id"] == vid_id]
    if not cand: sys.exit("업로드할 ready_to_upload 항목이 없습니다(또는 --id 불일치).")
    it = cand[0]
    video = REPO / it["mp4_path"]
    thumb = REPO / it["thumbnail_path"] if it.get("thumbnail_path") else None
    if not video.exists(): sys.exit(f"영상 없음: {video}")
    desc_file = HERE / f"_desc_{it['video_id']}.txt"
    desc_file.write_text(it["description"], encoding="utf-8")
    print(f"[업로드] '{it['title']}' → private (채널 가드: 아이와 AI교실)")
    url = YU.upload(video, it["title"], it["description"],
                    it["tags"], "private", it.get("category", "27"),
                    thumb, shorts=it.get("shorts", False), allow_any=False)   # ★항상 private
    # 큐 갱신
    it["status"] = "uploaded_private"; it["youtube_url"] = url; it["updated_at"] = "auto"
    _save(q)
    print(f"[큐] status→uploaded_private, url={url}")
    print("  ※ 공개는 사람이 스튜디오에서 검수 후 승인(approved_public). 자동 public 안 함.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--auth-only", action="store_true")
    ap.add_argument("--id", default=None)
    a = ap.parse_args()
    if a.auth_only: auth_only()
    else: do_upload(a.id)
