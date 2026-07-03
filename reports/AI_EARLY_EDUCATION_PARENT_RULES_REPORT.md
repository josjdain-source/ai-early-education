# AI_EARLY_EDUCATION_PARENT_RULES_REPORT

> 2026-07-03 · 기능화 4순위: 안전·윤리 축. home-experiments가 “해보자”라면 parent-rules는 “이 선을 넘지 말자”.
> 실험 페이지를 안정적으로 세우는 안전 난간. 지시 준수: 특정 AI 서비스 추천·공포 마케팅·유료/상품/쿠팡/영상/유튜브·아이 혼자 사용 권장·과도한 법률 자문 없음. ‘무조건 금지’ 아니라 ‘보호자와 함께 안전하게’. 국가 사실은 기존 자료만.

## 1. 생성한 URL
- `/ai-early-education/parent-rules.html` — “아이와 AI를 쓸 때 부모가 반드시 정해야 할 7가지 약속”
- 부제: “AI 조기교육의 안전은 차단이 아니라, 아이와 함께 정한 사용 규칙에서 시작된다.”

## 2. 수정한 파일
- 신규: `ai-early-education/parent-rules.html`, `reports/이 파일`
- `ai-early-education/index.html` — 세계 분석 섹션 버튼에 ‘🛡️ 부모가 정해야 할 7가지 약속’ 추가(부모 입구 버튼 4개째).
- `ai-early-education/home-experiments.html` — ‘실험 전 5가지 약속’ 섹션 상단에 parent-rules 안내(실험 전에 읽는 안전 가이드로 연결).
- `ai-early-education/for-parents.html`·`age-guide.html` — ‘다음 읽을 글’에 parent-rules 링크.
- `sitemap.xml` — parent-rules URL 추가(총 27).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.
- (생성기 수정 불필요 — 필수 링크 전부 비생성 페이지에서 나감)

## 3. 7가지 약속 목록
1. 혼자 쓰지 않기(유아·초등 저학년은 보호자와 함께) 2. 개인정보 넣지 않기(이름·학교·얼굴·주소·전화·친구·가족) 3. AI가 틀릴 수 있음을 알기(정답 아닌 ‘확인할 초안’) 4. 결과를 그대로 제출하지 않기(자기 생각과 AI 구분) 5. 이상한 답이 나오면 멈추고 말하기 6. AI에게 분명하게 말하기(설명하고 다시 요청) 7. 사용 후 한 줄 기록하기

## 4. home-experiments와 연결한 방식
- 역할 분담: home-experiments=“해보자”, parent-rules=“이 선을 넘지 말자”. 실험 페이지의 ‘실험 전 약속’ 섹션 상단에서 parent-rules로 유도 → 실험 시작 전 안전 가이드로 자리매김.
- parent-rules 6번 섹션에 ‘실험 전 체크리스트’(5항목 ☐) 배치 → home-experiments로 되돌려 보냄.
- 양방향: 실험 전엔 parent-rules를 읽고, parent-rules 끝에서 실험으로.

## 5. 세계 사례 → 안전 규칙 전환
- 혼자 안 둠: UNESCO 13세·싱가포르 초1~3 미사용·영국 13세 미만 학부모 동의 → 약속 1.
- 나이에 맞게 제한: 중국 초등 단독 사용 금지·에스토니아 고교부터 → 세계 원칙 2.
- 어른 먼저: 에스토니아 교사 먼저·싱가포르 부모 가이드 배포 → 원칙 3.
- 그대로 안 믿기: 영국 시험 출처 표기·할루시네이션 명시 → 약속 3·원칙 4.

## 6. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 7. 검증 결과 (11/11)
- 로컬 200 / 라이브 200: parent-rules·home-experiments·for-parents·age-guide·대문·sitemap
- 내부 링크: 필수 9개(home-experiments·for-parents·age-guide·matrix·models·singapore·china·uk·3편) 전부, 깨짐 0
- sitemap: 27 URL, XML 유효
- 모바일: 본문 max-width 790, `.rule`/`.promise`/`.check` 카드형
- 광고성 CTA: 없음
- 특정 AI 서비스 추천: 없음(서비스명 0회)
- 개인정보 입력 유도: 없음(오히려 ‘넣지 않기’가 약속 2)
- 과도한 법률 자문: 회피(‘법률 자문이 아닙니다’ 명시), ‘차단이 아니라 보호자와 함께 안전하게’ 톤
- 영상/유튜브/상품 파일 생성: 없음
- patch_log·working tree: 기능화 세트만 커밋

## 사이트 5축 완성
분석(세계) · 해석(부모 시작) · 연령(나이별) · 실험(오늘 뭘) · **안전(어떤 약속)**.

## 다음 기능화 후보
- `compare.html`(국가 비교 필터, “우리 아이 AI 교육 시작점 찾기”) 또는 `parent-checklist.html`.
- `source-library.html`(출처 라이브러리 정리).
