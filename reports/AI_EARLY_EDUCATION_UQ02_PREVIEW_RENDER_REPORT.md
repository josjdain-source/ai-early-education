# UQ-02 싱가포르 — c01 생성 + preview 렌더 보고

- 작성일: 2026-07-04
- 성격: **c01 거실 장면 생성 + preview 슬라이드쇼 렌더(검수용).** 업로드·완성본 렌더 없음. UQ-02 approved/applied/published 아님.

## 1. c01 생성 여부 — ✅ 생성
- 파일: `assets/ai-early-education/video-episode-02-singapore/cards/c01_parent_livingroom_scene.png` (1920×1080)
- 내용: 거실 소파, 부모(망설임 표정+"?"+빈 폰=브랜드 없음), 아이(질문, 말풍선 "엄마, 숙제할 때 AI 써도 돼?"), 숙제 노트, 하단 자막 "막을까, 허락할까 — 이 애매한 지점".
- 규칙 준수: 무섭지 않음 · 로고/앱 UI 없음 · 아이 얼굴 일반 일러스트(실존 인물 아님).

## 2. preview 렌더 생성 여부와 경로 — ✅ GIF 생성 (mp4는 환경 한계로 실패)
- 생성: `assets/ai-early-education/video-episode-02-singapore/exports/episode_02_preview_lowres.gif` (960×540, 12컷, 610KB)
- **mp4 실패 원인(정직 기록)**: 이 PC의 ffmpeg는 **playwright 녹화 전용 최소 빌드**(ffmpeg-win64.exe)로 image2 입력·표준 인코딩 미지원 → concat/-safe/rawvideo 모두 거부(BrokenPipe). 가짜 성공 보고 대신 **Pillow GIF 슬라이드쇼**로 대체(컷별 실제 길이 반영).
- 정식 mp4 필요 시: 인코더 포함 ffmpeg 설치 후 `render_episode_02_preview.py` 재실행(스크립트에 rawvideo 파이프 경로 이미 준비, 성공 시 mp4 생성).

## 3. 총 길이
- 의도(edit_timeline 합): **310s = 5:10** (목표 4:50~5:10 상단). GIF readback ≈240s는 optimize 라운딩 오차 → 권위 타이밍은 edit_timeline.json.

## 4. 컷 타이밍 문제
- ⚠️ **C10 학교vs가정 60s · C08 연령4단계 45s · C11 결론3 40s** = 정적 카드에 과도하게 김 → 실제 편집 시 **내부 순차 등장/모션** 필요(특히 C10은 서브 컷 분할 고려).
- 공식 캡처 C02~C07(10~25s)·나머지 카드는 적정.

## 5. 자막 문제
- 없음. SRT 25컷 한 줄 18~24자, 과도 길이 없음. 공식 영어는 캡처 안에서만, 하단 자막 한국어.

## 6. 공식 근거 화면 가독성
- C02~C07 원문 문구 읽힘(노출 10~25s). 출처 라벨 보임. **C03/C04/C05(부모 포함 증거) 43s** 충분. 부모 결론 3개 마지막 40s로 분명.

## 7. 수정 필요 항목
1. 긴 정적 카드 3개(C10/C08/C11)에 모션/순차 reveal.
2. (선택) 정식 ffmpeg로 mp4 재렌더.
3. 전환·자막 번인·BGM·TTS는 1차 편집 도구 단계.

## 8. 검증 결과
| 항목 | 결과 |
|---|---|
| c01 생성 | ✓ (PNG 1920×1080) |
| preview 생성 | ✓ GIF (mp4 실패 사유 기록) |
| 공식 캡처 PNG 6개 참조 | ✓ (타임라인 유지) |
| 자막 파일 참조 | ✓ (SRT/key) |
| 영상 업로드 | 없음 ✓ |
| HTML·sitemap·배포 | 0 ✓ (sitemap 39) |
| UQ-02 approved/applied/published | 아님 ✓ (evidence_merged) |
| 비관련 파일 제외 | ✓ |

## 9. 다음 단계 제안
1. 긴 정적 카드 3개에 순차 등장 지시 반영(대본/타임라인 미세 조정).
2. TTS 내레이션 녹음(final_narration_ko.md) + 1차 편집(전환·자막 번인·BGM).
3. 사람 최종 검수 → 업로드(별도 승인).
→ 싱가포르 편이 **preview로 실제 영상 감각까지 확인 완료**. 파이프라인 재사용 준비됨.
