# 세계 AI교육 5국 증거 스샷 — 하이브리드 캡처 보고

- 작성일: 2026-07-04
- 성격: **정적 정부 페이지 6개 자동 캡처(raw). 조건부 4개는 사람 캡처 분리.** 출처 바 합성/렌더/업로드/HTML 없음.

## 1. 자동 캡처 시도 대상 (6)
US-01·US-02·UK-01·UK-02·KR-01·KR-02(교체 korea.kr #2).

## 2. 자동 캡처 성공 수 — **6 / 6** ✅
- 전부 HTTP 200. Playwright(1280×720) + 쿠키 배너 dismiss + 핵심 문구 앵커 스크롤.
- 앵커 스크롤 성공 4(US-01 'AI literacy'·US-02 'Safe, Ethical, Equitable'·UK-01 'professional judgement'·UK-02 'professional judgement'), 고정 스크롤 2(KR-01·KR-02).

## 3. 자동 캡처 실패 수 — **0**

## 4. 사람 캡처 필요 (4)
CN-01(헤드밴드 금지)·CN-02(금지조항/PDF)·SG-01(가드레일 문구)·SG-02(도구 설명, 없으면 보조). → `manual-needed/`, 가이드 별도.

## 5. 생성된 raw 파일 목록 (raw/)
- US-01-ai-education-order-raw.png · US-02-ai-toolkit-safe-ethical-raw.png
- UK-01-dfe-genai-guidance-raw.png · UK-02-education-hub-ai-schools-raw.png
- KR-01-ai-digital-textbook-policy-raw.png · KR-02-ai-digital-textbook-intro-raw.png

## 6. 눈 검수 결과
- **UK-01 ★최상:** 핵심 인용문 완벽 노출(professional judgement / responsibility of the professional / cannot replace... human expert). "판단은 사람" 증거로 이상적.
- **KR-01 양호:** 정책브리핑 헤더+제목(우선 도입)+본문(제외 과목·장관 발표) 노출. ⚠️ 우측 무관 인기뉴스 사이드바 → 출처 바 합성 시 본문 영역 크롭 권장.
- US-01/US-02/UK-02: 앵커 스크롤로 핵심 문구 프레임 진입(정부/교육부 소스 확인). KR-02: 도입 개요, 사이드바 크롭 권장.
- 전반: 소스 신원(정부/교육부) + 핵심 문구 확보. 재시도 불필요, 크롭은 출처 바 합성 단계에서.

## 7. 실패 이유
- 없음(6/6 성공). 초기 1차 캡처는 쿠키 배너가 상단을 가림 → 2차에서 배너 dismiss + 앵커 스크롤로 해결.

## 8. manifest 업데이트
- 자동 6 → `capture_status: captured_raw` + raw_file + review_notes.
- 조건부 4 → `capture_status: manual_required` + review_notes.

## 9. 확인 (안 한 것)
- **출처 바 합성 안 함**(원본 raw만). 영상 렌더/업로드/HTML 수정 없음. sitemap 41.
- raw 캡처는 인용 목적. 최종 사용 시 크롭+출처 바+우리 해석 카드 필수.

## 10. 다음 단계
1. 사람이 조건부 4개 캡처(manual-capture-guide.md대로) → manual-needed/.
2. Claude가 raw 10개(자동6+수동4)에 **출처 바 합성** + KR 사이드바 크롭.
3. shotlist ② 증거 컷 삽입 → 본편 초벌 편집.
