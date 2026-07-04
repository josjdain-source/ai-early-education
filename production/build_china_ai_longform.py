#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""중국 AI교육 롱폼(4~6분) 빌드 — 플랜(china_ai_education_longform_plan.json) 기반.
일러스트(SDXL)+한글 오버레이(줌 위 정적)+약한 켄번즈+디졸브. 1280x720. 섹션 내레이션 싱크.
산출: assets/china-ai-education/render/china-ai-education-longform.mp4"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
A=f"{REPO}/assets/china-ai-education"; RENDER=f"{A}/render"; IMG=f"{A}/img"; OVL=f"{A}/ovl"; AUD=f"{A}/audio"
for d in (RENDER,IMG,OVL,AUD): os.makedirs(d,exist_ok=True)
sys.path.insert(0,HERE); import reassemble_dissolve as RD
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
PLAN=json.load(open(f"{HERE}/china_ai_education_longform_plan.json",encoding="utf-8"))
STYLE=PLAN["style"]
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, chinese text, watermark, logo, "
 "surveillance camera, cctv, military, weapon, soldier, flag closeup, propaganda, scary, dark, ugly, deformed, extra fingers, blurry")
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())
def tts(text,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([VENV,os.path.join(HERE,"_tts_synth.py"),tf,out])
def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"chinaLF","images":["8",0]}}}
    pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":uuid.uuid4().hex}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
    t0=time.time()
    while time.time()-t0<300:
        h=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
        if pid in h: break
        time.sleep(3)
    im=h[pid]["outputs"]["9"]["images"][0]
    q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
    open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read())
def overlay(title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); b=16
    for r in [(0,0,W,b),(0,H-b,W,H),(0,0,b,H),(W-b,0,W,H)]: d.rectangle(r,fill=(28,18,12,235))
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle([b,b,W-b,H-b],outline=(0,0,0,120),width=22)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    fs=44; f=F(KB,fs)
    while d.textlength(title,font=f)>W-360 and fs>24: fs-=2; f=F(KB,fs)
    tw=d.textlength(title,font=f); cx=W//2; y=34; pad=34; h=fs+28; x0,x1=cx-tw/2-pad,cx+tw/2+pad
    d.polygon([(x0-24,y+h/2),(x0,y+6),(x0,y+h-6)],fill=(196,60,50)); d.polygon([(x1+24,y+h/2),(x1,y+6),(x1,y+h-6)],fill=(196,60,50))
    d.rounded_rectangle([x0,y,x1,y+h],radius=12,fill=(245,232,205),outline=(196,60,50),width=4); d.text((cx-tw/2,y+13),title,font=f,fill=(60,40,20))
    cfs=42; cf=F(KB,cfs)
    while d.textlength(caption,font=cf)>W-80 and cfs>22: cfs-=2; cf=F(KB,cfs)
    cw=d.textlength(caption,font=cf); cxx=(W-cw)/2; cyy=H-cfs-48
    for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]: d.text((cxx+dx,cyy+dy),caption,font=cf,fill=(0,0,0))
    d.text((cxx,cyy),caption,font=cf,fill=(255,255,255)); im.save(out)

if __name__=="__main__":
    beats=[]; auds=[]; si=0
    for s in PLAN["sections"]:
        na=f"{AUD}/{s['key']}.mp3"; tts(s["narration"],na); auds.append(na)
        per=dur(na)/len(s["beats"]); title=s["title"]
        for bi,bt in enumerate(s["beats"]):
            ip=f"{IMG}/{s['key']}_{bi}.png"
            if not os.path.exists(ip): sdxl(bt["prompt"],9100+si*10+bi,ip)
            op=f"{OVL}/{s['key']}_{bi}.png"; overlay(title,bt["caption"],op)
            beats.append((ip,op,per))
        print(f" [{si+1}/{len(PLAN['sections'])}] {s['key']} {dur(na):.1f}s")
        si+=1
    out=f"{RENDER}/china-ai-education-longform.mp4"
    RD.assemble(beats,auds,out,f"{A}/_dtmp")
    print("롱폼 완성:",dur(out),"s ->",out)
