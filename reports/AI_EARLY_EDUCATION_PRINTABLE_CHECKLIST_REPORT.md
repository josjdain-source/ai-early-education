# AI_EARLY_EDUCATION_PRINTABLE_CHECKLIST_REPORT

> 2026-07-03 · 사용성 강화: 인쇄용 한 장 체크리스트. ‘읽는 사이트’ → ‘들고 쓰는 사이트’. 비행 전 점검표처럼 냉장고·책상에 붙여 쓰는 A4 실행 도구.
> 지시 준수: JS 없이 정적 · 특정 서비스·유료/상품/쿠팡/영상/유튜브·광고성 CTA·개인정보 유도 없음.

## 1. 생성한 URL
- `/ai-early-education/printable-checklist.html` — “AI 대화 실험 전 부모 체크리스트: 인쇄용 한 장”
- 부제: “아이와 AI를 켜기 전, 목적·시간·개인정보·역할·기록을 함께 확인하세요.”

## 2. 수정한 파일
- 신규: `ai-early-education/printable-checklist.html`, `reports/이 파일`
- `checklist.html` — printhint에 ‘인쇄용 한 장 버전’ 링크(설명형 웹 페이지는 그대로 유지, 1줄만).
- `parent-rules.html` — 다음 읽을 글에 인쇄용 링크.
- `home-experiments.html` — 실험 전 안내에 인쇄용 링크.
- `index.html` — Hero CTA에 ‘🧾 인쇄용 한 장’ 추가.
- `sitemap.xml` — printable-checklist URL 추가(총 32).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.

## 3. 인쇄용 체크리스트 구조(A4 한 장)
1. 제목 + 부제 + 인쇄 안내(Ctrl/⌘+P) · 관련 링크(인쇄 시 숨김).
2. 오늘의 실험 정보(날짜·아이 나이·주제·시간 — 손으로 채우는 기입란).
3. 실험 전(6) ☐ · 4. 실험 중(5) ☐ · 5. 실험 후(5) ☐ — 총 16 체크박스(요청은 압축).
6. 아이와 함께 읽는 약속 4문장.
7. 오늘의 한 줄 기록(요청/마음에 든 것/다음 말 — 밑줄 기입란).
8. 자세히 보기 링크(인쇄 시 숨김).

## 4. 기존 checklist.html과 역할 분리
- **checklist.html = 설명형 웹 페이지**(왜 필요한가·전/중/후·연령별·설명말) — 그대로 유지.
- **printable-checklist.html = A4 실행 출력용**(기입란 + 압축 체크 + 한 줄 기록). 웹 설명은 빼고 ‘종이에 쓰는’ 데 최적화.
- 서로 링크로 연결(설명↔출력).

## 5. 연결한 기존 페이지
- 역방향 유입: index Hero CTA · checklist printhint · parent-rules 다음글 · home-experiments 실험 전 안내(4곳).
- 페이지 내 링크: checklist·parent-rules·home-experiments·age-guide·compare(필수 5).

## 6. print CSS 적용 여부
- `@media print` + `@page{size:A4;margin:12mm}` 적용.
- 인쇄 시 nav·footer·툴바·관련 링크·웹 안내문 숨김(`display:none`), 배경 흰색, 폰트 축소, 테두리 회색 — 체크 항목·기입란만 한 장에.
- 배경색 과도하게 쓰지 않음(카드 배경 제거, 테두리만).
- **JS 없음**(인쇄 버튼 대신 Ctrl/⌘+P 안내 텍스트, onclick/script 0).

## 7. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 8. 검증 결과 (13/13)
- 로컬 200 / 라이브 200: printable·checklist·parent-rules·home-experiments·대문·sitemap
- 내부 링크: 필수 5개 전부, 깨짐 0
- sitemap: 32 URL, XML 유효
- 모바일 가독성: 정보 2열(모바일도 읽힘), 체크 카드 세로
- print CSS: @media print + @page A4 존재
- A4 한 장 구조: 정보+3블록+약속+기록이 한 장 분량(break-inside:avoid)
- 광고성 CTA·특정 서비스: 없음
- JS: 없음(onclick/script 0)
- 영상/유튜브/상품 파일 생성: 없음
- 기존 checklist.html: 무손상(설명형 유지, 링크 1줄만)
- patch_log·working tree: 세트만 커밋

## 다음 후보
- `start-here.html`(처음 온 부모를 위한 10분 안내) 또는 사이트 내부 색인 개선.
