#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch YouTube metadata and subtitles while preserving raw files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = Path(__file__).resolve().parent / "output"


def video_id_from_url(url: str) -> str:
    patterns = [
        r"[?&]v=([A-Za-z0-9_-]{6,})",
        r"youtu\.be/([A-Za-z0-9_-]{6,})",
        r"youtube\.com/shorts/([A-Za-z0-9_-]{6,})",
        r"youtube\.com/embed/([A-Za-z0-9_-]{6,})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    safe = re.sub(r"[^A-Za-z0-9_-]+", "_", url).strip("_")
    return safe[:80] or "manual_video"


def run_yt_dlp(url: str, out_dir: Path, langs: str = "ko,en") -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    base = out_dir / "source"
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-info-json",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        langs,
        "--sub-format",
        "json3/vtt/srv3/best",
        "-o",
        str(base),
        url,
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=180)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def load_info(out_dir: Path, url: str, video_id: str) -> dict[str, Any]:
    info_files = sorted(out_dir.glob("source.info.json"))
    if not info_files:
        return {"id": video_id, "webpage_url": url, "fetch_status": "metadata_missing"}
    data = json.loads(info_files[0].read_text(encoding="utf-8"))
    keep = {
        "id": data.get("id") or video_id,
        "title": data.get("title"),
        "webpage_url": data.get("webpage_url") or url,
        "channel": data.get("channel"),
        "uploader": data.get("uploader"),
        "duration": data.get("duration"),
        "upload_date": data.get("upload_date"),
        "language": data.get("language"),
        "availability": data.get("availability"),
    }
    return keep


def transcript_from_json3(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = []
    for event in data.get("events", []):
        segs = event.get("segs") or []
        text = "".join(seg.get("utf8", "") for seg in segs).strip()
        if not text:
            continue
        items.append({
            "start": event.get("tStartMs", 0) / 1000,
            "duration": event.get("dDurationMs", 0) / 1000,
            "text": text,
        })
    return items


def transcript_from_vtt(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    items = []
    buf: list[str] = []
    start = 0.0
    for line in lines:
        if "-->" in line:
            if buf:
                items.append({"start": start, "duration": 0, "text": " ".join(buf).strip()})
                buf = []
            start = parse_vtt_time(line.split("-->", 1)[0].strip())
        elif line.strip() and not line.startswith(("WEBVTT", "Kind:", "Language:")) and not line.strip().isdigit():
            buf.append(re.sub(r"<[^>]+>", "", line).strip())
    if buf:
        items.append({"start": start, "duration": 0, "text": " ".join(buf).strip()})
    return [x for x in items if x["text"]]


def parse_vtt_time(value: str) -> float:
    parts = value.replace(",", ".").split(":")
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
    except ValueError:
        return 0.0
    return 0.0


def choose_subtitle(out_dir: Path) -> Path | None:
    candidates = []
    for suffix in ("*.ko.json3", "*.en.json3", "*.json3", "*.ko.vtt", "*.en.vtt", "*.vtt"):
        candidates.extend(out_dir.glob(suffix))
    return candidates[0] if candidates else None


def write_transcript(out_dir: Path, transcript: list[dict[str, Any]]) -> None:
    (out_dir / "transcript_raw.json").write_text(json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = []
    for item in transcript:
        start = float(item.get("start") or 0)
        lines.append(f"[{format_time(start)}] {item.get('text', '').strip()}")
    (out_dir / "transcript.txt").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def format_time(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds//3600:02d}:{(seconds%3600)//60:02d}:{seconds%60:02d}"


def fetch(url: str, output_root: Path = OUTPUT_ROOT, transcript_file: Path | None = None) -> Path:
    video_id = video_id_from_url(url)
    out_dir = output_root / video_id
    out_dir.mkdir(parents=True, exist_ok=True)
    run_meta: dict[str, Any] = {"url": url, "video_id": video_id}

    if transcript_file:
        text = transcript_file.read_text(encoding="utf-8")
        transcript = [{"start": 0, "duration": 0, "text": line.strip()} for line in text.splitlines() if line.strip()]
        raw_meta = {"id": video_id, "webpage_url": url, "fetch_status": "manual_transcript"}
    else:
        run_meta["yt_dlp"] = run_yt_dlp(url, out_dir)
        raw_meta = load_info(out_dir, url, video_id)
        sub = choose_subtitle(out_dir)
        if sub and sub.suffix == ".json3":
            transcript = transcript_from_json3(sub)
        elif sub:
            transcript = transcript_from_vtt(sub)
        else:
            transcript = []
        raw_meta["subtitle_file"] = sub.name if sub else None
        raw_meta["fetch_status"] = "ok" if transcript else "transcript_missing"

    (out_dir / "raw_meta.json").write_text(json.dumps({**raw_meta, "run": run_meta}, ensure_ascii=False, indent=2), encoding="utf-8")
    write_transcript(out_dir, transcript)
    return out_dir


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--output-root", type=Path, default=OUTPUT_ROOT)
    ap.add_argument("--transcript-file", type=Path)
    args = ap.parse_args()
    print(fetch(args.url, args.output_root, args.transcript_file))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
