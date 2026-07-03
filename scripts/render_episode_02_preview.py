#!/usr/bin/env python3
"""
render_episode_02_preview.py — EP02 저해상도 미리보기(슬라이드쇼) 렌더.
⚠️ 별도 승인 전 실행 금지. 이 파일은 준비만. 업로드 기능 없음.

edit_timeline.json의 cut별 visual_asset을 start~end 길이만큼 이어붙여 무음(또는 BGM 없이) preview mp4를 만든다.
실제 방송본이 아니라 '컷 순서·타이밍 확인용' 미리보기.

전제: ffmpeg 필요. 내레이션 TTS·BGM·자막 번인은 이 스크립트 범위 밖(1차 편집 도구에서).

사용(승인 후):
  python scripts/render_episode_02_preview.py \
    --timeline assets/ai-early-education/video-episode-02-singapore/timeline/edit_timeline.json \
    --out assets/ai-early-education/video-episode-02-singapore/exports/ep02_preview.mp4
"""
import argparse, json, os, subprocess, tempfile, shutil, glob
from PIL import Image

BASE = "assets/ai-early-education/video-episode-02-singapore"
EVID = "assets/ai-early-education/singapore-evidence"
FRAME_W, FRAME_H = 1920, 1080

def normalize_frame(src, dst, bg=(24, 26, 42)):
    """이미지를 1920x1080으로 스케일+레터박스(비율 유지)해서 dst에 저장."""
    im = Image.open(src).convert("RGB")
    r = min(FRAME_W / im.width, FRAME_H / im.height)
    nw, nh = max(1, int(im.width * r)), max(1, int(im.height * r))
    im = im.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (FRAME_W, FRAME_H), bg)
    canvas.paste(im, ((FRAME_W - nw) // 2, (FRAME_H - nh) // 2))
    canvas.save(dst)

def find_ffmpeg():
    # 1) env  2) PATH  3) playwright 캐시(ffmpeg-win64.exe 등)
    if os.environ.get("FFMPEG_BIN") and os.path.isfile(os.environ["FFMPEG_BIN"]):
        return os.environ["FFMPEG_BIN"]
    w = shutil.which("ffmpeg")
    if w: return w
    for pat in [os.path.expanduser(r"~\AppData\Local\ms-playwright\ffmpeg-*\ffmpeg*.exe")]:
        hits = glob.glob(pat)
        if hits: return hits[0]
    return None

def tc_to_sec(tc):
    m, s = tc.split(":"); return int(m) * 60 + int(s)

def resolve(asset):
    # visual_asset 문자열에서 실제 경로 추정
    if "singapore-evidence/" in asset:
        return os.path.join(EVID, asset.split("singapore-evidence/")[1])
    if "cards/" in asset:
        p = os.path.join(BASE, "cards", asset.split("cards/")[1].split("(")[0].strip())
        return p if os.path.isfile(p) else None
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeline", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--placeholder", default="")  # c01 등 미생성분 대체 이미지
    args = ap.parse_args()

    ffmpeg = find_ffmpeg()
    print("[preview] ffmpeg:", ffmpeg or "(없음)")

    tl = json.load(open(args.timeline, encoding="utf-8"))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # 컷별 대표 프레임 1장 + 실제 길이(ms). 해상도 통일(960 wide 레터박스).
    frames, durations_ms, missing, total_s = [], [], [], 0
    for c in tl["cuts"]:
        dur = max(1, tc_to_sec(c["end"]) - tc_to_sec(c["start"]))
        img = resolve(c["visual_asset"]) or (args.placeholder or None)
        if not img or not os.path.isfile(img):
            missing.append(c["cut_id"]); continue
        im = Image.open(img).convert("RGB")
        r = min(960 / im.width, 540 / im.height)
        nw, nh = int(im.width * r), int(im.height * r)
        canvas = Image.new("RGB", (960, 540), (24, 26, 42))
        canvas.paste(im.resize((nw, nh), Image.LANCZOS), ((960 - nw) // 2, (540 - nh) // 2))
        frames.append(canvas.convert("P", palette=Image.ADAPTIVE))
        durations_ms.append(dur * 1000); total_s += dur
    if missing:
        print("[preview] 건너뛴 컷(에셋 없음):", missing)
    if not frames:
        raise SystemExit("생성할 프레임이 없음.")

    # 우선 GIF(컷 실제 길이 반영, ffmpeg 불필요) — 이 환경 ffmpeg는 녹화전용 최소빌드라 image2 미지원
    gif_out = os.path.splitext(args.out)[0] + ".gif"
    frames[0].save(gif_out, save_all=True, append_images=frames[1:],
                   duration=durations_ms, loop=0, optimize=True, disposal=2)
    print(f"[preview] GIF 완료: {gif_out}  (컷 {len(frames)}개, 총 약 {total_s}s, 컷별 실제 길이 반영)")

    # (선택) ffmpeg rawvideo 파이프로 mp4 시도. 실패해도 GIF는 이미 생성됨.
    if ffmpeg:
        try:
            outabs = os.path.abspath(args.out)
            W2, H2 = 960, 540
            proc = subprocess.Popen(
                [ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W2}x{H2}",
                 "-framerate", "1", "-i", "-", "-r", "30", "-pix_fmt", "yuv420p", outabs],
                stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            for f, dms in zip(frames, durations_ms):
                raw = f.convert("RGB").tobytes()
                for _ in range(max(1, dms // 1000)):
                    proc.stdin.write(raw)
            proc.stdin.close(); err = proc.stderr.read().decode("utf-8", "ignore"); proc.wait()
            if proc.returncode == 0 and os.path.exists(outabs):
                print(f"[preview] MP4 완료: {args.out}")
            else:
                print(f"[preview] MP4 실패(GIF로 대체됨). ffmpeg: {err.strip()[-200:]}")
        except Exception as e:
            print(f"[preview] MP4 시도 예외(GIF로 대체됨): {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()
