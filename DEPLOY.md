# 배포 가이드 — Cloudflare Pages (AI 조기교육 1편 홈페이지)

정적 사이트(빌드 불필요). 아래 둘 중 하나로 공개 주소(`https://<프로젝트명>.pages.dev`)를 만든다.

> 배포 전 점검(완료):
> - 서버 전용 기능 없음(순수 HTML/CSS/JS/JSON/assets, localhost 호출 0건)
> - 경로 6개 정상: `/` · `/make/door-sign/` · `/prompts/emotion-character-20/` · `/materials/` · `/templates/` · `/safety/`
> - 영상: `assets/video/ep01_door_sign_opening_candidate.mp4`, 홈 히어로·문패 상세가 `data/lessons.json`의 같은 `video_file`을 참조(단일 소스)
> - 이미지: 손 교정본 적용, 원본은 `assets/images/ep01/master/`에 보존, motion 복사본은 쇼츠용
> - 첫 화면 메시지: "우리 아이 첫 AI 조기교육 · 이렇게 시작하세요" → "코딩보다 먼저, 아이와 함께 AI에게 말 거는 법부터"
> - `assets/audio/`와 영상 렌더 임시 파일은 `.gitignore`로 배포 제외(용량↓), 디스크엔 보존

---

## 방법 A — GitHub 연결 (권장, 이후 자동 재배포)

1. **GitHub에 새 저장소 생성**(브라우저, 직접): 이름 예 `ai-early-education`, Public.
   - 이 폴더는 이미 **독립 git 저장소로 초기화 + 첫 커밋 완료**되어 있음(IGS_FINAL과 분리).
2. **원격 연결 + 푸시**(이 폴더에서):
   ```bash
   git remote add origin https://github.com/<your-id>/ai-early-education.git
   git branch -M main
   git push -u origin main
   ```
   - 푸시는 GitHub 로그인/토큰이 필요(직접). 터미널에서 `! git push -u origin main` 형태로 실행하면 인증창이 뜸.
3. **Cloudflare Pages 연결**(dash.cloudflare.com → Workers & Pages → Create → Pages → Connect to Git, 직접 로그인):
   - 저장소 선택, **Framework preset: None**, **Build command: (비움)**, **Build output directory: `/`**.
   - Save and Deploy → 잠시 후 `https://<프로젝트명>.pages.dev` 발급.

## 방법 B — Wrangler 직접 업로드 (GitHub 없이 한 번에)

```bash
npx wrangler pages deploy . --project-name=ai-early-education
```
- 최초 1회 `npx wrangler login`(브라우저 로그인, 직접) 필요.
- 같은 명령으로 재배포.

---

## 발급된 주소를 넣을 곳(배포 후)
- `content/video/ep01_youtube_meta.md` 의 설명문/고정댓글 URL 자리 3개(홈페이지·프롬프트·도안)
- 네이버 블로그 / 유튜브 설명·고정댓글

## 프로젝트명 후보(중복 시 조정)
`ai-early-education` · `ai-craft-kids` · `ai-first-talk` · `kids-ai-start`
