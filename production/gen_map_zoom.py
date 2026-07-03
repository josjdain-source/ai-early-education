#!/usr/bin/env python3
"""세계지도 → 특정 나라로 빠르게 줌인(가는 느낌) 프레임 시퀀스.
사용: python gen_map_zoom.py <country_key>  (cn/us/uk/sg/kr)
2560x1440 base map에서 창(window)을 좁히며 나라 마커로 이동 → 1280x720 출력."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
KB=r"C:\Windows\Fonts\malgunbd.ttf"
MAP="assets/world-ai-education-5min/map/world-map-base.png"
MW,MH=2560,1440; OW,OH=1280,720
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def proj(lon,lat): return ((lon+180)/360*MW,(90-lat)/180*MH)
CO={"cn":("중국",104,35,(230,70,80)),"us":("미국",-98,39,(70,120,210)),
    "uk":("영국",-2,54,(90,110,180)),"sg":("싱가포르",103.8,1.3,(230,110,70)),
    "kr":("한국",127.5,37,(70,140,210))}
def ease(t): return t*t*(3-2*t)  # smoothstep

def gen(key, outdir, n=42):
    os.makedirs(outdir,exist_ok=True)
    base=Image.open(MAP).convert("RGB")
    name,lon,lat,c=CO[key]; cx,cy=proj(lon,lat)
    # 시작 창=전체, 끝 창=나라 근접(약 2.9x)
    sw,sh=MW,MH; ew,eh=int(MW/2.9),int(MH/2.9)
    scx,scy=MW/2,MH/2; ecx,ecy=cx,cy
    for i in range(n):
        t=ease(i/(n-1))
        w=sw+(ew-sw)*t; h=sh+(eh-sh)*t
        ccx=scx+(ecx-scx)*t; ccy=scy+(ecy-scy)*t
        # 창이 맵 밖으로 안 나가게 클램프
        ccx=max(w/2,min(MW-w/2,ccx)); ccy=max(h/2,min(MH-h/2,ccy))
        box=(ccx-w/2,ccy-h/2,ccx+w/2,ccy+h/2)
        fr=base.crop((int(box[0]),int(box[1]),int(box[2]),int(box[3]))).resize((OW,OH))
        # 도착 근처에서 마커 펄스 링
        if t>0.6:
            d=ImageDraw.Draw(fr,"RGBA")
            mx=(cx-box[0])/w*OW; my=(cy-box[1])/h*OH
            pr=(t-0.6)/0.4
            R=int(30+40*math.sin(pr*math.pi))
            d.ellipse([mx-R,my-R,mx+R,my+R],outline=(c[0],c[1],c[2],int(180*(1-pr)+40)),width=4)
        fr.save(f"{outdir}/z{i:03d}.png")
    return n

if __name__=="__main__":
    key=sys.argv[1] if len(sys.argv)>1 else "cn"
    outdir=f"C:/Users/admin/AppData/Local/Temp/claude/mapzoom_{key}"
    n=gen(key,outdir); print(f"{key}: {n} frames -> {outdir}")
