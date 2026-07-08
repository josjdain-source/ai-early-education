#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local Qwen chunk indexer for YouTube intake.

Qwen is only used as a filing assistant. It does not produce final summaries,
fact judgments, or content-ready claims.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Any


OLLAMA_URL = "http://localhost:11434"
CONFIG_PATH = Path(__file__).with_name("config.json")
DEFAULT_MODELS = ["qwen3.5:9b", "qwen3:4b"]
ALLOWED_USE = {"shorts_intro", "blog_evidence", "background", "ignore"}
PROMPT_PATH = Path(__file__).with_name("prompts") / "qwen_index_prompt.txt"


def load_config() -> dict[str, Any]:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def ollama_json(path: str, payload: dict[str, Any] | None = None, timeout: int = 20) -> dict[str, Any]:
    url = load_config().get("ollama_base_url", OLLAMA_URL).rstrip("/") + path
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8"))


def installed_models() -> list[str]:
    try:
        data = ollama_json("/api/tags", timeout=8)
        models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
        if models:
            return models
    except Exception:
        pass

    try:
        proc = subprocess.run(["ollama", "list"], text=True, capture_output=True, timeout=10)
    except Exception:
        return []

    models = []
    for line in proc.stdout.splitlines()[1:]:
        parts = line.split()
        if parts:
            models.append(parts[0])
    return models


def choose_model(preferred: list[str] | None = None) -> str | None:
    preferred = preferred or load_config().get("model_preference") or DEFAULT_MODELS
    models = installed_models()
    if not models:
        return preferred[0] if preferred else None

    for name in preferred:
        if name in models:
            return name

    qwen_models = [m for m in models if re.search(r"qwen", m, re.I)]
    if not qwen_models:
        return None

    for key in ["qwen3.5", "qwen3", "qwen2.5", "qwen"]:
        matches = [m for m in qwen_models if key in m.lower()]
        if matches:
            return sorted(matches)[0]
    return sorted(qwen_models)[0]


def build_prompt(chunk_text: str) -> str:
    guardrail = PROMPT_PATH.read_text(encoding="utf-8")
    return f"{guardrail}\n\nchunk 원문:\n\"\"\"\n{chunk_text}\n\"\"\""


def qwen_index_chunk(chunk_text: str, model: str, timeout: int = 45) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.perf_counter()
    payload = {
        "model": model,
        "prompt": build_prompt(chunk_text),
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.1, "num_predict": 220},
    }
    meta = {"model": model, "used_fallback": False, "elapsed_ms": None, "error": None}
    try:
        data = ollama_json("/api/generate", payload=payload, timeout=timeout)
        meta["elapsed_ms"] = int((time.perf_counter() - started) * 1000)
        text = data.get("response") or data.get("thinking") or ""
        return normalize_index(parse_json_object(text)), meta
    except Exception as exc:
        meta["elapsed_ms"] = int((time.perf_counter() - started) * 1000)
        meta["used_fallback"] = True
        meta["error"] = str(exc)
        return fallback_index(chunk_text), meta


def parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def normalize_index(data: dict[str, Any]) -> dict[str, Any]:
    keywords = data.get("keywords", [])
    if isinstance(keywords, str):
        keywords = [x.strip() for x in re.split(r"[,;/|]", keywords) if x.strip()]
    keywords = [str(x).strip()[:40] for x in keywords if str(x).strip()][:8]

    possible_use = str(data.get("possible_use", "background")).strip()
    if possible_use not in ALLOWED_USE:
        possible_use = "background"

    try:
        confidence = float(data.get("confidence", 0.5) or 0.5)
    except (TypeError, ValueError):
        confidence = 0.5

    return {
        "keywords": keywords,
        "one_line_hint": str(data.get("one_line_hint", "")).strip()[:180],
        "possible_use": possible_use,
        "confidence": confidence,
        "needs_raw_check": True,
    }


def fallback_index(text: str) -> dict[str, Any]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}|[가-힣]{2,}", text)
    stop = {
        "그리고", "하지만", "그래서", "이것은", "저것은", "합니다", "있습니다", "됩니다",
        "있는지", "없는지", "오늘은", "동안", "먼저",
        "the", "and", "that", "this", "with", "from", "have", "will", "your",
    }
    freq: dict[str, int] = {}
    for word in words:
        key = word.lower() if re.match(r"[A-Za-z]", word) else word
        if key in stop:
            continue
        freq[key] = freq.get(key, 0) + 1

    keywords = [word for word, _ in sorted(freq.items(), key=lambda item: (-item[1], item[0]))[:8]]
    first_sentence = re.split(r"(?<=[.!?。！？])\s+|\n+", text.strip())[0] if text.strip() else ""
    return {
        "keywords": keywords,
        "one_line_hint": first_sentence[:160],
        "possible_use": "background" if keywords else "ignore",
        "confidence": 0.25,
        "needs_raw_check": True,
    }


def index_chunk_file(path: Path, model: str | None = None) -> dict[str, Any]:
    selected = model or choose_model()
    text = path.read_text(encoding="utf-8")
    if not selected:
        result = fallback_index(text)
        meta = {"model": None, "used_fallback": True, "elapsed_ms": 0, "error": "No Ollama Qwen model available"}
    else:
        result, meta = qwen_index_chunk(text, selected)
    result["raw_path"] = path.as_posix()
    result["qwen_meta"] = meta
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chunk")
    ap.add_argument("--model")
    args = ap.parse_args()
    print(json.dumps(index_chunk_file(Path(args.chunk), args.model), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
