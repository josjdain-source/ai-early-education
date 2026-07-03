# 5분 본편 pending 시각자산 제작 — 보고

- 작성일: 2026-07-04
- 성격: **pending 이미지 13개 제작(무료 Pillow, IMG-01~04 톤 통일).** 렌더/업로드/HTML/링크 교체 없음.

## 1. pending 이미지 수 — **13** (해소 완료)
timeline pending: 인포그래픽 8(IMG-05·07·09·11·13·14·15·16) + 부모 해석 카드 5.

## 2. 생성한 인포그래픽 수 — **12** (IMG-05~16)
- timeline 사용분 8 + 여유분 4(IMG-06·08·10·12, 나라별 2컷 대비 — 현재 timeline 미사용, 확장용).

## 3. 생성한 부모 해석 카드 수 — **5**
CN·US·UK·SG·KR-parent-interpretation.png.

## 4. 저장 위치
- 인포그래픽: `assets/world-ai-education-5min/images/`
- 해석 카드: `assets/world-ai-education-5min/interpretation-cards/`

## 5. 파일명 목록
- 인포그래픽: IMG-05-usa-literacy · IMG-06-usa-teacher-training · IMG-07-uk-teacher-check · IMG-08-uk-human-judgment · IMG-09-singapore-platform · IMG-10-singapore-guardrail · IMG-11-korea-digital-textbook · IMG-12-korea-parent-home · IMG-13-five-country-summary · IMG-14-question-judgment-revise · IMG-15-parent-child-retry · IMG-16-final-cta (.png)
- 카드: CN/US/UK/SG/KR-parent-interpretation.png
- (파일명 = timeline image_file과 정확히 일치)

## 6. 텍스트 깨짐 여부 — **없음**
malgun/malgunbd 폰트 직접 렌더. 검수(IMG-14·KR 카드) 텍스트 선명·정상.

## 7. 톤 일관성 검수
- IMG-01~04와 동일 팔레트(라벤더·블루·크림)·그라데이션 배경·흰 카드·드로잉 아이콘. evidence 컷과 튀지 않음.
- 국기 남발 없음, 정책 홍보/국가 선전/공포 없음. 텍스트 최소, 1초 가독.
- 해석 카드: 국가색 약하게(상단 얇은 선+코너), 큰 문장 중앙, 요약 카드 톤. 행동 결론으로 연결.

## 8. 확인 (안 한 것)
- **영상 렌더/업로드/HTML 수정/링크 교체 없음.** sitemap 41.

## 9. timeline pending 해소
- edit-timeline.json: **ready 26 / pending 0** (전 컷 이미지 확보).
- visual-assets-manifest.json: 31 자산(infographic 16·interpretation 5·evidence 10) 전부 ready, missing 0.

## 10. 다음 단계
1. **TTS 음성 생성**(production/world-ai-education-5min-tts-script.md).
2. **본편 초벌 조립·렌더**(timeline대로 이미지+TTS+자막, 증거 3~5초+해석 카드) → 사람 검수.
