# UQ-02 싱가포르 5분 영상 — 1차 편집 에셋 패키지 보고

- 작성일: 2026-07-04
- 성격: **1차 편집용 에셋 패키지.** 영상 완성본 렌더·업로드 없음. UQ-02 approved/applied/published 아님.

## 1. 생성한 폴더/파일
```
assets/ai-early-education/video-episode-02-singapore/
├─ narration/final_narration_ko.md            (낭독용 최종 대본, 호흡 표시)
├─ captions/episode_02_captions.srt           (SRT 25컷)
├─ captions/episode_02_key_captions.md        (강조 큰 자막)
├─ cards/  (실제 PNG 6 + 명세)
│   ├─ c08_age_4_steps_card.png ✅
│   ├─ c09_parent_questions_4_card.png ✅
│   ├─ c10_school_vs_home_card.png ✅
│   ├─ c11_three_actions_card.png ✅
│   ├─ c12_homepage_link_card.png ✅
│   ├─ source_label_card.png ✅
│   └─ cards_spec.md (c01 거실 장면 = 명세만)
├─ timeline/official_evidence_timeline.json   (공식 캡처 6컷 배치)
├─ timeline/edit_timeline.json                (전체 12컷 편집 타임라인)
├─ thumbnails/thumbnail_candidates.md         (기존5 + 증거형5)
├─ render_plan/episode_02_render_plan.md      (규격·톤·검수 체크)
└─ exports/  (비어있음, 렌더 산출물 자리)
scripts/make_ep02_cards.py                    (텍스트 카드 생성기, 실행됨)
scripts/render_episode_02_preview.py          (preview 렌더, ⚠️미실행)
```

## 2. 영상 편집 타임라인 요약 (edit_timeline.json, 12컷)
C01 거실(0:00) → **C02~C06 공식 근거 몰아치기(0:30~1:35)** → C08 연령 4단계(1:35) → C07 책임 문장(2:20) → C09 부모 질문(2:45) → C10 학교vs가정(3:10) → C11 결론3(4:10) → C12 홈 연결(4:50~5:10). 각 컷: visual_asset·narration·caption·transition·bgm·sfx·source_required·caution.

## 3. 공식 캡처 사용 구간 (official_evidence_timeline.json)
| 시간 | PNG | 노출 | 하이라이트 |
|---|---|---|---|
| 0:30 | C02 | 6s | Artificial intelligence in education |
| 0:42 | C03 | 8s | for Students and Parents... (허리) |
| 1:00 | C04 | 5s | Age-progressive Framework |
| 1:15 | C05 | 5s | Guide to Generative AI... (Parents Gateway) |
| 1:25 | C06 | 6s | Guidance on Generative AI / SLS |
| 2:20 | C07 | 9s | When used appropriately... |
→ 공식 캡처 총 ≈ 39초. 원문 변경/윤리4원칙/의역 금지.

## 4. 자막 생성 여부
- `episode_02_captions.srt` (25컷, 한 줄 18~24자) ✅
- `episode_02_key_captions.md` (강조 큰 자막) ✅
- 원칙: 공식 영어 문구는 캡처 이미지 안에서만, 하단 자막은 한국어 해설.

## 5. 추가 제작 필요한 이미지/카드
- **c01_parent_livingroom_scene** (거실 일러스트) — 명세만, 승인 후 이미지 생성 툴로.
- (선택) 증거형 썸네일 6~10 실제 이미지.
- TTS 내레이션 녹음(final_narration_ko.md 기반).

## 6. 렌더 가능 여부
- **preview 스크립트 준비 완료**(`render_episode_02_preview.py`) — 컷 순서·타이밍 확인용 저해상 슬라이드쇼. **별도 승인 전 미실행.** ffmpeg는 ms-playwright 캐시에 존재.
- 완성본 렌더(TTS·BGM·자막 번인·전환)는 1차 편집 도구(별도 단계).

## 7. 검증 결과
| 항목 | 결과 |
|---|---|
| 공식 캡처 PNG 6개 참조 | ✓ |
| 자막 파일 생성 | ✓ (srt + md) |
| edit_timeline.json JSON 유효 | ✓ |
| official_evidence_timeline.json JSON 유효 | ✓ |
| 내레이션 파일 생성 | ✓ |
| 카드/에셋 목록·실제 카드 6개 | ✓ (C01만 명세) |
| 업로드 | 없음 ✓ |
| HTML·sitemap·배포 | 0 ✓ (sitemap 39) |
| UQ-02 approved/applied/published | 아님 ✓ (evidence_merged) |
| 비관련 파일 제외 | ✓ |

## 8. 다음 단계
1. c01 거실 장면 생성(승인 후) + TTS 녹음.
2. (승인) preview 렌더로 컷 타이밍 확인.
3. 1차 편집(전환·자막 번인·BGM) → 사람 검수 → 업로드(별도 승인).
4. 이 폴더 구조·스크립트는 다음 국가 편에 재사용(공장 라인).
