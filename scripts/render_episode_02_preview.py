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
import argparse, json, os, subprocess, tempfile, shutil

BASE = "assets/ai-early-education/video-episode-02-singapore"
EVID = "assets/ai-early-education/singapore-evidence"

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

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg 없음. ms-playwright ffmpeg 경로를 PATH에 추가하거나 ffmpeg 설치 필요.")

    tl = json.load(open(args.timeline, encoding="utf-8"))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    tmp = tempfile.mkdtemp()
    listfile = os.path.join(tmp, "list.txt")
    missing = []
    with open(listfile, "w", encoding="utf-8") as lf:
        for c in tl["cuts"]:
            dur = max(1, tc_to_sec(c["end"]) - tc_to_sec(c["start"]))
            img = resolve(c["visual_asset"]) or (args.placeholder or None)
            if not img or not os.path.isfile(img):
                missing.append(c["cut_id"]); continue
            lf.write(f"file '{os.path.abspath(img)}'\n"); lf.write(f"duration {dur}\n")
        # ffmpeg concat: 마지막 이미지 한 번 더
        if tl["cuts"]:
            last = resolve(tl["cuts"][-1]["visual_asset"]) or args.placeholder
            if last and os.path.isfile(last):
                lf.write(f"file '{os.path.abspath(last)}'\n")

    if missing:
        print("[preview] 자리표시 없음으로 건너뛴 컷:", missing, "(--placeholder로 대체 가능)")

    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
           "-vf", "scale=960:-2,format=yuv420p", "-r", "30", args.out]
    print("[preview] 실행:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print("[preview] 완료:", args.out, "(미리보기 슬라이드쇼, 방송본 아님)")

if __name__ == "__main__":
    main()
