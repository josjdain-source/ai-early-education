#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""아이와 AI교실 채널 아트: 마스코트 로봇(SDXL) → 프로필(800x800)+배너(2048x1152, 안전영역 텍스트)."""
import json, time, uuid, os, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"; OUT=os.path.dirname(os.path.abspath(__file__))+"/branding"
os.makedirs(OUT,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def sdxl(prompt,neg,seed,w,h,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":w,"height":h,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":prompt,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":neg,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"chart","images":["8",0]}}}
    pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":uuid.uuid4().hex}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
    t0=time.time()
    while time.time()-t0<300:
        h2=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
        if pid in h2: break
        time.sleep(3)
    im=h2[pid]["outputs"]["9"]["images"][0]
    q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
    open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read())

STYLE="warm storybook editorial cartoon illustration, thick clean black outlines, semi-realistic, flat shading, soft warm lighting, cream background"
NEG="photo, text, letters, words, watermark, logo, ugly, deformed, extra fingers, blurry, scary, creepy, dark"

def build():
    robot=f"{OUT}/_mascot.png"
    print("마스코트 로봇 생성(SDXL)...")
    sdxl(f"a cute friendly educational white AI robot mascot with a warm smile and big friendly glowing eyes, waving hello, rounded body, {STYLE}, centered, simple warm cream background",NEG,20260705,1024,1024,robot)
    m=Image.open(robot).convert("RGB")
    # 프로필 800x800 (로봇 중앙, 크림 배경)
    prof=Image.new("RGB",(800,800),(251,240,222))
    r=m.resize((760,760)); prof.paste(r,(20,20))
    prof.save(f"{OUT}/profile.png"); print("profile.png 저장")
    # 배너 2048x1152
    W,H=2048,1152; ban=Image.new("RGB",(W,H),(251,240,222)); d=ImageDraw.Draw(ban,"RGBA")
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=(251-int(8*t),240-int(10*t),222-int(14*t)))
    for x,y,rr in [(320,300,260),(1750,850,300),(400,950,240)]:
        d.ellipse([x-rr,y-rr,x+rr,y+rr],fill=(232,120,90,26))
    # 마스코트 우측
    rm=m.resize((560,560)); ban.paste(rm,(1360,300))
    # 안전영역(중앙) 텍스트: x 406~1642, y 407~745
    d=ImageDraw.Draw(ban)
    d.rounded_rectangle([440,430,760,500],radius=34,fill=(232,120,90))
    d.text((470,445),"AI 조기교육",font=F(KB,38),fill=(255,255,255))
    d.text((440,520),"아이와 AI교실",font=F(KB,118),fill=(43,58,85))
    d.text((442,660),"결과물이 아니라 ",font=F(KB,46),fill=(58,75,107))
    w1=d.textlength("결과물이 아니라 ",font=F(KB,46))
    d.text((442+w1,660),"과정이 교육이다",font=F(KB,46),fill=(216,101,74))
    ban.save(f"{OUT}/banner.png"); print("banner.png 저장 (2048x1152, 안전영역 텍스트)")

if __name__=="__main__":
    build(); print("완료 →",OUT)
