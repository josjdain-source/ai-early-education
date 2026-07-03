# AI 조기교육 데일리 관측소 — 자동 파이프라인 (README)

매일 7축 소스를 자동으로 훑어 조기교육 연결성 점수(0~5)를 매기고,
**3점 이상만** update_queue에 `status=new`로 등록한다. **자동 발행/사이트 수정/영상/업로드는 하지 않는다.**

## 구성
- `ai_education_daily_pipeline.py` — 오케스트레이터(load→fetch→분류→점수→큐→daily_watch→run log)
- `ai_education_source_fetcher.py` — 소스 fetch(RSS/공식 페이지). 검색 페이지는 동적이라 `skipped_search`(결과 지어내지 않음)
- `ai_education_relevance_scorer.py` — 연결성 점수 0~5 + 연결 영역 + 부모 질문
- `ai_education_queue_writer.py` — 중복 방지·score≥3·필수 필드 등록(status=new, approved/applied=null)
- `ops/ai-early-education/pipeline_config.json` — 최소점수·업데이트타입 매핑·Safety Guard·캡처 정책

## 실행
```
# 기본은 안전한 dry-run(파일 미수정)
python scripts/ai_education_daily_pipeline.py --dry-run

# 실제 기록(daily_watch/pipeline_runs/queue 생성·추가)
python scripts/ai_education_daily_pipeline.py --write

# 옵션
  --date 2026-07-05           # 실행 날짜
  --only sg-moe,g-industry-media   # 특정 소스만
  --limit 6                   # 앞 N개만
```
- **dry-run**: fetch·점수·후보만 계산, 화면 요약. 파일 0 수정.
- **write**: `ops/ai-early-education/daily_watch/YYYY-MM-DD.md` + `pipeline_runs/YYYY-MM-DD.json` 생성, `update_queue.json`에 score≥3 추가.

## 7축
A 공식정책 · B 뉴스 · C 학회/연구 · D 학교현장 · E 학생프로젝트 · F 유튜브/부모 · G AI산업/빅테크.
분류·기본정책 = `source_taxonomy.json`. G축 상세 = `ai_news_relevance_rules.md`.

## 연결성 점수(0~5)
0 실적/투자(연결 없음) · 1 일반 신제품 · 2 검색·생성 간접 · 3 학교/숙제/가정 학습 · 4 안전·개인정보·감정·의존 · 5 미성년자·AI튜터·companion·학교 직접. **3+만 등록**, 0~2는 run log/daily_watch에만.

## update_queue 등록 규칙
- score≥3, 중복(제목/URL) 제외, `status=new`, `approved_by/applied_commit=null`, `checked_by=automated_pipeline`.
- 자동 id는 `UQ-YYYYMMDD-90~` (수동 UQ와 충돌 회피).
- 공식(A)=can_update_site_fact **true**. 그 외(뉴스/유튜브/기업/학생)=**false + do_not_use_as_policy_fact=true**.
- 학생/학교/AI companion/robotics=privacy/minor_data_risk **high + requires_anonymization**.

## Evidence capture 연결
- config `auto_capture_categories`(공식만)만 캡처 후보. `scripts/capture_evidence.py` 호출로 연동 설계.
- **뉴스/유튜브/학생/미성년자 가능 자료는 자동 캡처 금지** → text summary만.

## Safety Guard (자동 발행 금지)
- 허용 쓰기: `ops/ai-early-education/`, `reports/`, `assets/ai-early-education/singapore-evidence/`.
- **금지(코드 차단)**: `*.html`, `sitemap.xml`, `robots.txt`, 영상 exports, wrangler 배포, 업로드.
- `guard_write_path()`가 모든 쓰기 경로를 검사 → 금지 경로면 PermissionError.

## 사람 승인 이후 단계
1. daily_watch·queue 검토(queue_added·score·parent_question·can_update_site_fact).
2. 승인 항목만 → 대본/근거 캡처/사이트 초안(각 별도 승인).
3. 사이트 반영·영상·발행은 **사람 승인 후에만**.

## 자동 발행 금지 원칙
자동화가 하는 것: 찾기·분류·점수·큐 등록·관측 로그·증거 후보.
자동화가 **안 하는 것**: 사이트 수정·영상 업로드·정책 단정·뉴스를 사실로 반영·학생 얼굴/이름 노출·상품 홍보.
