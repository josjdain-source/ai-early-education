# 공식 자료 자동 캡처기 — 작업 보고

- 작성일: 2026-07-04
- 성격: **실제 브라우저 기반 자동 캡처 도구 구축 + C02~C07 시험 운전.** 영상 제작·업로드·HTML·sitemap·배포 없음.

## 1. 만든 스크립트
- `scripts/capture_evidence.py` — Playwright(Python)+Pillow. 실제 Chromium으로 공식 URL 열고 문구 위치 캡처, 상단 출처 라벨 바 합성, manifest 갱신.
- `scripts/capture_evidence_README.md` — 설치/실행/실패 보정/새 출처 추가/가짜 금지 원칙.

## 2. 실행 방법
```
python scripts/capture_evidence.py --manifest <manifest.json> --outdir <dir> [--only C03,C04] [--date 2026-07-04]
```
Playwright 내장 Chromium은 자동번역이 없어 **원문 영어 유지**(지난 Chrome 자동번역 문제 해결).

## 3. C02~C07 캡처 결과 — 6/6 captured
| cut | 상태 | 확인된 문구(visible_text_confirmed) |
|---|---|---|
| C02 | captured | "Artificial intelligence in education" |
| C03 | captured | "Developing Age-progressive Framework ... for Students and Parents across Educational Levels" |
| C04 | captured | "Age-progressive Framework" |
| C05 | captured | "Guide to Generative AI tools for Learning" |
| C06 | captured | "Guidance on Generative AI" |
| C07 | captured | "When used appropriately, these tools can support students..." |
| (C07-alt 윤리4원칙) | skip | 404 → not_found (인용 금지) |

## 4. captured / partial / failed 목록
- captured: C02·C03·C04·C05·C06·C07 (6)
- failed(초기)→재시도 captured: C05 (곱슬 아포스트로피 '·'...' 때문 최초 실패 → 아포스트로피 없는 부분문자열로 교체 후 성공)
- partial: 없음
- skip: C07-alt-ethics(404)

## 5. 생성된 PNG 파일
`assets/ai-early-education/singapore-evidence/`
- c02_moe_ai_education_20260704.png (~120KB, 1280×984)
- c03_students_parents_20260704.png (~127KB)
- c04_age_progressive_framework_20260704.png (~127KB)
- c05_parent_guide_genai_20260704.png (~115KB)
- c06_sls_guidance_genai_20260704.png (~113KB)
- c07_responsible_use_genai_20260704.png (~115KB)
> 각 이미지 = 상단 출처 라벨 바(우리 부착, 명시) + 하단 실제 페이지 캡처(원문 영어). 육안 검증: C03·C06 = 진짜 MOE/SLS 페이지 확인.

## 6. manifest 갱신 내용
- 각 컷: capture_status=captured, actual_capture_file, captured_at=2026-07-04, visible_text_confirmed, capture_method=automated_browser_playwright.
- C05 caution에 최초 failed→재시도 captured 이력 정직 기록.

## 7. 실패 원인 (해결됨)
- C05 최초 실패: `visible_highlight_text`에 `...`와 곱슬 아포스트로피(’) 포함 → 정확 매칭 실패. 해결: 아포스트로피 없는 부분문자열("Guide to Generative AI tools for Learning")로 교체 후 captured.

## 8. 검증 결과
| 항목 | 결과 |
|---|---|
| 스크립트 실행 가능 | ✓ |
| captured/partial/failed 정직 기록 | ✓ |
| PNG 실제 생성·크기≠0 | ✓ (6개, 112~127KB) |
| 캡처가 실제 웹페이지 본문 포함 | ✓ (C03·C06 육안 확인) |
| source_url 메타 바 포함 | ✓ (상단, 라벨 명시) |
| 미발견 문구 failed/skip | ✓ (C07-alt skip) |
| manifest JSON 유효 | ✓ |
| 영상 제작·업로드·HTML·sitemap·배포 | 0 ✓ |

## 9. 다음 단계
1. 캡처 6장 검수(필요 시 특정 컷 재캡처).
2. 대본 v2 타임코드에 캡처 삽입안 병합(별도 승인).
3. 이미지/카드 에셋 제작 → 1차 편집 → 사람 검수 → 업로드.
4. 재사용: UNESCO·영국 JCQ·한국 교육부도 같은 스크립트로 evidence manifest만 만들어 캡처.
