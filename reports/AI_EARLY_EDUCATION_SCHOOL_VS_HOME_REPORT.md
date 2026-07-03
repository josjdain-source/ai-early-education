# AI_EARLY_EDUCATION_SCHOOL_VS_HOME_REPORT

> 2026-07-03 · 메시지 강화: 학교 AI 교육 vs 가정 AI 교육 역할 분담. 부모의 반론(“그럼 학교는? 어디까지 가정이?”)에 답하는 해석 페이지.
> 지시 준수: 학교 비난 없음 · 가정이 학교 대체한다고 안 함 · 부모 책임 과도 전가 없음 · 특정 서비스·유료/상품/쿠팡/영상/유튜브·공포 마케팅 없음. 국가 사실은 기존 페이지/source-library 기반.

## 1. 생성한 URL
- `/ai-early-education/school-vs-home.html` — “학교 AI 교육과 가정 AI 교육은 무엇이 달라야 할까?”
- 부제: “학교는 제도와 공정성을 설계하고, 가정은 아이가 AI와 안전하게 대화해보는 작은 경험을 만든다.”

## 2. 수정한 파일
- 신규: `ai-early-education/school-vs-home.html`, `reports/이 파일`
- `index.html` — 세계 분석 섹션 안내줄에 ‘학교와 가정의 역할’ 링크.
- `for-parents.html` — 다음 읽을 글에 school-vs-home.
- `korea-ai-digital-textbook-controversy.html`(2편) — 하단 next 박스에 school-vs-home(함께 보기).
- `compare.html` — 경로 ④(학교 AI 교육)에 school-vs-home 링크.
- `source-library.html` — 하단 함께 보기에 school-vs-home.
- `sitemap.xml` — school-vs-home URL 추가(총 31).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.
- (생성기 수정 불필요 — 필수 링크 전부 비생성 페이지에서 나감)

## 3. 핵심 메시지
- AI 교육은 학교가 다 해줘야 하는 것도, 가정이 학교를 대신해야 하는 것도 아니다. **둘은 역할이 다르다.**
- 학교 = 교사 설계·평가·개인정보·형평성·공정한 규칙(제도). 가정 = 대화·관찰·안전한 작은 실험(밀착 경험).
- 한 줄: **학교는 제도와 공정성, 가정은 대화와 작은 실험. 기다리지도, 떠안지도 말고 오늘 할 수 있는 것부터.**

## 4. 학교/가정 역할 비교표 요약 (4열 × 8행, tablewrap overflow-x)
- 열: 항목 / 학교의 역할 / 가정의 역할 / 부모가 지금 할 수 있는 것.
- 행(8): 시작 목적 · 사용 시간 · 개인정보 · 결과 검증 · 과제 윤리 · 아이의 말하기 · 실험 기록 · 안전 약속.
- 각 행에서 학교=제도 설계, 가정=밀착 경험, 부모=오늘의 구체 행동으로 3분할.

## 5. 세계 사례와 연결한 방식
- 싱가포르(국가 플랫폼·교사 감독 + 정부 부모 가이드 별도) / 영국(과제·시험 윤리·출처 표기 + 부모 안내 별도) / 에스토니아(교사 먼저 = 학교 설계 역량) / 한국(빠른 도입보다 설계의 중요성 = 2편). → ‘역할 분담’이 세계 공통임을 근거로.
- 모델 비교·출처 라이브러리로 근거 유도(새 사실 없음).

## 6. 기존 페이지와 연결한 방식
- 2편(한국 논란) ↔ 가정 실험 가이드를 잇는 ‘해석 다리’. 2편 하단·for-parents·compare·source-library·대문에서 유입.
- 결론부에서 home-experiments·parent-rules·checklist·age-guide·for-parents로 분기(‘집에서 할 수 있는 3가지’).

## 7. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 8. 검증 결과 (12/12)
- 로컬 200 / 라이브 200: school-vs-home·대문·2편·compare·source-library·sitemap
- 내부 링크: 필수 12개 전부, 깨짐 0
- sitemap: 31 URL, XML 유효
- 모바일: 본문 max-width 820, 역할 2열·못하는것 2열(모바일 1열)
- 비교표 모바일: `.tablewrap` overflow-x + `min-width` 스크롤
- 광고성 CTA·특정 서비스: 없음
- 영상/유튜브/상품 파일 생성: 없음
- 기존 페이지: 무손상(2편·compare·source-library·for-parents 링크만 소량 추가, 총 +5줄)
- patch_log·working tree: 세트만 커밋

## 다음 후보
- 부모 체크리스트 인쇄본 정리(또는 사이트 내부 검색/색인 개선).
