# Qwen Local Upgrade Report

Date: 2026-07-08

## Goal

Use local Qwen as a low-risk assistant for YouTube transcript intake:

- chunk splitting
- keyword extraction
- raw chunk indexing
- short routing hints
- file organization

Qwen must not be used as the final judge for facts, content strategy, or final summaries.

## Local Ollama Status

Commands checked:

```powershell
ollama --version
ollama list
ollama ps
Invoke-RestMethod http://localhost:11434/api/tags
Invoke-RestMethod http://127.0.0.1:11435/api/tags
```

Initial results:

- Ollama version: `0.24.0`
- Ollama process: running
- Loaded models: none from `ollama ps`
- HTTP API `/api/tags` on `11434`: did not return reliably
- `/api/generate`: connection was closed by the local Ollama server

Control panel correction:

- `C:\Users\admin\Desktop\홈페이지 통합관리\ports.json` is the local port source of truth.
- The control panel project records for `video-auto-maker` and `country-ai-package` describe `Ollama(11435)+ComfyUI(8188)`.
- `ports.json` includes `11435` in `avoid`, which means it is reserved/occupied and should not be assigned to another service.
- Therefore `11434` is only a common Ollama default, not the fixed port for this workspace.
- `http://127.0.0.1:11435/api/tags` returns the installed model list successfully.

Follow-up stabilization attempt:

- Port `11434` was held by `svchost` rather than a normal Ollama server process.
- Restarting the visible Ollama processes did not restore a usable `11434` API.
- A separate server was started with `OLLAMA_HOST=http://127.0.0.1:11500`.
- The server briefly logged `Listening on 127.0.0.1:11500`, then exited.
- Ollama logs showed outbound calls to `ollama.com` failing with `WinError 10013`.
- Local calls to `127.0.0.1:11500` then failed with connection refused.

Latest recheck:

- `Get-Process ollama` shows `ollama.exe` running.
- `netstat -ano | findstr :11434` still shows `127.0.0.1:11434` held by PID `3612`.
- PID `3612` resolves to `svchost`, not the visible `ollama.exe`.
- `Invoke-RestMethod http://localhost:11434/api/tags` still fails with a closed connection.
- `Invoke-RestMethod http://127.0.0.1:11435/api/tags` succeeds.
- Do not treat PID `3612` on `11434` as the primary failure by itself; the workspace SSOT points Qwen/Ollama integration to `11435`.

Installed models from `ollama list`:

- `qwen3:4b` - 2.5 GB
- `qwen3.5:9b` - 6.6 GB
- `qwen2.5-coder:7b` - 4.7 GB
- `tinyllama:latest`
- `gemma4:e2b`
- `llama3:latest`
- `deepseek-coder:6.7b`
- `gemma2:9b`

Disk check:

- `C:\`: 150.57 GB free
- `D:\`: 80.19 GB free

## Official Model Check

The official Ollama library page lists `qwen3:8b` as a model tag. It also lists larger `qwen3:30b`, `qwen3:32b`, and `qwen3:235b` variants, but those were not pulled because of PC resource risk.

The official Ollama library also lists `qwen3.6`. `qwen3.6:latest` is about 24 GB with a 256K context window, so it is deferred for this transcript-indexing job.

Qwen coder option already installed:

- `qwen2.5-coder:7b`

## Upgrade Decision

No new model was pulled.

Reason:

- `qwen3:4b`, `qwen3.5:9b`, and `qwen2.5-coder:7b` are already installed.
- Ollama HTTP API is unstable in this environment, so pulling another model would not solve the immediate integration risk.
- `qwen3.5:9b` is now the configured first-choice indexing model.
- `qwen3:4b` is the configured fallback indexing model.
- Do not pull 30B/235B on this PC without explicit confirmation.
- Do not pull `qwen3.6:latest` for this workflow without explicit confirmation.

Optional next command after Ollama API is healthy and if `qwen3.5:9b` proves insufficient:

```powershell
ollama pull qwen3:8b
```

## Prompt Test

Prompt:

```text
너는 유튜브 자막 색인 생성기다. 원문을 판단하지 말고 chunk 제목과 키워드만 만든다.
```

Observed result:

- CLI test with `qwen3:4b` completed in about 29.7 seconds, but the response did not follow the requested concise indexing behavior.
- HTTP API tests failed on `11434` with connection closed by local host.
- HTTP API tests failed on `11500` after the alternate server exited.

Conclusion:

- Local Qwen models are installed, but Ollama HTTP serving is not yet reliable enough as a primary worker in this environment.
- The implementation therefore records Qwen failures and falls back to deterministic keyword indexing.
- Claude must treat Qwen output as an index only and must inspect raw chunks before using any content.
- Qwen should be operated through the configured `11435` HTTP endpoint unless the control panel port registry changes.

## Current Config

File:

`tools/youtube_intake/config.json`

Configured values:

- `ollama_base_url`: `http://127.0.0.1:11435`
- first indexing model: `qwen3.5:9b`
- fallback indexing model: `qwen3:4b`
- coding helper: `qwen2.5-coder:7b`
- deferred model: `qwen3.6:latest`
