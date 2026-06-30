# -*- coding: utf-8 -*-
"""1편 쇼츠 v3 — 새 포지셔닝(AI에게 다시 말하며 원하는 결과 만들기 = 핵심, 문패는 활용).
새 craft_narrator 내레이션(43.57s tail-safe)에 컷 동기화. v1/v2 보존, v3=별도 파일.
영상 길이 = 음성(43.57s). 자동 업로드 없음."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
AUDIO = os.path.join(ROOT, "assets", "audio", "door-sign-short-v3.tail2s.wav")
OUTDIR = os.path.join(ROOT, "assets", "video"); os.makedirs(OUTDIR, exist_ok=True)
TMP = os.path.join(OUTDIR, "_frames_v3"); os.makedirs(TMP, exist_ok=True)
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

def askcut(im, d, card):
    """사진 한 장 + 아이가 AI에게 말 거는 말풍선 (아직 결과는 안 보임 — 목소리와 동기화)."""
    pbox = (card[0]+200, card[1]+45, card[2]-200, card[1]+545)
    contained(im, os.path.join(ROOT,"assets","example_photo.png"), pbox)
    t = "감정 캐릭터로 만들어줘"
    fnt = f(FB,50); tw = d.textlength(t, font=fnt); bw = tw+80; bh = 102
    x0 = (card[0]+card[2])/2 - bw/2; y0 = card[3]-190
    d.rounded_rectangle([x0, y0, x0+bw, y0+bh], radius=34, fill=(224,138,78))
    d.text((x0+40, y0+bh/2-33), t, font=fnt, fill=(255,255,255))

def saycard(im, d, card, texts, top=False):
    """아이가 AI에게 '다시 말하는' 말풍선들. top=True면 상단 고정(누적 등장 시 안 흔들림)."""
    cx0, cy0, cx1, cy1 = card
    fnt = f(FB, 52); bh = 104; gap = 30
    if top:
        y = cy0 + 110
    else:
        total = len(texts)*bh + (len(texts)-1)*gap
        y = (cy0+cy1)/2 - total/2
    for t in texts:
        tw = d.textlength(t, font=fnt); bw = tw + 80
        x0 = (cx0+cx1)/2 - bw/2; x1 = x0 + bw
        d.rounded_rectangle([x0, y, x1, y+bh], radius=34, fill=(224,138,78))
        d.text((x0+40, y+bh/2-34), t, font=fnt, fill=(255,255,255))
        y += bh + gap

THEME = [(255,243,228),(253,246,238)]
# 컷 = 실측 문장/어절 경계(silencedetect)에 정렬. 말풍선은 어절마다 하나씩 등장(목소리와 동행).
B3 = ["더 귀엽게 해줘", "번호는 빼줘", "5열 4행으로 정리해줘"]
CUTS = [
    dict(dur=6.6,  kind="ask", title=["사진 한 장으로","AI에게 말을 걸어요"]),                 # 0.0   사진+부탁
    dict(dur=2.4,  img="example_emotion_sheet.png", title=["여러 표정이 나와요"]),              # 6.6   여러 표정을 그려줍니다
    dict(dur=3.04, img="example_emotion_sheet.png", title=["마음에 안 들면, 다시 말해요"]),     # 9.0   결과 보고 다시 말하기
    dict(dur=2.77, kind="say", saytop=True, says=B3[:1], title=["이렇게 다시 말해요"]),         # 12.04 "더 귀엽게"
    dict(dur=1.20, kind="say", saytop=True, says=B3[:2], title=["이렇게 다시 말해요"]),         # 14.81 "번호는 빼줘"
    dict(dur=1.79, kind="say", saytop=True, says=B3[:3], title=["이렇게 다시 말해요"]),         # 16.01 "5열 4행으로"
    dict(dur=2.83, img="example_emotion_sheet.png", title=["다시 말할수록","원하는 결과에 가까워져요"]),  # 17.8
    dict(dur=4.15, img="door-sign-sample.png", title=["완성! 오늘 마음 문패로 활용"]),          # 20.63 문패
    dict(dur=4.83, kind="say", says=["AI에게 어떻게 말할까?"], title=["핵심은 결과물이 아니라","AI에게 말하는 법을 배우는 거예요"]),  # 24.78 핵심
    dict(dur=7.46, img="hero-art.png", title=["AI 조기교육은","말하기부터 시작돼요"]),          # 29.61 코딩이 아니라
    dict(dur=6.50, img="hero-art.png", title=["AI 조기교육은","말하기부터 시작돼요"], sub="프롬프트는 홈페이지에"),  # 37.07 ~ 43.57
]

def render(i, c):
    im = grad(*THEME); d = ImageDraw.Draw(im)
    ctext(d, W/2, 110, ["아이와 함께 배우는 생성형 AI"], f(FB,40), (200,150,90), 50)
    card = [90, 360, W-90, 1180]
    d.rounded_rectangle(card, radius=40, fill=(255,255,255))
    box = (card[0]+50, card[1]+50, card[2]-50, card[3]-50)
    if c.get("kind") == "ask":
        askcut(im, d, card)
    elif c.get("kind") == "say":
        saycard(im, d, card, c["says"], c.get("saytop", False))
    elif c.get("img"):
        contained(im, os.path.join(ROOT,"assets",c["img"]), box)
    # 제목: 가장 긴 줄이 화면 폭에 맞도록 자동 축소
    size = 74; maxw = W - 96
    while size > 44 and max(d.textlength(ln, font=f(FB, size)) for ln in c["title"]) > maxw:
        size -= 3
    lh = int(size * 1.24)
    ctext(d, W/2, 1448, c["title"], f(FB, size), (58,50,44), lh)
    if c.get("sub"):
        sy = 1448 + len(c["title"]) * lh + 12
        ctext(d, W/2, sy, [c["sub"]], f(FR,46), (150,120,90), 56)
    p = os.path.join(TMP, f"f{i}.png"); im.save(p); return p

frames = [render(i,c) for i,c in enumerate(CUTS)]
lst = os.path.join(TMP, "list.txt")
with open(lst, "w", encoding="utf-8") as fh:
    for i,c in enumerate(CUTS):
        fh.write(f"file '{frames[i].replace(os.sep,'/')}'\nduration {c['dur']}\n")
    fh.write(f"file '{frames[-1].replace(os.sep,'/')}'\n")
vid = os.path.join(OUTDIR, "_video_only_v3.mp4")
out = os.path.join(OUTDIR, "ep01_door_sign_v3.mp4")
subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,"-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast",vid], check=True, capture_output=True)
subprocess.run([FF,"-y","-i",vid,"-i",AUDIO,"-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out], check=True, capture_output=True)
print("[OK]", out, os.path.getsize(out), "B")
