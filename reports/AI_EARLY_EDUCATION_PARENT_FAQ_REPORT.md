# AI_EARLY_EDUCATION_PARENT_FAQ_REPORT

> 2026-07-03 · 방파제: 부모가 검색창에 넣을 법한 질문을 한곳에서 받아내고 각 질문을 기존 핵심 페이지로 넘기는 입구.
> 역할 분리: start-here=10분 입문 / compare=길찾기 / parent-faq=망설임 제거. 답변 짧게, 깊이는 내부 링크로.
> 지시 준수: 특정 서비스·유료/상품/쿠팡/영상/유튜브·공포·아이 혼자 사용 권장 없음. 법률/의료/심리 상담 아님. 새 국가 사실 없음. JS 없음.

## 1. 생성한 URL
- `/ai-early-education/parent-faq.html` — “AI 조기교육, 부모가 가장 많이 묻는 질문”
- 부제: “몇 살부터 시작해야 하는지, 혼자 써도 되는지, 코딩을 먼저 해야 하는지에 대한 현실적인 답변을 정리했습니다.”

## 2. 수정한 파일
- 신규: `ai-early-education/parent-faq.html`, `reports/이 파일`
- `index.html` — Hero CTA에 ‘❓ 자주 묻는 질문’.
- `start-here.html`·`compare.html`·`for-parents.html` — 다음 읽을 글에 parent-faq(각 최상단).
- `sitemap.xml` — parent-faq URL 추가(총 34).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.
- (기존 4개 링크만 +1줄씩, 무손상)

## 3. FAQ 12개 목록(각 질문 = h2, SEO)
1. 몇 살부터? → age-guide
2. 초등학생이 생성형 AI 써도? → parent-rules·checklist
3. 코딩 먼저? → ai-conversation-before-coding(3편)
4. 학교가 하면 집은 안 해도? → school-vs-home
5. AI 교과서 논란 있는데 집에서 써도? → 2편·school-vs-home
6. AI 답 그대로 믿으면? → parent-rules·home-experiments
7. 개인정보 어디까지? → parent-rules·printable-checklist
8. 집에서 바로 해볼 활동? → home-experiments
9. AI로 숙제하면? → parent-rules·countries/uk·age-guide
10. 유료 도구·강의 꼭 필요? → start-here·printable-checklist
11. 다른 나라는 어떻게? → global-matrix·models·countries/
12. 사이트 근거는? → source-library·sources

## 4. start-here/compare와 연결한 방식
- 상단에 ‘처음 오셨다면 먼저 보기’ 3링크(start-here·compare·printable-checklist).
- 하단 ‘아직 답을 못 찾았다면’ 추천 경로(start-here/compare · for-parents · printable+home-experiments).
- 역방향 유입: 대문 Hero CTA·start-here·compare·for-parents에서 parent-faq로.
- 각 FAQ 답변은 2~3문장으로 치고, ‘자세히 →’ 링크로 기존 페이지에 깊이 위임(방파제형).

## 5. 검색 유입 SEO 처리
- title: `AI 조기교육 FAQ | 부모가 가장 많이 묻는 질문`, description에 대표 질문 키워드.
- **각 질문을 `<h2>`로** 구성(질문 문장 그대로 = 검색 쿼리와 매칭). Q./A. 접두는 CSS `::before`로 표시(마크업은 순수 질문/답변 텍스트라 SEO 친화).
- 검색으로 특정 질문에 바로 들어와도 상단 3링크·하단 경로로 사이트 내부 순환.

## 6. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 7. 검증 결과 (12/12)
- 로컬 200 / 라이브 200: parent-faq·대문·start-here·compare·for-parents·sitemap
- 내부 링크: 필수 17개 대상 전부, 깨짐 0
- sitemap: 34 URL, XML 유효
- 모바일: 본문 max-width 780, FAQ 카드 세로·상단 3링크(모바일 1열)
- FAQ heading 구조: `.faq > h2` 12개(질문별 h2)
- 광고성 CTA·특정 서비스: 없음
- 영상/유튜브/상품 파일 생성: 없음
- 기존 페이지: 무손상(4개 링크만 +4줄)
- JS: 없음
- patch_log·working tree: 세트만 커밋

## 다음 후보
- `glossary.html`(AI 조기교육 용어사전) 또는 콘텐츠 안정화(내부 링크 점검·robots/sitemap 정리).
