# AI 조기교육 — 인쇄용 연령별 시작 카드(age-cards.html) 발행 보고서

- 작성일: 2026-07-03
- 담당: Claude (사이트 운영 위임, MAINTENANCE.md 기준)
- 작업 범위: `ai-craft-kids/ai-early-education/` 내부만. 여행사이트 등 타 프로젝트 무손상. ai-craft-kids 내 비관련 미커밋 파일 제외.

## 1. 목표
downloads 출력 자료 허브의 **네 번째(마지막) 실제 출력물**. 부모가 아이 나이에 맞춰 AI 대화 실험 시작 방식을 바로 고르는 A4 출력용 카드.

## 2. 생성한 URL
- 라이브: `https://ai-early-education.pages.dev/ai-early-education/age-cards.html`
- 파일: `ai-early-education/age-cards.html`
- title: `연령별 AI 시작 카드 | 인쇄용 AI 조기교육 자료`
- description: `유아, 초등 저학년, 초등 고학년, 중학생 이상 아이에게 맞는 AI 대화 실험 방향을 한 장으로 정리한 인쇄용 자료입니다.`

## 3. 수정한 파일
| 파일 | 변경 |
|---|---|
| `ai-early-education/age-cards.html` | **신규 생성** (A4 연령 카드 4개) |
| `ai-early-education/downloads.html` | 연령 카드 '예정' → **'지금 사용' 승격** + 하단 관련읽기 |
| `ai-early-education/age-guide.html` | '다음 읽을 글' 최상단에 인쇄용 연령 카드 링크 |
| `ai-early-education/printable-checklist.html` | 하단 자세히보기에 age-cards 링크 |
| `ai-early-education/printable-rules.html` | 하단 자세히보기에 age-cards 링크 |
| `ai-early-education/experiment-log.html` | 하단 자세히보기에 age-cards 링크 |
| `ai-early-education/index.html` | 히어로 하단에 '📶 연령 카드' 링크 |
| `sitemap.xml` | age-cards URL 추가 (38 → **39**) |
| `../홈페이지 통합관리/projects.json` | live-age-cards 액션 + status/next_action 갱신 |
| `patch_log.json` | 항목 추가 |
| `reports/AI_EARLY_EDUCATION_AGE_CARDS_REPORT.md` | 본 보고서 |

## 4. 인쇄용 연령 카드 구조 (6단)
1. 상단 제목
2. 사용 방법 (4단계)
3. 연령별 카드 4개 (2×2 그리드) — 유아 / 초등 저학년 / 초등 고학년 / 중학생 이상. 각 카드 = 목표 · 부모 역할 · 추천 활동 · 하지 말 것 · 오늘의 질문
4. 모든 연령 공통 약속 (5개)
5. 오늘 고를 카드 체크 (4개)
6. 개인정보 주의 + 관련 자세히 보기 링크

## 5. age-guide.html과 역할 분리
- **age-guide** = 나이별 배경·이유를 설명하는 **웹 가이드** (유지, 변형 없음).
- **age-cards** = 그 원칙을 부모가 **나이에 맞춰 바로 고르는 A4 출력 카드**.
- 충돌 없음: age-guide '다음 읽을 글' 최상단에 age-cards **링크만** 추가(양방향).

## 6. 출력자료 4종 완성 여부 — 완성 ✅
downloads '지금 바로 쓸 수 있는 자료'가 4종 ready 카드로 완성:
1. **printable-checklist** — 시작 전 확인
2. **printable-rules** — 안전 약속
3. **experiment-log** — 실험 후 기록
4. **age-cards** — 나이별 시작점

> ⚠️ **잔여 항목 1건**: downloads '곧 추가할 자료'에 `start-here-print`(처음 온 부모 10분 안내 요약지) 예정 블록이 **아직 남아 있음.** 이는 원래 downloads 초안의 5번째 예정 항목으로, 이번에 언급된 '4종 세트'와는 별개. 이번 작업에서는 지시대로 손대지 않았음. **제작할지 / 예정 블록을 제거할지 결정 필요.**

## 7. print CSS 적용 여부
- 적용됨. `@page{size:A4;margin:11mm}` + `@media print`(nav/footer/toolbar/morelinks/lead 숨김, `break-inside:avoid`, 배경 제거, 그리드 간격 축소). 모바일에서는 카드 1열 세로. **JS 없는 정적 HTML.**

## 8. 배포 여부
- 배포: **완료** (git push origin main → wrangler 클린 배포).

## 9. 검증 결과
| 항목 | 결과 |
|---|---|
| 로컬 200 | ✓ age-cards / downloads / age-guide |
| 라이브 200 | ✓ |
| 내부 링크(7종) | 전부 실존 ✓ |
| sitemap 반영 | loc 39, age-cards 1건 ✓ |
| downloads 승격 | badge '지금 사용', ready 카드 4종 ✓ |
| 모바일 가독성 | 카드 1열 세로 배열 ✓ |
| print CSS / A4 한 장 | ✓ |
| 광고성 CTA / 특정 AI 추천 | 없음 ✓ |
| 영상/유튜브/상품/PDF 생성 | 0 ✓ |
| 새 출력자료 | age-cards까지만(정책) ✓ |
| 기존 페이지 무손상 / 여행사이트 미변경 | ✓ |
| 개인정보 | 입력 유도 없음, 혼자 사용 권장 없음 ✓ |
| working tree | 이번 작업 세트만 커밋, 비관련 제외 ✓ |
