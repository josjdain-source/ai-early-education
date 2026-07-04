#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""아이와 AI교실 채널 운영 매니저 (조종판 연동).
- status    : 채널 상태 + 업로드 대기열 + 매일 운영 체크리스트
- upload-cmd: ready_to_upload 항목의 '비공개 업로드 명령' 생성(실행 X, 사람이 실행)
★자동 public 발행 금지. 업로드는 private 기본. 공개는 사람이 approved_public 승인 후."""
import os, sys, json
HERE=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.dirname(HERE)
CFG=json.load(open(os.path.join(HERE,"channel_config.json"),encoding="utf-8"))
QF=os.path.join(HERE,"upload_queue.json")
def load_q(): return json.load(open(QF,encoding="utf-8"))
def ap(p): return os.path.join(REPO,p) if not os.path.isabs(p) else p
def yn(b): return "✅" if b else "❌"

def status():
    q=load_q(); items=q["queue"]
    print("="*60); print(f" 📺 {CFG['channel_name']} — 채널 운영 상태")
    print(f" 문구: {CFG['brand_message']}"); print(f" 기본 공개범위: {CFG['default_visibility']} · 자동공개: {CFG['auto_public_publish']}")
    print("="*60)
    cnt={}
    for it in items: cnt[it["status"]]=cnt.get(it["status"],0)+1
    print(" [대기열]", len(items),"편 ·", dict(cnt))
    for it in items:
        print(f"  - {it['title'][:34]} … [{it['status']}] vis={it.get('visibility_target')} url={'있음' if it.get('youtube_url') else '없음'}")
    # 렌더 폴더의 새 mp4가 큐에 없나
    rd=os.path.join(REPO,"assets/world-ai-education-5min/render")
    renders=[f for f in os.listdir(rd) if f.endswith(".mp4")] if os.path.isdir(rd) else []
    inq={os.path.basename(it["mp4_path"]) for it in items}
    unregistered=[f for f in renders if f not in inq and ("illust" in f or "auto" in f)]
    print("\n [매일 운영 체크리스트]")
    for it in items:
        print(f"  · {it['title'][:30]}")
        print(f"     {yn(os.path.exists(ap(it['mp4_path'])))} mp4 존재   {yn(bool(it.get('title')) and bool(it.get('description')) and bool(it.get('tags')))} 제목/설명/태그   {yn(os.path.exists(ap(it['thumbnail_path'])))} 썸네일")
        print(f"     {yn(os.path.exists(ap(it.get('detail_page','').lstrip('/'))))} 상세페이지   {yn(it.get('on_video_hub'))} 영상관 카드   {yn(bool(it.get('youtube_url')))} 업로드/URL")
        print(f"     {yn(it['status'] in ('uploaded_private','approved_public','published'))} 비공개 업로드   {yn(it['status']=='published')} 공개완료   {'⏳ 공개 승인 대기' if it['status']=='uploaded_private' else ''}")
    if unregistered:
        print("\n ⚠️ 큐에 없는 새 렌더:", unregistered, "→ 등록 필요")
    else:
        print("\n ✅ 새 렌더 모두 큐에 반영됨" if renders else "")
    print("\n 다음 할 일:", _next_action(items))

def _next_action(items):
    for it in items:
        if it["status"]=="ready_to_upload": return f"'{it['title'][:20]}…' 비공개 업로드 명령 생성 → python manage_channel.py upload-cmd {it['video_id']} (인증 후 사람이 실행)"
        if it["status"]=="uploaded_private": return f"'{it['title'][:20]}…' 유튜브 스튜디오에서 검수 → 공개 승인(approved_public)"
    return "새 렌더 대기 / 큐 등록"

def upload_cmd(vid=None):
    q=load_q(); items=q["queue"]
    target=[it for it in items if (vid is None and it["status"]=="ready_to_upload") or it["video_id"]==vid]
    if not target: print("ready_to_upload 항목 없음(또는 video_id 불일치)"); return
    it=target[0]
    desc_file=os.path.join(HERE,f"_desc_{it['video_id']}.txt")
    open(desc_file,"w",encoding="utf-8").write(it["description"])
    tool=CFG["upload_tool"]; mp4=ap(it["mp4_path"]); thumb=ap(it["thumbnail_path"])
    tags=",".join(it["tags"])
    cmd=(f'python "{tool}" "{mp4}" '
         f'--title "{it["title"]}" --desc-file "{desc_file}" --tags "{tags}" '
         f'--privacy {it.get("visibility_target","private")} --category {it["category"]} --thumb "{thumb}"')
    print(" ★전용 자동 업로드(권장): python youtube/upload_to_aiclassroom.py  (최초 1회 --auth-only)")
    print("="*60); print(" 🔒 비공개 업로드 명령 (사람이 실행)")
    print("="*60)
    print(" ⚠️ 전제: '아이와 AI교실' 채널 계정으로 youtube_upload.py 최초 OAuth 인증 완료.")
    print("    (youtube_upload.py는 채널 오인 방지 가드 있음 — 다른 채널이면 거부)")
    print(" ⚠️ 이 명령은 PRIVATE 업로드입니다. 공개는 업로드 후 사람이 스튜디오에서 승인.\n")
    print(cmd)
    print(f"\n 설명 파일 생성됨: {desc_file}")
    print(" 업로드 성공 후: upload_queue.json의 status→uploaded_private, youtube_url 기입.")

if __name__=="__main__":
    cmd=sys.argv[1] if len(sys.argv)>1 else "status"
    if cmd=="status": status()
    elif cmd=="upload-cmd": upload_cmd(sys.argv[2] if len(sys.argv)>2 else None)
    else: print("사용법: python manage_channel.py [status|upload-cmd <video_id>]")
