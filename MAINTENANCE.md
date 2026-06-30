# 운영 런북 (Claude가 관리)

> 사용자 지시(2026-06-30): "앞으로 너가 관리하라." 이 사이트의 수정·배포는 Claude가 담당.
> 다음 세션에서 컨텍스트가 비어도 이 문서대로 하면 바로 이어서 관리 가능.

## 좌표
- 라이브: **https://ai-early-education.pages.dev/**
- GitHub: **https://github.com/josjdain-source/ai-early-education** (브랜치 `main`)
- 작업 폴더: `C:\Users\admin\Desktop\ai-craft-kids` (독립 git repo, IGS_FINAL과 분리)
- CF Pages 프로젝트명: `ai-early-education` (account 1feef7...3f20d)

## 인증 (이미 저장됨, 재로그인 불필요)
- gh CLI: `C:\Users\admin\tools\gh\bin\gh.exe` (User PATH 등록, josjdain-source 로그인됨)
- wrangler: `npx -y wrangler ...` (CF OAuth 저장됨; APPDATA\xdg.config\.wrangler)

## 표준 작업 흐름 (수정 → 배포)
1. 파일 수정 (`index.html`, `data/lessons.json`, 페이지들, `assets/...`)
2. 커밋 + 푸시:
   ```bash
   git add -A && git -c core.autocrlf=false commit -m "..." && git push origin main
   ```
3. **클린 배포**(중요: `wrangler pages deploy .` 는 .gitignore를 무시해 음성·임시프레임까지 올림 →
   반드시 git 추적분만 추출해서 배포):
   ```bash
   TMP=<임시폴더>; rm -rf "$TMP"; mkdir -p "$TMP"
   git archive main | tar -x -C "$TMP"
   npx -y wrangler pages deploy "$TMP" --project-name=ai-early-education --branch=main --commit-dirty=true
   ```
4. 검증: `curl -s -o /dev/null -w "%{http_code}" https://ai-early-education.pages.dev/`

## 원칙 (불변)
- 영상 단일 소스 = `data/lessons.json` → `door-sign-01.video_file`. 홈 히어로(app.js renderHeroVideo)·문패 상세 둘 다 이걸 참조.
- 검수 통과 TTS 음성 재생성 금지(재생성 전 사용자 승인). 자동 유튜브 업로드·쿠팡 링크 임의생성 금지.
- 원본 이미지 보존(`assets/images/ep01/master/`), 손/얼굴/화면텍스트 재생성 금지.
- 포지셔닝 = `content/positioning_statement.md`(진실원본): "문패 만들기"가 아니라 "아이가 AI와 대화하는 첫 연습".
- `.gitignore`로 `assets/audio/`·영상 렌더 임시는 배포 제외(디스크엔 보존).

## 선택: Git 자동배포로 전환하고 싶을 때
CF 대시보드 → Pages 프로젝트 → Settings → Builds & deployments → Connect to Git(사용자 로그인 필요).
연결하면 `git push`만으로 자동 재배포(위 3번 클린배포 불필요).
