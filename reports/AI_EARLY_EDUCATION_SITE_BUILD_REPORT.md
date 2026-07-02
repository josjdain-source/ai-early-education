# AI_EARLY_EDUCATION_SITE_BUILD_REPORT

> 2026-07-03 · GLOBAL_AI_EDUCATION_RESEARCH_PACK → ai-craft-kids 'AI 조기교육' 코너 발행 구조화.
> 영상 제작 중단·유튜브 개설 보류·v2.4 판정 보류(지시 준수). 목표=사이트 1편 발행.

## 1. 생성한 URL
- `/ai-early-education/` — 코너 대문(포지션 문장 + 6카테고리 + 첫 5글 시리즈)
- `/ai-early-education/world-ai-education-map.html` — **1편 글**
- `/ai-early-education/sources.html` — 출처 170개 + 미확인 8건
- `/data/country_ai_education_matrix.json` — 9개국 매트릭스(데이터)
- `/sitemap.xml`, `/robots.txt` — 신규

## 2. 생성/수정 파일
- 신규: ai-early-education/index.html · world-ai-education-map.html · sources.html · data/country_ai_education_matrix.json · sitemap.xml · robots.txt · reports/이 파일
- 수정: index.html(홈 네비에 ‘AI 조기교육’ 링크 1줄 추가) — 그 외 기존 페이지 미변경

## 3. 1편 글 제목
**AI 교육, 다른 나라는 아이들에게 어떻게 가르치고 있을까?**
부제: 세계 9개국 AI 교육 정책을 조사해보니, 공통점은 “아이 혼자 AI에 던져두지 않는다”였다.

## 4. 핵심 메시지
- 포지션: AI 조기교육 = 프로그램 학습이 아니라 ‘말하고→보고→다시 요청하는’ 상호작용 경험.
- 국제 근거: UNESCO 학생용 12역량의 1번 = Human-centred mindset.
- 세계 공통 규칙 = 아이 혼자 AI를 쓰게 하지 않는다(부모 동반은 규제가 아니라 표준 학습법).

## 5. 출처 처리 방식
- 본문: 각 정책 문장에 위첨자 링크[n]로 정부/UNESCO/언론 인라인.
- 출처 페이지: sources.md를 파싱해 국가별 170개 자동 나열 + URL/한줄요약.
- **미확인 8건**을 별도 박스로 정직 표기(각국 초등 생성형 AI 전국 규정·부모 전용 정부 가이드 등).
- 모든 글에 ‘확인일 2026-07-03’ 명시(정책 변동성 고지).

## 6. 다음 글 후보
2편 “한국 AI 디지털교과서, 1년 만에 무슨 일이 있었나” → 3편 “아이 혼자 AI를 쓰게 하지 않는다” → 4편 “문패 만들기 30분” → 5편 “AI 캐릭터가 책상 위 인형극이 되기까지”(v2.4 재해석).

## 7. 배포 가능 여부
- **가능.** 로컬 검증(python http.server) 전 페이지 200, style.css 200, 내부 링크 정상, 매트릭스 JSON 유효, 모바일 폭 가로 넘침 없음(비교표 overflow-x 처리).
- 배포 경로 = repo `josjdain-source/ai-early-education` main push → Cloudflare Pages(ai-early-education.pages.dev) 자동 배포.
- 과장·단정 없음, 아이 단독사용 유도 표현 없음, 출처 없는 문장 없음.
