# 데일리 관측소 6축 확장 — 작업 보고

- 작성일: 2026-07-04
- 성격: **관측 축 확장(3→6축) + 학생사례 미성년자 보호.** 영상 제작·HTML·sitemap·배포 없음.

## 1. 변경한 파일
| 파일 | 변경 |
|---|---|
| `source_taxonomy.json` | 카테고리 16·use_policy 12·trust A~F로 확장, 6축, 미성년자 규칙, 뉴스/연구/학생 키워드 |
| `watch_sources.json` | meta 6축 + 신규 축(뉴스2·학회2·학교현장1·학생1) 출처 추가(미성년자 필드). 총 31 |
| `update_queue.json` | update_types 14종 확장 + type_rules(축별) |
| `daily_watch_template.md` | A~F 6섹션화 |
| `weekly_brief_template.md` | 공식/뉴스/연구/학교/학생/유튜브 6섹션 |
| `AI_EARLY_EDUCATION_DAILY_OBSERVATORY_PLAN.md` | 6축 섹션 |
| **신규** `news_watch_template.md`(B) · `research_watch_template.md`(C) · `school_practice_watch_template.md`(D) · `student_project_watch_template.md`(E) | 축별 기록 양식 |

## 2. 확장된 관측 축 (6축)
A 공식정책(사실) · B 뉴스(논란·변화) · C 학회/연구(연구 흐름) · D 학교현장/교사(수업 방식) · E 학생 프로젝트/대회(사용 사례) · F 유튜브/기관/부모(설명·질문).
- 신뢰도 A~F: A_official > B_academic_or_institutional > C_school_or_recognized_org > D_media_or_expert > E_creator_or_community > F_commercial_or_unverified.

## 3. 학생 사례 사용 원칙 (★미성년자 보호)
- 이름/얼굴/학교 특정 자료 **영상 직접 노출 금지** · 공개 보도도 흐림/일반화.
- '한 학교 사례'/'한 수업 사례'로 표현 · **단일 사례 전체 흐름처럼 과장 금지**.
- 작품 이미지 **권리 확인 전 사용 금지** · 성과 과장 금지 · **재구성 카드 우선**.
- 필드로 강제: student_project = minor_data_risk high · requires_anonymization=true · visual_use_allowed=false · direct_quote_allowed=false · can_update_site_fact=false · use_policy=student_activity_example.

## 4. 학회/연구 자료 사용 원칙
- '연구 흐름'으로만 인용(단정 금지). 동료심사·표본 확인. **단일 논문 일반화 금지**. use_policy=research_context, can_update_site_fact=false.

## 5. 뉴스 자료 사용 원칙
- 사회 반응·논란·변화 감지용. **공식(축A) 확인 전 사실 수정 금지**. controversy_signal/policy_signal. 미성년자 언급 기사 익명화. 단일 보도 과장 금지.

## 6. update_queue 확장 내용
14종: fact_update·page_update·policy_signal·controversy_signal·research_context·teaching_activity·student_activity_example·school_practice·parent_question·explanation_pattern·video_topic·fact_check·source_lead·hold. type_rules로 축별 제약(fact 수정은 축A만).

## 7. 다음 Daily Watch에서 확인할 6축
A 공식(fact_update) · B 뉴스(controversy_signal) · C 연구(research_context) · D 학교(school_practice/teaching_activity) · E 학생(student_activity_example, 익명화) · F 유튜브/부모(video_topic/parent_question).

## 8. 검증 결과
| 항목 | 결과 |
|---|---|
| JSON 유효(taxonomy/watch_sources/update_queue) | ✓ |
| 기존 공식 출처 구조 보존 | ✓ (축A 18개 기본정책 상속) |
| 뉴스/학회/학교/학생/유튜브 분리 | ✓ (source_category·use_policy 명시) |
| 각 카테고리 use_policy 명확 | ✓ (default_policy_by_category) |
| 미성년자/개인정보 위험 필드 추가 | ✓ (privacy_risk·minor_data_risk·requires_anonymization 등) |
| 학생 사례=fact 아님(practice/example) | ✓ (student_activity_example) |
| daily/weekly 6축 반영 | ✓ |
| 새 HTML·sitemap·배포·영상 제작 | 0 ✓ (sitemap 39) |
| 출처 수 | 31(축A 18 + 뉴스2·학회2·학교1·학생1 + 기관4·유튜브3) |
