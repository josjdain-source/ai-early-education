# AI 조기교육 — 부모용 출력 자료 허브(downloads.html) 발행 보고서

- 작성일: 2026-07-03
- 담당: Claude (사이트 운영 위임, MAINTENANCE.md 기준)
- 작업 범위: `ai-craft-kids/ai-early-education/` 내부만. 여행사이트 등 타 프로젝트 무손상.

## 1. 목표
부모가 실제로 출력해서 쓸 수 있는 자료(체크리스트·약속표·실험 기록지)를 한곳에 모은 **출력/인쇄 자료 허브**를 만든다.
실제 파일 다운로드가 아니라 **"인쇄용 HTML 보기"** 허브로 설명한다(브라우저 인쇄 Ctrl/⌘+P). PDF 생성 없음.

## 2. 생성한 URL
- 라이브: `https://ai-early-education.pages.dev/ai-early-education/downloads.html`
- 로컬 파일: `ai-early-education/downloads.html`
- title: `부모용 AI 조기교육 출력 자료 모음 | 체크리스트·약속표·실험 기록지`
- description: `AI 조기교육을 집에서 안전하게 시작하려는 부모를 위해 인쇄용 체크리스트, 약속표, 실험 기록지 등 출력 자료를 모았습니다.`

## 3. 수정한 파일
| 파일 | 변경 |
|---|---|
| `ai-early-education/downloads.html` | **신규 생성** (허브 본문) |
| `ai-early-education/index.html` | 히어로 하단에 `🖨️ 출력 자료 모음` 링크 추가 |
| `ai-early-education/printable-checklist.html` | 하단 자세히보기에 downloads 링크 |
| `ai-early-education/checklist.html` | 하단 관련 페이지에 downloads 링크 |
| `ai-early-education/parent-rules.html` | 하단 이어서 보면 좋은 글에 downloads 링크 |
| `ai-early-education/home-experiments.html` | 하단 이어서 보면 좋은 글에 downloads 링크 |
| `ai-early-education/start-here.html` | 하단 준비됐다면에 downloads 링크 |
| `sitemap.xml` | downloads.html URL 추가 (35 → **36**) |
| `../홈페이지 통합관리/projects.json` | live-downloads·downloads-report 액션 + status/next_action 갱신 |
| `patch_log.json` | 신규 생성(이 작업 기록) |
| `reports/AI_EARLY_EDUCATION_DOWNLOADS_REPORT.md` | 본 보고서 |

## 4. downloads 페이지 구조 (6단)
1. 왜 출력 자료가 필요한가
2. 지금 바로 쓸 수 있는 자료
3. 곧 추가할 자료 (예정 표시만, 링크 없음)
4. 어떤 순서로 쓰면 좋은가
5. 자료를 사용할 때 주의할 점
6. 관련 읽기 링크

## 5. 지금 사용 가능한 자료
1. **AI 대화 실험 전 부모 체크리스트: 인쇄용 한 장** (`printable-checklist.html`) — 실험 전 5분 확인
2. **설명형 체크리스트** (`checklist.html`) — 왜 전/중/후 체크가 필요한지 먼저 이해

## 6. 준비 중(예정) 자료 — 링크 걸지 않음
1. 아이와 AI를 쓸 때 7가지 약속표 → (예정) `printable-rules.html` / 현재는 `parent-rules.html` 연결
2. 오늘의 AI 대화 실험 기록지 → (예정) `experiment-log.html` / 현재는 `home-experiments.html` 연결
3. 연령별 시작 카드 → (예정) `age-cards.html` / 현재는 `age-guide.html` 연결
4. 처음 온 부모 10분 안내 요약지 → (예정) `start-here-print.html` / 현재는 `start-here.html` 연결

> 예정 자료는 미존재 파일로 링크하지 않고 '예정' 배지로만 표시 → **깨진 링크 0건**.

## 7. 기존 printable-checklist와 연결한 방식
- downloads가 printable-checklist를 **'지금 바로 쓸 수 있는 자료' 1순위**로 안내(허브 → 출력물).
- 역방향으로 printable-checklist 하단에 downloads 허브 링크를 넣어 **양방향 연결**.
- 사용 순서(4단)에서 `start-here → parent-rules → printable-checklist(출력) → home-experiments → 한 줄 기록` 흐름의 3번째 단계로 배치.

## 8. 배포 여부
- 배포: **완료** (Cloudflare Pages, git push + wrangler 클린 배포)
- 검증: 아래 참조.

## 9. 검증 결과
| 항목 | 결과 |
|---|---|
| 로컬 200 | downloads / printable-checklist / 코너 대문 모두 200 |
| 라이브 200 | downloads.html 200 |
| 내부 링크 | downloads 내부 링크 10종 전부 실존 파일 |
| 준비 중 자료 깨진 링크 | 없음(예정 표시만) |
| sitemap 반영 | loc 36개, downloads 1건 |
| 모바일 가독성 | 기존 style.css + 반응형 카드/정의목록 |
| 광고성 CTA | 없음 |
| 특정 AI 서비스 추천 | 없음 |
| 영상/유튜브/상품 파일 | 생성 없음 |
| PDF 파일 | 생성 없음 |
| 기존 페이지 | 무손상(하단 링크 1줄 추가만) |
| 여행사이트 | **미변경** |
