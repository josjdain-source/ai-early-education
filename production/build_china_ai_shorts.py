#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""중국 AI교육 쇼츠 5편 빌드 — 플랜(china_ai_education_shorts_plan.json) 기반.
독립 후킹구조(hook/problem/fact/parent/cta). 1080x1920. 상단 큰 후킹문구·중앙 일러스트·하단 자막·빠른 디졸브.
산출: assets/china-ai-education/render/shorts/china-short-<s>.mp4"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
A=f"{REPO}/assets/china-ai-education"; RENDER=f"{A}/render/shorts"; IMG=f"{A}/simg"; FR=f"{A}/sframe"; AUD=f"{A}/saud"
for d in (RENDER,IMG,FR,AUD): os.makedirs(d,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
PLAN=json.load(open(f"{HERE}/china_ai_education_shorts_plan.json",encoding="utf-8")); STYLE=PLAN["style"]
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, chinese text, watermark, logo, "
 "surveillance camera, cctv, military, weapon, soldier, flag closeup, scary, dark, ugly, deformed, extra fingers, blurry")
CREAM=(251,246,238); NAVY=(43,58,85); CORAL=(232,120,90); INK=(51,64,90); PAPER=(255,253,248)
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
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1024,"height":1024,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"chinaSH","images":["8",0]}}}
    pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":uuid.uuid4().hex}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
    t0=time.time()
    while time.time()-t0<300:
        h=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
        if pid in h: break
        time.sleep(3)
    im=h[pid]["outputs"]["9"]["images"][0]
    q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
    open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read())
def wrap(d,text,font,maxw):
    out=[]; line=""
    for w in text.split():
        t=(line+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: line=t
        else:
            if line: out.append(line)
            line=w
    if line: out.append(line)
    return out
def frame(short_title,head,caption,img,role,idx,n,out):
    W,H=1080,1920; im=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(im)
    # 상단 타이틀 칩
    cf=F(KB,34); cw=d.textlength(short_title,font=cf); px=28
    d.rounded_rectangle([(W-cw)/2-px,70,(W+cw)/2+px,70+58],radius=29,fill=CORAL)
    d.text(((W-cw)/2,82),short_title,font=cf,fill=(255,255,255))
    # 상단 큰 후킹 문구(head)
    hs=76 if role=="hook" else 66; hf=F(KB,hs)
    lines=wrap(d,head,hf,W-150)
    while len(lines)>2 and hs>44: hs-=4; hf=F(KB,hs); lines=wrap(d,head,hf,W-150)
    y=180
    for ln in lines:
        lw=d.textlength(ln,font=hf); col=CORAL if role=="hook" else NAVY
        d.text(((W-lw)/2,y),ln,font=hf,fill=col); y+=hs+8
    # 중앙 일러스트 카드(커버 크롭)
    cx0,cy0,cx1,cy1=60,470,1020,1290
    card=Image.open(img).convert("RGB"); cw2,ch2=cx1-cx0,cy1-cy0
    r=max(cw2/card.width,ch2/card.height); card=card.resize((int(card.width*r),int(card.height*r)))
    card=card.crop(((card.width-cw2)//2,(card.height-ch2)//2,(card.width-cw2)//2+cw2,(card.height-ch2)//2+ch2))
    mask=Image.new("L",(cw2,ch2),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,cw2,ch2],radius=28,fill=255)
    im.paste(card,(cx0,cy0),mask); d.rounded_rectangle([cx0,cy0,cx1,cy1],radius=28,outline=(60,40,20),width=5)
    # 하단 자막 밴드
    d.rounded_rectangle([60,1360,1020,1810],radius=26,fill=PAPER,outline=(234,224,206),width=3)
    sf=F(KB,46); slines=wrap(d,caption,sf,860)
    while len(slines)>4 and sf.size>32: sf=F(KB,sf.size-2); slines=wrap(d,caption,sf,860)
    ty=1380+(430-len(slines)*(sf.size+14))//2
    for ln in slines:
        lw=d.textlength(ln,font=sf); d.text(((W-lw)/2,ty),ln,font=sf,fill=INK); ty+=sf.size+14
    # 진행 점
    dotw=22; tot=n*dotw+(n-1)*14; sx=(W-tot)//2
    for i in range(n):
        c=CORAL if i==idx else (222,210,190)
        d.ellipse([sx+i*(dotw+14),1850,sx+i*(dotw+14)+dotw,1872],fill=c)
    im.save(out)

if __name__=="__main__":
    only=sys.argv[1] if len(sys.argv)>1 else None
    for si,sh in enumerate(PLAN["shorts"]):
        if only and sh["key"]!=only: continue
        segs=[]; auds=[]; beat_d=[]; XF=0.3; n=len(sh["beats"])
        for bi,bt in enumerate(sh["beats"]):
            ap=f"{AUD}/{sh['key']}_{bi}.mp3"; tts(bt["text"],ap); auds.append(ap); bd=dur(ap); beat_d.append(bd)
            ip=f"{IMG}/{sh['key']}_{bi}.png"
            if not os.path.exists(ip): sdxl(bt["prompt"],7000+si*20+bi,ip)
            fp=f"{FR}/{sh['key']}_{bi}.png"; frame(sh["title"],bt["head"],bt["text"],ip,bt["role"],bi,n,fp)
            seg=f"{FR}/v_{sh['key']}_{bi}.mp4"
            run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",fp,"-t",f"{bd+XF}","-vf","format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","20","-r","30","-s","1080x1920",seg])
            segs.append(seg)
        # 디졸브 체인
        args=[FF,"-hide_banner","-loglevel","error","-y"]
        for s in segs: args+=["-i",s]
        chain=[]; prev="[0:v]"; cum=0.0
        for k in range(1,len(segs)):
            cum+=beat_d[k-1]; lbl=f"[vx{k}]"; chain.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cum:.3f}{lbl}"); prev=lbl
        args+=["-filter_complex",";".join(chain),"-map",prev,"-c:v","libx264","-preset","veryfast","-crf","20","-r","30",f"{FR}/_v_{sh['key']}.mp4"]; run(args)
        al=f"{FR}/_a_{sh['key']}.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{a}'" for a in auds))
        run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",f"{FR}/_a_{sh['key']}.mp3"])
        out=f"{RENDER}/china-short-{sh['key']}.mp4"
        run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{FR}/_v_{sh['key']}.mp4","-i",f"{FR}/_a_{sh['key']}.mp3",
             "-filter_complex","[1:a]apad=pad_dur=1.0[a]","-map","0:v","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
        print(f"쇼츠 {sh['key']}: {dur(out):.1f}s -> {out}")
