# 조건부 4개 자동 캡처 — 검수 보고

- 작성일: 2026-07-04
- 성격: **조건부 4개(CN-01/CN-02/SG-01/SG-02) 자동 캡처 + 검수.** 출처 바 합성/렌더/업로드/HTML 없음.

## 1. 자동 캡처 시도 대상 (4)
CN-01(CGTN)·CN-02(CSET)·SG-01(MOE SLS)·SG-02(GovTech).

## 2~5. 검수 결과 분류
| 구분 | 수 | 대상 |
|---|---|---|
| captured_pass | **3** | CN-02·SG-01·SG-02 |
| captured_partial | **1** | CN-01(크롭 필요) |
| captured_rejected | 0 | — |
| auto_failed | 0 | (CN-01 1차 404 → /p.html 재캡처로 해결) |

## 6. 생성된 이미지 파일 (manual-needed/)
- CN-01-classroom-ai-policy-raw.png
- CN-02-genai-guide-guardrail-raw.png
- SG-01-moe-ai-sls-raw.png
- SG-02-govtech-ai-classroom-raw.png

## 7. 각 이미지 검수 결과
- **CN-01 (captured_partial):** CGTN 제목 + 교실 AI 장면(로봇+학생+교사). **뇌파 헤드밴드 없음 ✅.** 단 우측 TOP NEWS에 시진핑/군 인사 정치뉴스 + 하단 쿠키 배너 → **본문 좌측 컬럼만 크롭 필수**(정치 선전 오독 방지). 크롭 후 사용 가능.
- **CN-02 (captured_pass):** 핵심 문구 완벽 — *"avoiding potential harms such as plagiarism and cheating"* + CSET 번역 출처 + 중국 교육부 가이드 명시. "과의존 경계" 증거로 최적.
- **SG-01 (captured_pass):** SLS 맥락 + *"additional guardrails are deployed for students to have a safe learning experience"* + About AI in SLS 출처. "가드레일" 증거 완벽.
- **SG-02 (captured_pass):** 배너 아님. **실제 AI 도구 상세**(Speech Evaluation Tool·Learning Assistant·Authoring Copilot·Data Assistant, 학생·교사용) + GovTech 로고. "안전한 틀" 보강 확보.

## 8. CN-01 헤드밴드 프레임 여부 — **없음 ✅**
교실 AI 수업 장면(로봇·학생·교사)만 포함. 뇌파 헤드밴드/감시 프레임 미포함. (단 우측 정치 사이드바는 크롭으로 제거.)

## 9. SG-02 보조 격하 여부 — **격하 안 함 (captured_pass)**
실제 도구 4종 설명이 명확해 메인 증거로 사용 가능.

## 10. 확인 (안 한 것)
- **출처 바 합성 안 함**(원본 raw만). 영상 렌더/업로드/HTML 수정 없음. sitemap 41.
- 크롭 대상: **CN-01**(정치 사이드바+쿠키), **KR-01·KR-02**(우측 인기뉴스 사이드바). 나머지 minor(chat 위젯).

## 11. 다음 단계
1. 10개 raw 사용 가능(pass 9 + partial 1). **크롭 3개(CN-01·KR-01·KR-02)** 먼저.
2. **출처 바 합성**(국문/영문, 출처 성격 포함) → captured/ 최종본.
3. shotlist ② 증거 컷 삽입 → 본편 초벌 편집.

## 요약(완료 보고용)
- 자동 캡처 시도 4 / pass 3 / partial 1 / rejected 0 / failed 0.
- 사용 가능 10/10(자동6+조건부4, CN-01은 크롭 후). 사용 금지 0.
