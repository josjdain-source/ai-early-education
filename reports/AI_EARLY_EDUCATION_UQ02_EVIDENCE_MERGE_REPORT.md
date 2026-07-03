# UQ-02 싱가포르 5분 영상 — 대본×캡처 병합 보고

- 작성일: 2026-07-04
- 성격: **대본 타임코드 + 자동 캡처 PNG 병합(편집 지침).** 영상 제작·렌더·업로드·HTML·sitemap·배포 없음.
- 대상: `content/longform/ai-early-education/episode_02_singapore_parent_framework_5min.md` §10·§11 추가

## 1. 병합한 PNG 목록 (6/6, captured·크기≠0)
| cut | 파일 | 크기 | 확인 문구 |
|---|---|---|---|
| C02 | c02_moe_ai_education_20260704.png | 119,945 | Artificial intelligence in education |
| C03 ★ | c03_students_parents_20260704.png | 126,797 | ...for Students and Parents across Educational Levels |
| C04 | c04_age_progressive_framework_20260704.png | 126,687 | Age-progressive Framework |
| C05 ★ | c05_parent_guide_genai_20260704.png | 114,861 | Guide to Generative AI tools for Learning |
| C06 | c06_sls_guidance_genai_20260704.png | 112,835 | Guidance on Generative AI / SLS |
| C07 | c07_responsible_use_genai_20260704.png | 114,859 | When used appropriately, these tools can support students... |

## 2. 타임코드별 배치 요약 (대본 §10 병합표)
- 0:30~0:42 **C02** — MOE AI in Education 출처 카드
- 0:42~1:00 **C03** — "Students and Parents" 제목 하이라이트 (영상의 허리)
- 1:00~1:15 **C04** — "Age-progressive Framework" (C03과 동일 페이지)
- 1:15~1:25 **C05** — "A Parent's Guide..."(Parents Gateway) (부모 포함 결정적 증거)
- 1:25~1:35 **C06** — SLS / Guidance on Generative AI
- 2:20~2:45 **C07** — "When used appropriately..." 확인 문장
- 4:50~5:10 **홈 연결 카드** — age-guide·age-cards·parent-rules·printable-checklist

## 3. 공식 근거 화면 표시 방식
- 원문 캡처 2~4초 → 핵심 문구 확대/하이라이트 2~3초 → 한국어 요약 카드 3~5초.
- 하단 **출처 라벨 유지**(기관+확인일 2026-07-04+URL, "정책 변동 가능").
- 허용: 하이라이트 박스·확대 크롭·한국어 요약 카드. **금지: 원문 문구 변경·번역 삽입·미확인 문구 강조·윤리 4원칙 재삽입·정답 연출.**

## 4. 추가로 필요한 에셋 (대본 §11, 미확보)
부모/아이 거실 장면 · 연령 4단계 카드 · 부모 질문 4개 카드 · 학교 vs 가정 도식 · 결론 3개 카드 · 홈페이지 연결 카드 · 출처 표기 카드 템플릿 · 자막/BGM 프리셋.
→ 공식 근거 PNG는 확보 완료. 제작 에셋은 편집 착수(별도 승인) 시 생성.

## 5. update_queue 상태
- UQ-20260704-02: **reviewing → evidence_merged**. `approved_by`/`applied_commit` 여전히 null. **approved/applied/published 아님.**

## 6. 검증 결과
| 항목 | 결과 |
|---|---|
| PNG 6개 존재·크기≠0 | ✓ (112~127KB) |
| manifest captured 상태 | ✓ (C02~C07 captured, C07-alt skip) |
| 대본 타임코드 병합표 추가 | ✓ (§10) |
| 확인된 문구만 사용 | ✓ |
| 윤리 4원칙 미사용 | ✓ ("Agency"는 재삽입 금지 경고로만 등장) |
| 싱가포르 과장 없음 | ✓ |
| 영상 제작·렌더·업로드 | 0 ✓ |
| HTML·sitemap·배포 | 0 ✓ (sitemap 39) |
| JSON 유효 | ✓ |
| UQ-02 approved/applied 아님 | ✓ (evidence_merged) |

## 7. 다음 단계
싱가포르 편이 **관측→큐→대본→근거 설계→자동 캡처→병합**까지 닫힘(첫 완성 사례). 다음(별도 승인): 제작 에셋 생성 → 1차 편집 → 사람 검수 → 업로드. 이후 다음 국가/주제는 이 파이프라인 재사용.
