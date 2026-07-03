# scorer 교육 키워드 정밀화 — 작업 보고

- 작성일: 2026-07-04
- 성격: **연결성 점수 정밀화(오탐 감소).** 자동 발행·HTML·sitemap·배포·영상 없음. update_queue 6항목 보존.

## 1. 변경한 파일
| 파일 | 변경 |
|---|---|
| `scripts/ai_education_relevance_scorer.py` | 3층 신호 + 카테고리 전용 룰 + 감점 + ML 용어 억제 + `--test` |
| `ops/ai-early-education/scorer_test_cases.json` | 테스트 55케이스 |
| `reports/AI_EARLY_EDUCATION_SCORER_REFINEMENT_REPORT.md` | 본 보고서 |

## 2. 새 점수 규칙
- **3층 신호**: A 강한 교육(children/student/school/teacher/parent/homework/AI tutor/AI companion/K-12/literacy/child safety…) · B 중간(responsible use/privacy/media literacy/academic integrity/AI in education…) · C 일반 기술(model release/benchmark/chip/GPU/agent/revenue…).
- **카테고리 전용 룰**:
  - **research(arXiv/학회)**: 일반 ML/LLM = 0~1. education/student/child/tutor/assessment 있어야 3+.
  - **bigtech(G축)**: 기본 1. 아동/학교/교육/companion 연결 있을 때만 3+.
  - **news**: 실적·제품발표·주가·M&A = 0~1. 교육/학생/학교/부모/아동/안전 연결 시 3+.
  - **official**: 교육 신호 있으면 3+, child면 4.
- **감정/companion 전용**: companion/emotional AI/humanoid/social robot/dependency 등은 교육 직접신호 없어도 3(아동이면 4) + hype_risk 상향.
- **감점**: stock/revenue/earnings/chip supply/data center/gaming GPU 등은 교육 없으면 0~1.
- **5점 승격**: 아동 + (tutor/companion/homework/assessment/emotional).
- **ML 용어 억제**: "student-teacher/knowledge distillation/teacher network" 등 + 실제 교육 맥락 없으면 → 1점(오탐 방지).

## 3. 테스트 결과 — **55/55 통과**
| 그룹 | 케이스 | 결과 |
|---|---|---|
| 교육 직접(children/student/tutor/companion) | 10 | 3~5 ✓ |
| 일반 AI 기술 뉴스 | 10 | 0~2 ✓ |
| 빅테크 뉴스(교육 연결/무연결 혼합) | 10 | 0~1 / 3~5 ✓ |
| 감정·AI companion | 5 | 3~5(+caution) ✓ |
| 학생/학교/부모/공식 | 10 | 3~5 ✓ |
| 오탐 예상(learning/search/use/student-teacher) | 10 | 0~2 ✓ |

## 4. 오탐 줄인 방식
1. 일반 명사("learning"·"search"·"use")를 교육 신호에서 제거 → ML 논문 오탐 차단.
2. 카테고리별 기본 점수 차등(research/bigtech/news 기본 1) → 교육 신호 있어야 상승.
3. **ML 전문용어 억제**("student-teacher distillation" 등) → 교육 맥락 없으면 1점.
4. 감점 키워드(실적/칩/데이터센터) → 교육 없으면 눌림.
- 실제 효과: 오늘 피드 dry-run에서 이전 오탐 4건(arxiv score 3)이 전부 **1점**으로 하락, queue_added 0(교육 항목 없는 날 = 0, 정직).

## 5. API 연동 전 남은 위험
- 스코어는 여전히 **제목 기반 휴리스틱**. 본문/description 미반영(경미한 미탐 가능).
- 한국어 교육 뉴스는 키워드 커버리지 확대 필요(교과서/융합교육 등 일부).
- companion/robotics 과탐 위험: hype_risk로 표기하되 사람 검수 필수.
- → **사람 승인 게이트가 최종 안전장치.** API 연동은 이 정밀도 위에서 진행하면 큐 폭주 위험 낮음.

## 6. 검증 결과
| 항목 | 결과 |
|---|---|
| JSON 유효 / scorer 테스트 | 55/55 ✓ |
| 일반 ML/LLM 논문 무조건 5점 아님 | ✓ (1점) |
| 빅테크 교육 무연결 0~2 | ✓ |
| child/student/school/parent/tutor/companion 3~5 | ✓ |
| 감정/companion caution 포함 | ✓ (hype_risk 상향) |
| update_queue 6항목 보존 | ✓ (dry-run만, 미기록) |
| 새 HTML·sitemap·배포·영상 | 0 ✓ (sitemap 39) |

## 7. 다음 단계
① 내일 07:30 실운영 결과에서 오탐/미탐 관찰 → ② scorer 미세조정(한국어 커버리지·본문 반영) → ③ 검색 API(유튜브/뉴스) 연동(정밀도 확보 후).
