#!/usr/bin/env python3
"""데이터 모션 데모(참고영상 #6): 숫자 카운터 0→N% + 성장 막대. 프리미엄 딥네이비 톤. 1280x720.
※ 참고영상형 explainer의 핵심 부품 '되는가' 증명용. 실제 통계+출처 표기(수치 조작 금지)."""
import os, math
from PIL import Image, ImageDraw, ImageFont
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
W,H=1280,720; GOLD=(255,224,130); PUR=(124,108,255); WHITE=(245,247,255)
FR="C:/Users/admin/AppData/Local/Temp/claude/datamotion"; os.makedirs(FR,exist_ok=True)
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def ease(t): return 1-(1-t)**3

# 실제 통계: 싱가포르 교사의 약 3/4가 수업에 AI 활용(교사 AI 활용 국제 조사, 2024)
TARGET=75; KICK="싱가포르"; TITLE="교사의 AI 활용"
SUB="교사 4명 중 3명이 수업에 AI를 씁니다"
SRC="출처: 교사 AI 활용 국제 조사(2024) · 약 3/4"

def bg():
    im=Image.new("RGB",(W,H),(14,16,28)); d=ImageDraw.Draw(im,"RGBA")
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=(14+int(10*t),16+int(14*t),28+int(28*t)))
    for x,y,r in [(300,240,150),(950,300,150),(700,560,150)]:
        d.ellipse([x-r,y-r,x+r,y+r],fill=(60,80,140,35))
    return im
def frame(i,n):
    t=ease(min(1,i/(n*0.55)))  # 0.55구간에 카운트업, 이후 홀드
    val=TARGET*t
    im=bg(); d=ImageDraw.Draw(im,"RGBA")
    # 킥커
    f=F(KB,32); tw=d.textlength(KICK,font=f)
    d.rounded_rectangle([100,90,100+tw+44,144],radius=26,fill=(230,110,70)); d.text((122,100),KICK,font=f,fill=(255,255,255))
    d.text((100,170),TITLE,font=F(KB,54),fill=WHITE)
    # 큰 숫자 카운터
    num=f"{val:.0f}%"; d.text((100,250),num,font=F(KB,170),fill=GOLD)
    # 성장 막대
    bx0,by0,bx1,by1=100,470,1180,530
    d.rounded_rectangle([bx0,by0,bx1,by1],radius=30,fill=(40,46,72,255))
    ww=(bx1-bx0)*(val/100)
    d.rounded_rectangle([bx0,by0,bx0+max(60,ww),by1],radius=30,fill=(230,110,70,255))
    # 4명중 3명 아이콘(사람 픽토그램)
    for k in range(4):
        cx=120+k*70; col=(255,224,130) if (k< round(val/100*4)) else (90,95,120)
        d.ellipse([cx-14,560,cx+14,588],fill=col); d.rounded_rectangle([cx-18,592,cx+18,636],radius=14,fill=col)
    d.text((410,586),SUB,font=F(KF,32),fill=(210,214,230))
    d.text((100,662),SRC,font=F(KF,20),fill=(150,155,180))
    im.convert("RGB").save(f"{FR}/d{i:03d}.png")

if __name__=="__main__":
    N=90  # 3s @30fps
    for i in range(N): frame(i,N)
    print("frames",N,"->",FR)
