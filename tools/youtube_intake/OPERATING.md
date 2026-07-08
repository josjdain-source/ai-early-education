# YouTube Intake Operating Notes

## Role Split

Qwen is only a chunk indexing worker.

Qwen may create:

- keywords
- one_line_hint
- possible_use
- confidence as a weak routing signal

Qwen must not create:

- final factual judgments
- final summaries
- content-ready claims
- source claims absent from the raw chunk

Claude is the final editor, but Claude must not trust the Qwen index without checking the raw chunk.

## Claude Entry Point

Start here:

```text
tools/youtube_intake/output/<video_id>/claude_brief.md
```

Then open only the needed raw chunk paths listed in:

```text
tools/youtube_intake/output/<video_id>/chunk_index.json
```

Do not load these by default:

```text
tools/youtube_intake/output/<video_id>/transcript.txt
tools/youtube_intake/output/<video_id>/transcript_raw.json
```

Use full transcript files only when explicitly needed and after deciding why the chunk map is insufficient.

## Normal Run

Fetch and index a URL:

```powershell
python tools/youtube_intake/youtube_index.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Index an already fetched video output:

```powershell
python tools/youtube_intake/youtube_index.py VIDEO_ID
```

Manual transcript fallback:

```powershell
python tools/youtube_intake/youtube_index.py "https://www.youtube.com/watch?v=VIDEO_ID" --transcript-file path\to\transcript.txt
```

## Ollama

Current intended model order:

1. `qwen3.5:9b`
2. `qwen3:4b`

Coding-only helper:

- `qwen2.5-coder:7b`

Deferred:

- `qwen3.6:latest`

Do not pull `qwen3.6:latest` for routine transcript indexing without explicit confirmation. It is a large model and not needed for chunk routing.

Port source of truth:

```text
C:\Users\admin\Desktop\홈페이지 통합관리\ports.json
```

Preferred local endpoint for this workspace, based on the control panel records:

```text
http://127.0.0.1:11435
```

Treat `11434` only as Ollama's common default, not as this workspace's fixed port. In this environment, the control panel project records describe `Ollama(11435)+ComfyUI(8188)`, and `ports.json` includes `11435` in `avoid`, meaning it is reserved/occupied and should not be assigned to another service.

## Required Warnings

Every `claude_brief.md` must contain:

- 이 문서는 Qwen이 만든 색인이다.
- 최종 판단 전 필요한 raw chunk를 직접 확인하라.
- 원문 자막 전체를 기본으로 Claude에게 넣지 말라.
- 콘텐츠에 쓸 문장은 raw chunk에서 확인하라.
- 원문 복붙 금지, 출처 링크 필요.
