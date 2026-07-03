# AI 조기교육 데일리 관측소 — 매일 자동 실행 (작업 스케줄러)

관측소의 심장박동. 매일 아침 7:30에 7축 파이프라인을 `--write`로 자동 실행한다.
**자동 관측만.** 사이트 수정/영상/업로드/자동 발행 없음. update_queue는 항상 `status=new`(사람 승인 게이트).

## 파일
- `run_ai_education_daily_pipeline.bat` — 실행 러너(로그 저장). 순수 ASCII.
- `register_ai_education_daily_task.ps1` — 작업 스케줄러 등록(매일 07:30).
- `unregister_ai_education_daily_task.ps1` — 등록 해제.
- 로그: `ops/ai-early-education/pipeline_runs/logs/run_YYYY-MM-DD_HH-mm-ss.log` (실패 시 `error_...log`)

## 1) BAT 수동 실행 (먼저 이걸로 테스트)
```
"C:\Users\admin\Desktop\ai-craft-kids\scripts\run_ai_education_daily_pipeline.bat"
```
또는 프롬프트에서 `! scripts\run_ai_education_daily_pipeline.bat`
→ pipeline이 `--write`로 돌고, daily_watch/pipeline_runs/queue 갱신 + 로그 저장.

## 2) 작업 스케줄러 등록 (사용자 승인 후 직접)
```
powershell -ExecutionPolicy Bypass -File "C:\Users\admin\Desktop\ai-craft-kids\scripts\register_ai_education_daily_task.ps1"
```
- 작업 이름: **AI Early Education Daily Watch**
- 시간: 매일 **07:30**
- 로그인 사용자로 실행(비밀번호 저장 불필요).
- 확인: `Get-ScheduledTask -TaskName "AI Early Education Daily Watch"`
- 지금 한 번 실행(테스트): `Start-ScheduledTask -TaskName "AI Early Education Daily Watch"`

## 3) 해제
```
powershell -ExecutionPolicy Bypass -File "C:\Users\admin\Desktop\ai-craft-kids\scripts\unregister_ai_education_daily_task.ps1"
```

## 4) 로그 확인 위치
`ops\ai-early-education\pipeline_runs\logs\`
- `run_...log` : 정상 실행 출력(요약·added ids)
- `error_...log` : 실패 시에만 생성(내용 있을 때만 유지)
- 관측 결과 자체: `ops\ai-early-education\daily_watch\YYYY-MM-DD.md`, `pipeline_runs\YYYY-MM-DD.json`

## 5) 실패 시 확인할 것
- Python 경로: BAT의 `PY` 변수(`Python313\python.exe`) 존재 여부. 없으면 `python`(PATH) 폴백.
- 네트워크 차단/403: 일부 공식 사이트 봇 차단 → `pipeline_runs` json의 `errors` 확인.
- 권한: 작업 스케줄러는 로그인 상태에서 실행. 컴퓨터가 꺼져 있으면 `StartWhenAvailable`로 다음 로그인 때 실행.

## 6) dry-run vs write
- **dry-run**(기본, 안전): `python scripts\ai_education_daily_pipeline.py --dry-run` — 파일 미수정, 화면 요약만.
- **write**(스케줄러가 쓰는 것): daily_watch/pipeline_runs/queue 기록. queue는 score≥3만 `status=new`.

## 7) 자동 발행 금지 원칙 (불변)
- 자동화: 찾기·분류·점수·큐 등록·관측 로그·(공식만)증거 후보.
- **자동화가 안 하는 것**: 사이트 HTML/sitemap 수정·배포·영상 렌더/업로드·정책 단정·뉴스를 사실로 반영·학생 얼굴/이름 노출.
- Safety Guard(`pipeline` 코드)가 금지 경로 쓰기를 차단. queue는 `approved_by/applied_commit=null` 유지.
- 사람이 매일 `queue_added·score·parent_question·can_update_site_fact`를 검수 → 승인 항목만 다음 단계.
