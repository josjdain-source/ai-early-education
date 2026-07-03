# AI_EARLY_EDUCATION_SOURCE_LIBRARY_REPORT

> 2026-07-03 · 신뢰성 장치: 출처 라이브러리. 이 사이트가 ‘말 잘하는 블로그’가 아니라 ‘출처를 들고 분석하는 작은 연구소’임을 보여주는 페이지.
> 지시 준수: 새 사실 생성 없음(기존 sources.html/matrix 재사용), 미확인 항목 정직 표기, 영상/유튜브/상품/쿠팡·특정 서비스·광고성 CTA 없음.

## 1. 생성한 URL
- `/ai-early-education/source-library.html` — “AI 조기교육 출처 라이브러리: 세계 9개국 분석은 어떤 자료를 바탕으로 했나”
- 부제: “UNESCO, 각국 교육부, 교사 가이드, 정책 문서, 언론 보도를 구분해 정리했습니다.”

## 2. 수정한 파일
- 신규: `ai-early-education/source-library.html`, `reports/이 파일`
- `ai-early-education/index.html` — 세계 분석 섹션 아래 ‘출처 라이브러리’ 안내 링크.
- 생성기(`build_global_analysis.py`) 수정 후 재생성 → `global-matrix.html`·`models.html`·`countries/index.html` 하단에 source-library 링크(산출물).
- `sitemap.xml` — source-library URL 추가(총 30).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.
- `sources.html` — **미수정(무손상)**: 원자료 목록 그대로 유지.

## 3. 출처 라이브러리 구조(7섹션)
1. 왜 출처 라이브러리가 필요한가.
2. 출처를 읽는 기준 — 5유형 배지 카드(공식/국제기구/교사·학생 가이드/언론/미확인).
3. 핵심 기준 출처 — UNESCO 2건 · 각국 교육부 예 · 시험·평가 기관(JCQ).
4. 국가별 출처 묶음 — 9개국 각 대표 출처 2건 + 상세 페이지 링크.
5. 이 사이트에서 출처를 사용하는 방식 — matrix/countries/models/부모 가이드.
6. 미확인 항목 처리 원칙 5가지.
7. 원자료 전체 보기 → sources.html.

## 4. sources.html과 역할 분리
- **sources.html = 원자료/출처 목록**(170여 건, 미확인 포함) — 그대로 유지·무손상.
- **source-library.html = 사람이 읽는 해설 허브** — 유형·국가·활용 목적별로 구분해 “왜 이 자료가 근거인가”를 설명하고, 상세/원자료로 유도.
- 즉 라이브러리는 목록을 대체하지 않고 그 앞단의 ‘읽는 층’.

## 5. 국가별 출처 묶음 처리 방식
- 9개국 각각: 한 줄 요약 + 대표 공식/언론 출처 2건(전부 기존 sources.html/matrix에서 재사용) + 상세 페이지 링크.
- 미확인이 있는 나라는 요약에 명시(핀란드 초등 전국 연령선 미확인, 인도 초등 생성형 AI 규정 미확인 등).
- 전체 6건씩·170건은 각 상세 페이지·sources.html로 유도(중복 재게시 회피).

## 6. 미확인 항목 처리 원칙
- 공식 문서 우선 / 보도만 있으면 그렇게 표시 / 확인일 표기 / 추측으로 안 채움(‘미확인’) / 부모용은 번역이 아니라 가정 행동으로 해석임을 밝힘.

## 7. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 8. 검증 결과 (11/11)
- 로컬 200 / 라이브 200: source-library·대문·매트릭스·모델·countries 허브·sitemap
- 내부 링크: 필수 6개(sources·matrix·models·countries·compare·for-parents) 전부 + 9개국 상세, 깨짐 0
- 외부 출처 링크: 25건(전부 기존 검증 자료)
- sitemap: 30 URL, XML 유효
- 모바일: 본문 max-width 820, 유형 카드·국가 카드 반응형(모바일 1열)
- 기존 sources.html: 무손상(변경 0)
- 국가별 출처 링크: 정상(각 상세로 연결)
- 광고성 CTA·특정 서비스: 없음
- 영상/유튜브/상품 파일 생성: 없음
- patch_log·working tree: 신뢰성 세트만 커밋

## 다음 후보
- `school-vs-home.html`(학교 AI 교육 vs 가정 AI 교육 — 제도/교사/평가/공정성 ↔ 대화/관찰/안전한 작은 실험).
- 이후 부모 체크리스트 인쇄본 정리.
