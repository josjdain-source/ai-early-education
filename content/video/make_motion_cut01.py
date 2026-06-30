# -*- coding: utf-8 -*-
"""cut01 모션 컷 — 검수 통과 원본(아이가 AI에게 질문) 보존, 복사본으로 Ken Burns 약한 움직임.
원칙: 원본 절대 수정 X / AI 재생성 X / 얼굴·손·화면텍스트·구도 변형 X.
움직임 = ffmpeg zoompan 아주 느린 중앙 확대(1.00→1.04)만. 회전·흔들림·전환 없음.
세로 1080x1920: 원본 전체를 흐린 배경 위에 그대로 얹어(피사체 무변형) 얼굴·손·말풍선 모두 살림."""
import os, shutil, subprocess
from PIL import Image, ImageFilter

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
SRC = os.path.join(ROOT, "assets", "process-a-ask.png")  # 현재 검수통과 이미지(손 교정본)

MASTER_DIR = os.path.join(ROOT, "assets", "images", "ep01", "master")
MOTION_DIR = os.path.join(ROOT, "assets", "images", "ep01", "motion")
VID_DIR = os.path.join(ROOT, "assets", "video", "ep01")
for d in (MASTER_DIR, MOTION_DIR, VID_DIR):
    os.makedirs(d, exist_ok=True)

MASTER = os.path.join(MASTER_DIR, "computer_dinosaur_question.png")
MOTION = os.path.join(MOTION_DIR, "cut01_child_asking_ai.png")
STILL2X = os.path.join(VID_DIR, "_cut01_still2x.png")  # 합성용 임시(2배=zoompan 지터 감소)
OUT = os.path.join(VID_DIR, "cut01_child_asking_ai_motion.mp4")

# 1) 원본 보존 + 영상용 복사본 (바이트 단위 그대로 복사, 무변형)
shutil.copy2(SRC, MASTER)
shutil.copy2(SRC, MOTION)
print("[copy] master :", MASTER, os.path.getsize(MASTER), "B")
print("[copy] motion :", MOTION, os.path.getsize(MOTION), "B")

# 2) 세로 합성 스틸(2배 해상도) — 피사체는 손대지 않고 전체를 그대로 중앙 배치
W, H = 2160, 3840
src = Image.open(MOTION).convert("RGB")
# 배경: 원본을 캔버스 cover 후 강한 블러(피사체 아닌 채움용)
sc = max(W/src.width, H/src.height)
bg = src.resize((int(src.width*sc), int(src.height*sc)), Image.LANCZOS)
bx, by = (bg.width-W)//2, (bg.height-H)//2
bg = bg.crop((bx, by, bx+W, by+H)).filter(ImageFilter.GaussianBlur(60))
bg = Image.eval(bg, lambda p: int(p*0.82))  # 살짝 어둡게(피사체 강조)
# 전경: 원본 전체를 캔버스 폭 94%로(잘림 방지 여백 확보), 무변형 그대로 중앙
fw = int(W*0.94); fh = int(fw*src.height/src.width)
fg = src.resize((fw, fh), Image.LANCZOS)
canvas = bg.copy()
canvas.paste(fg, ((W-fw)//2, (H-fh)//2))
canvas.save(STILL2X)
print("[still]", STILL2X, canvas.size)

# 3) Ken Burns — 중앙 기준 1.00→1.04 아주 느린 확대(9초, 30fps). 회전·흔들림 없음.
FPS, DUR = 30, 9
N = FPS*DUR  # 270
vf = (f"zoompan=z='min(1.0+0.04*on/{N-1},1.04)':d={N}:"
      f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS},format=yuv420p")
subprocess.run([FF, "-y", "-loop", "1", "-i", STILL2X, "-vf", vf,
                "-t", str(DUR), "-r", str(FPS),
                "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", OUT],
               check=True, capture_output=True)
os.remove(STILL2X)
print("[OK]", OUT, os.path.getsize(OUT), "B")
