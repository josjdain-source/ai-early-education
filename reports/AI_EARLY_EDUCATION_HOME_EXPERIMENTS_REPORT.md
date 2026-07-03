# AI_EARLY_EDUCATION_HOME_EXPERIMENTS_REPORT

> 2026-07-03 · 기능화 3순위: 집에서 해볼 AI 대화 실험 10가지. 사이트를 ‘읽고 끝’에서 ‘오늘 30분 해봄’으로.
> 지시 준수: 특정 AI 서비스 추천·아이 혼자 사용 권장·개인정보 입력 유도·유료/상품/쿠팡/영상/유튜브·공포 마케팅·성과 과장 없음. 국가 사실은 기존 자료만.

## 1. 생성한 URL
- `/ai-early-education/home-experiments.html` — “집에서 해볼 수 있는 AI 대화 실험 10가지”
- 부제: “AI 조기교육은 거창한 수업이 아니라, 아이가 말하고 관찰하고 다시 요청해보는 작은 실험에서 시작된다.”

## 2. 수정한 파일
- 신규: `ai-early-education/home-experiments.html`, `reports/이 파일`
- `ai-early-education/index.html` — 세계 분석 섹션 버튼에 ‘🧪 집에서 해볼 AI 대화 실험 10가지’ 추가(부모/연령별 옆).
- `ai-early-education/for-parents.html` — ‘다음 읽을 글’에 home-experiments 링크.
- `ai-early-education/age-guide.html` — ‘다음 읽을 글’ 최상단에 home-experiments 링크.
- `sitemap.xml` — home-experiments URL 추가(총 26).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.
- (생성기 수정 불필요 — 이번 필수 링크는 전부 비생성 페이지에서 나감)

## 3. 실험 10가지 목록
1. 이상한 동물 만들기(상상·수정) 2. 우리 가족 캐릭터 만들기(비식별 표현) 3. 같은 요청 다르게 말하기(결과 비교) 4. 마음에 안 드는 결과 고치기(피드백) 5. 이야기 이어 만들기(상상 이어가기) 6. 그림 보고 설명하기(관찰) 7. AI가 틀린 답 찾기(의심) 8. 역할 바꿔보기(의도 표현) 9. 현실 만들기 연결(화면 밖으로) 10. 오늘의 AI 사용 기록(돌아보기)

## 4. for-parents·age-guide와 연결한 방식
- 3층 부모 입구 완성: for-parents(어디서 시작) → age-guide(나이별) → home-experiments(오늘 뭘). 서로의 ‘다음 읽을 글’에 상호 배치.
- 대문에 버튼 3개(부모/연령별/실험) 나란히 노출.
- home-experiments 기본 순서 6걸음 = 3편 5단계 + ‘기록’, age-guide 연령 원칙과 정합.

## 5. 연령별 추천 구조
- 유아: 1·5·6(부모 조작, 아이는 상상·말하기)
- 초등 저학년: 1·3·4·6·9(부모와 함께)
- 초등 고학년: 3·4·7·8·10(결과 비교·수정)
- 중학생 이상: 7·8·10(출처·윤리·자기 생각 구분)
- + 실험 전 5약속 + 부모가 대신하면 안 되는 것 + 실험 후 질문 5개.

## 6. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 7. 검증 결과 (10/10)
- 로컬 200 / 라이브 200: home-experiments·for-parents·age-guide·대문·sitemap
- 내부 링크: 필수 7개(for-parents·age-guide·3편·matrix·models·singapore·korea) 전부, 깨짐 0
- sitemap: 26 URL, XML 유효
- 모바일: 본문 max-width 800, `.exp`/`.agegrid`(모바일 1열) 카드형
- 광고성 CTA: 없음
- 개인정보 입력 유도: 없음(실험 2는 ‘비식별 요소로’ + ‘개인정보 넣지 않는다’ 명시)
- 특정 서비스명: 0회
- 영상/유튜브/상품 파일 생성: 없음
- patch_log·working tree: 기능화 세트만 커밋

## 다음 기능화 후보
- `parent-rules.html` — “아이와 AI를 쓸 때 부모가 반드시 정해야 할 7가지 약속”(안전·윤리 검색 유입).
- 이후 `compare.html`(국가 비교 필터)·`source-library.html`(출처 라이브러리).
