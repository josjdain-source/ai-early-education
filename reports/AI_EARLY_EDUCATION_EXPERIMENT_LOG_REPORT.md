# AI 조기교육 — 인쇄용 실험 기록지(experiment-log.html) 발행 보고서

- 작성일: 2026-07-03
- 담당: Claude (사이트 운영 위임, MAINTENANCE.md 기준)
- 작업 범위: `ai-craft-kids/ai-early-education/` 내부만. 여행사이트 등 타 프로젝트 무손상. ai-craft-kids 내 비관련 미커밋 파일 제외.

## 0. 선행 확인 — 잘못된 URL 문자열
- 이전 완료 보고의 채팅 문구에 `https://ai-early-education.printable-rules.html`(도메인 형태 오류)가 있었음.
- **실제 파일(reports/·projects.json·patch_log.json·*.html) 전수 검색 결과: 해당 문자열 0건.**
- report에는 정상 URL `https://ai-early-education.pages.dev/ai-early-education/printable-rules.html`만 존재.
- **결론: 실제 파일 오류 없음. 채팅 보고 문구만의 오타로 확정** (수정 대상 없음).

## 1. 목표
downloads 출력 자료 허브의 **세 번째 실제 출력물**. 실험 후 아이가 무엇을 요청했고·무엇이 달랐고·다음엔 어떻게 말할지 남기는 A4 한 장 기록지.

## 2. 생성한 URL
- 라이브: `https://ai-early-education.pages.dev/ai-early-education/experiment-log.html`
- 파일: `ai-early-education/experiment-log.html`
- title: `오늘의 AI 대화 실험 기록지 | 인쇄용 AI 조기교육 활동지`
- description: `아이와 AI 대화 실험을 한 뒤 처음 요청, 마음에 든 점, 다시 요청한 말, 다음에 바꿔볼 표현을 기록할 수 있는 인쇄용 활동지입니다.`

## 3. 수정한 파일
| 파일 | 변경 |
|---|---|
| `ai-early-education/experiment-log.html` | **신규 생성** (A4 기록지) |
| `ai-early-education/downloads.html` | 기록지 '예정' → **'지금 사용' 승격** + 사용순서 5단계 링크 + 하단 관련읽기 |
| `ai-early-education/home-experiments.html` | #10 '오늘의 AI 사용 기록' 카드 하단에 인쇄용 기록지 링크 |
| `ai-early-education/printable-checklist.html` | 하단 자세히보기에 experiment-log 링크 |
| `ai-early-education/printable-rules.html` | 하단 자세히보기에 experiment-log 링크 |
| `ai-early-education/index.html` | 히어로 하단에 '✍️ 실험 기록지' 링크 |
| `sitemap.xml` | experiment-log URL 추가 (37 → **38**) |
| `../홈페이지 통합관리/projects.json` | live-experiment-log 액션 + status/next_action 갱신 |
| `patch_log.json` | 항목 추가 |
| `reports/AI_EARLY_EDUCATION_EXPERIMENT_LOG_REPORT.md` | 본 보고서 |

## 4. 인쇄용 실험 기록지 구조 (11단)
제목 → 실험 정보(날짜·아이 이름 또는 별명·시간·오늘 고른 실험) → ① 오늘 부탁한 것 → ② 처음 요청한 말 → ③ 마음에 든 점 → ④ 예상과 달랐던 점 → ⑤ 다시 요청한 말 → ⑥ 다시 요청하니 달라진 점 → ⑦ 오늘 배운 한 가지 → ⑧ 다음에 말해볼 것 → 보호자 메모 + 다음 실험 날짜 → 개인정보 주의 + 관련 링크.
각 항목에 아이용 쉬운 문장 병기("처음엔 이렇게 말했어요." 등). **체크박스보다 빈칸(밑줄) 중심.**

## 5. home-experiments.html과 역할 분리
- **home-experiments** = 무엇을 해볼까 (실험 아이디어 10가지, 유지·변형 없음).
- **experiment-log** = 실험 후 무엇을 남길까 (A4 기록지).
- 충돌 없음: home-experiments #10 카드 하단에 experiment-log **링크만** 추가(연결).
- 흐름 완성: checklist/printable-rules(**시작 전**) + home-experiments(**중간**) + experiment-log(**실험 후**) = 출력 자료 3종 세트.

## 6. downloads에서 승격한 방식
- '곧 추가할 자료(예정)'의 실험 기록지 항목 삭제 → **'2. 지금 바로 쓸 수 있는 자료'에 badge='지금 사용'(ready) 카드로 이동**(용도·사용 시점·추천 대상 명시).
- 사용 순서 5단계와 하단 관련읽기에도 링크 추가.

## 7. print CSS 적용 여부
- 적용됨. `@page{size:A4;margin:12mm}` + `@media print`에서 nav/footer/toolbar/morelinks/lead 숨김, `break-inside:avoid`, 배경 제거, 링크 검정. **JS 없는 정적 HTML.**

## 8. 배포 여부
- 배포: **완료** (git push origin main → wrangler 클린 배포).

## 9. 검증 결과
| 항목 | 결과 |
|---|---|
| 로컬 200 | ✓ experiment-log / downloads / home-experiments |
| 라이브 200 | ✓ |
| 내부 링크(7종) | 전부 실존 ✓ |
| sitemap 반영 | loc 38, experiment-log 1건 ✓ |
| downloads 승격 | badge '지금 사용' 확인 ✓ |
| 모바일 가독성 | 기존 style.css + 반응형 ✓ |
| print CSS / A4 한 장 | ✓ |
| 광고성 CTA / 특정 AI 추천 | 없음 ✓ |
| 영상/유튜브/상품/PDF 생성 | 0 ✓ |
| age-cards 생성 | 안 함(정책) ✓ |
| 잘못된 printable-rules URL 문자열 | 파일 내 0건 ✓ |
| 기존 페이지 무손상 / 여행사이트 미변경 | ✓ |
| 개인정보 | 별명 허용 + 업로드 금지 안내 ✓ |
| working tree | 이번 작업 세트만 커밋, 비관련 제외 ✓ |
