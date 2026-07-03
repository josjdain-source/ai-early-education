# AI 조기교육 — 뉴스 칸 포함 배포 보고 (편성표 완성)

- 작성일: 2026-07-04
- 성격: **라이브 배포 완료(뉴스 칸 포함).** 배포·검증만, 추가 수정 없음.

## 1. 배포 정보
- 대상 커밋: **ac8d8d7** (세계 AI교육 뉴스 카테고리 + ai-education-news.html)
- 방식: `git archive main | tar -x` → `wrangler pages deploy` (추적분만)
- 결과: ✨ Deployment complete · 신규 6파일 업로드 · alias `https://684208f7.ai-early-education.pages.dev`
- 프로덕션: **https://ai-early-education.pages.dev/ai-early-education/**

## 2. 배포 후 검증 (12항목)
| # | 항목 | 결과 |
|---|---|---|
| 1 | 라이브 메인 200 | ✅ |
| 2 | 메인에 '세계 AI교육 뉴스' 카드 노출 | ✅ (카드 + 링크 확인) |
| 3 | ai-education-news 200 | ✅ (308→200 클린URL) |
| 4 | sitemap 41 반영 | ✅ 라이브 41, ai-education-news 포함 |
| 5 | 나라별 카드 → video-countries 연결 | ✅ |
| 6 | 뉴스 카드 → ai-education-news 연결 | ✅ |
| 7 | 뉴스 주제 카드 6개 노출 | ✅ (6개 제목 전부 확인) |
| 8 | 뉴스 영상 카드 5개 노출 | ✅ (vcard 5) |
| 9 | 관측소 신호 '검토 중/연구 동향' 안전 표시 | ✅ (연구 동향 1 · 검토 중 2 · 게이트 문구) |
| 10 | source-library·global-matrix·video-countries·근거 링크 | ✅ 전부 200 |
| 11 | 모바일 카테고리 카드 밀도 | ✅ 라이브 390px 1열, 쾌적 |
| 12 | 배포 보고서 | ✅ 본 문서 |

## 3. 관찰 사항 (수정 안 함)
- `ai-education-news.html`·`video-countries.html` → CF Pages 클린URL 308 리다이렉트(최종 200 정상). 이전 배포와 동일한 기본 동작.
- 검증 중 `grep -c 'class="tcard"'`가 0으로 보였으나 `grep -o` 재확인 결과 tcard 13회·주제 제목 6개 전부 노출 = 라인 카운트 착시. **실제 6개 정상.**

## 4. 편성표 완성 판정
4칸 전부 라이브:
- **나라별 AI교육**(정책·교육 방식) · **세계 AI교육 뉴스**(언론·논쟁) · **오늘의 이슈**(관측소) · **출처 보관소**(근거).
- 한쪽 다리 빠진 상태 해소 → AI 조기교육 방송국 편성표 완성. 영상은 준비 중이나 전 카드가 실존 근거 연결.

## 5. 다음 (사이트 아님, 영상)
1. **세계 AI 조기교육 5분 본편 대본** (중국·미국·영국·싱가포르·한국 압축)
2. 쇼츠 6개: 중국/미국/영국/싱가포르/한국 + **세계 뉴스는 AI 교육을 왜 걱정할까**
3. 썸네일 문구
4. video-countries·ai-education-news 카드 '준비 중' → 실제 영상 링크 교체.
