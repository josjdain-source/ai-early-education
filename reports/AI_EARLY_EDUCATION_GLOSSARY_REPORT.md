# AI_EARLY_EDUCATION_GLOSSARY_REPORT

> 2026-07-03 · 용어 장벽 제거: 용어사전. parent-faq(질문 흡수)·source-library(근거 신뢰)와 함께 검색 유입 방어막 3종의 마지막.
> 역할: parent-faq=질문으로 들어온 부모 / glossary=단어에서 막힌 부모 / source-library=근거 궁금한 독자.
> 지시 준수: 특정 서비스·유료/상품/쿠팡/영상/유튜브·공포·아이 혼자 사용 권장 없음. 저작권·개인정보는 일반 안전 안내 수준. 법률 자문 아님. 새 국가 사실 없음. JS 없음.

## 1. 생성한 URL
- `/ai-early-education/glossary.html` — “AI 조기교육 용어사전: 부모가 알아야 할 핵심 단어”
- 부제: “생성형 AI, 프롬프트, 할루시네이션, AI 리터러시 같은 용어를 부모 눈높이로 정리했습니다.”

## 2. 수정한 파일
- 신규: `ai-early-education/glossary.html`, `reports/이 파일`
- `index.html`(세계 분석 안내줄에 📖 용어사전), `parent-faq.html`(‘못 찾았다면’에 용어사전), `start-here.html`(다음 글), `source-library.html`(함께 보기), `ai-conversation-before-coding.html`(하단 ‘용어 낯설다면’)
- `sitemap.xml` — glossary URL 추가(총 35).
- 조종판 `projects.json` 액션·status · `patch_log.json` 기록.
- (기존 5개 링크만 +5줄, 무손상)

## 3. 핵심 용어 12개 목록 (각 h3, SEO)
1. 생성형 AI 2. 프롬프트 3. AI 리터러시 4. 디지털 리터러시 5. 할루시네이션 6. 개인정보 7. 보호자 동반 8. 교사 감독 9. 과제 윤리 10. 출처 확인 11. AI 디지털교과서 12. AI 튜터
- 각 카드 구조: **뜻(l-mean) / 부모용(l-parent) / 조심(l-care) / 관련 글**. 학술 정의 아니라 ‘우리 집 연결’ 중심.

## 4. 안전·윤리 용어 처리 방식
- 별도 섹션(미니 카드): 편향·저작권·AI 사용 표시·데이터 학습·부적절한 답변·나이 제한.
- **저작권·개인정보는 ‘일반 안전 안내 수준’으로만** 명시(‘법률 자문이 아닙니다’ 문구). 자세한 약속은 parent-rules로 위임.
- 학교·정책 용어(AI 교육 정책·국가 플랫폼·교사 연수·형평성·평가 공정성·생성형 AI 가이드라인)는 매트릭스/모델/국가별로 연결.

## 5. 기존 FAQ/source-library/start-here와 연결
- **검색 방어막 3종 완성**: parent-faq(질문)·glossary(용어)·source-library(근거)가 서로 링크로 물림.
- 역방향 유입: index·parent-faq·start-here·source-library·3편(ai-conversation)에서 glossary로.
- glossary → 각 용어의 ‘관련 글’로 행동 페이지(home-experiments·parent-rules·checklist·printable 등) 분기. 하단 다음글에 parent-faq·start-here·source-library·matrix.

## 6. SEO 처리
- title: `AI 조기교육 용어사전 | 부모가 알아야 할 생성형 AI·프롬프트·할루시네이션 뜻`, description에 대표 용어.
- 각 용어를 **h3**(용어명 그대로 = ‘생성형 AI 뜻’ 류 검색 매칭), 섹션은 h2. 영문 병기(generative AI 등)로 추가 매칭.

## 7. 배포 여부
- **배포 완료**(예정): commit → push → 런북 클린 배포. 라이브 200.

## 8. 검증 결과 (12/12)
- 로컬 200 / 라이브 200: glossary·index·parent-faq·start-here·source-library·3편·sitemap
- 내부 링크: glossary 내 전부 유효, 깨짐 0 · 전체 사이트 재크롤 깨진 링크 0
- sitemap: 35 URL, XML 유효
- 모바일: 본문 max-width 800, 용어 카드·미니 카드(모바일 1열)
- 용어 heading 구조: `.term > h3` 12개 + 섹션 h2
- 광고성 CTA·특정 서비스: 없음
- 영상/유튜브/상품 파일 생성: 없음
- 기존 페이지: 무손상(5개 링크만 +5줄)
- JS: 없음
- patch_log·working tree: 세트만 커밋

## 다음 후보
- `downloads.html`(부모용 출력 자료 모음 — printable-checklist 중심, 이후 약속표·실험 기록지 확장).
