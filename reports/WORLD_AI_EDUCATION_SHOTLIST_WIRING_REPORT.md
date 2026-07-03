# 세계 AI교육 5분 본편 — shotlist 증거 컷 배선 보고

- 작성일: 2026-07-04
- 성격: **shotlist에 evidence 배선 + 편집 타임라인 정리.** 렌더/업로드/HTML/영상 링크 교체 없음.

## 1. 연결한 evidence 이미지 수 — **10 / 10**
각 나라 2장씩(중/미/영/싱/한). 전부 final/(출처 바 내장). raw 미사용.

## 2. 국가별 3단 구조 배선 결과
| 나라 | ①인포그래픽 | ②증거 2장 | ③부모 해석 카드 |
|---|---|---|---|
| 중국 | IMG-03(ready) | CN-01·CN-02 | C06 "빨리 접하되 안 맡긴다" |
| 미국 | IMG-05(pending) | US-01·US-02 | C10 "이해·의심·고쳐 쓰기" |
| 영국 | IMG-07(pending) | UK-01·UK-02 | C14 "판단은 사람" |
| 싱가포르 | IMG-09(pending) | SG-01·SG-02 | C18 "안전한 틀" |
| 한국 | IMG-11(pending) | KR-01·KR-02 | C22 "학교 도입≠아이 습관, 집에서 다시 묻기"(결론부) |
- 모든 증거 컷 뒤에 부모 해석 카드 배치(편집국 표준 3단). 총 26컷, 5:00.

## 3. 생성한 edit shotlist
`production/world-ai-education-5min-edit-shotlist.md` (26컷 표: 유형·이미지·상태·자막·전환·줌팬·주의).

## 4. 생성한 timeline JSON
`production/world-ai-education-5min-edit-timeline.json` (26 cut 객체: id/start/end/duration/section/country/visual_type/image_file/image_status/narration_ref/subtitle/transition/motion/notes).
- evidence 10 · ready 이미지 13 · pending 이미지 13.

## 5. 문제 이미지 여부 — **없음**
- 증거 10개 전부 출처 바 내장 final 사용. raw 실수 사용 0.
- CN-01 정치 사이드바/헤드밴드 재유입 없음.
- ⚠️ 단, **인포그래픽 IMG-05~16(8개)·부모 해석 카드 5개 = pending(미생성)** — 증거 컷은 완비, 편집 전 이 pending 이미지 제작 필요(별도 단계). timeline에 image_status=pending 명시.

## 6. 확인 (안 한 것)
- **영상 렌더/업로드/HTML 수정/영상 링크 교체 없음.** sitemap 41.

## 7. 다음 단계: 본편 초벌 편집
1. pending 인포그래픽(IMG-05~16)·부모 해석 카드 제작(무료 인포그래픽 방식, 톤 통일).
2. TTS(production/world-ai-education-5min-tts-script.md) 음성 생성.
3. timeline대로 조립(이미지+TTS+자막), 증거 컷 3~5초 정지 + 뒤 해석 카드.
4. 초벌 렌더 → 사람 검수 → (승인 후) video-countries 카드 링크 교체.
