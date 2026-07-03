# AI_EARLY_EDUCATION_AGE_GUIDE_REPORT

> 2026-07-03 · 기능화 2순위: 연령별 가이드. for-parents가 “어디서 시작하나”라면 age-guide는 “우리 아이 나이엔 무엇을?”.
> 지시 준수: 특정 AI 서비스 추천·‘몇 살부터 특정 도구’ 단정·아이 혼자 사용 권장·공포 마케팅·유료/상품/쿠팡/영상/유튜브 없음. 국가 사실은 기존 matrix/country/sources에서만.

## 1. 생성한 URL
- `/ai-early-education/age-guide.html` — “연령별 AI 조기교육 가이드: 유아부터 중학생까지 무엇이 달라야 할까?”
- 부제: “AI를 빨리 쓰게 하는 것이 아니라, 나이에 맞게 상상·대화·관찰·수정의 깊이를 다르게 설계해야 한다.”
- SEO: title/description에 검색어(유아 AI 교육·초등학생 AI 교육·초등 저학년 ChatGPT·중학생 AI 활용·연령별 AI 조기교육) 배치.

## 2. 수정한 파일
- 신규: `ai-early-education/age-guide.html`, `reports/이 파일`
- `ai-early-education/index.html`(대문) — 세계 분석 섹션 버튼에 ‘📶 연령별 가이드’ 추가(for-parents 옆, 대문은 생성기 아님).
- `ai-early-education/for-parents.html` — ‘다음 읽을 글’ 최상단에 age-guide 링크(직접 편집).
- 생성기(`build_global_analysis.py`) 매트릭스 하단 keyline에 age-guide 추가 후 **재생성**(global-matrix가 산출물이라 생성기 수정=재생성 시 유지).
- `sitemap.xml` — age-guide URL 추가(총 25).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.

## 3. 연령별 핵심 메시지
- 나이가 어릴수록 도구 사용보다 **상상·언어 표현**이 먼저, 올라갈수록 **결과 비교·수정 요청·출처 의심·윤리적 사용**으로 확장.
- 중요한 건 “몇 살부터 쓰느냐”가 아니라 “**어른이 어떤 구조 안에서 함께 쓰게 하느냐**”.
- 4단계: 유아(직접 사용 아님·상상 말하기, 부모가 조작/아이는 선택·설명) → 초등 저학년(함께 요청·관찰·개인정보 금지·혼자 금지) → 초등 고학년(다르게 말해보기·결과 비교·틀린 정보 찾기·그대로 안 믿기) → 중학생+(과제 윤리·출처 확인·AI 사용 표시·자기 생각과 구분).

## 4. for-parents와 연결한 방식
- 도입부에서 “for-parents=어디서 시작 / age-guide=우리 아이 나이엔?”로 역할을 명확히 구분·상호 링크.
- for-parents ‘다음 읽을 글’ 최상단 → age-guide. age-guide ‘다음 읽을 글’ 최상단 → for-parents. 두 부모 입구가 서로를 물어 순환.
- 대문 버튼 2개(부모 시작 / 연령별)로 나란히 노출.

## 5. 세계 사례 → 연령별 행동 전환
- 유아: 핀란드(3세 비판적 읽기)·인도(초등 펜·종이) → ‘직접 사용보다 상상·놀이’.
- 초등 저학년: 싱가포르(초1~3 미사용, 초4 교사 감독)·한국(13세 미만 보호자 동의) → ‘보호자와 함께’.
- 초등 고학년: 3편(관찰·다시 요청) → ‘비교·수정·의심’.
- 중학생+: 영국(시험 AI 출처 표기) → ‘윤리·출처·자기표현’.
- 연령 무관 5약속 + 연령별 30분 실험 카드(유아·저·고·중학)로 행동화.

## 6. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포(git archive → wrangler). 라이브 200.

## 7. 검증 결과 (9/9)
- 로컬 200 / 라이브 200: age-guide·for-parents·대문·매트릭스·sitemap
- 내부 링크: 필수 7개(for-parents·matrix·models·singapore·uk·finland·3편) 전부, 깨짐 0
- sitemap: 25 URL, XML 유효
- 모바일: 본문 max-width 800, `.stage`/`.rule`/`.expcard` 카드형 세로 정렬
- 광고성 CTA: 없음(‘유료’·‘특정 AI 서비스’는 면책 문구)
- ‘몇 살부터 특정 도구’ 단정·아이 혼자 사용 권장: 없음
- 영상/유튜브/상품 파일 생성: 없음
- patch_log·working tree: 기능화 세트만 커밋

## 다음 기능화 후보
1. (완료) for-parents.html
2. (완료) age-guide.html
3. `home-experiments.html` — 집에서 해볼 AI 대화 실험 10가지(실사용성↑)
4. `compare.html` — 국가 비교 필터
5. `source-library.html` — 출처 라이브러리
