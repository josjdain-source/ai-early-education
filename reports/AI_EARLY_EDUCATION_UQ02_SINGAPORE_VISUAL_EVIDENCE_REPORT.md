# UQ-02 싱가포르 5분 영상 — 근거 화면 설계 보고

- 작성일: 2026-07-04
- 성격: **근거 화면(시각 증거) 설계.** 영상 제작·캡처·업로드·HTML·sitemap·배포 없음.
- 파일: `content/longform/ai-early-education/episode_02_singapore_visual_evidence_plan.md`
- 함께 수정: 대본 v2 블로그 요약문 "두 가지 → 세 가지"(결론 3개와 일치)

## 1. 생성/수정한 파일
- (재작성) `episode_02_singapore_visual_evidence_plan.md` — 컷별 전체 필드 스키마로 구조화
- (수정) `episode_02_singapore_parent_framework_5min.md` — 블로그 요약문 3가지로 정정
- (신규) `reports/AI_EARLY_EDUCATION_UQ02_SINGAPORE_VISUAL_EVIDENCE_REPORT.md` — 본 보고서

## 2. 근거 컷 개수
**11컷** = 필수 6(C02~C07) + 지원 3(C08~C10) + 연결 2(C01·C11) + 보조 전환 3(T1~T3, 짧게).
각 컷 필드: cut_id · timecode · narration_reference · visual_type · source_priority · source_url · what_to_show · highlight_text · korean_overlay · why_needed · caution.

## 3. 필수 공식 자료 컷 목록
| cut | 무엇 | 하이라이트 | 검증 |
|---|---|---|---|
| C02 | MOE AI in Education 페이지 + 출처 카드 | "Artificial Intelligence in Education" | URL 확인 |
| C03 | ★국회답변 제목 | **"Students and Parents"** | ✅ 문구 실증(2026-07-04) |
| C04 | 같은 제목 | **"Age-progressive Framework"** | ✅ 실증 |
| C05 | ★학부모용 가이드(Parents Gateway) | **"A Parent's Guide to Generative AI"** | ✅ 답변 본문 언급 확인 |
| C06 | SLS Guidance on Generative AI | "Student Learning Space" | 캡처 시 확인 |
| C07 | Responsible/Safe use 가이드 | "responsible use"/"safe" | ⚠️ 4원칙은 미확인→조건부 |

## 4. 타임코드별 배치 요약
- 0:00~0:20 부모 장면(C01, +T3 ≤1s)
- 0:20~1:22 싱가포르 근거 집중(C02→C03→C04→C05→C06, +T1) — 초반에 증거를 몰아 신뢰 선점
- 1:22~2:20 우리 해설 연령 4단계(C08)
- 2:55~3:20 근거+해설(C07→C09 부모 질문4)
- 3:20~4:10 학교 vs 가정(C10)
- 4:20~5:00 홈페이지 연결(C11)
> 공식 근거(C02~C07) ≈ 1:25 ≈ **28%** (목표 30% 근접). 부모장면 20 / 우리해설 35 / 연결 15 설계.

## 5. 필요한 에셋 목록
공식 페이지 캡처 6종(URL 바 포함) · 출처 카드 템플릿 · 부모/아이 거실 일러스트 · 교사·학생·부모 아이콘 · 연령 4단계 카드 · 부모 질문 4개 카드 · 학교 vs 가정 도식 · 홈페이지 연결 카드 · 국기/추상 교실/도시 상징(≤1s).

## 6. 저작권/출처 표기 방식
- 공식 화면은 **일부 캡처 2~4초 + 핵심 문구만 하이라이트**(원문 장시간 노출 금지)
- **출처 카드 상시**: "Singapore MOE/SLS · 확인일 2026-07-04 · 정책은 바뀔 수 있음"
- 원문 왜곡·과장 크롭·의역 금지(번역 자막은 '번역' 표기)
- 확인 안 된 문구 사용 금지 → C07의 AIEd 4원칙(Agency·Inclusivity·Fairness·Safety)은 **직접 확인 실패**로 캡처 시 공식 페이지 확인 전 화면 표기 금지, 실패 시 "책임 있는 사용 원칙" 일반 표현 대체.

## 7. 검증 결과
| 항목 | 결과 |
|---|---|
| 근거 컷 8~12개 | 11(+보조3) ✓ |
| 필수 공식 자료 컷 6종 요구 충족 | C02~C07 ✓ (MOE·students and parents·age-progressive·SLS·responsible use·홈연결은 C11) |
| 비율 20/30/35/15 설계 | ✓ (근거 ≈28%) |
| 관광 이미지 보조·≤1s | ✓ (T3) |
| 싱가포르=정답 과장 | 없음 ✓ |
| 원문 짧은 하이라이트+출처 카드 | ✓ |
| 부모 이해용 한국어 해설 카드 병치 | ✓ (korean_overlay) |
| 사실 실증/조건부 명시 | C03·C04·C05 실증, C06·C07 캡처 시 확인 ✓ |
| 블로그 요약 3가지 정정 | ✓ |
| 새 HTML·sitemap·배포·영상 제작·업로드 | 0 ✓ |
| UQ-02 상태 | reviewing(draft), applied 아님 ✓ |

## 8. 다음 (승인 후)
C02~C07 페이지 재방문 → 문구 현존 확인 → 캡처(URL 바) → 출처 카드 → 대본 v2에 컷 타임코드 병합 → (별도 승인) 편집·렌더·검수·업로드.
