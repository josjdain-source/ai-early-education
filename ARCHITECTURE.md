# AI 조기교육 — 아키텍처 (진실 원본)

> 구조 작업 전 항상 이 문서 참조·갱신. 상세 운영은 `MAINTENANCE.md`, 배포는 `DEPLOY.md`.
> 최종 갱신: 2026-07-04

## 0. 한 줄 정체성
정적 자료실이 아니라 **매일 깨어나는 AI 조기교육 편집국**: 고정 자료실 + 7축 자동 관측소 + 근거 기반 영상 라인. 사람은 "찾기"가 아니라 **"승인·방향 판단"**.

## 1. 좌표
- 라이브: https://ai-early-education.pages.dev/ · repo: github.com/josjdain-source/ai-early-education (main)
- 폴더: `C:\Users\admin\Desktop\ai-craft-kids` (독립 git) · CF Pages: `ai-early-education`
- 인증: gh CLI(josjdain-source)·wrangler(CF OAuth) 저장됨(MAINTENANCE.md)

## 2. 3개 축 (전체 구조)
```
[A] 고정 자료실(사이트)  →  부모가 읽는 근거 창고
[B] 데일리 관측소(ops/)  →  매일 7축 자동 관측 → update_queue(승인 게이트)
[C] 영상 라인(content/·assets/) → 근거 기반 5분 해설/숏폼
        A는 B·C의 목적지(링크 허브), B는 C의 소재 공급, 사람이 승인으로 연결
```

## 3. [A] 사이트 (ai-early-education/*.html, sitemap 40 URL)
- **메인(index)=분야별 영상 카테고리판**(유튜브/넷플릭스형): 대표=나라별 AI교육(video-countries.html), 그리드=연령별/대화놀이/부모가이드/출력자료/5분핵심영상/오늘이슈. 썸네일=CSS gradient+▶(영상 미완성, 공개 시 href 교체). 큰 영상 1개 주인공 아님.
- **video-countries.html**: 나라별 영상 카드 5(중국/미국/영국/싱가포르/한국)+세계 5분 본편. 각 카드 '준비 중'+countries/*.html(근거) 연결.
- **불변 축**: 9개국 매트릭스(global-matrix)·부모 가이드(for-parents/age-guide/parent-rules)·출력자료 4종 세트(downloads → printable-checklist/printable-rules/experiment-log/age-cards)·FAQ/용어사전/출처(parent-faq/glossary/source-library)·해석다리(school-vs-home)·시리즈 1·2·3
- **9개국·출처=삭제 아니라 하단 '근거'로 재배치**(영상의 원자료)
- 배포: git push → wrangler 클린 배포(git archive). SEO: title/desc 중복0·내부링크 순환(대문↔허브↔FAQ)
- **사이트 수정은 사람 승인 후에만.**

## 4. [B] 데일리 관측소 (ops/ai-early-education/)
### 7축 (source_taxonomy.json = 분류 단일 진실원본)
A 공식정책(fact·사이트수정 가능) · B 뉴스(논란·변화) · C 학회/연구 · D 학교현장 · E 학생프로젝트(★미성년자 보호) · F 유튜브/기관/부모 · **G AI산업/빅테크(교육 연결성만)**
- 신뢰도 A_official > B_academic > C_school/industry > D_media > E_creator > F_commercial
- **유튜브/뉴스/기업=사실 근거 아님**(do_not_use_as_policy_fact). 사실 수정은 축A만(can_update_site_fact).
- 미성년자 필드: privacy_risk·minor_data_risk·requires_anonymization·can_use_as_student_example
### 자동 파이프라인 (scripts/)
```
watch_sources.json → fetch(RSS 기사단위만; 랜딩/검색=확인만) → 7축 분류
→ 연결성 점수 0~5(ai_news_relevance_rules.md, 항목별 제목 기준)
→ update_type → update_queue 자동등록(score≥3·중복방지·status=new·approved null)
→ daily_watch/{date}_auto.md + pipeline_runs/{date}.json (사람 수동 {date}.md는 별도 보존)
→ ★사람 승인 → (승인분만) 사이트/영상/발행
```
- 모듈: ai_education_daily_pipeline / _source_fetcher / _relevance_scorer / _queue_writer. scorer 테스트 55/55(scorer_test_cases.json)
- **Safety Guard**(pipeline_config.json): HTML/sitemap/robots/exports/wrangler/upload 쓰기 코드 차단
- 실행: `--dry-run`(기본,무수정) / `--write`. 스케줄러: 작업 "AI Early Education Daily Watch" 매일 07:30(run BAT, auto_publish=false)
- RSS 피드 8: arXiv cs.AI/cs.CY·OpenAI·NVIDIA·TechCrunch·Verge·MIT-TR·연합뉴스. 검색형=API 필요(다음)
### 큐/기록
- update_queue.json(수동 curated + 자동 UQ-{date}-90~). status: new→reviewing→approved→applied/rejected
- issue_notes/(수동 이슈, 예: 중국 감성로봇 UQ-06) · research_notes/(연구 신호, 예: UQ-90 LLM 채점)
- 템플릿: daily/weekly/news/research/school_practice/student_project/industry/web_resource_watch

## 5. [C] 영상 라인 (content/·assets/ai-early-education/video-episode-*)
- 시리즈: "부모를 위한 AI 조기교육 50초"(숏폼 대본1~5) + 5분 정밀 해설(감정 AI 편 등)
- 파이프라인(싱가포르 편=첫 완성): 대본 v2 → 근거설계 → **자동 캡처(capture_evidence.py, 실제 페이지+출처 라벨, 가짜 이미지 금지)** → 병합 → 에셋(카드 make_ep02_cards/subcards) → preview(GIF, ffmpeg 최소빌드라 mp4 대체) → 1차 편집
- 원칙: 공식 캡처 원문 변경 금지·미확인 문구(윤리4원칙 등) 금지·"정답 연출" 금지·업로드는 사람 승인 후

## 6. 절대 원칙 (자동화 가드)
자동화 O: 찾기·분류·점수·큐등록·관측로그·(공식만)증거후보.
자동화 X: 사이트 수정·영상 업로드·정책 단정·뉴스를 사실로 반영·학생 얼굴/이름 노출·상품 홍보.
→ 큐는 항상 approved/applied=null 유지, 사람 승인이 최종.

## 7. 다음
① 검색형 소스 API(YouTube Data/뉴스) ② scorer 한국어 커버리지 ③ 싱가포르 편 TTS/BGM/자막 번인 → 검수 → 업로드(승인) ④ 내일 07:30 무인 운전 확인
