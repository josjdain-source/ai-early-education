# 바이럴 원칙 (진실원본) — 울분 대변·속시원함

> ★핵심: **정보 전달보다, 시청자의 울분을 얼마나 속시원하게 대변하느냐**가 조회·좋아요의 엔진이다.
> 시청자가 속으로 삭이던 좌절·후회를 영상이 대신 터뜨려 줄 때(사이다), 좋아요·댓글·공유가 터진다.

## 실측 근거
- **한국의 잃어버린 AI 10년, 청년의 취업난** (youtube.com/shorts/unLYYN_aTPk)
- 사전 휴리스틱 예측: **D · 0점**("정책/거대담론 약함")
- 실제: **좋아요 많음** → 예측 오류. 원인 = '잃어버린·취업난·뼈아프다'가 시청자의 삭인 좌절을 **속시원하게 대변**.

## 쇼츠 제작 방향 (영구 적용)
1. **울분 대변(Catharsis) 레버를 1순위로**: 잃어버린·뒤처짐·취업난·격차·뼈아프다·이래서 안 된다 → 대신 시원하게 짚어준다.
2. 구조: **공감되는 울분 제시 → "그래서 이게 문제다" 시원하게 터뜨림 → 그래서 이렇게(해결/희망)**.
3. '건조한 제도 설명(제도·커리큘럼·도입 절차)'은 여전히 감점 — 감정 없는 나열 금지.
4. 정보는 근거로 깔되, **표현은 속시원하게**. 얌전한 정보나열 < 속시원한 대변.
5. 제목: Catharsis + Stop Power + (해당 시) Personal Pain + Clear Takeaway.

## 점수 모델
Viral Test = Stop Power + Personal Pain + **Catharsis(울분 대변)** + Curiosity Gap + Watch Completion + Clear Takeaway − Boring Policy(건조한 제도만) − Abstract Talk − Clickbait Mismatch
- 데이터·상세: `content_bank/pattern_lab.json`, 화면: `/content-bank` 🔬 Pattern Lab
- 재계산: `python production/build_pattern_lab.py` (실측 유입 시 갱신)

## 음성 확정 (2026-07-07)
- **울분 대변·임팩트 패턴 = ko-KR-InJoonNeural** (남성, 단호·진중). unLYYN(build_klad_illust) 실측.
- 경로: `_tts_param.py <txt> <out> ko-KR-InJoonNeural +0% +0Hz`, 속도 atempo 1.12~1.2.
- gentle 부모코칭만 SunHi 허용. 그 외 쇼츠 기본 = InJoon.
