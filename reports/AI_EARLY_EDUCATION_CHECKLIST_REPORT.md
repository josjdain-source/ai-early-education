# AI_EARLY_EDUCATION_CHECKLIST_REPORT

> 2026-07-03 · 기능화 6순위: checklist.html = 실행 직전 안전벨트. home-experiments(무엇을)·parent-rules(무엇을 지킬까) 사이의 “지금 켜기 전에 뭘 확인할까”.
> 지시 준수: 특정 AI 서비스 추천·공포 마케팅·유료/상품/쿠팡/영상/유튜브·아이 혼자 사용 권장·과도한 법률 자문 없음. parent-rules와 충돌 없음. 국가 사실 신규 생성 없음. JS 없이 작동·인쇄 친화.

## 1. 생성한 URL
- `/ai-early-education/checklist.html` — “AI 대화 실험 전 부모 체크리스트”
- 부제: “아이와 AI를 시작하기 전, 5분만 확인하면 실험이 훨씬 안전하고 교육적으로 바뀐다.”

## 2. 수정한 파일
- 신규: `ai-early-education/checklist.html`, `reports/이 파일`
- `ai-early-education/index.html` — 부모 입구 버튼에 ‘🧷 실험 전 부모 체크리스트’ 추가(6개째).
- `ai-early-education/home-experiments.html` — 실험 전 약속 안내 문장에 checklist 링크(실행 직전 연결).
- `ai-early-education/parent-rules.html` — ‘다음 읽을 글’ 최상단에 checklist.
- `ai-early-education/compare.html` — 경로 ②(초등학생과 집에서)에 checklist 링크.
- `sitemap.xml` — checklist URL 추가(총 29).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.
- (생성기 수정 불필요 — 필수 링크 전부 비생성 페이지에서 나감)

## 3. 체크리스트 핵심 메시지
- AI 실험은 도구를 켜는 순간이 아니라, 부모가 **목적·시간·개인정보·역할·기록 방식**을 정하는 순간 시작된다.
- 체크리스트는 아이를 통제하는 문서가 아니라, **함께 안전하게 실험하기 위한 약속표**(규정 아님, 5분 확인).

## 4. 실험 전/중/후 체크 항목 요약(체크박스 ☐, 총 24항목)
- **전(6):** 목적 한 문장 / 10~30분 / 보호자 동반 / 개인정보 금지 / “틀릴 수 있음” 예고 / 오늘 목표=‘다시 말해보기’.
- **중(5):** 부모가 대신 다 안 써줌 / 좋은·아쉬운 점 말하기 / 결과 같이 살펴보기 / 멈출 준비 / ‘다시 요청’ 1회 이상.
- **후(5):** 무엇을 요청했나 / 무엇이 예상과 달랐나 / 다음엔 어떻게 말할지 한 줄 / AI 도움과 내 생각 구분 / 시간 안 길어짐.
- **연령별(4):** 유아=말하기·고르기 / 초저=함께 수정 요청 / 초고=비교·틀린 정보 찾기 / 중학+=출처·윤리·표시.
- + 아이에게 설명하는 말 4개.

## 5. parent-rules·home-experiments와 연결한 방식
- 3종 세트 완성: home-experiments(무엇을 해볼까) → parent-rules(무엇을 지킬까) → **checklist(지금 켜기 전 뭘 확인할까)**.
- checklist는 parent-rules의 요약 실행판(충돌 없이 재사용): 약속을 실행 시점 확인표로 변환.
- 역방향 유입: 대문 버튼 + home-experiments 실험 전 안내 + parent-rules 다음글 + compare 경로②.
- 인쇄 친화: `@media print`로 nav/footer/버튼 숨김, 체크 항목만 깔끔히 출력(냉장고에 붙여 쓰기).

## 6. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 7. 검증 결과 (12/12)
- 로컬 200 / 라이브 200: checklist·대문·home-experiments·parent-rules·compare·sitemap
- 내부 링크: 필수 6개 전부, 깨짐 0
- sitemap: 29 URL, XML 유효
- 모바일: 본문 max-width 780, `.cl` 카드형·`.check` 체크박스 UI 깨짐 없음
- 체크박스/카드 UI: ☐ 정상, 4블록 24항목
- 광고성 CTA: 없음
- 특정 AI 서비스 추천: 없음(서비스명 0회)
- 영상/유튜브/상품 파일 생성: 없음
- 기존 페이지: 무손상(링크만 추가)
- patch_log·working tree: 기능화 세트만 커밋

## 부모 실사용 3종 세트 완성
실험 아이디어(home-experiments) → 안전 약속(parent-rules) → 실행 체크리스트(checklist).

## 다음 후보
- 판단: checklist 다음은 **대문(index) 개편** — 페이지가 많아졌으니 첫 화면을 핵심 경로로 재정리(또는 source-library.html).
