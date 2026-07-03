# AI 조기교육 — parent-cluster SEO / 내부 링크 점검 보고서

- 작성일: 2026-07-03
- 담당: Claude (사이트 운영 위임, MAINTENANCE.md 기준)
- 성격: **점검 + 최소 수정**(새 페이지·PDF·sitemap URL 추가 없음). 여행사이트 무손상, ai-craft-kids 비관련 미커밋 제외.

## 1. 점검한 페이지 수 — 15개
index, start-here, compare, parent-faq, for-parents, age-guide, home-experiments, parent-rules, checklist, printable-checklist, printable-rules, experiment-log, age-cards, downloads, school-vs-home

## 2. 발견한 문제
1. **downloads title/description 노후** — '출력 자료 모음 · 체크리스트·약속표·실험 기록지'(3종)로, 4종 세트 정리(연령 카드 추가)와 불일치. "다운로드"로 오해될 여지.
2. **checklist ↔ printable-checklist 검색의도 중복** — checklist description이 "인쇄해서 쓰는 부모 체크리스트"라고 해 printable-checklist(인쇄용)와 겹침. checklist는 '설명형(왜)'이어야 함.
3. **내부 링크 흐름 갭 2건** — 권장 흐름 대비: `for-parents → downloads` 누락, `home-experiments → printable-rules` 누락.
4. **앵커 텍스트 불일치** — 3개 페이지(checklist/parent-rules/home-experiments)가 downloads를 아직 '출력 자료 모음(체크리스트·약속표·기록지)' 3종 문구로 링크.
5. **index 히어로 과밀** — '그 외' 줄에 인쇄물 4종을 개별 나열 + downloads 허브까지 = 6개 링크로 첫 화면 과점유(허브와 중복).

> 모호한 anchor("여기 클릭" 등) : **0건**. 중복 title : **0건**.

## 3. 수정한 파일
| 파일 | 변경 |
|---|---|
| `downloads.html` | title/description/og → '출력 자료 4종 세트'(연령 카드 포함), '브라우저 인쇄' 문구로 PDF 오해 차단 |
| `checklist.html` | description → 설명형(왜·무엇을) 의도로 분리, '인쇄해서 쓰는' 제거 · downloads 앵커 4종 통일 |
| `for-parents.html` | 내부 링크 `→ downloads` 추가(갭 메움) |
| `home-experiments.html` | 내부 링크 `→ printable-rules` 추가 + 실험 준비물 3종 줄 · downloads 앵커 4종 통일 |
| `parent-rules.html` | downloads 앵커 4종 통일 |
| `index.html` | 히어로 '그 외' 줄: 인쇄물 4종 개별 → downloads 허브 1개로 통합(+FAQ·용어사전) |
| `../홈페이지 통합관리/projects.json` | next_action 갱신 |
| `patch_log.json` | 항목 추가 |
| `reports/AI_EARLY_EDUCATION_PARENT_CLUSTER_SEO_AUDIT_REPORT.md` | 본 보고서 |

## 4. title/description 점검 결과
- 15/15 페이지 모두 title + description 존재.
- **중복 title 0.** 검색 의도 페이지별 분리 확인(start-here=입문 / compare=시작점 / faq=질문 / for-parents=한국 부모 / age-guide=연령 설명 / age-cards=연령 인쇄카드 / home-experiments=실험 / parent-rules=약속 / checklist=설명형 / printable-*=인쇄용 / experiment-log=기록지 / downloads=4종 허브 / school-vs-home=역할 비교).
- 수정으로 checklist(설명)↔printable-checklist(인쇄), downloads(3종→4종) 의도 겹침 해소.

## 5. 내부 링크 흐름 점검 결과
- 권장 흐름 대부분 충족. **갭 2건 메움**(for-parents→downloads, home-experiments→printable-rules).
- 클러스터 전체 내부 링크 **깨짐 0**.
- downloads 앵커 텍스트 3곳 4종으로 통일 → 사이트 전반 일관성 확보.
- index 히어로는 downloads를 단일 허브로 두어 순환(대문→허브→4종, 각 자료→허브·FAQ) 강화.

## 6. downloads 최종 상태
- 예정/soon/start-here-print/요약지 문자열 **0**.
- ready 자료 **4종**, 사용 순서 1~5 유지.
- title/description이 4종 세트로 정합, 'PDF 다운로드' 오해 문구 없음('인쇄용 HTML 보기').

## 7. sitemap URL 수
- **39 유지** (URL 추가/삭제 없음).

## 8. 배포 여부
- 배포: **완료** (git push origin main → wrangler 클린 배포).

## 9. 검증 결과
| 항목 | 결과 |
|---|---|
| 로컬 200 | ✓ |
| 라이브 200 | ✓ |
| 대상 15페이지 title/description 존재 | ✓ (15/15) |
| 중복 title | 0 ✓ |
| 내부 링크 깨짐 | 0 ✓ |
| downloads 예정/soon/start-here-print | 0 ✓ |
| index 히어로 CTA 3개 유지 | ✓ |
| 광고성 CTA / 특정 AI 추천 | 없음 ✓ |
| PDF/영상/상품/새 페이지 생성 | 0 ✓ |
| sitemap URL 수 39 유지 | ✓ |
| 기존 페이지 무손상 / 여행사이트 미변경 | ✓ |
| working tree | 이번 점검 세트만 커밋, 비관련 제외 ✓ |
