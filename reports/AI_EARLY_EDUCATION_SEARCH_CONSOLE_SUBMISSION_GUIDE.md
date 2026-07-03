# AI 조기교육 — Google Search Console 제출 · 색인 점검 가이드

- 작성일: 2026-07-03
- 담당: Claude (문서 작성) / 실제 제출: **사용자 수동 진행** (Claude는 Search Console에 로그인 불가)
- 성격: 운영 절차 문서. **새 HTML·sitemap 변경 없음.**

> ⚠️ 과장 금지 원칙: **sitemap을 제출한다고 바로 검색에 노출되는 것이 아닙니다.** 색인(구글이 페이지를 저장)까지 며칠~몇 주, 검색 순위 반영은 그 이후입니다. 이 문서는 "제출 + 색인 확인"까지를 다룹니다.

---

## 1. 현재 사이트 상태 요약 (2026-07-03 라이브 실측)
| 항목 | 상태 |
|---|---|
| 라이브 도메인 | `https://ai-early-education.pages.dev` (Cloudflare Pages) |
| sitemap | `https://ai-early-education.pages.dev/sitemap.xml` — **HTTP 200, loc 39개** |
| robots.txt | `User-agent: * / Allow: / / Sitemap: …/sitemap.xml` — **차단 없음, sitemap 등록됨** |
| canonical | 핵심 URL 10개 전부 자기 URL로 정확히 지정(자가참조) ✅ |
| 핵심 URL 10개 | 전부 **HTTP 200** ✅ |
| 출력자료 | 4종 세트 완성(downloads 허브) |
| 부모 클러스터 | 15페이지, 중복 title 0 · 깨진 내부 링크 0 |

→ **기술적으로 제출 준비 완료 상태.**

## 2. 제출할 sitemap URL
```
https://ai-early-education.pages.dev/sitemap.xml
```
- Search Console Sitemaps 칸에는 도메인 뒤 경로만 넣으면 됩니다: `sitemap.xml`
- (robots.txt에도 이미 이 sitemap이 선언되어 있어, 구글이 자동으로도 발견할 수 있음. 그래도 수동 제출이 더 빠름.)

## 3. Search Console에서 할 일 (수동 절차)
1. **Google Search Console 접속** — https://search.google.com/search-console (제출 계정으로 로그인)
2. **속성 선택 또는 추가**
   - 아직 속성이 없으면 **URL 접두어** 방식으로 `https://ai-early-education.pages.dev` 추가
   - 소유권 확인: Cloudflare Pages는 서버 파일 업로드가 번거로우므로 **DNS 확인** 또는 **HTML 태그** 방식 권장. (HTML 태그 방식이면 확인 메타태그를 받아 사용자가 알려주면 Claude가 index에 삽입 가능 — 단, 그때 별도 요청할 것.)
3. **Sitemaps 메뉴 이동** → 새 사이트맵에 `sitemap.xml` 입력 → 제출
4. 상태가 "성공"으로 뜨고 발견된 URL 수가 **39**에 가깝게 잡히는지 확인
5. **URL 검사(색인 생성)** 로 아래 4번 핵심 URL을 하나씩 검사
6. "색인 생성 요청" 버튼이 활성화된 URL은 **5번 우선순위**대로 요청
7. **며칠 뒤** 색인 상태(색인 생성됨/제외됨)를 재확인

## 4. 우선 색인 확인할 핵심 URL (전부 라이브 200 확인됨)
1. `https://ai-early-education.pages.dev/ai-early-education/` — 코너 대문(허브)
2. `https://ai-early-education.pages.dev/ai-early-education/start-here.html` — 입문
3. `https://ai-early-education.pages.dev/ai-early-education/compare.html` — 시작점 찾기
4. `https://ai-early-education.pages.dev/ai-early-education/parent-faq.html` — FAQ(검색 대응)
5. `https://ai-early-education.pages.dev/ai-early-education/glossary.html` — 용어사전
6. `https://ai-early-education.pages.dev/ai-early-education/source-library.html` — 출처(신뢰)
7. `https://ai-early-education.pages.dev/ai-early-education/global-matrix.html` — 9개국 매트릭스
8. `https://ai-early-education.pages.dev/ai-early-education/countries/` — 국가별 허브
9. `https://ai-early-education.pages.dev/ai-early-education/downloads.html` — 출력자료 4종
10. `https://ai-early-education.pages.dev/ai-early-education/printable-checklist.html` — 인쇄용 체크리스트

## 5. 색인 요청 우선순위
검색 유입을 만들 확률과 클러스터 순환 기준으로:
1. **대문** `/ai-early-education/` — 나머지로 링크가 퍼지는 허브
2. **parent-faq** — "몇 살부터 / ChatGPT 초등학생 / 코딩 먼저" 등 질문형 검색에 직접 대응
3. **compare** — "우리 아이 AI 교육 시작점" 의도
4. **global-matrix** — "세계 AI 교육 비교" 정보형, 링크 자산
5. **start-here** — 입문 진입점
6. **downloads** — "AI 교육 체크리스트/약속표" 실용 검색
7. 나머지(glossary, source-library, countries, printable-checklist)

## 6. 제출 후 확인할 항목 (며칠~몇 주)
- Sitemaps: 상태 "성공", 발견 URL ≈ 39
- 색인 생성 리포트: "색인 생성됨" 페이지 수 증가 추이
- 페이지 리포트에서 "제외됨" 사유 확인(아래 7번)
- 실적(성능) 리포트: 노출(impression)이 잡히기 시작하는지 — 노출 → 클릭 순으로 나타남
- 어떤 페이지가 먼저 잡히는지: 대문·FAQ·매트릭스가 먼저 뜨는 경향이면 정상

## 7. 문제가 생겼을 때 대응
| 증상 | 원인/대응 |
|---|---|
| sitemap "가져올 수 없음" | URL 오타 확인. `curl -I https://ai-early-education.pages.dev/sitemap.xml`로 200 재확인 |
| "발견됨 – 현재 색인 생성 안 됨" | 정상적 대기 상태일 수 있음. 며칠 기다린 뒤 URL 검사에서 색인 요청 |
| "크롤링됨 – 색인 미생성" | 콘텐츠 얇음/중복 신호. 해당 페이지 본문·내부 링크 보강 검토(단, 무리한 증식 금지) |
| "리디렉션 포함" | Pages는 `.html` → 확장자 없는 경로로 308 정규화함. canonical이 자기 URL이면 문제 아님 |
| "대체 페이지(적절한 표준 포함)" | canonical이 다른 URL을 가리키는지 확인 — 현재는 전부 자가참조라 정상 |
| 소유권 확인 실패 | DNS(Cloudflare) 방식 재시도, 또는 HTML 메타태그 방식으로 전환 후 태그를 Claude에게 전달 |

## 8. 다음 콘텐츠 제작 기준 (제출 이후)
**제출 직후 새 글로 달리지 말 것.** 며칠간 아래를 관찰:
1. 어떤 페이지가 먼저 색인되는가
2. FAQ/glossary가 검색에 잡히는가
3. start-here·compare가 내부 이동을 만드는가(실적 리포트의 페이지별 노출)
4. downloads가 체류·순환을 만드는가

관찰 후, 신규 콘텐츠는 **감이 아니라 검색 의도별로 선별**. 후보(우선순위 미확정):
- 초등학생 ChatGPT 사용법
- 초등학생 AI 교육 주의사항
- AI 디지털교과서, 집에서 어떻게 대비할까
- AI 조기교육 몇 살부터
- 아이와 ChatGPT 쓸 때 개인정보 주의

→ 이 중 **parent-faq에서 노출이 잡히는 질문**을 골라 독립 페이지로 확장하는 것이 가장 안전(수요 검증 후 제작). 무리한 페이지 증식은 지양.

---

### 부록: 검증 로그 (2026-07-03 실측)
- `sitemap.xml` → HTTP 200, loc 39
- `robots.txt` → `Allow: /`, `Sitemap: …/sitemap.xml`, 차단 없음
- 핵심 URL 10개 → 전부 HTTP 200, canonical 자가참조 일치
