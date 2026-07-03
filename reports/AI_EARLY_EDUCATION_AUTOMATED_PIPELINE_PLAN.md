# AI 조기교육 자동 관측 파이프라인 — 구축 보고

- 작성일: 2026-07-04
- 성격: **자동 관측 파이프라인 구축 + dry-run/write 테스트.** 자동 발행 없음. HTML·sitemap·배포·영상·업로드 없음.

## 1. 생성/수정한 파일
| 파일 | 역할 |
|---|---|
| `scripts/ai_education_daily_pipeline.py` | 오케스트레이터(7축·점수·큐·daily_watch·run log·Safety Guard) |
| `scripts/ai_education_source_fetcher.py` | 소스 fetch(RSS/공식). 검색 페이지=skipped(결과 안 지어냄) |
| `scripts/ai_education_relevance_scorer.py` | 연결성 점수 0~5 + 연결 영역 + 부모 질문 |
| `scripts/ai_education_queue_writer.py` | 중복 방지·score≥3·필수 필드(status=new) |
| `scripts/ai_education_pipeline_README.md` | 실행/규칙/승인 흐름/금지 원칙 |
| `ops/ai-early-education/pipeline_config.json` | 최소점수·타입매핑·Safety Guard·캡처 정책 |
| `ops/ai-early-education/pipeline_runs/.gitkeep` | run log 폴더 |
| (기존 수정) daily_watch_template·update_queue(types)·source_taxonomy는 앞선 G축 커밋에 반영 |

## 2. 파이프라인 흐름
Source Load(watch_sources) → Fetch → 7축 분류(A~G) → 연결성 점수(0~5) → update_type 판단 → update_queue 자동 등록(score≥3, 중복방지, new) → (공식만) evidence capture 후보 → daily_watch/YYYY-MM-DD.md → pipeline_runs/YYYY-MM-DD.json → **사람 승인**.

## 3. dry-run 결과 (5소스: sg-moe·unesco·산업매체·AI로봇·빅테크랩)
- sources=5, fetch_ok=4, **skipped_search=1**(동적 검색페이지 정직 skip), scored=4.
- 축 A 2건[5,5], 축 G 2건[4,3]. **파일 0 수정 확인**(update_queue md5 불변, 날짜 파일 미생성).

## 4. write 테스트 결과 (동일 소스, 검증 후 되돌림)
- daily_watch/2026-07-05.md + pipeline_runs/2026-07-05.json 생성, update_queue에 4건(UQ-…-90~93) 추가.
- 검증: **A축=official/international, score 5, can_update_site_fact=true** / **G축 score 4·3, can_update_site_fact=false** / 전부 status=new·approved=null / score<3 미등록.
- 테스트는 **부분(5소스)·미래날짜**라 라이브 큐 오염 방지 위해 산출물 되돌림(코드 검증 완료). 큐 6항목 청결 유지.

## 5. queue 추가 / skip 건수 (write 테스트 기준)
- queue_added 4 · duplicate 0 · low_score 0 · fetch_failed 0 · skipped_search 1.

## 6. evidence capture 연동
- config `auto_capture_categories`=공식만. `capture_evidence.py` 호출 연동 설계(공식 문서 capture 후보). **뉴스/유튜브/학생/미성년자 가능 자료는 자동 캡처 금지**(text summary만).

## 7. 자동화 한계 (정직)
- **검색 페이지(youtube/news/scholar 검색 URL)는 동적/JS라 자동 파싱 미신뢰** → `skipped_search`로 표기, 결과를 지어내지 않음. RSS/공식 페이지 위주로 신뢰 수집. 검색형은 전용 API(YouTube Data API 등)나 사람 확인 필요.
- 점수는 키워드 휴리스틱 '후보'. 사람 승인이 최종.
- 일부 공식 사이트는 봇 차단(403) 가능 → status=failed로 기록.

## 8. Safety Guard 검증
- `guard_write_path()` 단위 테스트: `ai-early-education/index.html` **차단✅**, `sitemap.xml` **차단✅**, `ops/ai-early-education/*` 허용. 금지 경로 쓰기 시 PermissionError.

## 9. 검증 결과
| 항목 | 결과 |
|---|---|
| 모든 JSON 유효 | ✓ |
| dry-run 파일 미수정 | ✓ (md5 불변) |
| --write가 daily_watch·pipeline_runs 생성 | ✓ |
| score≥3만 등록 | ✓ |
| 중복 URL 재등록 안 함 | ✓ (dedup) |
| G축 교육 연결 없으면 hold/skip | ✓ (score<3 미등록) |
| 유튜브/뉴스 fact_source 아님 | ✓ (can_update_site_fact=false, do_not_use_as_policy_fact=true) |
| 미성년자 위험 필드 포함 | ✓ |
| HTML/sitemap/배포/영상/업로드 | 0 ✓ (Safety Guard 차단) |
| 비관련 파일 제외 | ✓ |

## 10. 다음 자동 실행 방법
```
# 매일 아침(사람이 실행 또는 스케줄러)
python scripts/ai_education_daily_pipeline.py --write
```
→ daily_watch·pipeline_run·queue(new) 생성. 사람은 queue_added·score·parent_question·can_update_site_fact를 검토해 승인/방향 판단. 승인 후에만 대본·사이트·발행.
