# capture_evidence.py — 공식 자료 자동 캡처기 (사용법)

관측소의 evidence manifest를 읽어 **실제 브라우저(Playwright/Chromium)**로 공식 페이지를 열고,
핵심 문구가 보이는 위치를 캡처해 PNG로 저장한다. 상단에 출처 라벨 바를 합성한다.

## 핵심 원칙 (불변)
- **AI 생성 이미지로 공식 페이지를 흉내내지 않는다.** 본문 화면은 반드시 실제 브라우저 캡처.
- 상단 출처 바는 '생성 증거'가 아니라 **우리가 붙인 출처 라벨**(메타데이터). 이미지에도 그 사실을 명시.
- 문구를 못 찾으면 **failed/partial로 정직하게 기록**(가짜 캡처 금지).
- Playwright 내장 Chromium은 Chrome의 Google 자동번역이 없어 **원문 언어 유지**(번역 오염 없음).

## 설치
- Python 3.13, `playwright`(pip), `Pillow` 필요. Chromium 브라우저는 ms-playwright 캐시에 있으면 재사용.
- 브라우저 없으면: `python -m playwright install chromium`

## 실행
```
python scripts/capture_evidence.py \
  --manifest assets/ai-early-education/singapore-evidence/evidence_manifest.json \
  --outdir  assets/ai-early-education/singapore-evidence \
  [--only C03,C04] [--date 2026-07-04] [--headed]
```
- `--only`: 특정 cut_id만 (쉼표구분). 생략 시 전체.
- `--date`: captured_at/출처 바에 표기. 생략 시 오늘.
- `--headed`: 브라우저 창 보이게(디버깅용).

## manifest 구조 (읽는 필드)
- `cut_id`, `filename`, `source_url`, `source_name`, `visible_highlight_text`
- `visible_highlight_text`는 `|`로 여러 후보 분리. 스크립트가 긴 문구→앞 6/4단어 순으로 탐색.
- `capture_status=skip` 또는 `verification_status=not_found` 또는 `filename`이 `(`로 시작 → 건너뜀.

## 스크립트가 쓰는 필드 (갱신)
- `capture_status`: captured(전체 문구 매치) / partial(부분 매치) / failed(문구 미발견·에러)
- `actual_capture_file`, `captured_at`, `visible_text_confirmed`, `capture_method=automated_browser_playwright`
- `caution`에 `[auto <date>] <note>` 추가

## 실패 시 수동 보정법
1. `visible_highlight_text`에서 곱슬 아포스트로피(’)·`...`·특수문자 제거 → 아포스트로피 없는 부분문자열로 교체(예: "A Parent's..." → "Guide to Generative AI tools for Learning").
2. `capture_status`를 다시 `pending_manual`로 되돌리고 `--only <cut>` 재실행.
3. 그래도 실패 시 페이지가 JS 렌더/로그인/구조 변경 → `failed` 유지, caution에 원인 기록. 억지 캡처 금지.

## 새 국가/출처 추가 방법
1. 해당 출처의 evidence manifest(같은 필드 스키마)를 만든다. 예: `assets/ai-early-education/uk-evidence/evidence_manifest.json`
2. `--manifest`/`--outdir`를 그 경로로 지정해 실행.
3. `visible_highlight_text`는 **먼저 WebFetch/브라우저로 실제 페이지에서 확인한 문구만** 넣는다(미확인 문구 금지).

## 가짜 이미지 생성 금지 원칙 (재확인)
- 이 스크립트는 **캡처 도구**다. 어떤 경우에도 페이지를 그려내거나 합성 본문을 만들지 않는다.
- 출처 바는 라벨일 뿐이며, 본문이 실제 캡처가 아니면 그 컷은 사용하지 않는다.
