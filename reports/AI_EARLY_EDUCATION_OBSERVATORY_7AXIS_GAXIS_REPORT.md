# 데일리 관측소 G축 추가(7축) — 작업 보고

- 작성일: 2026-07-04
- 성격: **AI 산업/빅테크 축(G) 추가 + 교육 연결성 점수.** 영상 제작·HTML·sitemap·배포 없음.

## 1. 변경한 파일
| 파일 | 변경 |
|---|---|
| `source_taxonomy.json` | G 카테고리 10·use_policy 7·trust 4 추가, G축 정의, education_relevance_score(0~5), 고연결 태그, G 기본정책, update_types 8 추가 |
| `watch_sources.json` | meta 7축 + G 출처 3(빅테크랩·AI로봇/동반자·산업매체)에 G 필드(education_relevance_required·can_trigger_parent_alert·hype_risk) |
| `update_queue.json` | update_types 22종(industry_signal·ai_companion_issue 등) + **UQ-06을 G구조로 승격**(ai_companion_issue, relevance 4) |
| `daily_watch_template.md` | G 섹션(연결성 점수·연결 영역 체크·보류 사유) |
| `weekly_brief_template.md` | 7-G AI 산업 변화 |
| `AI_EARLY_EDUCATION_DAILY_OBSERVATORY_PLAN.md` | 7축 |
| **신규** `industry_watch_template.md`, `ai_news_relevance_rules.md` | 축G 기록·점수 규칙 |

## 2. G축 추가 내용
- 카테고리: ai_company_news·ai_lab_release·ai_model_release·ai_robotics·ai_hardware·ai_agent·ai_search·ai_companion·ai_safety_company·ai_education_product
- use_policy: industry_signal·technology_shift·child_education_implication·parent_awareness_topic·future_risk_signal·device_environment_signal·hold_no_education_link
- trust: B_company_official·C_industry_media·D_creator_analysis·E_unverified_hype
- 출처: 빅테크/랩 블로그(OpenAI·Google/DeepMind·Meta·MS·Apple·NVIDIA·Anthropic·xAI), AI 로봇/동반자, 산업매체(Verge·MIT TR·TechCrunch·Reuters·Bloomberg·IEEE)

## 3. AI 산업 뉴스 사용 원칙
- **메인 뉴스 아님.** 투자·주가·기업홍보·신제품 소개 채널 금지.
- "아이 교육과 무슨 관련?"만 본다. 교육 연결성 없으면 **hold_no_education_link**.
- 기업 발표 = 기술 변화 근거로만. **정책 fact 수정 근거 아님**(official보다 낮은 B_company_official, 과장 가능 hype_risk).
- 미성년자·감정·친밀감·의존 뉴스는 caution 상향(requires_anonymization). 고연결 태그(ai_robot·ai_companion·ai_agent·ai_search·ai_glasses·ai_video_generation·ai_tutor·ai_device·on_device_ai) 별도 추적.

## 4. 교육 연결성 점수 규칙 (0~5)
0 실적/투자(연결 없음→hold) · 1 일반 신제품(약함) · 2 검색·생성 간접 · 3 학교/숙제/가정 학습(등록 가능) · 4 안전·개인정보·감정·의존(caution 상향) · 5 미성년자·AI튜터·companion·학교 직접(우선). **3+만 등록.** 상세=ai_news_relevance_rules.md.

## 5. 중국 감성 로봇 이슈 등록(G구조 승격)
- UQ-20260704-06: update_type **ai_companion_issue**, source_category=youtube_video/ai_robotics/news_media, trust=C_industry_media, **education_relevance_score=4**, hype_risk=medium, impact=medium, status=new, can_update_site_fact=false, do_not_use_as_policy_fact=true, minor/privacy_risk=medium, requires_anonymization=true. 이슈노트 유지.

## 6. 다음 Daily Watch에서 볼 7축
A 공식(fact) · B 뉴스(controversy) · C 연구(research_context) · D 학교(school_practice) · E 학생(student_example, 익명) · F 유튜브/부모(video_topic/parent_question) · **G AI산업/빅테크(교육 연결성 점수→3+만 등록, 기업발표=기술 변화 근거만)**.

## 7. 검증 결과
| 항목 | 결과 |
|---|---|
| JSON 유효(taxonomy/watch_sources/update_queue) | ✓ |
| 기존 6축 구조 보존 | ✓ |
| G축 추가 | ✓ (출처 3, 카테고리 10) |
| 기업 뉴스≠교육 정책 fact_source | ✓ (can_update_site_fact=false, B_company_official) |
| 교육 연결성 점수 규칙 | ✓ (0~5 + rules 파일) |
| 중국 감성 로봇 UQ-06 등록 | ✓ (ai_companion_issue, relevance 4) |
| daily/weekly G축 반영 | ✓ |
| 새 HTML·sitemap·배포·영상 제작 | 0 ✓ (sitemap 39) |
| 출처 수 | 34(축A~F 31 + G 3) |
