#!/usr/bin/env python3
"""세계 AI교육 5분 본편 이미지 — 무료 플랫 인포그래픽 방식(16:9, 1920x1080).
톤 통일: 사이트 팔레트(라벤더·블루·크림), 드로잉 아이콘 중심, 텍스트 최소, 국기 남발 금지.
gpt-image-1 결제한도 초과로 API 미사용. 톤 고정 1차=IMG-01~04.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "assets/world-ai-education-5min/images"
W, H = 1920, 1080
KB = r"C:\Windows\Fonts\malgunbd.ttf"; KF = r"C:\Windows\Fonts\malgun.ttf"
# 팔레트
BG1, BG2 = (243, 240, 255), (238, 246, 255)
PUR, BLUE, GREEN, ORG = (124, 108, 255), (47, 107, 216), (10, 138, 74), (192, 81, 43)
INK, GRAY, CARD = (36, 36, 51), (150, 150, 170), (255, 255, 255)
SOFT = (225, 222, 240)

def F(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()

def bg():
    im = Image.new("RGB", (W, H), BG1)
    top = Image.new("RGB", (W, H), BG2)
    mask = Image.new("L", (W, H))
    md = ImageDraw.Draw(mask)
    for y in range(H):
        md.line([(0, y), (W, y)], fill=int(255 * (y / H)))
    im = Image.composite(top, im, mask)
    d = ImageDraw.Draw(im, "RGBA")
    # 부드러운 배경 원(깊이감)
    for (cx, cy, r, col) in [(300, 200, 260, (124,108,255,26)), (1650, 900, 320, (47,107,216,22)),
                             (1500, 150, 180, (192,81,43,18))]:
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col)
    return im, d

def shadow_card(im, xy, r=28, fill=CARD, outline=None, ow=0):
    x0, y0, x1, y1 = xy
    sh = Image.new("RGBA", (W, H), (0,0,0,0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle([x0+6, y0+10, x1+6, y1+12], radius=r, fill=(80,70,140,60))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    im.paste(Image.alpha_composite(im.convert("RGBA"), sh).convert("RGB"), (0,0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=ow)
    return d

# ── 드로잉 아이콘(플랫) ──
def ic_school(d, cx, cy, s, col):
    d.polygon([(cx-s, cy-s*0.1), (cx, cy-s*0.7), (cx+s, cy-s*0.1)], fill=col)  # 지붕
    d.rounded_rectangle([cx-s*0.7, cy-s*0.1, cx+s*0.7, cy+s*0.7], radius=8, fill=col)
    d.rectangle([cx-s*0.15, cy+s*0.25, cx+s*0.15, cy+s*0.7], fill=CARD)  # 문
def ic_book(d, cx, cy, s, col):
    d.rounded_rectangle([cx-s*0.7, cy-s*0.55, cx+s*0.7, cy+s*0.55], radius=8, fill=col)
    d.line([(cx, cy-s*0.5), (cx, cy+s*0.5)], fill=CARD, width=5)
    d.line([(cx-s*0.4, cy-s*0.15), (cx-s*0.15, cy-s*0.15)], fill=CARD, width=4)
def ic_check(d, cx, cy, s, col):
    d.ellipse([cx-s*0.7, cy-s*0.7, cx+s*0.7, cy+s*0.7], fill=col)
    d.line([(cx-s*0.28, cy), (cx-s*0.05, cy+s*0.28), (cx+s*0.35, cy-s*0.3)], fill=CARD, width=9, joint="curve")
def ic_shield(d, cx, cy, s, col):
    d.polygon([(cx, cy-s*0.7), (cx+s*0.6, cy-s*0.4), (cx+s*0.6, cy+s*0.2),
               (cx, cy+s*0.7), (cx-s*0.6, cy+s*0.2), (cx-s*0.6, cy-s*0.4)], fill=col)
    d.line([(cx-s*0.2, cy), (cx-s*0.02, cy+s*0.22), (cx+s*0.3, cy-s*0.2)], fill=CARD, width=7, joint="curve")
def ic_tablet(d, cx, cy, s, col):
    d.rounded_rectangle([cx-s*0.5, cy-s*0.68, cx+s*0.5, cy+s*0.68], radius=10, fill=col)
    d.rounded_rectangle([cx-s*0.36, cy-s*0.52, cx+s*0.36, cy+s*0.42], radius=5, fill=CARD)
    d.ellipse([cx-s*0.06, cy+s*0.5, cx+s*0.06, cy+s*0.62], fill=CARD)
def ic_spark(d, cx, cy, s, col):  # AI 반짝
    pts = []
    for i in range(8):
        ang = math.pi/4*i
        rr = s*0.7 if i % 2 == 0 else s*0.28
        pts.append((cx+rr*math.cos(ang), cy+rr*math.sin(ang)))
    d.polygon(pts, fill=col)
def ic_caution(d, cx, cy, s, col):
    d.polygon([(cx, cy-s*0.7), (cx+s*0.75, cy+s*0.55), (cx-s*0.75, cy+s*0.55)], fill=col)
    d.line([(cx, cy-s*0.25), (cx, cy+s*0.15)], fill=CARD, width=9)
    d.ellipse([cx-6, cy+s*0.28, cx+6, cy+s*0.4], fill=CARD)
def ic_bubble(d, cx, cy, s, col):
    d.rounded_rectangle([cx-s*0.8, cy-s*0.55, cx+s*0.8, cy+s*0.35], radius=16, fill=col)
    d.polygon([(cx-s*0.3, cy+s*0.3), (cx-s*0.5, cy+s*0.62), (cx-s*0.05, cy+s*0.32)], fill=col)
    for i in range(3):
        d.ellipse([cx-s*0.35+i*s*0.32, cy-s*0.18, cx-s*0.2+i*s*0.32, cy-s*0.03], fill=CARD)
def ic_person(d, cx, cy, s, col):
    d.ellipse([cx-s*0.28, cy-s*0.6, cx+s*0.28, cy-s*0.04], fill=col)  # head
    d.rounded_rectangle([cx-s*0.5, cy+s*0.05, cx+s*0.5, cy+s*0.7], radius=20, fill=col)  # body

def label_pill(d, cx, cy, text, col):
    f = F(KB, 30)
    tb = d.textbbox((0,0), text, font=f); tw = tb[2]-tb[0]
    d.rounded_rectangle([cx-tw/2-18, cy-24, cx+tw/2+18, cy+24], radius=22, fill=col)
    d.text((cx-tw/2, cy-20), text, font=f, fill=CARD)

def tiny_tag(d, cx, cy, text, col):
    f = F(KB, 26)
    tb = d.textbbox((0,0), text, font=f); tw = tb[2]-tb[0]
    d.rounded_rectangle([cx-tw/2-14, cy-18, cx+tw/2+14, cy+18], radius=16, fill=(245,244,250))
    d.text((cx-tw/2, cy-15), text, font=f, fill=col)

def save(im, name):
    os.makedirs(OUT, exist_ok=True)
    im.convert("RGB").save(os.path.join(OUT, name))
    print("saved", name)

# ── 세계지도(추상 블롭) ──
def draw_map(d, alpha=70):
    blobs = [ (520,430,190,120),(720,400,120,90),(1080,470,240,150),(1250,430,120,90),
              (1420,560,150,110),(600,650,150,90),(1150,700,130,80) ]
    for (x,y,rw,rh) in blobs:
        d.ellipse([x-rw, y-rh, x+rw, y+rh], fill=(190,186,220,alpha))

# ── IMG-01 오프닝: 지도 + 5개국 카드 ──
def img01():
    im, d = bg()
    draw_map(d)
    cards = [("school",PUR),("book",BLUE),("check",GREEN),("shield",ORG),("tablet",(90,73,214))]
    icons = {"school":ic_school,"book":ic_book,"check":ic_check,"shield":ic_shield,"tablet":ic_tablet}
    pos = [(430,300),(760,240),(1090,300),(1400,250),(1560,470)]
    d2 = ImageDraw.Draw(im)
    for (name,col),(x,y) in zip(cards,pos):
        shadow_card(im, [x-95,y-95,x+95,y+95], r=26)
        dd = ImageDraw.Draw(im)
        icons[name](dd, x, y-8, 78, col)
    save(im, "IMG-01-opening-map.png")

# ── IMG-02 부모 질문: 5카드 한 줄 + 질문 모티프 ──
def img02():
    im, d = bg()
    # 상단 질문 모티프(부모+아이 + 물음표)
    ic_person(d, 820, 300, 110, PUR)
    ic_person(d, 980, 330, 80, BLUE)
    d.text((1080, 210), "?", font=F(KB, 200), fill=(124,108,255))
    # 5개국 카드 한 줄
    names = [("school",PUR),("book",BLUE),("check",GREEN),("shield",ORG),("tablet",(90,73,214))]
    icons = {"school":ic_school,"book":ic_book,"check":ic_check,"shield":ic_shield,"tablet":ic_tablet}
    n=5; cw=250; gap=40; x0=(W-(cw*n+gap*(n-1)))//2; y=740
    for i,(name,col) in enumerate(names):
        x=x0+i*(cw+gap)
        shadow_card(im, [x, y, x+cw, y+230], r=24)
        dd=ImageDraw.Draw(im); icons[name](dd, x+cw/2, y+115, 82, col)
    save(im, "IMG-02-parent-question.png")

# ── IMG-03 중국 교실: 칠판 + AI 반짝 + 책상 ──
def img03():
    im, d = bg()
    # 칠판
    shadow_card(im, [560, 210, 1360, 560], r=22, fill=(28,92,66))
    dd = ImageDraw.Draw(im)
    ic_spark(dd, 960, 330, 90, (255, 214, 122))
    dd.line([(720,470),(1200,470)], fill=(180,214,196), width=6)
    dd.line([(760,510),(1080,510)], fill=(180,214,196), width=6)
    # 책상 3개
    for x in (700, 960, 1220):
        shadow_card(im, [x-110, 720, x+110, 860], r=18, fill=CARD)
        d3 = ImageDraw.Draw(im); ic_person(d3, x, 700, 70, (200,196,224))
    save(im, "IMG-03-china-classroom.png")

# ── IMG-04 중국 가드레일: AI + 경고 + 태그 ──
def img04():
    im, d = bg()
    shadow_card(im, [560, 300, 1360, 780], r=30)
    dd = ImageDraw.Draw(im)
    ic_spark(dd, 780, 540, 120, PUR)
    ic_caution(dd, 1120, 540, 130, (224, 168, 60))
    dd.line([(910,540),(1010,540)], fill=SOFT, width=10)
    tiny_tag(dd, 1000, 720, "표절", ORG)
    tiny_tag(dd, 1130, 720, "과의존", ORG)
    save(im, "IMG-04-china-guardrail.png")

if __name__ == "__main__":
    img01(); img02(); img03(); img04()
    print("batch1 (IMG-01~04) done")
