# AI_EARLY_EDUCATION_INDEX_REDESIGN_REPORT

> 2026-07-03 · 대문(index.html)을 단순 링크 목록 → **AI 조기교육 관제판**으로 개편.
> 페이지가 많아진 사이트에서 방문자가 “나는 어디부터 봐야 하지?”를 바로 고르게 만드는 첫 화면.
> 지시 준수: 영상/유튜브/상품/쿠팡 언급 없음. JS 없이 정적. 기존 링크 무손상.

## 0. URL 오타 확인(선행 요청)
- 결과: **잘못된 URL 표기 없음.** reports·projects.json·patch_log 전체에서 `https://ai-early-education/`(.pages.dev 누락) 형태 0건.
- checklist 보고서는 상대경로 `/ai-early-education/checklist.html`(정상)을 사용. 실제 라이브 URL = `https://ai-early-education.pages.dev/ai-early-education/checklist.html`(200 검증됨). 수정 불필요.

## 1. 수정한 파일
- `ai-early-education/index.html` — 전면 개편(관제판).
- `reports/AI_EARLY_EDUCATION_INDEX_REDESIGN_REPORT.md` — 신규.
- 조종판 `projects.json` status·next 갱신 · `patch_log.json` 기록.
- `sitemap.xml` — 미수정(신규 URL 없음, index lastmod 이미 2026-07-03).

## 2. 대문 구조(7섹션)
1. **Hero** — “AI 조기교육, 어디서부터 시작해야 할까?” + 부제 + 대표 CTA 3개.
2. **부모가 바로 쓰는 가이드**(4카드) — 시작 가이드 / 연령별 / 실험 10가지 / 7가지 약속.
3. (포지션 문장) — “AI 조기교육은 프로그램이 아니라 말하고·관찰·다시 요청하는 경험”(UNESCO 근거).
4. **세계 분석**(3카드) — 매트릭스 / 모델 비교 / 국가별.
5. **국가별 빠른 이동** — 9개국 플래그 카드(모델 한 줄 캡션 포함).
6. **핵심 시리즈 글** — 1·2·3편.
7. **이 사이트, 어떻게 쓰면 좋을까** — 방문자별 4경로 + **다음 확장 예고**.

## 3. 대표 CTA 3개 (첫 화면 노출)
- 🧭 우리 아이 시작점 찾기 → `compare.html`
- 🧪 집에서 해볼 실험 10가지 → `home-experiments.html`
- 🧷 시작 전 체크리스트 → `checklist.html`

## 4. 방문자별 추천 경로
- 🌱 처음 온 부모: compare → for-parents → checklist
- 📶 아이 나이 궁금: age-guide → home-experiments
- 🛡️ 안전 걱정: parent-rules → checklist
- 🌍 세계 흐름 궁금: global-matrix → models → countries

## 5. 관제판 역할 정리
대문=길 안내판 · compare=라우터 · for-parents=해석 · age-guide=나이별 · home-experiments=실행 · parent-rules=안전 · checklist=출발 전 확인 · global-matrix/models/countries=근거.

## 6. SEO 개선
- title: `AI 조기교육 가이드 | 세계 9개국 비교와 부모 실전 시작법`
- description: `AI 조기교육을 어디서 시작해야 할지 고민하는 부모를 위해 세계 9개국 AI 교육 사례, 연령별 가이드, 집에서 해볼 실험, 안전 체크리스트를 정리했습니다.`
- og:title/description도 관제판 메시지로 갱신.

## 7. 다음 확장 예고(대문 노출)
- 부모 체크리스트 인쇄본 · 출처 라이브러리 · 학교·가정 비교. (영상/유튜브/상품 예고 없음)

## 8. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 9. 검증 결과 (9/9)
- 로컬 200 / 라이브 200: 대문
- 대문 주요 링크: 23개 대상 전부 200(깨짐 0)
- 첫 화면 CTA 3개(compare·home-experiments·checklist) 노출
- 모바일: 카드 grid 반응형(4→2→1열), 플래그 3→2열, 경로 2→1열
- 영상/유튜브/상품/쿠팡 언급: 없음
- 기존 페이지: 무손상(대문만 개편, 타 페이지 링크 그대로)
- SEO title/description 개선
- patch_log·working tree: 개편 세트만 커밋

## 다음 후보
- `source-library.html`(출처 라이브러리) 또는 학교·가정 비교 페이지.
