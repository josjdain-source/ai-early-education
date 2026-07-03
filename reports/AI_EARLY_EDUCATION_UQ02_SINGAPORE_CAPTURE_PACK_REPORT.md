# UQ-02 싱가포르 캡처팩 — 작업 보고

- 작성일: 2026-07-04
- 성격: **공식 자료 문구 검증 + 캡처 manifest.** 영상 제작·렌더·업로드·HTML·sitemap·배포 없음.
- 폴더: `assets/ai-early-education/singapore-evidence/`

## 0. 정직성 고지 (중요)
- 저(AI)는 외부 정부 페이지의 **진짜 스크린샷 PNG를 생성할 수 없습니다.** 임의로 이미지 파일을 만들면 그것은 '가짜 증거'가 되어 이 콘텐츠의 신뢰 원칙에 정면 위배됩니다.
- 그래서 이번 단계에서 **실제로 수행한 것 = 각 공식 URL을 열어 문구 존재 여부 검증(WebFetch, 2026-07-04)** + **manifest/지침 작성**.
- **실제 PNG 캡처는 브라우저 수동 단계**로 남김(`CAPTURE_INSTRUCTIONS.md`). manifest의 `capture_status=pending_manual`.

## 1. 생성한 파일
- `assets/ai-early-education/singapore-evidence/evidence_manifest.json` — 컷별 검증·메타
- `assets/ai-early-education/singapore-evidence/CAPTURE_INSTRUCTIONS.md` — 실제 캡처 지침
- (수정) `episode_02_singapore_visual_evidence_plan.md` — C07을 확인된 문장으로 교체
- (신규) 본 보고서
> 캡처 이미지(.png) 6종은 **아직 미생성**(pending_manual). 가짜 생성 안 함.

## 2. confirmed / partial / not_found 상태
| cut | 문구 검증 | 캡처 |
|---|---|---|
| C02 MOE AI in Education | **confirmed** | pending |
| C03 Students and Parents | **confirmed** | pending |
| C04 Age-progressive | **confirmed** | pending |
| C05 Parent's Guide | **confirmed** | pending |
| C06 SLS Guidance on GenAI | **confirmed** | pending |
| C07 책임 사용 문장 | **confirmed(문장 교체)** | pending |
| (C07 윤리 4원칙 전용 페이지) | **not_found (404)** | skip |

## 3. 실제 확인된 핵심 문구 (2026-07-04)
- C02: "Artificial intelligence in education" / "responsible and age- and developmental- appropriate use of AI" / "Learning Assistant ... Primary 4 students and above"
- C03: "...Responsible Use of GenAI for **Students and Parents** across Educational Levels"
- C04: "**Age-progressive** Framework"
- C05: "MOE has also provided parents with resources such as **'A Parent's Guide to Generative AI tools for Learning'**, which can be found on **Parents Gateway**."
- C06: "**Guidance on Generative AI**" / "**Singapore Student Learning Space (SLS)**"
- C07: "When used appropriately, these tools can support students in their learning when students have mastered basic concepts and thinking skills."

## 4. 영상에서 쓸 수 있는 컷
- **C02, C03, C04, C05, C06, C07** — 문구 confirmed. 캡처만 하면 사용 가능.
- 특히 **C03·C05가 핵심**('부모 포함'을 제목+실제 부모 가이드로 이중 증명).

## 5. 사용할 수 없는 컷과 이유
- **AIEd 윤리 4원칙 전용 페이지**: URL **404**(2026-07-04) → 원칙명(Agency·Inclusivity·Fairness·Safety) 화면 표기·인용 **금지**.
- **C06의 'responsible use'/'safe' 단어 하이라이트**: 해당 단어가 본문에 안 보임(URL 경로에만) → 단어 하이라이트 금지, 대신 C07의 확인된 문장 사용.
- **C02의 'Primary 4 and above'**: 학습보조도구(Learning Assistant) 한정 문구 → '초등 전체 규칙'처럼 일반화 금지.

## 6. 출처 표기 방식
- 각 컷: 일부 캡처 2~4초 + 핵심 문구 하이라이트 + 우측 한국어 요약 카드 + 하단 출처 카드("Singapore MOE/SLS · 확인일 2026-07-04 · 정책 변동 가능").
- 원문 장시간 노출·왜곡 크롭·의역 금지. 확인 안 된 문구 사용 금지.

## 7. 검증 결과
| 항목 | 결과 |
|---|---|
| C02~C07 캡처/상태 기록 완료 | ✓ (confirmed 6, not_found 1) |
| evidence_manifest.json JSON 유효 | ✓ |
| source_url·verification_date 기록 | ✓ |
| 확인된 문구만 highlight_text | ✓ |
| 확인 안 된 문구 단정 없음 | ✓ (4원칙 skip, responsible/safe 금지) |
| 영상 제작 / 업로드 / HTML / sitemap / 배포 | 0 ✓ |
| 가짜 PNG 생성 | 안 함 ✓ (pending_manual) |

## 7-B. 실제 Chrome 캡처 시도 결과 (2026-07-04)
- **한 것**: claude-in-chrome으로 C02·C03/C04 공식 페이지를 실제로 열어 **눈으로 확인**(WebFetch보다 강한 검증).
  - C02: 영어 원문 "Artificial intelligence in education" + "Singapore Government Agency Website" 배너 + "responsible and age- and developmental- appropriate use" 실견 ✅
  - C03/C04: 영어 원문 제목 "Developing Age-progressive Framework for Responsible Use of GenAI for **Students and Parents** across Educational Levels" + "Published on: 04 Nov 2025" 실견 ✅ (영상 허리 확보)
- **막힌 것 (2가지 환경 한계)**:
  1. 스크린샷 도구가 **repo 경로로 파일 저장을 못 함**(경로 미반환, temp/assets에 파일 없음) → 진짜 PNG를 assets 폴더에 자동 안착 불가.
  2. **Chrome 자동번역**이 본문을 한국어로 바꿔 원문 영어 캡처를 방해.
- **결정**: 3가지 장애(타임아웃·자동번역·저장경로 부재)에서 브라우저 강행 중단. **가짜 PNG는 만들지 않음.** capture_status=pending_manual 유지, 실제 저장은 사람 몫으로 남김.
- **manifest 반영**: C02/C03/C04에 `browser_view`(실견 내용) 기록.

## 8. 다음 단계
1. `CAPTURE_INSTRUCTIONS.md`대로 브라우저에서 C02~C07 실제 캡처(주소창 포함) → 이 폴더에 저장 → manifest `capture_status=captured`·`capture_date` 기록.
   - (원하시면 제가 사용자 Chrome을 구동해 캡처를 시도할 수 있음 — 별도 승인 시.)
2. 캡처 manifest 검수.
3. 대본 v2 타임코드에 캡처 삽입안 병합(별도 승인).
4. 이후 이미지/카드 에셋 → 1차 편집 → 사람 검수 → 업로드.
