# b-roll timeline 업데이트 — 작업 보고

- 작성일: 2026-07-04
- 성격: **evidence를 실제 영상장면(4국)+영국 문서로 교체한 timeline 생성.** 렌더/업로드/HTML/링크 없음.

## 1. UK 결정 — **A안(문서 evidence 유지)**
- 영국 파트 = UK-01 DfE 문서(정책 "AI는 교사를 대체하지 않고, 최종 판단·책임은 사람에게"). teacherless 영상 미사용.

## 2. teacherless footage 배제 이유
- David Game 'teacherless' = 우리 메시지 "AI는 도구, 판단은 사람"과 **정면 충돌** → 절대 사용 안 함. 영국 핵심은 현장이 아니라 **정책 원칙**이라 DfE 문서가 가장 정확.

## 3. 영상 장면으로 교체한 국가 수 — **4** (중국·미국·싱가포르·한국)
- CN-video-scene(WSJ 유치원 AI로봇) · US-video-scene(InvestigateTV 교실+노트북) · SG-video-scene(CNA 학생 태블릿) · KR-video-scene(MOE AI교과서 UI).

## 4. 문서 evidence 유지 국가 — **1** (영국, UK-01 DfE)

## 5. 기존 문서 스샷 10장 중 본편 사용 수 — **1** (UK-01만). 나머지 9장 = 본편 제외(근거 보관용).

## 6. 새 timeline 길이 — **3:44 (225s)** (compact와 동일 유지)

## 7. 제거/통합한 evidence 컷 수
- **제거 5컷**(각 나라 둘째 evidence: C05·C09·C13·C17·C21) → 해당 시간 각 나라 **해석 카드로 흡수**.
- 나라별 evidence 2컷 → **1컷**으로 통합. 총 26컷 → **21컷**.

## 8. 확인 (안 한 것)
- **영상 렌더/업로드/HTML 수정/링크 교체 없음.** sitemap 41. compact판 timeline 보존.

## 9. 생성/수정 파일
- `production/world-ai-education-broll-edit-timeline.json` (21컷, evidence-scene 5)
- `production/world-ai-education-broll-edit-shotlist.md`
- `production/world-ai-education-video-scene-replacement-plan.md` (확정 반영 추가)
- `reports/WORLD_AI_EDUCATION_BROLL_TIMELINE_UPDATE_REPORT.md`

## 10. 다음 단계
- b-roll timeline 기준 **draft-v2 렌더**(이미지 21컷 + TTS + 자막). draft-v1과 동일 파이프라인(ffmpeg concat, 섹션 A/V 싱크). 사람 검수 후 링크 교체(별도 승인).
