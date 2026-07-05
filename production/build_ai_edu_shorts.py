#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""아이와 AI교실 쇼츠 빌더 — 콘텐츠 금고 패키지(content_bank/approved/shorts/*.json) 기반.
build_china_ai_shorts.py 계열(세로 1080x1920, 상단 후킹·중앙 일러스트·하단 자막·디졸브). 인물=한국인(kr).
엔진: 로컬 ComfyUI(SDXL RealVisXL_V5.0) + edge-tts + ffmpeg. 자동발행 없음 — mp4만 생성, 업로드는 사람.
사용: python build_ai_edu_shorts.py            (전체 4편)
      python build_ai_edu_shorts.py shorts-parent-001   (한 편만)
전제: Ollama 언로드 후 ComfyUI(8188) 실행."""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys, glob
from PIL import Image, ImageDraw, ImageFont
SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
PKG_DIR=os.path.join(REPO,"content_bank","approved","shorts")
A=f"{REPO}/assets/ai-edu-shorts"; RENDER=f"{A}/render"; IMG=f"{A}/simg"; FR=f"{A}/sframe"; AUD=f"{A}/saud"
for d in (RENDER,IMG,FR,AUD): os.makedirs(d,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"
SPEED=1.15; TAIL=2.0; BRAND="아이와 AI교실"
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, logo, "
 "western people, caucasian, european, american, white people, blonde hair, blue eyes, "
 "scary, dark, ugly, deformed, extra fingers, extra limbs, blurry")
CREAM=(251,246,238); NAVY=(43,58,85); CORAL=(232,120,90); INK=(51,64,90); PAPER=(255,253,248)
def eth(region):
    return ("Korean East Asian people, Korean children and parents, black hair, " if region=="kr"
            else "East Asian people, black hair, ")
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())
def tts(text,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([VENV,os.path.join(HERE,"_tts_synth.py"),tf,out])
def sdxl(scene,style,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1024,"height":1024,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+style,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"aieduSH","images":["8",0]}}}
    for attempt in range(3):
        try:
            pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":uuid.uuid4().hex}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
            t0=time.time(); ok=False
            while time.time()-t0<180:
                h=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
                if pid in h and h[pid].get("outputs"): ok=True; break
                time.sleep(3)
            if not ok: raise TimeoutError("comfy timeout")
            im=h[pid]["outputs"]["9"]["images"][0]
            q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
            open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read()); return
        except Exception as e:
            print(f"  [sdxl 재시도 {attempt+1}/3] {out}: {repr(e)[:60]}"); time.sleep(6)
    raise RuntimeError(f"sdxl 3회 실패: {out}")
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
def frame(chip,head,caption,img,role,idx,n,out):
    W,H=1080,1920; im=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(im)
    cf=F(KB,34); cw=d.textlength(chip,font=cf); px=28
    d.rounded_rectangle([(W-cw)/2-px,70,(W+cw)/2+px,70+58],radius=29,fill=CORAL)
    d.text(((W-cw)/2,82),chip,font=cf,fill=(255,255,255))
    hs=76 if role=="hook" else 66; hf=F(KB,hs)
    lines=wrap(d,head,hf,W-150)
    while len(lines)>2 and hs>44: hs-=4; hf=F(KB,hs); lines=wrap(d,head,hf,W-150)
    y=180
    for ln in lines:
        lw=d.textlength(ln,font=hf); col=CORAL if role in ("hook","cta") else NAVY
        d.text(((W-lw)/2,y),ln,font=hf,fill=col); y+=hs+8
    cx0,cy0,cx1,cy1=60,470,1020,1290
    card=Image.open(img).convert("RGB"); cw2,ch2=cx1-cx0,cy1-cy0
    r=max(cw2/card.width,ch2/card.height); card=card.resize((int(card.width*r),int(card.height*r)))
    card=card.crop(((card.width-cw2)//2,(card.height-ch2)//2,(card.width-cw2)//2+cw2,(card.height-ch2)//2+ch2))
    mask=Image.new("L",(cw2,ch2),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,cw2,ch2],radius=28,fill=255)
    im.paste(card,(cx0,cy0),mask); d.rounded_rectangle([cx0,cy0,cx1,cy1],radius=28,outline=(60,40,20),width=5)
    d.rounded_rectangle([60,1360,1020,1810],radius=26,fill=PAPER,outline=(234,224,206),width=3)
    sf=F(KB,46); slines=wrap(d,caption,sf,860)
    while len(slines)>4 and sf.size>32: sf=F(KB,sf.size-2); slines=wrap(d,caption,sf,860)
    ty=1380+(430-len(slines)*(sf.size+14))//2
    for ln in slines:
        lw=d.textlength(ln,font=sf); d.text(((W-lw)/2,ty),ln,font=sf,fill=INK); ty+=sf.size+14
    dotw=22; tot=n*dotw+(n-1)*14; sx=(W-tot)//2
    for i in range(n):
        c=CORAL if i==idx else (222,210,190)
        d.ellipse([sx+i*(dotw+14),1850,sx+i*(dotw+14)+dotw,1872],fill=c)
    im.save(out)

QF=os.path.join(REPO,"youtube","upload_queue.json")
def register_to_studio(pkg, mp4):
    """완성 mp4를 8971 영상 스튜디오(아이와 AI교실 채널=upload_queue)에 등록. 자동 공개/업로드 아님(ready_to_upload·public=False)."""
    try:
        q=json.load(open(QF,encoding="utf-8"))
    except Exception:
        return
    vid="aiedu-"+pkg["id"]
    rel=os.path.relpath(mp4,REPO).replace("\\","/")
    desc=pkg.get("description","")+"\n\n"+" ".join("#"+t for t in pkg.get("hashtags",[]))
    entry={"video_id":vid,"title":pkg.get("final_title",pkg["id"]),"video_type":"short",
           "series":pkg.get("series",""),"mp4_path":rel,"thumbnail_path":"",
           "status":"ready_to_upload","upload_status":"ready_to_upload","public":False,"public_status":"none",
           "youtube_id":"","youtube_url":"","created_at":"2026-07-06","description":desc,
           "source":f"content_bank/approved/shorts/{pkg['id']}.json",
           "note":"쇼츠 빌더 렌더본. 업로드는 사람 승인(자동 공개 금지)."}
    for i,it in enumerate(q["queue"]):
        if it.get("video_id")==vid: q["queue"][i]={**it,**entry}; break
    else: q["queue"].append(entry)
    json.dump(q,open(QF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"  → 스튜디오(8971 아이와 AI교실) 등록: {vid}")

def build_one(pkg):
    key=pkg["id"]; style=pkg["image_style"]["style_token"]; beats=pkg["beats"]; n=len(beats); XF=0.25
    segs=[]; auds=[]; beat_d=[]
    for bi,bt in enumerate(beats):
        raw=f"{AUD}/{key}_{bi}_raw.mp3"; tts(bt["text"],raw)
        ap=f"{AUD}/{key}_{bi}.mp3"
        run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={SPEED}",ap])
        auds.append(ap); bd=dur(ap); beat_d.append(bd)
        ip=f"{IMG}/{key}_{bi}.png"
        if not os.path.exists(ip): sdxl(eth(bt.get("region","kr"))+bt["prompt"],style,7300+bi,ip)
        fp=f"{FR}/{key}_{bi}.png"; frame(BRAND,bt["head"],bt["text"],ip,bt["role"],bi,n,fp)
        seg=f"{FR}/v_{key}_{bi}.mp4"
        run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",fp,"-t",f"{bd+XF}","-vf","format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","20","-r","30","-s","1080x1920",seg])
        segs.append(seg)
    args=[FF,"-hide_banner","-loglevel","error","-y"]
    for s in segs: args+=["-i",s]
    chain=[]; prev="[0:v]"; cum=0.0
    for k in range(1,len(segs)):
        cum+=beat_d[k-1]; lbl=f"[vx{k}]"; chain.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cum:.3f}{lbl}"); prev=lbl
    if chain: args+=["-filter_complex",";".join(chain),"-map",prev]
    else: args+=["-map","0:v"]
    args+=["-c:v","libx264","-preset","veryfast","-crf","20","-r","30",f"{FR}/_v_{key}.mp4"]; run(args)
    al=f"{FR}/_a_{key}.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{a}'" for a in auds))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",f"{FR}/_a_{key}.mp3"])
    out=f"{RENDER}/{key}.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{FR}/_v_{key}.mp4","-i",f"{FR}/_a_{key}.mp3",
         "-filter_complex",f"[1:a]apad=pad_dur={TAIL}[a]","-map","0:v","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    print(f"쇼츠 {key}: {dur(out):.1f}s -> {out}")
    register_to_studio(pkg, out)
    return out

if __name__=="__main__":
    only=sys.argv[1] if len(sys.argv)>1 else None
    files=sorted(glob.glob(f"{PKG_DIR}/*.json"))
    done=[]
    for f in files:
        pkg=json.load(open(f,encoding="utf-8"))
        if "beats" not in pkg: continue
        if only and pkg["id"]!=only: continue
        done.append(build_one(pkg))
    print(f"\n완료 {len(done)}편:", *("\n  "+d for d in done))
