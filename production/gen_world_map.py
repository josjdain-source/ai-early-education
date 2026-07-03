#!/usr/bin/env python3
"""프리미엄 어두운 세계지도(대륙 단순 폴리곤 + 5개국 글로우 마커). 2560x1440(줌인용 고해상).
등장방식: 국경 데이터(geopandas) 없어 대륙 윤곽을 단순 폴리곤으로 직접 그림 — '실제로 그 나라로 가는' 줌 배경용."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
KB=r"C:\Windows\Fonts\malgunbd.ttf"
OUT="assets/world-ai-education-5min/map"
W,H=2560,1440
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def proj(lon,lat):
    return ((lon+180)/360*W, (90-lat)/180*H)

# 단순화한 대륙 윤곽(lon,lat) — 인식 가능한 수준
CONT = {
 "N.America":[(-168,66),(-160,71),(-130,70),(-95,69),(-82,73),(-60,60),(-55,52),(-70,45),(-80,26),(-97,18),(-105,23),(-115,30),(-125,40),(-130,55),(-168,66)],
 "S.America":[(-81,8),(-60,10),(-50,0),(-35,-8),(-40,-23),(-55,-35),(-65,-45),(-73,-52),(-72,-40),(-70,-20),(-80,-5),(-81,8)],
 "Europe":[(-10,44),(-9,52),(-5,58),(5,60),(15,68),(28,70),(40,66),(45,55),(40,47),(28,40),(15,38),(2,42),(-10,44)],
 "Africa":[(-16,26),(-5,34),(10,37),(32,32),(43,12),(51,12),(40,-5),(38,-18),(25,-34),(18,-34),(12,-18),(8,4),(-8,10),(-16,26)],
 "Asia":[(26,40),(45,42),(50,55),(60,72),(100,78),(140,72),(160,68),(145,55),(135,45),(122,40),(120,30),(108,20),(95,20),(98,8),(80,8),(70,22),(58,25),(45,38),(26,40)],
 "SEAsia":[(95,6),(105,2),(118,-2),(130,-6),(140,-8),(120,-10),(105,-8),(98,0),(95,6)],
 "Australia":[(114,-22),(130,-12),(142,-11),(150,-25),(150,-38),(138,-38),(128,-32),(115,-34),(114,-22)],
}
COUNTRIES=[("중국",104,35,(230,70,80)),("미국",-98,39,(70,120,210)),
           ("영국",-2,54,(90,110,180)),("싱가포르",103.8,1.3,(230,110,70)),("한국",127.5,37,(70,140,210))]

def build():
    os.makedirs(OUT,exist_ok=True)
    im=Image.new("RGB",(W,H),(11,13,24)); d=ImageDraw.Draw(im,"RGBA")
    # 배경 그라데이션 + 위도경도 그리드
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=(11+int(8*t),13+int(11*t),24+int(24*t)))
    for lon in range(-180,181,30):
        x=proj(lon,0)[0]; d.line([(x,0),(x,H)],fill=(255,255,255,10))
    for lat in range(-60,91,30):
        y=proj(0,lat)[1]; d.line([(0,y),(W,y)],fill=(255,255,255,10))
    # 대륙(글로우 → 채움 → 외곽)
    glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    for name,pts in CONT.items():
        xy=[proj(a,b) for a,b in pts]
        gd.polygon(xy,fill=(90,120,190,120))
    glow=glow.filter(ImageFilter.GaussianBlur(18)); im=Image.alpha_composite(im.convert("RGBA"),glow)
    d=ImageDraw.Draw(im,"RGBA")
    for name,pts in CONT.items():
        xy=[proj(a,b) for a,b in pts]
        d.polygon(xy,fill=(46,60,96,255),outline=(120,150,210,220))
    # 국가 마커(글로우 점 + 라벨)
    for name,lon,lat,c in COUNTRIES:
        x,y=proj(lon,lat)
        for r,al in ((34,50),(22,90),(12,230)):
            d.ellipse([x-r,y-r,x+r,y+r],fill=(c[0],c[1],c[2],al))
        d.ellipse([x-6,y-6,x+6,y+6],fill=(255,255,255,255))
        f=F(40); tw=d.textlength(name,font=f)
        d.rounded_rectangle([x-tw/2-14,y+18,x+tw/2+14,y+74],radius=16,fill=(15,17,30,220))
        d.text((x-tw/2,y+26),name,font=f,fill=(240,244,255,255))
    im.convert("RGB").save(os.path.join(OUT,"world-map-base.png"))
    print("world map saved 2560x1440 ·", OUT)

if __name__=="__main__":
    build()
