# 아이와 함께 배우는 생성형 AI — 콘텐츠 허브 (홈페이지 MVP)

부모와 아이가 **사진 한 장·그림 한 장으로 직접 만들기**를 하며 생성형 AI를 자연스럽게 체험하는 코너.
유튜브(영상 유입) · 블로그(검색 유입) · 홈페이지(정리/저장/수익화 허브)가 함께 도는 구조.
수익화 = 만들기 콘텐츠를 보여주고 **준비물을 쿠팡 파트너스로 연결**(콘텐츠가 본체, 상품은 준비물).

## 프레임워크
**정적 사이트 — 빌드 불필요.** 순수 HTML + CSS + 바닐라 JS. 데이터(JSON)만 늘리면 카드가 자동 추가.
(korea-life-kit처럼 Cloudflare Pages에 그대로 배포 가능)

## 페이지
| URL | 파일 | 내용 |
|---|---|---|
| `/` | index.html | 히어로(시안 일러스트)+CTA+배지 / 이번 주 만들기(데이터) / 왜 이 사이트 |
| `/make/door-sign/` | make/door-sign/index.html | 영상·완성예시 자리, 만들기 6단계, 준비물, 블로그 링크 자리, 안전 |
| `/materials/` | materials/index.html | 준비물(카테고리별, 쿠팡 링크 자리) |
| `/templates/` | templates/index.html | 무료 도안(샘플 1개 다운로드 + 곧 추가) |
| `/safety/` | safety/index.html | 아이/이미지/음성 안전 안내 |

## 데이터 파일
- `data/lessons.json` — 만들기 콘텐츠(6개). youtube_url/blog_url/page 비면 placeholder.
- `data/materials.json` — 준비물(13개, category별). affiliate_url 비면 "링크 입력 필요".
- `data/templates.json` — 도안. file+status=available 이면 다운로드 활성.

## 자산
- `assets/style.css` · `assets/app.js`
- `assets/hero-art.png` — 히어로 일러스트(사용자 GPT 시안에서 크롭)
- `assets/homepage_mockup.png` — 전체 디자인 시안(참고)
- `templates/sample_door_sign_template.png` — 감정 문패 도안 샘플(다운로드 가능)

## 로컬 실행
```
cd Desktop\ai-craft-kids
python -m http.server 8830
# 브라우저: http://127.0.0.1:8830/
```
※ 루트 기준 절대경로(/assets, /data)를 쓰므로 file:// 직접 열기 대신 http.server로 실행.

## 배포 가능 여부
✅ 가능. Cloudflare Pages(정적) — 빌드 명령 없음, 루트 디렉터리 그대로 업로드/연결.

## 아직 비어 있는 링크 (발행 시 입력)
- 모든 준비물 `affiliate_url` (쿠팡 파트너스 — 지금 임의 생성 금지)
- 모든 lesson `youtube_url` / `blog_url`
- `/make/door-sign/` 유튜브 임베드 · 완성 예시 이미지 · 블로그 링크
- 도안 3종(도어행거/키링/스티커) — "곧 추가"

## 공개 배포 안전 정책 (예시 이미지)
- 공개 페이지 예시는 **모두 AI로 만든 이미지**(실제 아이 아님) — 그대로 노출. before = AI 실사 여자아이, after = AI 만화 감정 캐릭터 20종.
- 따라서 **실제 아이 얼굴은 공개 페이지에 싣지 않음** → 블러 잠금 불필요(이전 blur 토글 정책 대체).
- 사용자가 **자기 아이 사진**으로 직접 만들 때만: 부모와 함께 확인, 실명·학교·주소·전화번호가 보이는 이미지 **사용 금지**(안내 문구로 고지).
- 자산: `assets/example_photo.png`(AI 실사 여자아이=`image.png`, before) · `assets/example_emotion_sheet.png`(만화 20종 시트, after) · `assets/stickers/s01~s20.png`(시트 20칸 분할 갤러리).

## 다음 단계
1편 영상 제작 · 블로그 글 작성 · 쿠팡 파트너스 링크 입력 · 무료 도안 추가 · 유튜브 링크 연결.
(자동 업로드/쇼츠 자동 생성기 연결은 아직 안 함 — 홈페이지 MVP 먼저)
