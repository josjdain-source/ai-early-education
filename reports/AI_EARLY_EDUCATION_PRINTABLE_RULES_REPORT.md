# AI 조기교육 — 인쇄용 7가지 약속표(printable-rules.html) 발행 보고서

- 작성일: 2026-07-03
- 담당: Claude (사이트 운영 위임, MAINTENANCE.md 기준)
- 작업 범위: `ai-craft-kids/ai-early-education/` 내부만. 여행사이트 등 타 프로젝트 무손상. ai-craft-kids 내 비관련 미커밋 파일 제외.

## 1. 목표
downloads 출력 자료 허브에 꽂을 **두 번째 실제 출력물**. 부모와 아이가 함께 읽고 체크할 수 있는 A4 한 장 안전 약속표.

## 2. 생성한 URL
- 라이브: `https://ai-early-education.pages.dev/ai-early-education/printable-rules.html`
- 파일: `ai-early-education/printable-rules.html`
- title: `아이와 AI를 쓸 때 7가지 약속표 | 인쇄용 AI 조기교육 안전 자료`
- description: `아이와 AI를 안전하게 사용하기 위해 부모와 아이가 함께 읽고 체크할 수 있는 인쇄용 7가지 약속표입니다.`

## 3. 수정한 파일
| 파일 | 변경 |
|---|---|
| `ai-early-education/printable-rules.html` | **신규 생성** (A4 약속표) |
| `ai-early-education/downloads.html` | 약속표 '예정' → **'지금 사용'으로 승격** + 하단 관련읽기 링크 |
| `ai-early-education/parent-rules.html` | 7가지 약속 목록 하단에 '인쇄용 약속표 보기' 안내 추가 |
| `ai-early-education/printable-checklist.html` | 하단 자세히보기에 printable-rules 링크 |
| `ai-early-education/index.html` | 히어로 하단에 '🛡️ 인쇄용 약속표' 링크 |
| `sitemap.xml` | printable-rules URL 추가 (36 → **37**) |
| `../홈페이지 통합관리/projects.json` | live-printable-rules 액션 + status/next_action 갱신 |
| `patch_log.json` | 항목 추가 |
| `reports/AI_EARLY_EDUCATION_PRINTABLE_RULES_REPORT.md` | 본 보고서 |

## 4. 인쇄용 약속표 구조 (7단)
1. 상단 제목
2. 오늘의 약속 정보 — 날짜 / 아이 이름 또는 별명 / 보호자 이름 / 함께 읽은 시간
3. 아이와 함께 읽는 7가지 약속 (번호+체크박스+아이 눈높이 문장)
4. 부모가 기억할 3가지
5. 아이가 직접 고르는 오늘의 약속 1개 (5개 체크)
6. 서명 영역 (아이 / 보호자 / 날짜)
7. 자세히 보기 링크 + 개인정보 주의 박스

## 5. parent-rules.html과 역할 분리
- **parent-rules.html** = 왜 이런 약속이 필요한가를 세계 사례로 설명하는 **웹 안전 가이드** (유지, 변형 없음).
- **printable-rules.html** = 그 7가지 약속을 아이와 **함께 읽고 체크·서명하는 A4 출력 도구**.
- 충돌 없음: 설명형은 그대로 두고, parent-rules 하단에서 printable-rules로 **연결**만 추가(양방향).

## 6. downloads에서 승격한 방식
- 기존 '곧 추가할 자료(예정)'에 있던 약속표 항목을 삭제하고, **'2. 지금 바로 쓸 수 있는 자료'에 badge='지금 사용'(ready) 카드로 이동**.
- 용도·사용 시점·추천 대상 3항목 명시. 하단 '관련 읽기'에도 링크 추가.

## 7. print CSS 적용 여부
- 적용됨. `@page{size:A4;margin:12mm}` + `@media print`에서 nav/footer/toolbar/morelinks/lead 숨김, `break-inside:avoid`, 배경색 제거, 링크 검정 처리. **JS 없음(정적)**.

## 8. 배포 여부
- 배포: **완료** (git push origin main → wrangler 클린 배포).

## 9. 검증 결과
| 항목 | 결과 |
|---|---|
| 로컬 200 | ✓ printable-rules / downloads / parent-rules |
| 라이브 200 | ✓ |
| 내부 링크 | printable-rules 내부 링크 전부 실존 ✓ |
| sitemap 반영 | loc 37, printable-rules 1건 ✓ |
| downloads 승격 | badge '지금 사용' 확인 ✓ |
| 모바일 가독성 | 기존 style.css + 반응형 ✓ |
| print CSS | @page A4 존재 ✓ |
| A4 한 장 구조 | ✓ |
| 광고성 CTA / 특정 AI 추천 | 없음 ✓ |
| 영상/유튜브/상품/PDF 생성 | 0 ✓ |
| experiment-log / age-cards 생성 | 안 함(정책) ✓ |
| 기존 페이지 | 무손상 ✓ |
| 개인정보 | 별명 허용 + 업로드 금지 안내 ✓ |
| 여행사이트 | 미변경 ✓ |
| working tree | 이번 작업 세트만 커밋, 비관련 제외 ✓ |
