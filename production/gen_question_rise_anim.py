#!/usr/bin/env python3
"""썸네일 '오늘, 아이에게' 말풍선의 물음표에 생동감:
큰 '?'가 밑에서 올라와(ease-out) 살짝 튕기고(overshoot bounce) 은은히 맥동.
프레임 PNG 시퀀스 → ffmpeg로 mp4+gif. 1280x720."""
import os, math
from PIL import Image, ImageDraw, ImageFont
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
W,H=1280,720
GOLD=(255,224,130); PUR=(124,108,255)
FR="C:/Users/admin/AppData/Local/Temp/claude/qrise"; os.makedirs(FR,exist_ok=True)
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()

def base():
    """썸네일 배경 재구성(말풍선 포함, 단 물음표는 애니로 따로 그림)."""
    im=Image.new("RGB",(W,H),(16,18,30)); d=ImageDraw.Draw(im,"RGBA")
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=(16+int(14*t),18+int(16*t),30+int(30*t)))
    for x,y,rw,rh in [(300,300,150,95),(430,270,95,70),(720,330,180,120),(880,300,95,70),(1000,420,120,90),(360,470,110,70)]:
        d.ellipse([x-rw,y-rh,x+rw,y+rh],fill=(60,80,130,50))
    pts=[(280,300),(640,260),(760,330),(900,300),(1010,400)]
    for i in range(len(pts)-1): d.line([pts[i],pts[i+1]],fill=(124,150,255,70),width=2)
    for x,y in pts: d.ellipse([x-7,y-7,x+7,y+7],fill=(150,180,255,220))
    d.rounded_rectangle([70,64,470,116],radius=26,fill=PUR)
    d.text((92,74),"세계 5개국 · AI 조기교육",font=F(KB,32),fill=(255,255,255))
    d.text((70,300),"AI를 맡기는 게 아니라",font=F(KB,84),fill=(255,255,255))
    d.text((70,400),"다시 묻는 힘",font=F(KB,110),fill=GOLD)
    # 말풍선(물음표 자리는 비워둠)
    bx0,by0,bx1,by1=830,470,1210,650
    d.rounded_rectangle([bx0,by0,bx1,by1],radius=24,fill=(255,255,255))
    d.polygon([(bx0+60,by1-6),(bx0+40,by1+40),(bx0+110,by1-6)],fill=(255,255,255))
    d.text((bx0+28,by0+26),"오늘, 아이에게",font=F(KB,30),fill=(90,73,214))
    d.text((bx0+28,by0+74),"\"AI 답에서 이상한",font=F(KF,32),fill=(36,36,51))
    d.text((bx0+28,by0+116),"부분 찾아볼까",font=F(KF,32),fill=(36,36,51))
    return im
BASE=base()
# 물음표 목표 위치(‘찾아볼까’ 끝, 말풍선 안 우측)
TX, TY = 1150, 118+470  # 말풍선 문장 라인 옆
def draw_q(im, cy, scale, alpha=255, glow=0):
    """(TX, cy) 중심에 물음표. scale=크기배율."""
    lay=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    fs=int(96*scale); f=F(KB,fs)
    q="?"; tw=d.textlength(q,font=f); asc=fs
    x=TX-tw/2; y=cy-fs*0.62
    if glow>0:
        for r in (glow, glow//2):
            d.text((x,y),q,font=f,fill=(255,224,130,60));
    # 외곽 소프트 그림자
    d.text((x+3,y+4),q,font=f,fill=(120,90,10,int(0.5*alpha)))
    d.text((x,y),q,font=f,fill=(255,206,90,alpha))
    im2=im.convert("RGBA"); im2.alpha_composite(lay); return im2.convert("RGB")

def ease_out_cubic(t): return 1-(1-t)**3
if __name__=="__main__":
    FPS=30
    frames=[]
    start_y=H+140; end_y=TY
    RISE=int(FPS*0.9)   # 0.9s 상승
    BOUNCE=int(FPS*0.45)
    HOLD=int(FPS*0.9)
    idx=0
    # 상승
    for i in range(RISE):
        t=ease_out_cubic(i/(RISE-1))
        cy=start_y+(end_y-start_y-26)*t  # 살짝 위로 오버슛(-26)
        sc=0.8+0.35*t
        f=draw_q(BASE,cy,sc,alpha=255); f.save(f"{FR}/f{idx:03d}.png"); idx+=1
    # 오버슛 되돌림 + 작은 바운스
    for i in range(BOUNCE):
        t=i/(BOUNCE-1)
        cy=end_y-26 + 26*math.sin(t*math.pi)  # 위→제자리 바운스
        sc=1.15-0.15*math.sin(t*math.pi)
        f=draw_q(BASE,cy,sc); f.save(f"{FR}/f{idx:03d}.png"); idx+=1
    # 맥동 홀드
    for i in range(HOLD):
        t=i/(HOLD-1)
        sc=1.0+0.05*math.sin(t*2*math.pi)
        f=draw_q(BASE,end_y,sc,glow=6); f.save(f"{FR}/f{idx:03d}.png"); idx+=1
    print("frames",idx,"→",FR)
