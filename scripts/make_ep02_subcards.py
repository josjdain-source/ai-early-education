#!/usr/bin/env python3
"""EP02 긴 정적 카드(C08/C10/C11) 순차 등장용 하위 카드 생성(1920x1080). 우리 자체 콘텐츠."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "assets/ai-early-education/video-episode-02-singapore/cards"
KB = r"C:\Windows\Fonts\malgunbd.ttf"; KF = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1920, 1080
LAV = (243, 240, 255); LBLUE = (238, 246, 255)
BLUE = (47, 107, 216); PUR = (124, 108, 255); GREEN = (10, 138, 74); ORANGE = (192, 81, 43)
INK = (31, 31, 40); GRAY = (120, 120, 140); DIM = (205, 205, 218)

def F(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()
def ctext(d, t, f, y, fill, w=W):
    bb = d.textbbox((0,0), t, font=f); d.text(((w-(bb[2]-bb[0]))/2, y), t, font=f, fill=fill)
def base(bg=LAV):
    im = Image.new("RGB",(W,H),bg); return im, ImageDraw.Draw(im)
def rr(d,xy,r,fill,outline=None,width=2): d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)
def save(im,n): im.save(os.path.join(OUT,n)); print("saved",n)

AGES = [("유아","상상하고 말하기",BLUE),("초등 저학년","함께 보고 다시 말하기",PUR),
        ("초등 고학년","비교하고 틀린 답 찾기",ORANGE),("중학생","출처와 윤리까지",GREEN)]

def c08(active):
    im,d=base(); ctext(d,"나이에 맞게, 어떻게 쓰냐",F(KB,78),70,INK)
    cw,gap=400,40; x0=(W-(cw*4+gap*3))//2
    for i,(a,b,c) in enumerate(AGES):
        x=x0+i*(cw+gap); on=(i==active)
        col=c if on else DIM; tcol=INK if on else DIM
        rr(d,[x,300,x+cw,820],28,(255,255,255),col,10 if on else 4)
        bb=d.textbbox((0,0),a,font=F(KB,50)); d.text((x+(cw-(bb[2]-bb[0]))/2,360),a,font=F(KB,50),fill=col)
        for j,line in enumerate([b] if len(b)<12 else b.split("·")):
            bb2=d.textbbox((0,0),line,font=F(KF,38)); d.text((x+(cw-(bb2[2]-bb2[0]))/2,500+j*58),line,font=F(KF,38),fill=tcol)
        if on: ctext(d,"▲",F(KB,54),830,c) if False else d.text((x+cw//2-16,835),"▲",font=F(KB,50),fill=c)
    ctext(d,"어릴수록 직접 사용보다 안내·보호 먼저",F(KF,44),920,GRAY)
    save(im,f"c08_step{active+1}.png")

def c10(stage):
    im,d=base(); ctext(d,"역할이 다른 거지, 빠져도 되는 게 아니다",F(KB,64),80,INK)
    s_on = stage in (0,2); h_on = stage in (1,2)
    rr(d,[180,300,900,820],32,(255,255,255),BLUE if s_on else DIM,10 if s_on else 4)
    rr(d,[1020,300,1740,820],32,(255,255,255),GREEN if h_on else DIM,10 if h_on else 4)
    d.text((240,360),"학교",font=F(KB,70),fill=BLUE if s_on else DIM)
    for i,t in enumerate(["제도","감독","평가"]): d.text((240,500+i*90),"· "+t,font=F(KF,52),fill=INK if s_on else DIM)
    d.text((1080,360),"가정",font=F(KB,70),fill=GREEN if h_on else DIM)
    for i,t in enumerate(["실험","약속","체크"]): d.text((1080,500+i*90),"· "+t,font=F(KF,52),fill=INK if h_on else DIM)
    if stage==2: ctext(d,"학교=제도·감독 / 가정=안전한 첫 경험",F(KB,46),900,PUR)
    else: ctext(d,("학교가 맡는 것" if stage==0 else "가정이 맡는 것"),F(KB,46),900,(BLUE if stage==0 else GREEN))
    save(im,f"c10_{['school','home','both'][stage]}.png")

ACTS=[("①","앱보다 나이별 시작 방식을 먼저",PUR),("②","혼자가 아니라 함께 쓰는 구조",BLUE),
      ("③","AI 답을 그대로 믿지 않고 다시 확인하는 습관",GREEN)]
def c11(upto):
    im,d=base(LBLUE); ctext(d,"한국 부모가 오늘 가져갈 세 가지",F(KB,74),80,INK)
    for i,(n,t,c) in enumerate(ACTS):
        y=300+i*220; on=(i<=upto)
        rr(d,[220,y,1700,y+180],28,(255,255,255),c if on else DIM,8 if on else 3)
        d.text((270,y+45),n,font=F(KB,90),fill=c if on else DIM)
        d.text((420,y+60),(t if on else "…"),font=F(KB,52),fill=INK if on else DIM)
    save(im,f"c11_{upto+1}.png")

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True)
    for i in range(4): c08(i)
    for i in range(3): c10(i)
    for i in range(3): c11(i)
    print("done")
