#!/usr/bin/env python3
"""구간별 '메시지 배경 카드'(어두운 미니다큐 톤). 썸네일 미학 재사용.
내레이션 핵심을 함축해 배경에 크게 깔아 화면+대화가 같이 살게. 1280x720."""
import os, math
from PIL import Image, ImageDraw, ImageFont
OUT="assets/world-ai-education-5min/premium-cards"
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
W,H=1280,720
GOLD=(255,224,130); PUR=(124,108,255); WHITE=(245,247,255); DIM=(150,165,205)
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()

def bg(accent):
    im=Image.new("RGB",(W,H),(14,16,28))
    for y in range(H):
        t=y/H; im.putpixel  # noop
    d=ImageDraw.Draw(im,"RGBA")
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=(14+int(a*t),16+int(b*t),28+int(c*t)))\
            if False else d.line([(0,y),(W,y)],fill=(14+int(10*t),16+int(14*t),28+int(28*t)))
    # 은은한 세계지도 블롭
    for x,y,rw,rh in [(300,250,170,105),(430,220,100,72),(760,300,190,120),(940,260,100,74),(1030,420,120,90)]:
        d.ellipse([x-rw,y-rh,x+rw,y+rh],fill=(60,80,140,45))
    # 5개국 연결점
    pts=[(280,250),(660,215),(780,300),(950,265),(1040,400)]
    for i in range(len(pts)-1): d.line([pts[i],pts[i+1]],fill=(124,150,255,55),width=2)
    for x,y in pts: d.ellipse([x-6,y-6,x+6,y+6],fill=(150,180,255,180))
    # accent 코너 글로우
    d.ellipse([-160,H-160,240,H+160],fill=(accent[0],accent[1],accent[2],28))
    return im,ImageDraw.Draw(im)

def kicker(d,t,accent):
    f=F(KB,32); tw=d.textlength(t,font=f)
    d.rounded_rectangle([70,70,70+tw+44,124],radius=26,fill=accent)
    d.text((92,80),t,font=f,fill=(255,255,255))

def card(name,kick,lines,accent,gold_idx=1):
    im,d=bg(accent); kicker(d,kick,accent)
    # 2줄 큰 카피(첫줄 흰, 둘째줄 골드 강조)
    y=300
    for i,ln in enumerate(lines):
        fs=88 if len(ln)<=13 else 74
        f=F(KB,fs); col=GOLD if i==gold_idx else WHITE
        d.text((72,y),ln,font=f,fill=col); y+=fs+18
    im.convert("RGB").save(os.path.join(OUT,name)); print("saved",name)

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True)
    card("00-opening.png","세계 5개국 · AI 조기교육",["세계는 아이에게 AI를","어떻게 가르칠까?"],PUR,gold_idx=1)
    card("01-china.png","중국",["학교 안으로 AI,","그래도 맡기진 않는다"],(200,70,80))
    card("02-usa.png","미국",["많이 쓰기가 아니라","이해·의심·고쳐 쓰는 힘"],(60,110,200))
    card("03-uk.png","영국",["AI는 도구,","판단은 사람"],(70,90,150))
    card("04-singapore.png","싱가포르",["쓰게 하되,","안전한 틀 안에서"],(210,90,70))
    card("05-korea.png","한국",["학교 도입과 아이 습관은 다르다","다시 묻기는 집에서"],(70,130,200),gold_idx=1)
    card("06-common.png","5개국 공통점",["AI를 막는 게 아니라","다루는 힘"],(20,150,110))
    card("07-conclusion.png","오늘, 우리 집",["정답이 아니라,","다시 묻는 힘"],PUR)
    print("done · 8 premium cards")
