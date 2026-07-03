# UQ-06 — 중국 감성형 AI 로봇 이슈 관측 큐 등록 보고

- 작성일: 2026-07-04
- 성격: **새 관측 큐 등록 + 이슈 노트.** 싱가포르 편 무변경. 영상 제작·HTML·sitemap·배포 없음.

## 1. 추가한 update_queue 항목
- **UQ-20260704-06** — "중국 감성형 AI 로봇 보도와 AI 조기교육의 감정·관계 쟁점"
- source_category=youtube_video · update_type=**video_topic** · trust=D_media_or_expert · impact=medium · status=new
- **can_update_site_fact=false · do_not_use_as_policy_fact=true · privacy_risk/minor_data_risk=medium · requires_anonymization=true**
- affected_pages(잠재, 반영 아님): parent-rules·school-vs-home·parent-faq·source-library
- source_url: https://www.youtube.com/watch?v=BtBCiby3eDI

## 2. issue note 생성 여부 — ✅
`ops/ai-early-education/issue_notes/china_emotional_ai_robot_20260704.md` (10섹션). daily_watch/2026-07-04.md에 '추가 관측' 블록 참조 추가.

## 3. 이슈의 핵심 쟁점
AI가 아이의 '학습 도구'를 넘어 **감정·친밀감·관계·의존** 영역으로 확장. 관심은 '중국이 무섭다'가 아니라 **보호자 역할과 미성년자 보호**. 싱가포르 편(책임 사용 구조)과 별개의 '감정 AI 편'.

## 4. 확인/미확인 분리 (정직)
- ✅ 확인(WebFetch 2026-07-04): SBS 보도 제목 "최대 2억 넘는데 벌써 '1만 대' 주문..중국 '감성 로봇' 실물 보니", 가격 2억↑·1만 대 주문(보도 주장).
- ⚠️ 미확인(사용자 전언, 사실화 금지): 유비테크 U1 계열·실리콘 피부·88관절·동반자 로봇 논란, UNICEF China 아동 대상 가상 친밀관계 금지선 → 공식/1차 보도로 교차확인 전 영상·사이트에 사실로 쓰지 않음.

## 5. 부모에게 중요한 질문
- 아이가 AI를 친구/가족/연인처럼 여기면? · 감정 의존이 정서 발달에 미치는 영향? · 감정 상담을 AI에 맡겨도 되나, 보호자 개입 범위? · '친밀감 파는 제품'과 '학습 도구' 구분?

## 6. 5분 영상 후보 (topic만, 제작 아님)
1. AI가 아이의 감정까지 다루기 시작했다
2. 중국 감성 로봇 보도에서 부모가 봐야 할 것
3. AI 조기교육의 다음 쟁점: 감정, 의존, 관계
4. 아이에게 AI 친구를 허용해도 될까?
5. AI는 선생님이 될까, 친구가 될까?

## 7. 추가 확인할 연구/자료 (축C follow-up)
emotional AI robot children education · AI companion robot children emotional development · parent AI collaboration emotion education (PACEE 류) · AI powered robots preschool emotional development · virtual companion AI children regulation · child protection AI emotional dependency · (중국 유치원)LLM assistant teacher-child interaction assessment.
> 연구는 '효과 가능성'이지 가정 사용 근거 아님.

## 8. 검증 결과
| 항목 | 결과 |
|---|---|
| 싱가포르 편 수정 | 없음 ✓ |
| 새 HTML / sitemap 변경 | 0 / 39 유지 ✓ |
| 배포 / 영상 제작 | 0 ✓ |
| update_queue JSON 유효 | ✓ |
| 유튜브/뉴스=fact_source 아님 | ✓ (video_topic, do_not_use_as_policy_fact=true) |
| 미성년자 보호 필드 포함 | ✓ (minor_data_risk·privacy_risk·requires_anonymization) |
| 공포 마케팅 표현 | 없음 ✓ ('중국=위험' 명시적 배격) |
| 비관련 파일 제외 | ✓ |

## 9. 다음
축A(공식 규제)·축C(연구)로 교차확인 자료 수집 → 확인분만 승격. 승인 시 '감정 AI 편' 대본(별도). 지금은 큐+노트까지. parent-rules 잠재 영향(사람처럼 의존 금지 등)은 **큐 상태로만**, 사이트 반영 금지.
