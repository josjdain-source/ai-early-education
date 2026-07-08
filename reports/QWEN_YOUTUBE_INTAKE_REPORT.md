# Qwen YouTube Intake Report

Date: 2026-07-08

## Implemented Files

Created:

- `tools/youtube_intake/youtube_fetch.py`
- `tools/youtube_intake/youtube_index.py`
- `tools/youtube_intake/qwen_indexer.py`
- `tools/youtube_intake/prompts/qwen_index_prompt.txt`
- `tools/youtube_intake/config.json`
- `tools/youtube_intake/OPERATING.md`

Generated sample output:

- `tools/youtube_intake/output/lY9B2t1k1Io/raw_meta.json`
- `tools/youtube_intake/output/lY9B2t1k1Io/transcript_raw.json`
- `tools/youtube_intake/output/lY9B2t1k1Io/transcript.txt`
- `tools/youtube_intake/output/lY9B2t1k1Io/chunk_index.json`
- `tools/youtube_intake/output/lY9B2t1k1Io/chunks/c001.txt`
- `tools/youtube_intake/output/lY9B2t1k1Io/chunks/c002.txt`
- `tools/youtube_intake/output/lY9B2t1k1Io/claude_brief.md`

## Design Guardrails

The module is intentionally constrained:

- Qwen does not make final factual judgments.
- Qwen does not make content strategy decisions.
- Qwen does not create a final summary of the full transcript.
- Qwen only indexes each chunk.
- Each chunk result keeps `raw_path`.
- Claude should read `claude_brief.md` first, then open only the relevant raw chunk files.
- Claude should not load `transcript.txt` by default.

## Qwen Prompt

Prompt file:

`tools/youtube_intake/prompts/qwen_index_prompt.txt`

It explicitly says:

- Qwen is not the final judge.
- Use only the given chunk.
- Do not add facts, numbers, people, or sources absent from the chunk.
- Output JSON only.

Expected JSON fields:

- `keywords`
- `one_line_hint`
- `possible_use`
- `needs_raw_check`

The implementation also records:

- `confidence`
- `raw_path`
- `qwen_meta`

## Model Selection

Default preference:

1. `qwen3.5:9b`
2. `qwen3:4b`
3. installed local Qwen model

In this environment:

- `qwen3.5:9b` is installed.
- `qwen3:4b` is installed.
- `qwen2.5-coder:7b` is installed for coding/tool work, not transcript indexing.
- `qwen3.6:latest` exists in the official Ollama library but is deferred because it is about 24 GB.

Port source of truth:

- `C:\Users\admin\Desktop\홈페이지 통합관리\ports.json` is the SSOT for local service ports.
- The control panel project records describe `Ollama(11435)+ComfyUI(8188)`.
- `tools/youtube_intake/config.json` now uses `http://127.0.0.1:11435`.
- `11434` is treated only as a generic Ollama default, not this workspace's fixed port.

If `/api/tags` fails, `qwen_indexer.py` falls back to parsing `ollama list`.
If model discovery still fails, it records the configured first-choice model and falls back after the API call fails.

## Failure Handling

If Qwen output is invalid JSON:

- parse recovery is attempted
- if still invalid, deterministic fallback is used

If Ollama API fails:

- deterministic fallback is used
- error is stored in `qwen_meta.error`
- `used_fallback` is set to `true`

Observed in earlier sample run:

- Ollama API initially closed connections with `WinError 10054`
- A temporary `127.0.0.1:11500` endpoint was tested; the server exited and calls failed with connection refused
- fallback indexer was used
- `raw_path` remained present in every chunk item
- `qwen_meta.model` now records `qwen3.5:9b`

Observed after applying the control panel port:

- `http://127.0.0.1:11435/api/tags` returns installed models successfully.
- `qwen3.5:9b` generated chunk indexes through `/api/generate`.
- `qwen_meta.used_fallback` is now `false` for the regenerated sample chunks.
- `qwen3:4b` responds faster but returned an empty/weak index for the Korean sample, so `qwen3.5:9b` remains the first-choice model.

## YouTube Fetch Test

Sample URL:

`https://www.youtube.com/watch?v=lY9B2t1k1Io`

Direct `yt-dlp` transcript fetch was attempted.

Result:

- `yt-dlp` executable exists.
- YouTube network access failed with `WinError 10013`.
- `raw_meta.json` records `fetch_status: transcript_missing` for the direct fetch test.
- Running the direct `yt-dlp` command outside the Python wrapper produced the same `WinError 10013`, so this is an environment/socket permission issue rather than a module parsing issue.
- A repeat direct `yt-dlp` test on 2026-07-08 produced the same `WinError 10013`.
- `where.exe python` did not resolve via PATH, but `python.exe` resolves to `C:\Users\admin\AppData\Local\Programs\Python\Python313\python.exe`.
- `where.exe yt-dlp` did not resolve via PATH, but `yt-dlp.exe` resolves to `C:\Users\admin\AppData\Local\Programs\Python\Python313\Scripts\yt-dlp.exe`.
- `python -c "import urllib.request; ..."` also fails with `WinError 10013`, so this is not limited to `yt-dlp`.

Because network fetch was blocked, the validation run used the same sample URL with a manual transcript file to test the full output pipeline.

## Validation

Checks performed:

- `python -m py_compile tools/youtube_intake/youtube_fetch.py tools/youtube_intake/qwen_indexer.py tools/youtube_intake/youtube_index.py`
- sample output generated under `tools/youtube_intake/output/lY9B2t1k1Io/`
- `transcript.txt` preserved
- `transcript_raw.json` preserved
- chunk files preserved under `chunks/`
- `chunk_index.json` includes `raw_path`
- `claude_brief.md` includes the required warnings
- `claude_brief.md` maps each chunk to raw file path and hints
- existing output can be re-indexed with `python tools/youtube_intake/youtube_index.py <video_id>`
- UTF-8 verification confirms the generated Korean warnings and fallback keywords are intact; PowerShell `Get-Content` may display some UTF-8 files incorrectly depending on console encoding.

## Operating Document

Added:

`tools/youtube_intake/OPERATING.md`

Key rule:

Claude should read `claude_brief.md` first, then open only the needed raw chunks. Claude should not read `transcript.txt` or `transcript_raw.json` by default.

## Claude Usage Rule

Claude should start from:

`tools/youtube_intake/output/<video_id>/claude_brief.md`

Then open only the needed:

`tools/youtube_intake/output/<video_id>/chunks/cNNN.txt`

Do not use Qwen `one_line_hint` as content-ready copy.
Do not write content from the full transcript without raw chunk verification.
