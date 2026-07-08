#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create chunk files, Qwen chunk index, and Claude brief for YouTube intake."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from qwen_indexer import index_chunk_file
from youtube_fetch import OUTPUT_ROOT, fetch, video_id_from_url


def chunk_transcript(transcript_path: Path, chunks_dir: Path, max_chars: int = 2400) -> list[dict]:
    text = transcript_path.read_text(encoding="utf-8")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    chunks_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[dict] = []
    current: list[str] = []
    current_len = 0

    for line in lines:
        if current and current_len + len(line) + 1 > max_chars:
            chunks.append(write_chunk(chunks_dir, len(chunks) + 1, current))
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line) + 1

    if current:
        chunks.append(write_chunk(chunks_dir, len(chunks) + 1, current))
    return chunks


def write_chunk(chunks_dir: Path, idx: int, lines: list[str]) -> dict:
    chunk_id = f"c{idx:03d}"
    path = chunks_dir / f"{chunk_id}.txt"
    content = "\n".join(lines).strip() + "\n"
    path.write_text(content, encoding="utf-8")
    return {
        "chunk_id": chunk_id,
        "raw_path": path.as_posix(),
        "char_count": len(content),
        "line_count": len(lines),
    }


def build_index(out_dir: Path, model: str | None = None) -> list[dict]:
    chunks = chunk_transcript(out_dir / "transcript.txt", out_dir / "chunks")
    index = []
    for chunk in chunks:
        result = index_chunk_file(Path(chunk["raw_path"]), model)
        index.append({**chunk, **result})
    (out_dir / "chunk_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    write_claude_brief(out_dir, index)
    return index


def write_claude_brief(out_dir: Path, index: list[dict]) -> None:
    meta = json.loads((out_dir / "raw_meta.json").read_text(encoding="utf-8"))
    lines = [
        "# Claude Brief",
        "",
        "- 이 문서는 Qwen이 만든 색인이다.",
        "- 최종 판단 전 필요한 raw chunk를 직접 확인하라.",
        "- 원문 자막 전체를 기본으로 Claude에게 넣지 말라.",
        "- 콘텐츠에 쓸 문장은 raw chunk에서 확인하라.",
        "- 원문 복붙 금지, 출처 링크 필요.",
        "",
        f"Source URL: {meta.get('webpage_url') or meta.get('run', {}).get('url')}",
        f"Video ID: {meta.get('id')}",
        f"Fetch status: {meta.get('fetch_status')}",
        "",
        "## Chunk Map",
        "",
    ]
    for item in index:
        keywords = ", ".join(item.get("keywords", []))
        lines.extend([
            f"### {item['chunk_id']}",
            f"- raw_path: `{item['raw_path']}`",
            f"- possible_use: {item.get('possible_use')}",
            f"- keywords: {keywords}",
            f"- one_line_hint: {item.get('one_line_hint', '')}",
            f"- needs_raw_check: {item.get('needs_raw_check', True)}",
            "",
        ])
    (out_dir / "claude_brief.md").write_text("\n".join(lines), encoding="utf-8")


def output_dir_for(target: str, output_root: Path) -> Path:
    if re.match(r"https?://", target):
        return output_root / video_id_from_url(target)
    return output_root / target


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("target", help="YouTube URL or existing output video_id")
    ap.add_argument("--output-root", default=str(OUTPUT_ROOT))
    ap.add_argument("--transcript-file", help="Manual transcript fallback file")
    ap.add_argument("--model", help="Explicit Ollama model name")
    ap.add_argument("--max-chars", type=int, default=2400)
    args = ap.parse_args()

    output_root = Path(args.output_root)
    target = args.target
    out_dir = output_dir_for(target, output_root)

    if re.match(r"https?://", target) or args.transcript_file:
        out_dir = fetch(target, output_root, transcript_file=Path(args.transcript_file) if args.transcript_file else None)

    if not (out_dir / "transcript.txt").exists() or not (out_dir / "transcript.txt").read_text(encoding="utf-8").strip():
        raise SystemExit(f"No transcript available: {out_dir / 'transcript.txt'}")

    chunks = chunk_transcript(out_dir / "transcript.txt", out_dir / "chunks", args.max_chars)
    index = []
    for chunk in chunks:
        result = index_chunk_file(Path(chunk["raw_path"]), args.model)
        index.append({**chunk, **result})
    (out_dir / "chunk_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    write_claude_brief(out_dir, index)
    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
