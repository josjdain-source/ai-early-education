#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""광주 반도체 55초 쇼츠 — 숫자 대비(평택 vs 광주). build_ai_edu_shorts 계열(세로 1080x1920). 속도 1.2.
플랜=gwangju_semi_short_plan.json. 숫자는 자막으로만(이미지 NEG 차단). 완료 시 8971 자동 등록(private)."""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont
SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
PLAN=json.load(open(f"{HERE}/gwangju_semi_short_plan.json",encoding="utf-8"))
KEY=PLAN["id"]; SPEED=PLAN.get("speed",1.2); TAIL=2.0; BRAND=PLAN.get("brand","광주 반도체 시나리오")
STYLE=PLAN["style_token"]; NEG=PLAN["negative"]
A=f"{REPO}/assets/gwangju-semi"; RENDER=f"{A}/render"; IMG=f"{A}/simg"; FR=f"{A}/sframe"; AUD=f"{A}/saud"
for d in (RENDER,IMG,FR,AUD): os.makedirs(d,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"
CREAM=(244,242,236); NAVY=(30,44,66); BLUE=(40,90,150); GOLD=(196,140,50); INK=(40,44,54); PAPER=(255,253,248)
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
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"gjSH","images":["8",0]}}}
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
    d.rounded_rectangle([(W-cw)/2-px,70,(W+cw)/2+px,70+58],radius=29,fill=BLUE)
    d.text(((W-cw)/2,82),chip,font=cf,fill=(255,255,255))
    hs=88 if role in ("hook","cta") else 78; hf=F(KB,hs)
    lines=wrap(d,head,hf,W-150)
    while len(lines)>2 and hs>44: hs-=4; hf=F(KB,hs); lines=wrap(d,head,hf,W-150)
    y=180
    for ln in lines:
        lw=d.textlength(ln,font=hf); col=GOLD if role in ("hook","cta") else NAVY
        d.text(((W-lw)/2,y),ln,font=hf,fill=col); y+=hs+8
    cx0,cy0,cx1,cy1=60,470,1020,1290
    card=Image.open(img).convert("RGB"); cw2,ch2=cx1-cx0,cy1-cy0
    r=max(cw2/card.width,ch2/card.height); card=card.resize((int(card.width*r),int(card.height*r)))
    card=card.crop(((card.width-cw2)//2,(card.height-ch2)//2,(card.width-cw2)//2+cw2,(card.height-ch2)//2+ch2))
    mask=Image.new("L",(cw2,ch2),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,cw2,ch2],radius=28,fill=255)
    im.paste(card,(cx0,cy0),mask); d.rounded_rectangle([cx0,cy0,cx1,cy1],radius=28,outline=(30,44,66),width=5)
    d.rounded_rectangle([60,1360,1020,1810],radius=26,fill=PAPER,outline=(214,222,232),width=3)
    sf=F(KB,46); slines=wrap(d,caption,sf,860)
    while len(slines)>4 and sf.size>32: sf=F(KB,sf.size-2); slines=wrap(d,caption,sf,860)
    ty=1380+(430-len(slines)*(sf.size+14))//2
    for ln in slines:
        lw=d.textlength(ln,font=sf); d.text(((W-lw)/2,ty),ln,font=sf,fill=INK); ty+=sf.size+14
    dotw=22; tot=n*dotw+(n-1)*14; sx=(W-tot)//2
    for i in range(n):
        c=BLUE if i==idx else (210,216,224)
        d.ellipse([sx+i*(dotw+14),1850,sx+i*(dotw+14)+dotw,1872],fill=c)
    im.save(out)

def register_to_studio(mp4, poster):
    QF=os.path.join(REPO,"youtube","upload_queue.json")
    try: q=json.load(open(QF,encoding="utf-8"))
    except Exception: return
    vid="gwangju-semi-short"
    rel=os.path.relpath(mp4,REPO).replace("\\","/"); prel=os.path.relpath(poster,REPO).replace("\\","/") if poster else ""
    desc=("평택은 반도체로 지역총생산이 2배가 됐습니다. 광주 군공항 반도체 클러스터가 성공하면? 숫자로 본 긍정 시나리오. "
          "★공식 예측 아님. 수치는 보도·통계+가정.\\n\\n#광주 #반도체 #평택 #군공항 #지역경제 #Shorts")
    entry={"video_id":vid,"title":PLAN.get("final_title","평택은 반도체로 2배 커졌다, 광주 군공항은?"),"video_type":"short",
           "series":"S08_region_scenario","mp4_path":rel,"poster_path":prel,"thumbnail_path":prel,
           "tags":["광주","반도체","평택","군공항","지역경제"],"shorts":True,"category":"25",
           "status":"ready_to_upload","upload_status":"ready_to_upload","public":False,"public_status":"none",
           "youtube_id":"","youtube_url":"","created_at":"2026-07-06","description":desc,
           "source":"production/gwangju_semi_short_plan.json","note":"긍정 시나리오·공식예측 아님. 업로드는 사람 승인."}
    for i,it in enumerate(q["queue"]):
        if it.get("video_id")==vid: q["queue"][i]={**it,**entry}; break
    else: q["queue"].append(entry)
    json.dump(q,open(QF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"  → 스튜디오(8971) 등록: {vid}")

if __name__=="__main__":
    beats=PLAN["beats"]; n=len(beats); XF=0.25
    segs=[]; auds=[]; beat_d=[]
    for bi,bt in enumerate(beats):
        raw=f"{AUD}/{KEY}_{bi}_raw.mp3"; tts(bt["text"],raw)
        ap=f"{AUD}/{KEY}_{bi}.mp3"
        run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={SPEED}",ap])
        auds.append(ap); bd=dur(ap); beat_d.append(bd)
        ip=f"{IMG}/{KEY}_{bi}.png"
        if not os.path.exists(ip): sdxl(bt["prompt"],7700+bi,ip)
        fp=f"{FR}/{KEY}_{bi}.png"; frame(BRAND,bt["head"],bt["text"],ip,bt["role"],bi,n,fp)
        seg=f"{FR}/v_{KEY}_{bi}.mp4"
        D=int((bd+XF)*30)+2
        z=("min(1.0+0.0007*on,1.10)" if bi%2==0 else "max(1.10-0.0007*on,1.0)")
        kb=f"scale=2160:3840,zoompan=z='{z}':d={D}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p"
        run([FF,"-hide_banner","-loglevel","error","-y","-i",fp,"-vf",kb,"-frames:v",str(D),"-c:v","libx264","-preset","veryfast","-crf","20","-r","30",seg])
        segs.append(seg)
    args=[FF,"-hide_banner","-loglevel","error","-y"]
    for s in segs: args+=["-i",s]
    chain=[]; prev="[0:v]"; cum=0.0
    for k in range(1,len(segs)):
        cum+=beat_d[k-1]; lbl=f"[vx{k}]"; chain.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cum:.3f}{lbl}"); prev=lbl
    if chain: args+=["-filter_complex",";".join(chain),"-map",prev]
    else: args+=["-map","0:v"]
    args+=["-c:v","libx264","-preset","veryfast","-crf","20","-r","30",f"{FR}/_v_{KEY}.mp4"]; run(args)
    al=f"{FR}/_a_{KEY}.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{a}'" for a in auds))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",f"{FR}/_a_{KEY}.mp3"])
    out=f"{RENDER}/{KEY}.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{FR}/_v_{KEY}.mp4","-i",f"{FR}/_a_{KEY}.mp3",
         "-filter_complex",f"[1:a]apad=pad_dur={TAIL}[a]","-map","0:v","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    poster=f"{RENDER}/{KEY}-poster.jpg"
    try: run([FF,"-hide_banner","-loglevel","error","-y","-ss","1","-i",out,"-frames:v","1","-q:v","3",poster])
    except Exception: poster=""
    print(f"쇼츠 완성: {dur(out):.1f}s -> {out}")
    register_to_studio(out, poster if poster and os.path.exists(poster) else "")
