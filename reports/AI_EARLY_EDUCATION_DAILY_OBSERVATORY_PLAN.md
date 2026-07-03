# AI 조기교육 데일리 관측소 — 운영 설계

- 작성일: 2026-07-03
- 성격: **운영 구조 설계 + 양식 구축.** 새 부모용 HTML 0, 사이트 구조 변경 0, 자동 발행 0. 사람 승인 전 반영 금지.

## 1. 왜 (편집국 전환)
홈페이지 한 번 만들고 끝내면 박제된 보고서가 된다. 사이트를 **고정 자료실 + 매일 변하는 AI 교육 감시 + 정기 발행**으로 운영한다. 도서관이 아니라 **작은 편집국.**

- **변하지 않는 축**: 9개국 매트릭스 · 부모 가이드 · 출력자료 4종 · FAQ/용어사전/출처 라이브러리
- **자주 바뀌는 축**: 각국 AI 교육 정책 · 한국 AIDT 이슈 · 학교 AI 가이드 · 연령 제한/보호자 동의 · 과제 윤리 · 국제기구 발표
- **발행 축**: 매일 관측 / 주간 브리핑 / 5분 정밀 영상 / 필요 시 긴급 업데이트

## 2. 생성한 파일
| 파일 | 역할 |
|---|---|
| `ops/ai-early-education/watch_sources.json` | 확인할 출처 목록(18개, 그룹별) |
| `ops/ai-early-education/update_queue.json` | 발견→승인→반영 큐(예시 1건, rejected) |
| `ops/ai-early-education/daily_watch_template.md` | 매일 관측 기록 양식 |
| `ops/ai-early-education/weekly_brief_template.md` | 주간 부모 브리핑 양식 |
| `content/longform/ai-early-education/production_calendar.md` | 정기 발행 캘린더·5분 영상 구조 |
| `reports/AI_EARLY_EDUCATION_DAILY_OBSERVATORY_PLAN.md` | 본 설계 문서 |

## 3. 출처 그룹 (watch_sources.json, 18개)
- **국제기구**: UNESCO(AI in Education), OECD.AI, EU AI Act/AI literacy
- **한국**: 교육부, KERIS, 주요 언론(교차확인용)
- **싱가포르**: MOE, SLS, IMDA
- **중국**: 교육부(EN)
- **영국**: DfE, JCQ(AI in assessments)
- **에스토니아**: 교육연구부(AI Leap)
- **핀란드**: OPH/EDUFI
- **일본**: MEXT
- **인도**: Ministry of Education/CBSE(NEP)
- **미국**: Dept of Ed OET, 주별 가이드
- 각 출처 필드: id · country · source_type(official/international/guide/media/research) · name · url · check_frequency(daily/weekly/monthly) · volatility(high/med/low) · related_pages(실제 사이트 slug) · last_checked(현재 전부 null=미확인) · note
- ⚠️ url은 안정적 공식 랜딩. **첫 Daily Watch에서 실제 정책 딥링크 확인 후 note 갱신.**

## 4. update_queue 구조
- 필드: id · discovered_date · source_id · title · summary · affected_pages · impact_level(low/med/high) · update_type(note/page_update/video_topic/fact_check/hold) · status(new/reviewing/approved/applied/rejected) · reason · source_url · checked_by · approved_by · applied_commit
- id 규칙: `UQ-YYYYMMDD-NN`
- 현재: 구조 예시 1건(status=rejected, 실데이터 아님)

## 5. 정기 발행 캘린더
- 매일=관측(비공개), 공개 발행 **주 2~3회**(금 주간 브리핑 고정 + 5분 영상 + 선택 1)
- 월 관찰포인트 / 화 국가별 요약 / 수 FAQ / 목 5분 대본 / 금 브리핑(공개) / 토 실천 콘텐츠 / 일 큐 정리
- 5분 영상: 4:30~5:30, 공식 자료 기반, source-library 연결, 출처 카드 화면. 쇼츠는 30초 클립 파생

## 6. 사람 승인 규칙 (핵심)
Claude가 하는 것: **발견 · 요약 · 영향 분석 · 수정 초안 · update_queue 등록**까지.
사람 승인 후에만: **HTML 수정 · sitemap lastmod 수정 · 배포 · patch_log 기록.**
> 자동으로 막 고치면 사이트가 미꾸라지 수조가 된다.

### 업데이트 판단 기준
- **수정(page_update)**: 공식 정책 변경 / 국제기구·교육부 새 가이드 / 기존 수치·상태 변화 / 논란의 법·제도 단계 변화 / 부모 행동 가이드 영향
- **보류(hold)**: 단일 언론 보도 / 출처 불명 / 의견 칼럼 / 기존 결론에 영향 없음 / 확인 필요

## 7. 다음 실행 방법
1. `daily_watch_template.md` 복사 → `ops/ai-early-education/daily_watch/2026-07-04.md`로 첫 관측
2. 변화 발견 시 `update_queue.json`에 `UQ-20260704-01` 등록(출처·확인일 필수)
3. 금요일 `weekly_brief_template.md`로 첫 브리핑 초안 → 사람 승인 후 공개
4. 승인된 page_update만 사이트 반영(그때 sitemap lastmod·patch_log·배포)
5. watch_sources `last_checked` 갱신

## 8. 가드레일 (이번 작업 준수)
- 새 부모용 HTML 생성 ❌ / 사이트 구조 변경 ❌ / sitemap 변경 ❌
- Search Console 메타태그 대기 상태 유지 / 영상 업로드 ❌
- 뉴스·정책 단정 ❌ → 출처 URL + 확인일 필수
- 자동 발행 ❌ → 사람 승인 게이트
