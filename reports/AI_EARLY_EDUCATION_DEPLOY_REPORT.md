# AI 조기교육 — 영상 카테고리판 배포 보고

- 작성일: 2026-07-04
- 성격: **라이브 배포 완료(wrangler 클린 배포).** 배포·검증만, 추가 수정 없음.

## 1. 배포 정보
- 방식: `git archive main | tar -x` → `npx wrangler pages deploy` (추적분만, .gitignore 임시/음성 제외)
- 프로젝트: `ai-early-education` (Cloudflare Pages) · 커밋 기준: `81a9d71`
- 결과: ✨ Deployment complete · 이번 배포 alias `https://01e624b6.ai-early-education.pages.dev`
- 프로덕션: **https://ai-early-education.pages.dev/ai-early-education/**

## 2. 배포 후 검증 (10항목)
| # | 항목 | 결과 |
|---|---|---|
| 1 | 라이브 메인 200 | ✅ 200 |
| 2 | video-countries 200 | ✅ 308→**200** (CF Pages가 `.html`→`/video-countries` 클린URL로 자동 리다이렉트, 브라우저 투명 처리) |
| 3 | sitemap 40 URL 반영 | ✅ 라이브 40, video-countries 포함 |
| 4 | 메인 = 분야별 영상 카테고리판 | ✅ "영상으로 먼저 보세요" + 대표(나라별) 1 + 카테고리 6 |
| 5 | 나라별 대표 카드 → video-countries 연결 | ✅ `/video-countries.html`(+#feature) |
| 6 | 중국·미국·영국·싱가포르·한국·세계5분 카드 노출 | ✅ 6장 전부 |
| 7 | 각 나라 '근거 보기' 실존 연결 | ✅ china/us/uk/singapore/korea 전부 200 |
| 8 | source-library·global-matrix 연결 | ✅ 둘 다 200 |
| 9 | 모바일 카드 1열 정렬 | ✅ 라이브 모바일(390px) 1열 확인 |
| 10 | 배포 보고서 | ✅ 본 문서 |

## 3. 관찰 사항 (수정 안 함, 보고만)
- **video-countries.html → 308 리다이렉트**: Cloudflare Pages 기본 동작(`.html` 제거한 클린 URL로 영구 리다이렉트). 최종 200 정상 착지, 링크 클릭에 문제 없음. 내부 링크를 확장자 없는 형태로 바꾸면 리다이렉트 홉 1회를 줄일 수 있으나 **지시대로 임의 수정하지 않음**(추후 결정 사항).
- wrangler 실행 중 홈 디렉토리 정션(Application Data 등) 접근 경고 → 권한 없는 Windows 시스템 폴더, 배포와 무관(업로드는 $TMP 추출본만).

## 4. 판정
- **무대(방송국 건물) 라이브 완료.** 영상은 '준비 중'이지만 모든 카드가 실존 근거 페이지로 연결 → 빈껍데기 아님.
- 구조가 라이브로 고정됨. 이제 홈페이지를 더 흔들지 않고 **영상 제작**에 집중 가능.

## 5. 다음 순서 (사이트 아님, 영상)
1. 세계 AI 조기교육 5분 본편 대본
2. 중국·미국·영국·싱가포르·한국 쇼츠 5개 대본
3. 영상 썸네일 문구
4. video-countries.html 카드의 '준비 중' → 실제 영상 링크로 교체(구조 그대로 href만).
