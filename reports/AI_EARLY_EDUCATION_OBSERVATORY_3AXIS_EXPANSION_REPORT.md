# 데일리 관측소 3축 확장 — 작업 보고

- 작성일: 2026-07-04
- 성격: **관측 구조 확장(공식/기관·홈페이지/유튜브 3축) + 분류 체계.** 영상 제작·HTML·sitemap·배포 없음.

## 1. 변경한 파일
| 파일 | 변경 |
|---|---|
| `ops/ai-early-education/source_taxonomy.json` | **신규** — 분류 단일 진실원본(카테고리/타입/use_policy/trust_level, 3축, 기본정책, 유튜브 필드·키워드) |
| `ops/ai-early-education/watch_sources.json` | meta에 3축·taxonomy 참조 + 축2(기관 4)·축3(유튜브 3) 출처 신규 필드로 추가 |
| `ops/ai-early-education/update_queue.json` | update_types 확장(fact_update/explanation_pattern/parent_question/teaching_activity/source_lead 등) + type_rules |
| `ops/ai-early-education/daily_watch_template.md` | A(공식)/B(기관·홈)/C(유튜브) 3섹션으로 재구성 |
| `ops/ai-early-education/weekly_brief_template.md` | 공식/기관트렌드/유튜브 부모질문/영상후보 등 확장 |
| `ops/ai-early-education/youtube_watch_template.md` | **신규** — 축3 영상 기록 양식 |
| `ops/ai-early-education/web_resource_watch_template.md` | **신규** — 축2 기관 자료 기록 양식 |
| `reports/AI_EARLY_EDUCATION_DAILY_OBSERVATORY_PLAN.md` | 3축 섹션 추가 |

## 2. 새 source taxonomy
- **source_category**: official_policy, international_org, school_or_institution, nonprofit_or_research, education_company, media_report, youtube_channel, youtube_video, parent_community, unknown
- **source_type**: official, guide, curriculum, explainer, news, research, video, community, commercial
- **use_policy**: fact_source, context_source, trend_source, explanation_pattern, parent_question_source, video_topic_source, hold_until_verified
- **trust_level**: A_official > B_institutional > C_media_or_expert > D_community_or_creator > E_commercial_or_unverified
- watch_sources 추가 필드: source_category·use_policy·trust_level·monetization_risk·language·region·topic_tags·can_update_site_fact·can_generate_video_topic·notes_for_use
- 기존 공식 18개는 `default_policy_by_category`로 상속(fact_source·A·can_update_site_fact=true) — 개별 재기입 없이 문서화.

## 3. 유튜브 자료 사용 원칙
- **사실 근거 금지.** use_policy = explanation_pattern / parent_question_source / video_topic_source.
- 모든 유튜브 주장: `fact_claims_need_verification=true`, `do_not_use_as_policy_fact=true` → 사실은 축1에서 별도 확인.
- 영상/댓글 보고 **사이트 사실 자동 수정 금지.** 개별 영상은 youtube_watch_template로 기록(설명 방식·부모 질문·후킹만).

## 4. 홈페이지/기관 자료 사용 원칙
- **공식성/상업성 구분.** 학교·비영리·연구 = context_source(B), 교육기업 = trend_source(E, monetization_risk high).
- 사실 수정 불가(can_update_site_fact=false). 실천 예시·가이드 구조·트렌드만.
- **상업 자료는 상품 추천 근거 금지.** 비영리/연구 중 정책 성격은 원문 확인 후 축1 승격 가능.

## 5. update_queue 변경
- update_types를 taxonomy와 일치하게 확장(fact_update·page_update·video_topic·explanation_pattern·parent_question·teaching_activity·source_lead·fact_check·hold·note).
- type_rules: **fact_update/page_update/fact_check는 축1 근거 있을 때만.** 축2·축3은 explanation_pattern/parent_question/teaching_activity/video_topic/source_lead로만.

## 6. 다음 Daily Watch에서 확인할 3축
- **A 공식**: 교육부·UNESCO·JCQ·MOE 등(사실). 변화 시 fact_update/page_update(근거 필수).
- **B 기관·홈**: Common Sense Media·AI for Education·UNICEF 등(실천·부모 가이드). explanation_pattern/teaching_activity/source_lead.
- **C 유튜브**: parents guide to AI / AI literacy for children / (한국어)AI 조기교육 검색(설명 방식·부모 질문). video_topic/parent_question.

## 7. 검증 결과
| 항목 | 결과 |
|---|---|
| JSON 유효(taxonomy/watch_sources/update_queue) | ✓ |
| 기존 공식 출처 구조 보존 | ✓ (18개 유지, 기본정책 상속) |
| 축2·축3이 공식(축1)과 분리 | ✓ (source_category·use_policy·trust_level 명시) |
| 유튜브=fact 아님, trend/explanation/topic | ✓ (do_not_use_as_policy_fact) |
| update_queue 타입 확장 | ✓ |
| daily/weekly 템플릿 3축 반영 | ✓ |
| 새 HTML·sitemap·배포·영상 제작 | 0 ✓ |
| 출처 수 | 25(축1 18 + 축2 4 + 축3 3) |
