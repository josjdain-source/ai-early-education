# EP02 싱가포르 — 렌더 계획

> ⚠️ **실제 렌더·업로드는 별도 승인 전 하지 않는다.** 이 문서는 계획 + preview 명령만.

## 1. 규격
- 화면 비율: **16:9 기본(1920×1080)**, 9:16 파생 가능(쇼츠 클립)
- 1차 영상 길이: **4:50~5:10** + 끝 2초 무음 tail
- 프레임: 30fps

## 2. 톤
- BGM: 밝고 잔잔한 로파이/어쿠스틱, -18dB. C01 불안 구간·C10 차분 구간만 -22dB
- 목소리: 따뜻한 여성 톤 1개 고정. 겁주지 않기. TTS 사용 시 시리즈 공통 보이스

## 3. 공식 캡처 표시 원칙
- `official_evidence_timeline.json`대로 2~4초 노출 + 핵심 문구 확대 2~3초 + 한국어 요약 카드 3~5초
- 하단 출처 라벨 유지(캡처 이미지에 이미 합성됨 / 또는 source_label_card 겹침)
- **원문 문구 변경·의역 삽입·미확인 문구 강조·윤리 4원칙 재삽입 금지**

## 4. 저작권/출처 표시 원칙
- 공식 페이지는 일부 캡처 + 핵심 문구 하이라이트(전체 장시간 노출 금지). 해설·교육 목적, 출처 명시.
- 캡처 이미지의 출처 라벨 바를 가리지 않기.

## 5. 편집 순서 (edit_timeline.json 기준)
C01(거실) → C02~C06(공식 근거 몰아치기) → C08(연령 카드) → C07(책임 문장) → C09(부모 질문) → C10(학교vs가정) → C11(결론3) → C12(홈 연결)

## 6. 에셋 상태
- 공식 캡처 C02~C07: **확보 ✅** (singapore-evidence/)
- 텍스트 카드 c08~c12 + source_label: **확보 ✅** (cards/)
- c01 거실 장면: **미생성**(cards_spec.md 프롬프트로 승인 후 생성)
- 자막: episode_02_captions.srt ✅ / key_captions.md ✅
- 내레이션: final_narration_ko.md ✅ (TTS 녹음 필요)

## 7. preview 렌더 (승인 후에만 실행)
- 스크립트: `scripts/render_episode_02_preview.py` (저해상도 슬라이드쇼 미리보기용)
- 명령(참고, **지금 실행 금지**):
  ```
  python scripts/render_episode_02_preview.py \
    --timeline assets/ai-early-education/video-episode-02-singapore/timeline/edit_timeline.json \
    --out assets/ai-early-education/video-episode-02-singapore/exports/ep02_preview.mp4
  ```
- 전제: ffmpeg 필요(ms-playwright 캐시에 ffmpeg 있음). c01 미생성분은 자리표시(placeholder)로 대체.

## 8. 최종 검수 체크리스트 (렌더 후, 업로드 전)
- [ ] 길이 4:50~5:10 + tail 2s
- [ ] 공식 캡처 원문 문구 변형 0 · 출처 라벨 보임
- [ ] 윤리 4원칙 미등장
- [ ] "싱가포르=정답" 연출 없음
- [ ] 특정 AI 서비스 추천·상품·유료강의 없음
- [ ] 아이 혼자 사용 권장 없음
- [ ] 자막 가독(한 줄 18~24자)
- [ ] 사람 최종 승인 → 그 다음에만 업로드
