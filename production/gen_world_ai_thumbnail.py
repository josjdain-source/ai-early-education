#!/usr/bin/env python3
"""세계 AI교육 본편 썸네일(1280x720). 어두운 배경+세계지도(추상)+아이 질문 카드. 부모용 미니 다큐 톤."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT="assets/world-ai-education-5min/thumbnail"
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
W,H=1280,720
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()

im=Image.new("RGB",(W,H),(16,18,30))
d=ImageDraw.Draw(im,"RGBA")
# 어두운 딥네이비 그라데이션
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=(16+int(14*t),18+int(16*t),30+int(30*t)))
# 은은한 세계지도(추상 대륙 블롭, 저채도)
blobs=[(300,300,150,95),(430,270,95,70),(720,330,180,120),(880,300,95,70),(1000,420,120,90),(360,470,110,70)]
for x,y,rw,rh in blobs:
    d.ellipse([x-rw,y-rh,x+rw,y+rh],fill=(60,80,130,50))
# 5개국 점(연결)
pts=[(280,300),(640,260),(760,330),(900,300),(1010,400)]
for i in range(len(pts)-1):
    d.line([pts[i],pts[i+1]],fill=(124,150,255,70),width=2)
for x,y in pts:
    d.ellipse([x-7,y-7,x+7,y+7],fill=(150,180,255,220))
# 상단 킥커
d.rounded_rectangle([70,64,470,116],radius=26,fill=(124,108,255))
d.text((92,74),"세계 5개국 · AI 조기교육",font=F(KB,32),fill=(255,255,255))
# 메인 카피(2줄, 크게)
d.text((70,300),"AI를 맡기는 게 아니라",font=F(KB,84),fill=(255,255,255))
d.text((70,400),"다시 묻는 힘",font=F(KB,110),fill=(255,224,130))
# 아이 질문 말풍선 카드(우하단)
bx0,by0,bx1,by1=830,470,1210,650
d.rounded_rectangle([bx0,by0,bx1,by1],radius=24,fill=(255,255,255))
d.polygon([(bx0+60,by1-6),(bx0+40,by1+40),(bx0+110,by1-6)],fill=(255,255,255))
d.text((bx0+28,by0+26),"오늘, 아이에게",font=F(KB,30),fill=(90,73,214))
d.text((bx0+28,by0+74),"\"AI 답에서 이상한",font=F(KF,34),fill=(36,36,51))
d.text((bx0+28,by0+118),"부분 찾아볼까?\"",font=F(KF,34),fill=(36,36,51))
# 국기 대신 5색 점 라벨(하단)
labels=[("중국",(200,60,70)),("미국",(50,90,180)),("영국",(40,70,120)),("싱가포르",(200,80,60)),("한국",(60,120,190))]
x=70
for name,c in labels:
    d.ellipse([x,676,x+18,694],fill=c); d.text((x+26,672),name,font=F(KB,26),fill=(200,205,225)); x+=int(F(KB,26).getlength(name))+70
im.convert("RGB").save(os.path.join(OUT,"world-ai-education-main-thumbnail.png"))
print("thumbnail saved")
