# AI 조기교육 메인 — 부모용 관제판 개편 실행 보고

- 작성일: 2026-07-04
- 성격: **index.html 재구성(로컬 수정·검증까지).** ⚠️ **배포 안 함.** 페이지·자료 삭제 없음.

## 1. 수정한 파일
- `ai-early-education/index.html` (메인 대문 → 부모용 관제판 9단 재구성)
- 백업: 개편 직전 커밋(`e7900ac`)의 index.html = git 히스토리 백업(`git show HEAD~1:ai-early-education/index.html`). 임시 .bak/preview png는 정리.

## 2. 변경 전 문제
- 첫 화면 kicker가 "세계 9개국 AI 교육 비교"로 시작 → 연구자 인상.
- "오늘의 이슈"·"5분 영상" 섹션 없음. 출력자료는 보조줄 링크에만.
- 9개국 매트릭스·국기 grid가 상단(섹션 ②③) → 첫 화면 무거움. "그래서 뭘 하지?"가 안 보임.

## 3. 변경 후 메인 9단 구조
1. **Hero** — "AI 시대, 먼저 필요한 건 코딩이 아니라 대화하고 고쳐 말하는 힘" + CTA 3(대화 시작/5분 영상/출력자료). 9개국 문구 제거.
2. **오늘의 AI 교육 이슈** — 관측소 신호를 부모 언어로. 라벨 카드 3(연구 동향·검토 중·부모 체크) + 승인 게이트 안내.
3. **오늘 바로 할 수 있는 3가지** — 행동 버튼 3(대화 1번/5분 영상/활동지 출력).
4. **5분 정밀 영상** — "곧 공개" 썸네일 + 요약 3줄 + 실험 버튼(깨진 링크 없음).
5. **출력자료 4종** — 연령 카드·약속표·체크리스트·기록지 각 "출력하기" 버튼.
6. **부모 가이드** — "출력물은 결과, 교육은 과정" + 6단계(떠올리기→요청→관찰→찾기→다시 말하기→조건 바꾸기).
7. **세계 9개국(하단 신뢰 근거)** — 매트릭스·모델·국가별 + 국기 9개 + 시리즈 1·2·3.
8. **근거 보관소** — 출처 라이브러리·전체 출처·학교vs가정.
9. **Footer CTA** — "오늘 아이와 AI에게 한 번만 다시 말해보게 하세요" + 대화 연습 버튼.

## 4. 유지한 기존 자료와 링크 (삭제 0)
- 9개국: global-matrix·models·countries/(9개국)·world-ai-education-map → **하단 ⑦로 이동(유지)**
- 출처: source-library·sources → **⑧ 근거 보관소(유지)**
- 관측소: ops 신호 → **② 오늘의 이슈(부모 언어)로 연결**
- 가이드/출력/시리즈: for-parents·age-guide·parent-rules·parent-faq·glossary·home-experiments·compare·checklist·school-vs-home·downloads·age-cards·printable-rules·printable-checklist·experiment-log·start-here·korea-controversy·ai-conversation-before-coding → 전부 유지, 위치만 재배치.

## 5. 관측소 approved 없음 처리
- 현재 큐: approved 0 / reviewing·new 6 → 지시대로 **섹션 숨기지 않고 fallback**:
  - "연구 동향"(UQ-90 반영): "AI가 시험 채점에 활용될 수 있다는 연구… 단, 초등 조기교육에 바로 적용할 내용은 아니며 참고용" (과장 금지)
  - "검토 중": "여러 나라가 학교 AI 사용 기준을 만드는 중… 부모용 자료로 확정 전, 관찰 단계"
  - "부모 체크": "AI 답을 그대로 믿게 하기보다 다시 질문하는 연습이 중요"
- **new/reviewing이 승인 콘텐츠처럼 보이지 않게** 라벨(검토 중/연구 동향/부모 체크) + 하단 게이트 문구로 명시.

## 6. 깨진 링크 검증 결과
- index 내부 링크 **30개 전부 실존**(countries/ 디렉토리 포함). `href="#"`/빈 링크 **0**. 앵커 `#video` 존재.
- 로컬 200: 대문·age-cards·downloads·global-matrix·source-library 모두 200.
- 5분 영상/미완성 자료 = "곧 공개"·실제 실험 페이지로 우회(깨진 버튼 없음).

## 7. 배포 여부
- **배포 안 함.** wrangler 미실행. sitemap 미변경(신규 페이지 0, 대문 URL 이미 존재, 39 유지).
- 커밋·푸시는 함(로컬·GitHub). **라이브 반영은 별도 승인 후 wrangler 클린 배포.**

## 8. 다음 작업
1. (승인 시) wrangler 클린 배포 → 라이브 확인.
2. 5분 영상 완성 → "곧 공개"를 실제 임베드로 교체.
3. 관측소 항목 사람 승인(approved) → "오늘의 이슈"를 자동/반자동 연결(approved.json).
4. 모바일 실기기 가독성 최종 점검.
