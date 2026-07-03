#!/usr/bin/env python3
"""증명 2단계: SDXL 일러스트에 Pillow로 한글 타이틀 배너+하단 자막+액자 프레임 오버레이(참고영상 포맷)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
OUT="assets/world-ai-education-5min/illust"
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()

def banner(d,cx,y,text,fs=52):
    f=F(KB,fs); tw=d.textlength(text,font=f); pad=40; h=fs+34
    x0,x1=cx-tw/2-pad,cx+tw/2+pad
    # 리본 끝 접힘
    d.polygon([(x0-28,y+h/2),(x0,y+6),(x0,y+h-6)],fill=(150,96,52))
    d.polygon([(x1+28,y+h/2),(x1,y+6),(x1,y+h-6)],fill=(150,96,52))
    d.rounded_rectangle([x0,y,x1,y+h],radius=14,fill=(245,232,205),outline=(150,96,52),width=4)
    d.text((cx-tw/2,y+15),text,font=f,fill=(60,40,20))

def caption(d,W,H,text,fs=46):
    f=F(KB,fs); tw=d.textlength(text,font=f); x=(W-tw)/2; y=H-fs-54
    for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]:
        d.text((x+dx,y+dy),text,font=f,fill=(0,0,0))
    d.text((x,y),text,font=f,fill=(255,255,255))

def frame_vignette(im):
    W,H=im.size; d=ImageDraw.Draw(im,"RGBA")
    b=18
    d.rectangle([0,0,W,b],fill=(30,20,14,230)); d.rectangle([0,H-b,W,H],fill=(30,20,14,230))
    d.rectangle([0,0,b,H],fill=(30,20,14,230)); d.rectangle([W-b,0,W,H],fill=(30,20,14,230))
    # 안쪽 소프트 섀도
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.rectangle([b,b,W-b,H-b],outline=(0,0,0,120),width=26)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    return im

if __name__=="__main__":
    im=Image.open(os.path.join(OUT,"aiedu-concept-raw.png")).convert("RGBA")
    W,H=im.size
    im=frame_vignette(im); d=ImageDraw.Draw(im,"RGBA")
    banner(d,W//2,40,"AI는 도구, 곁엔 사람")
    caption(d,W,H,"아이에게 물어봐 주세요 — \"이상한 부분, 찾아볼까?\"")
    im.convert("RGB").save(os.path.join(OUT,"aiedu-concept-final.png"))
    print("완성 ->",os.path.join(OUT,"aiedu-concept-final.png"))
