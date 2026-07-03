# 싱가포르 근거 캡처 — 실행 지침 (사람/브라우저 단계)

> 문구 검증은 완료(2026-07-04, evidence_manifest.json 참조). 아래는 **실제 PNG 캡처**만 남은 단계.
> AI가 정부 페이지의 진짜 스크린샷을 대신 만들 수 없음 → 브라우저에서 직접 캡처(가짜 이미지 금지).

## 공통 규칙
- 브라우저 **주소창(URL)이 보이게** 캡처.
- 캡처 전 페이지에서 아래 "필수 확인 문구"가 **실제로 보이는지** 눈으로 확인. 안 보이면 캡처하지 말 것.
- 파일은 이 폴더에 manifest의 filename 그대로 저장.
- 쿠키/배너는 닫고, 핵심 문구가 화면에 나오도록 스크롤.

## 캡처 목록
| 파일명 | URL | 필수 확인 문구 |
|---|---|---|
| c02_moe_ai_education_20260704.png | .../artificial-intelligence-in-education | "Artificial intelligence in education" · "age- and developmental- appropriate" |
| c03_students_parents_20260704.png | .../20251104-developing-age-progressive-framework...students-and-parents... | 제목 "...for **Students and Parents** across Educational Levels" |
| c04_age_progressive_framework_20260704.png | (C03과 동일 페이지) | 제목 "**Age-progressive** Framework" |
| c05_parent_guide_genai_20260704.png | (C03 답변 본문) 또는 Parents Gateway | "**A Parent's Guide to Generative AI tools for Learning**" |
| c06_sls_guidance_genai_20260704.png | .../ai-in-sls/responsible-ai/guidance-on-generative-ai/ | "Guidance on Generative AI" · "Singapore Student Learning Space (SLS)" |
| c07_responsible_use_genai_20260704.png | (C06과 동일 페이지) | "When used appropriately, these tools can support students..." |

## 사용 금지 (확인 실패)
- AIEd Ethics Framework 페이지 `.../ai-in-education-ethics-framework/` → **404(2026-07-04).** 4원칙(Agency·Inclusivity·Fairness·Safety) 화면 표기·인용 금지.
- C06 페이지의 "responsible use" / "safe" 단어 → 본문 미노출. 하이라이트 금지.

## 캡처 후
1. manifest의 `capture_status`를 `pending_manual` → `captured`로, `capture_date` 기록.
2. 대본 v2 타임코드에 컷 삽입안 병합(다음 단계, 별도 승인).
