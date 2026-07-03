# 세계 AI교육 본편 — 검수용 draft mp4 렌더 보고

- 작성일: 2026-07-04
- 성격: **검수용 초벌 렌더(draft-v1).** 업로드/HTML/링크 교체 없음. 최종본 아님.

## 1. 사용한 timeline
`production/world-ai-education-compact-edit-timeline.json` (3:45, 섹션 오디오 실측 경계에 컷 정렬).

## 2. 사용한 오디오
`assets/world-ai-education-5min/audio/world-ai-education-5min-narration.mp3` (edge-tts SunHi, 섹션 concat, 내레이션 3:28 + 무음).

## 3. 사용한 이미지 수 — **26컷** (evidence 10 · 인포그래픽/해석 16). raw 미사용, evidence는 final만.

## 4. 생성한 mp4 파일
`assets/world-ai-education-5min/render/world-ai-education-compact-draft-v1.mp4` (5.6MB, 로컬 재생용·gitignore).

## 5. 영상 길이 — **3:45 (225.0s)** (목표 3:40~3:55 달성)

## 6. 해상도/fps/코덱 — **1280×720 · 30fps · H.264 / AAC 44.1kHz mono**

## 7. 자막 생성 여부 — ✅
`world-ai-education-compact-draft-v1.srt` (16큐). 화면 하단(MarginV=28, 반투명 박스). **evidence 컷은 자막 없음**(출처 바 내장 → 겹침 방지).

## 8. 검수 결과
| # | 항목 | 결과 |
|---|---|---|
| 1 | 길이 3:40~3:55 | ✅ 3:45 |
| 2 | 오디오 정상 | ✅ (aac, 섹션 concat) |
| 3 | 26컷 모두 | ✅ |
| 4 | evidence 10장 | ✅ |
| 5 | raw 미사용 | ✅ |
| 6 | final evidence만 | ✅ |
| 7 | 자막이 출처 바 안 가림 | ✅ (evidence 컷 자막 없음) |
| 8 | CN-01 정치/헤드밴드 없음 | ✅ (final 크롭본) |
| 9 | KR 인기뉴스 없음 | ✅ (final 크롭본) |
| 10 | 한국 결론 마지막 자연 | ✅ (2:15~2:30 KR 카드 → 공통→CTA) |
| 11 | 최종 문구 없음 | ✅ (draft, CTA만) |
| 12 | 파일명 draft-v1 | ✅ |

## 9. ★A/V 싱크 처리(중요)
- **초기 렌더는 컷 배분이 내레이션 섹션 길이와 안 맞아 어긋남** 발견 → 섹션별 오디오를 따로 합성해 실측(opening 23·china 27.8·usa 24.4·uk 22.9·sg 22.3·kr 30.4·common 31.1·parent 26.7s)하고 **컷을 그 경계에 재정렬**. 프레임 검수(2:20=한국 카드) 섹션 싱크 확인.
- 섹션 단위 싱크. 문장 단위 정밀 싱크는 사람 청취 후 미세조정 가능(선택).

## 10. 문제 컷 여부 — 없음
- 참고: CTA(C26)는 3:28~3:45 무음 홀드(내레이션 종료 후 엔드카드). 의도된 구성.

## 11. 확인 (안 한 것)
- **업로드/HTML/링크 교체/최종본 명명 없음.** sitemap 41. draft mp4는 로컬(gitignore).

## 12. 다음 단계
사람이 draft-v1 재생 → 검수(발음 청취·섹션 싱크·자막) → 수정 지시 or 최종 렌더 승인 → (승인 후) video-countries 카드 링크 교체.
