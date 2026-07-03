# AI_EARLY_EDUCATION_COMPARE_REPORT

> 2026-07-03 · 기능화 5순위: compare.html = 국가 비교 + 부모용 길찾기 허브.
> 단순 표가 아니라, 방문자가 어디로 들어와도 다음 길이 생기는 관제탑. 지시 준수: 특정 AI 서비스 추천·공포 마케팅·유료/상품/쿠팡/영상/유튜브·아이 혼자 사용 권장 없음. 국가 사실은 기존 자료만(즉흥 생성 없음). JS 없이 정적 카드 UI.

## 1. 생성한 URL
- `/ai-early-education/compare.html` — “우리 아이 AI 교육 시작점 찾기: 9개국 사례로 보는 비교 가이드”
- 부제: “아이의 나이, 부모의 역할, 학교 준비 정도에 따라 AI 조기교육의 시작점은 달라진다.”

## 2. 수정한 파일
- 신규: `ai-early-education/compare.html`, `reports/이 파일`
- `ai-early-education/index.html` — 세계 분석 섹션 대표 버튼 ‘🧭 우리 아이 AI 교육 시작점 찾기’(primary, 부모 입구 맨 앞).
- `for-parents.html`·`age-guide.html`·`home-experiments.html`·`parent-rules.html` — ‘다음 읽을 글’ 최상단에 compare 링크(4개 부모 페이지 모두).
- 생성기(`build_global_analysis.py`) 수정 후 재생성 → `global-matrix.html`·`models.html` 하단 keyline에 compare 링크.
- `sitemap.xml` — compare URL 추가(총 28).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.

## 3. compare 핵심 메시지
- AI 조기교육에는 하나의 정답 루트가 없다. 9개국을 보면 나이·보호자 동반·교사 준비·윤리 규칙에 따라 시작 방식이 다르다.
- 한국 부모에게 필요한 건 남들보다 빨리가 아니라 **우리 아이에게 맞는 안전한 시작점**.
- 현실 순서 한 줄: **약속 → 나이에 맞는 방향 → 작은 실험**(빨리가 아니라, 안전하게 그리고 함께).

## 4. 상황별 추천 경로 6개 (JS 없는 정적 카드)
1. 🧸 아이가 아직 어리다 → age-guide · parent-rules · finland · singapore
2. 🧪 초등학생과 집에서 → home-experiments · 3편(ai-conversation) · for-parents
3. 🛡️ 안전 먼저 → parent-rules · uk · china · global-matrix
4. 🏫 학교 AI 교육 궁금 → 2편(korea-controversy) · countries/korea · japan · models
5. 🌍 세계 흐름 비교 → global-matrix · models · countries/
6. 📝 중학생+ 과제 활용 걱정 → parent-rules · age-guide · uk
+ 4가지 질문 카드(나이/시간/필요/경험)로 방향 잡기, 9개국 한눈 요약(→매트릭스 유도), 6모델 요약(→models 유도).

## 5. 기존 부모 안내축과 연결한 방식
- compare = 5축(분석·해석·연령·실험·안전)의 **진입 라우터**. 6개 경로가 각 축의 페이지로 분기.
- 역방향: 대문 대표 버튼 + 4개 부모 페이지(for-parents·age-guide·home-experiments·parent-rules) 다음글 + 매트릭스·모델 하단에서 compare로 유입.
- 방문자가 어느 페이지로 들어와도 compare를 거쳐 자기 상황의 다음 길을 찾음 → ‘미로’가 아니라 ‘관제탑’.

## 6. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 7. 검증 결과 (11/11)
- 로컬 200 / 라이브 200: compare·대문·4부모페이지·매트릭스·모델·sitemap
- 내부 링크: 필수 13개 전부(countries/는 디렉토리 링크로 200), 깨짐 0
- sitemap: 28 URL, XML 유효
- 모바일: 본문 max-width 840, `.qgrid`/`.models`(모바일 1열)·`.route` 카드형, JS 없이 읽힘
- 광고성 CTA: 없음
- 특정 AI 서비스 추천: 없음(서비스명 0회)
- 영상/유튜브/상품 파일 생성: 없음
- 기존 페이지: 무손상(부모 페이지·매트릭스·모델은 링크만 추가)
- patch_log·working tree: 기능화 세트만 커밋

## 사이트 구조(현재)
데이터베이스 → 해석 → 연령별 안내 → 실험 → 안전 규칙 → **개인별 시작점 찾기(compare)**.

## 다음 기능화 후보
- `checklist.html`(AI 대화 실험 전 부모 체크리스트, 실사용성↑) 또는 `source-library.html`(출처 라이브러리).
- 판단: compare 다음은 checklist가 실사용성이 더 강함.
