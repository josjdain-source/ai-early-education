# 아이와 AI교실 — 유튜브 자동 업로드 세팅 (B: API 자동화)

## 상태
- OAuth 앱·라이브러리·인프라: ✅ 이미 작동(기존 무풍/IGS 자동업로드로 검증)
- 전용 스크립트: youtube/upload_to_aiclassroom.py (채널 가드=아이와 AI교실, 토큰 별도, 항상 private)

## 최초 1회(사람) — OAuth 동의
1. `python youtube/upload_to_aiclassroom.py --auth-only` → 동의 URL 출력(포트 8765 대기)
2. 그 URL을 '아이와 AI교실' 계정 브라우저에서 열기 → 채널 선택 시 **아이와 AI교실** → **허용**
3. token_aiclassroom.json 저장 + 채널 일치 확인 출력되면 완료

## 이후(자동) — Claude/조종판
- `python youtube/upload_to_aiclassroom.py` → upload_queue.json의 ready_to_upload를 **private 업로드**
- 성공 시 status→uploaded_private, youtube_url 기입
- ★공개(public)는 절대 자동 안 함. 스튜디오에서 사람이 검수→승인.
