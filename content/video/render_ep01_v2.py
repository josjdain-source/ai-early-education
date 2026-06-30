# -*- coding: utf-8 -*-
"""1편 쇼츠 v2 — 초반 3초 안에 before/after 후킹(사진 한 장 → 감정 캐릭터 20종) + 프롬프트 카드 컷.
v1(ep01_door_sign.mp4)은 보존, v2는 별도 파일 ep01_door_sign_v2.mp4로 출력.
영상 길이 = tail-safe 음성(38.3s, 끝 2초 무음). 음성 재생성 없음. 자동 업로드 없음."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
AUDIO = os.path.join(ROOT, "assets", "audio", "door-sign-short-01.tail2s.wav")
OUTDIR = os.path.join(ROOT, "assets", "video"); os.makedirs(OUTDIR, exist_ok=True)
TMP = os.path.join(OUTDIR, "_frames_v2"); os.makedirs(TMP, exist_ok=True)
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
    px, py = int(x0+((x1-x0)-im.width)/2), int(y0+((y1-y0)-im.height)/2)
    canvas.paste(im, (px, py), im); return (px, py, im.width, im.height)

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

def beforeafter(im, d, card):
    # 사진(작게) → 화살표 → 감정 20종 시트  (한 화면 before/after)
    pbox = (card[0]+30, 470, card[0]+360, 1010)
    sbox = (card[0]+470, 470, card[2]-30, 1010)
    _, _, pw, ph = contained(im, os.path.join(ROOT,"assets","example_photo.png"), pbox)
    contained(im, os.path.join(ROOT,"assets","example_emotion_sheet.png"), sbox)
    ax = (pbox[2]+sbox[0])/2
    aw = d.textlength("→", font=f(FB,110)); d.text((ax-aw/2, 690), "→", font=f(FB,110), fill=(224,138,78))
    ctext(d, (pbox[0]+pbox[2])/2, 1030, ["사진"], f(FB,40), (138,125,112), 48)
    ctext(d, (sbox[0]+sbox[2])/2, 1030, ["감정 20종"], f(FB,40), (138,125,112), 48)

def promptcard(im, d, card):
    # GPT 프롬프트 카드 느낌 (faux prompt box + 복사 pill)
    bx = (card[0]+70, card[1]+70, card[2]-70, card[3]-110)
    d.rounded_rectangle(bx, radius=28, fill=(255,253,248), outline=(236,226,214), width=4)
    d.text((bx[0]+34, bx[1]+30), "GPT 프롬프트", font=f(FB,40), fill=(201,116,58))
    ys = bx[1]+110; widths = [0.86,0.72,0.9,0.64,0.8,0.7,0.58]
    for w in widths:
        d.rounded_rectangle([bx[0]+34, ys, bx[0]+34+(bx[2]-bx[0]-68)*w, ys+26], radius=13, fill=(229,222,212)); ys += 52
    pill = [bx[2]-300, bx[3]-90, bx[2]-34, bx[3]-30]
    d.rounded_rectangle(pill, radius=30, fill=(224,138,78))
    t = "프롬프트 복사"; tw = d.textlength(t, font=f(FB,40))
    d.text(((pill[0]+pill[2])/2-tw/2, pill[1]+8), t, font=f(FB,40), fill=(255,255,255))

THEME = [(255,243,228),(253,246,238)]
CUTS = [
    dict(dur=2.5, kind="beforeafter", title=["사진 한 장이","감정 캐릭터 20종으로!"], step=""),
    dict(dur=2.5, kind="promptcard", title=["프롬프트는","홈페이지에서 복사해요"], step=""),
    dict(dur=5.0, img="example_emotion_sheet.png", title=["AI로 감정 캐릭터 만들기"], step="STEP 1"),
    dict(dur=4.5, icon="printer", title=["프린터로 출력해요"], step="STEP 2"),
    dict(dur=4.5, icon="laminate", title=["손코팅지로 코팅해요"], step="STEP 3"),
    dict(dur=5.0, icon="scissors", title=["폼보드에 붙이고 잘라요"], step="STEP 4"),
    dict(dur=6.0, img="door-sign-sample.png", title=["문 앞에 걸면 완성!"], step="STEP 5"),
    dict(dur=8.3, img="hero-art.png", title=["아이와 함께 만들어보는 AI"], step="", sub="프롬프트는 홈페이지에 있어요"),
]

def render(i, c):
    im = grad(*THEME); d = ImageDraw.Draw(im)
    ctext(d, W/2, 110, ["아이와 함께 배우는 생성형 AI"], f(FB,40), (200,150,90), 50)
    card = [90, 360, W-90, 1180]
    d.rounded_rectangle(card, radius=40, fill=(255,255,255))
    box = (card[0]+50, card[1]+50, card[2]-50, card[3]-50)
    if c.get("kind") == "beforeafter":
        beforeafter(im, d, card)
    elif c.get("kind") == "promptcard":
        promptcard(im, d, card)
    elif c.get("img"):
        contained(im, os.path.join(ROOT,"assets",c["img"]), box)
    elif c.get("icon"):
        cx, cy = W/2, (card[1]+card[3])/2; s = 230
        {"printer":icon_printer,"laminate":icon_laminate,"scissors":icon_scissors}[c["icon"]](d, cx, cy, s)
    if c["step"]:
        cw = d.textlength(c["step"], font=f(FB,46)); pill=[W/2-cw/2-40, 1300, W/2+cw/2+40, 1380]
        d.rounded_rectangle(pill, radius=40, fill=(224,138,78)); d.text((W/2-cw/2, 1314), c["step"], font=f(FB,46), fill=(255,255,255))
    ctext(d, W/2, 1440, c["title"], f(FB,78), (58,50,44), 96)
    if c.get("sub"):
        sy = 1440 + len(c["title"]) * 96 + 14
        ctext(d, W/2, sy, [c["sub"]], f(FR,46), (150,120,90), 56)
    p = os.path.join(TMP, f"f{i}.png"); im.save(p); return p

frames = [render(i,c) for i,c in enumerate(CUTS)]

lst = os.path.join(TMP, "list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for i,c in enumerate(CUTS):
        fh.write(f"file '{frames[i].replace(os.sep,'/')}'\nduration {c['dur']}\n")
    fh.write(f"file '{frames[-1].replace(os.sep,'/')}'\n")

vid = os.path.join(OUTDIR, "_video_only_v2.mp4")
out = os.path.join(OUTDIR, "ep01_door_sign_v2.mp4")
subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,"-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast",vid], check=True, capture_output=True)
subprocess.run([FF,"-y","-i",vid,"-i",AUDIO,"-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out], check=True, capture_output=True)
print("[OK]", out, os.path.getsize(out), "B")
