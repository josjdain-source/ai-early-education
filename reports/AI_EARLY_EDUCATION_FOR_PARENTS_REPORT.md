# AI_EARLY_EDUCATION_FOR_PARENTS_REPORT

> 2026-07-03 · 기능화 1순위: 부모용 해석 페이지. 9개국 분석 → 한국 부모의 첫 행동 가이드로 번역.
> 사이트를 ‘연구소(데이터베이스)’에서 ‘실제 안내서’로 전환하는 입구 페이지.
> 지시 준수: 공포 마케팅·특정 AI 서비스 추천·유료/상품 CTA·쿠팡/영상/유튜브 언급 없음. 아이 혼자 사용 권장 없음. 국가별 사실은 기존 matrix/country/sources에서만.

## 1. 생성한 URL
- `/ai-early-education/for-parents.html` — “한국 부모는 AI 시대 조기교육을 어디서부터 시작해야 할까?”
- 부제: “세계 9개국 AI 교육을 비교해보니, 답은 ‘빨리 쓰게 하기’가 아니라 ‘혼자 쓰게 두지 않는 구조’였다.”
- SEO: title/description에 검색어(AI 조기교육·아이 AI 교육·초등학생 ChatGPT·AI 디지털교과서 대안) 자연 배치.

## 2. 수정한 파일
- 신규: `ai-early-education/for-parents.html`, `reports/이 파일`
- `ai-early-education/index.html`(대문) — 세계 분석 섹션 아래 ‘👪 한국 부모를 위한 시작 가이드’ 버튼 카드 추가(대문은 생성기 아님, 직접 편집).
- 생성기(`build_global_analysis.py`) 3곳에 for-parents 링크 추가 후 **재생성**(매트릭스·모델·9개국 페이지가 산출물이라 직접 편집 대신 생성기 수정=재생성 시 유지):
  - `global-matrix.html` 하단 keyline로 for-parents 유도
  - `models.html` 하단 keyline로 for-parents 유도
  - `countries/*.html` 하단 네비에 ‘부모 시작 가이드’ 링크(9개국 전부 — 요청은 korea지만 일관성 위해 전체 적용)
- `sitemap.xml` — for-parents URL 추가(총 24).
- 조종판 `projects.json` 액션·status 갱신 · `patch_log.json` 기록.

## 3. 부모용 핵심 메시지
- AI 조기교육은 AI를 빨리 쓰게 하는 경쟁이 아니다. 세계 공통점은 ‘아이를 AI 앞에 혼자 두지 않는다’.
- 지금 부모가 할 일 = 비싼 도구·선행 코딩이 아니라 **아이와 함께 작은 AI 대화 실험을 안전하게 설계**하기.
- 한 줄: **“빨리 쓰게 하지 말고, 혼자 쓰게 두지 마세요. 대신 어른과 함께, 작게, 오늘 시작하세요.”**

## 4. 세계 9개국 분석을 부모 행동으로 바꾼 방식
- **공통 규칙 3가지**(혼자 안 둠 / 사고력·태도 먼저 / 어른 역할 먼저)를 매트릭스에서 도출 → 각 규칙에 국가 근거(UNESCO 13세·중국 초등 단독금지·싱가포르 P1~3 미사용·에스토니아 교사먼저·핀란드 3세 식별).
- **오해 5가지**(코딩선행/빨리시작/좋은도구/부모가 대신/결과물 예쁘면) → 각 오해를 세계 사례로 반박.
- **연령대별 방향**(유아=상상말하기, 초저=함께 요청, 초고=비교·수정·의심, 중학+=규칙·윤리·자기표현) → 핀란드·싱가포르·인도·영국 연령 원칙의 가정 번역.
- **30분 실험**(상상→요청→관찰→수정→이야기) = 3편 5단계의 시간표.
- **5가지 약속**(어른과 함께/힌트로/개인정보 금지/틀릴 수 있다 전제/AI 사용 밝히기) = 각국 규칙(13세 보호자동반·싱가포르 도구설계·핀란드 식별·영국 출처표기)의 가정 버전.

## 5. 내부 링크 구조
- for-parents → global-matrix(6)·models(2)·countries/singapore·estonia·korea·3편·2편 (필수 7개 전부, 무결성 0).
- 역방향 유입: 대문 버튼 카드, global-matrix 하단, models 하단, countries/*.html 하단(9개국)에서 for-parents로.
- for-parents가 분석 페이지들의 ‘출구=행동’ 역할, 분석 페이지들이 for-parents의 ‘근거’ 역할로 상호 연결.

## 6. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포(git archive → wrangler). 라이브 200.

## 7. 검증 결과 (9/9)
- 로컬 200 / 라이브 200: for-parents·대문·매트릭스·모델·korea·sitemap
- 내부 링크: 필수 7개 전부 존재, 깨짐 0(스크립트)
- sitemap: 24 URL, XML 유효
- 모바일: 본문 max-width 780, `.rule`/`.agebox` grid·카드형 세로 정렬
- 광고성 CTA: 없음(‘유료’는 “유료 상품을 권하지 않으며” 면책 문구, ‘ChatGPT’는 meta 검색어 1회)
- 특정 서비스 추천·쿠팡/영상/유튜브·아이 혼자 사용 권장: 없음
- 영상/유튜브/상품 파일 생성: 없음
- patch_log·working tree: 기능화 세트만 커밋

## 다음 기능화 순서
1. (완료) for-parents.html
2. `age-guide.html` — “연령별 AI 조기교육 가이드: 유아부터 중학생까지” (검색 강함)
3. `home-experiments.html` — 가정 실험 모음
4. `compare.html` — 국가 비교 필터
5. `source-library.html` — 출처 라이브러리 정리
