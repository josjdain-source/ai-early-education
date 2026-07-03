# 관측소 소스 피드 정비 — 감사 보고

- 작성일: 2026-07-04
- 성격: **랜딩페이지 노이즈 제거 + RSS/피드 단위 전환.** 자동 발행·HTML·sitemap·배포·영상 없음. update_queue 6항목 보존.

## 1. 문제와 해결
- **문제**: 첫 자동 실행이 소스 홈페이지 `<title>`을 큐에 등록(예: "Ministry of Education(MOE)"·"연합뉴스"·"OpenAI News") = 노이즈.
- **해결**: (1) 실제 RSS 피드 8개 검증·추가, (2) fetch_mode 필드로 랜딩/검색 소스는 큐 미등록, (3) **RSS 기사 항목만** 후보, (4) 항목별 점수를 '그 항목 제목'만으로(피드 공유 키워드 부풀림 제거).

## 2. 전체 소스 (42개)
| 구분 | 수 |
|---|---|
| 총 소스 | 42 |
| **RSS 피드(queue_allowed=true, 즉시 자동 관측 가능)** | **8** |
| 랜딩페이지/검색페이지 only(queue_allowed=false, 확인만) | 34 |

## 3. RSS/Atom으로 실제 항목을 가져온 소스 (검증 2026-07-03)
| id | 매체 | 축 | items |
|---|---|---|---|
| feed-arxiv-csai | arXiv cs.AI | C 연구 | 353 |
| feed-arxiv-cscy | arXiv cs.CY | C 연구 | 44 |
| feed-openai-news | OpenAI News | G 산업 | 다수 |
| feed-nvidia-blog | NVIDIA Blog | G 산업 | 18 |
| feed-techcrunch-ai | TechCrunch AI | G 산업 | 20 |
| feed-theverge-ai | The Verge AI | G 산업 | 10 |
| feed-mittr-ai | MIT Tech Review | G 산업 | 10 |
| feed-yna-news | 연합뉴스 | B 뉴스 | 120(전체→교육 필터) |

## 4. 랜딩페이지 only 소스 (queue_allowed=false, 34개)
기존 공식/국제기구/기관/유튜브 검색 소스 대부분(kr-moe·sg-moe·uk-dfe·UNESCO·g-industry-media 등). URL이 랜딩/검색 페이지 → 기사 항목 없음 → daily_watch에 "확인만(신규 기사 없음)"으로만 기록, **큐 미등록**. (딥링크 RSS가 있으면 향후 feed-* 로 승격.)

## 5. API 필요 / manual_review 소스
- 유튜브 검색(yt-*·student/school 검색): 동적 → `skipped_search`. **YouTube Data API** 필요.
- 뉴스/학술 검색 URL(naver/google/scholar/riss): 동적 → `skipped_search`. 뉴스 API 또는 사람 확인.
- anthropic RSS: 404(현재 경로 없음) → 보류. deepmind: 피드 구조 상이 → 보류.

## 6. fetch_mode 분류 결과
- rss: 8(queue 후보 가능) · webpage_change(기본, 랜딩): 다수 · search_query(skipped): 유튜브/뉴스/학술 검색 · api_required/manual_review: 유튜브·일부 검색.
- 규칙(watch_sources meta): fetch_mode 미표기 = queue_allowed=false·item_level_available=false 간주.

## 7. dry-run/write 테스트 결과
- **전체 42소스 dry-run**: scored=25(피드 8에서만), queue_added=4(score≥3), low_score=21. **랜딩 34소스 = 큐 0**(노이즈 제거 확인).
- **제한 write 테스트**(arxiv×2·openai·mittr): 4건 등록, 전부 실제 기사(arxiv.org/abs URL)·status=new·can_update_site_fact=false. 2건 진짜 교육("시험 채점 보조 LLM"), 2건 일반 키워드 오탐(경미). **테스트분은 큐 청결 위해 되돌림**(내일 07:30 실운영이 신선 수확).

## 8. update_queue 오염 여부
- **오염 0.** 큐 6항목(수동 curated) 보존, 자동 등록분 0(테스트 되돌림). 홈페이지 제목 노이즈 재발 없음.

## 9. 남은 한계 / 다음 단계
- 점수 정밀도: 일부 arXiv ML 논문이 "search"/"use" 등 일반 키워드로 score 3 오탐(경미) → 사람 검수로 거름. 추후 scorer 교육 키워드 정밀화.
- 검색형(유튜브/뉴스/학술): **API 연동** 필요(다음 단계).
- 딥링크 RSS 확보 시 공식 소스도 feed-* 승격.
- 매일 07:30 자동 실행 → daily_watch·queue(new) → 사람 검수.
