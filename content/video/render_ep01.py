# -*- coding: utf-8 -*-
"""1편 쇼츠 영상 렌더 — 세로 9:16 프레임(PIL) → ffmpeg로 tail-safe 음성과 합성.
영상 길이 = 음성 길이(38.3s, 끝 2초 무음). 마지막 컷 8.3s(>=2s 유지). 자동 업로드 없음."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
AUDIO = os.path.join(ROOT, "assets", "audio", "door-sign-short-01.tail2s.wav")
OUTDIR = os.path.join(ROOT, "assets", "video"); os.makedirs(OUTDIR, exist_ok=True)
TMP = os.path.join(OUTDIR, "_frames"); os.makedirs(TMP, exist_ok=True)
FB = r"C:\Windows\Fonts\malgunbd.ttf"; FR = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1080, 1920

def f(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()

def grad(top, bot):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3)))
    return im

def ctext(d, cx, y, lines, font, fill, lh):
    for ln in lines:
        w = d.textlength(ln, font=font); d.text((cx - w/2, y), ln, font=font, fill=fill); y += lh

def contained(canvas, path, box):
    im = Image.open(path).convert("RGBA"); x0,y0,x1,y1 = box
    sc = min((x1-x0)/im.width, (y1-y0)/im.height)
    im = im.resize((max(1,int(im.width*sc)), max(1,int(im.height*sc))), Image.LANCZOS)
    canvas.paste(im, (int(x0+((x1-x0)-im.width)/2), int(y0+((y1-y0)-im.height)/2)), im)

# 간단 아이콘 (PIL 도형)
def icon_printer(d, cx, cy, s):
    d.rounded_rectangle([cx-s, cy-s*0.2, cx+s, cy+s*0.6], radius=24, fill=(180,186,196))
    d.rectangle([cx-s*0.6, cy-s*0.8, cx+s*0.6, cy-s*0.1], fill=(255,255,255), outline=(120,126,136), width=5)
    d.rectangle([cx-s*0.6, cy+s*0.4, cx+s*0.6, cy+s], fill=(255,255,255), outline=(120,126,136), width=5)
def icon_laminate(d, cx, cy, s):
    d.rounded_rectangle([cx-s, cy-s*0.7, cx+s*0.5, cy+s*0.7], radius=20, fill=(210,236,250), outline=(120,170,200), width=5)
    d.rounded_rectangle([cx-s*0.5, cy-s, cx+s, cy+s*0.4], radius=20, fill=(235,247,253), outline=(120,170,200), width=5)
def icon_scissors(d, cx, cy, s):
    d.ellipse([cx-s*0.9, cy+s*0.1, cx-s*0.2, cy+s*0.8], outline=(224,138,78), width=14)
    d.ellipse([cx+s*0.2, cy+s*0.1, cx+s*0.9, cy+s*0.8], outline=(224,138,78), width=14)
    d.line([cx-s*0.55, cy+s*0.4, cx+s*0.7, cy-s*0.8], fill=(120,126,136), width=14)
    d.line([cx+s*0.55, cy+s*0.4, cx-s*0.7, cy-s*0.8], fill=(120,126,136), width=14)

THEME = [(255,243,228),(253,246,238)]
CUTS = [
    dict(dur=4.5, img="hero-art.png", title=["사진 한 장으로","오늘 마음 문패 만들기"], step=""),
    dict(dur=5.5, crop=("hero-art.png",(150,75,375,295)), title=["AI로 감정 캐릭터 만들기"], step="STEP 1"),
    dict(dur=4.5, icon="printer", title=["프린터로 출력해요"], step="STEP 2"),
    dict(dur=4.5, icon="laminate", title=["손코팅지로 코팅해요"], step="STEP 3"),
    dict(dur=5.0, icon="scissors", title=["폼보드에 붙이고 잘라요"], step="STEP 4"),
    dict(dur=6.0, img="door-sign-sample.png", title=["문 앞에 걸면 완성!"], step="STEP 5"),
    dict(dur=8.3, img="hero-art.png", title=["아이와 함께 만들어보는 AI","다음 만들기에서 또 만나요"], step=""),
]

def render(i, c):
    im = grad(*THEME); d = ImageDraw.Draw(im)
    ctext(d, W/2, 110, ["아이와 함께 배우는 생성형 AI"], f(FB,40), (200,150,90), 50)
    # 가운데 카드
    card = [90, 360, W-90, 1180]
    d.rounded_rectangle(card, radius=40, fill=(255,255,255))
    box = (card[0]+50, card[1]+50, card[2]-50, card[3]-50)
    if c.get("img"):
        contained(im, os.path.join(ROOT,"assets",c["img"]), box)
    elif c.get("crop"):
        src, reg = c["crop"]; tmp = os.path.join(TMP, f"crop{i}.png")
        Image.open(os.path.join(ROOT,"assets",src)).convert("RGBA").crop(reg).save(tmp)
        contained(im, tmp, box)
    elif c.get("icon"):
        cx, cy = W/2, (card[1]+card[3])/2; s = 230
        {"printer":icon_printer,"laminate":icon_laminate,"scissors":icon_scissors}[c["icon"]](d, cx, cy, s)
    # step chip
    if c["step"]:
        cw = d.textlength(c["step"], font=f(FB,46)); pill=[W/2-cw/2-40, 1300, W/2+cw/2+40, 1380]
        d.rounded_rectangle(pill, radius=40, fill=(224,138,78)); d.text((W/2-cw/2, 1314), c["step"], font=f(FB,46), fill=(255,255,255))
    # 자막
    ctext(d, W/2, 1440, c["title"], f(FB,78), (58,50,44), 96)
    p = os.path.join(TMP, f"f{i}.png"); im.save(p); return p

frames = [render(i,c) for i,c in enumerate(CUTS)]

# concat 리스트
lst = os.path.join(TMP, "list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for i,c in enumerate(CUTS):
        fh.write(f"file '{frames[i].replace(os.sep,'/')}'\nduration {c['dur']}\n")
    fh.write(f"file '{frames[-1].replace(os.sep,'/')}'\n")

vid = os.path.join(OUTDIR, "_video_only.mp4")
out = os.path.join(OUTDIR, "ep01_door_sign.mp4")
subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,"-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast",vid], check=True, capture_output=True)
subprocess.run([FF,"-y","-i",vid,"-i",AUDIO,"-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out], check=True, capture_output=True)
print("[OK]", out, os.path.getsize(out), "B")
