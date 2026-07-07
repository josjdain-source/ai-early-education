#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""교육↔현실직업 3부작 쇼츠 빌더 — 플랜=ai_jobs_series_plan.json (S10_edu_to_jobs).
build_re100_short 계열(풀블리드·초대형 헤드·느린 줌인·InJoon). 완료 시 8971 자동 등록(private).
사용: python build_ai_jobs_series.py            (전체 3편)
      python build_ai_jobs_series.py jobs-10x-market   (한 편만)"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
PLAN=json.load(open(f"{HERE}/ai_jobs_series_plan.json",encoding="utf-8"))
SPEED=PLAN.get("speed",1.4); TAIL=2.0; BRAND=PLAN.get("brand","AI 시대 리포트")
STYLE=PLAN["style_token"]; NEG=PLAN["negative"]; SERIES=PLAN.get("series","S10_edu_to_jobs")
A=f"{REPO}/assets/ai-jobs-series"; RENDER=f"{A}/render"; IMG=f"{A}/simg"; FR=f"{A}/sframe"; AUD=f"{A}/saud"
for d in (RENDER,IMG,FR,AUD): os.makedirs(d,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())
def tts(text,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([VENV,os.path.join(HERE,"_tts_param.py"),tf,out,"ko-KR-InJoonNeural","+0%","+0Hz"])
def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1024,"height":1024,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"jobsSH","images":["8",0]}}}
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
def _stroke(d,pos,text,font,fill,sw=5,scol=(0,0,0)):
    x,y=pos
    for dx in range(-sw,sw+1,2):
        for dy in range(-sw,sw+1,2):
            if dx or dy: d.text((x+dx,y+dy),text,font=font,fill=scol)
    d.text((x,y),text,font=font,fill=fill)
def frame(chip,head,caption,img,role,idx,n,out):
    W,H=1080,1920
    src=Image.open(img).convert("RGB")
    r=max(W/src.width,H/src.height); card=src.resize((int(src.width*r),int(src.height*r)))
    ox=(card.width-W)//2; oy=(card.height-H)//2; card=card.crop((ox,oy,ox+W,oy+H))
    im=card.convert("RGBA")
    scr=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(scr)
    th=int(H*0.46)
    for i in range(th): sd.line([(0,i),(W,i)],fill=(8,11,20,int(165*(1-i/th))))
    bh=int(H*0.52)
    for i in range(bh): sd.line([(0,H-1-i),(W,H-1-i)],fill=(6,9,16,int(205*(1-i/bh))))
    im=Image.alpha_composite(im,scr); d=ImageDraw.Draw(im)
    cf=F(KB,34); cw=d.textlength(chip,font=cf); px=26
    d.rounded_rectangle([(W-cw)/2-px,54,(W+cw)/2+px,54+56],radius=28,fill=(40,90,150,240))
    d.text(((W-cw)/2,66),chip,font=cf,fill=(255,255,255))
    col=(255,206,92) if role in ("hook","cta") else (255,255,255)
    hs=132; hf=F(KB,hs); lines=wrap(d,head,hf,W-96)
    while (len(lines)>2 or (lines and max(d.textlength(l,font=hf) for l in lines)>W-96)) and hs>60:
        hs-=6; hf=F(KB,hs); lines=wrap(d,head,hf,W-96)
    yy=210
    for ln in lines:
        lw=d.textlength(ln,font=hf); _stroke(d,((W-lw)/2,yy),ln,hf,col,6); yy+=hs+8
    sf=F(KB,56); slines=wrap(d,caption,sf,W-96)
    while len(slines)>3 and sf.size>38: sf=F(KB,sf.size-3); slines=wrap(d,caption,sf,W-96)
    ty=H-150-len(slines)*(sf.size+14)
    for ln in slines:
        lw=d.textlength(ln,font=sf); _stroke(d,((W-lw)/2,ty),ln,sf,(255,255,255),4); ty+=sf.size+14
    dotw=20; tot=n*dotw+(n-1)*13; sx=(W-tot)//2
    for i in range(n):
        d.ellipse([sx+i*(dotw+13),H-64,sx+i*(dotw+13)+dotw,H-64+dotw],fill=(255,206,92) if i==idx else (255,255,255,110))
    im.convert("RGB").save(out)

def register_to_studio(sh, mp4, poster):
    QF=os.path.join(REPO,"youtube","upload_queue.json")
    try: q=json.load(open(QF,encoding="utf-8"))
    except Exception: return
    vid=sh["id"]
    rel=os.path.relpath(mp4,REPO).replace("\\","/"); prel=os.path.relpath(poster,REPO).replace("\\","/") if poster else ""
    desc=(chr(10)+chr(10)).join(sh["desc_lines"])
    entry={"video_id":vid,"title":sh["final_title"],"video_type":"short",
           "series":SERIES,"mp4_path":rel,"poster_path":prel,"thumbnail_path":prel,
           "tags":sh.get("tags",[]),"shorts":True,"category":"27",
           "status":"ready_to_upload","upload_status":"ready_to_upload","public":False,"public_status":"none",
           "youtube_id":"","youtube_url":"","created_at":"2026-07-07","description":desc,
           "source":"production/ai_jobs_series_plan.json","note":"교육↔직업 연결 3부작. 발언 인용 원칙·인물 언급 없음. 업로드는 사람 승인."}
    for i,it in enumerate(q["queue"]):
        if it.get("video_id")==vid: q["queue"][i]={**it,**entry}; break
    else: q["queue"].append(entry)
    json.dump(q,open(QF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"  → 스튜디오(8971) 등록: {vid}")
    print("  desc 첫줄:", desc.split(chr(10))[0][:56])

def build_one(sh, base_seed):
    key=sh["id"]; beats=sh["beats"]; n=len(beats); XF=0.25
    spd=sh.get("speed", SPEED)  # 쇼츠별 속도 오버라이드
    segs=[]; auds=[]; beat_d=[]
    for bi,bt in enumerate(beats):
        raw=f"{AUD}/{key}_{bi}_raw.mp3"; tts(bt["text"],raw)
        ap=f"{AUD}/{key}_{bi}.mp3"
        run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={spd}",ap])
        auds.append(ap); bd=dur(ap); beat_d.append(bd)
        ip=f"{IMG}/{key}_{bi}.png"
        if not os.path.exists(ip): sdxl(bt["prompt"],base_seed+bi,ip)
        fp=f"{FR}/{key}_{bi}.png"; frame(BRAND,bt["head"],bt["text"],ip,bt["role"],bi,n,fp)
        seg=f"{FR}/v_{key}_{bi}.mp4"
        D=int((bd+XF)*30)+2
        z="min(1.0+0.00033*on,1.06)"
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
    args+=["-c:v","libx264","-preset","veryfast","-crf","20","-r","30",f"{FR}/_v_{key}.mp4"]; run(args)
    al=f"{FR}/_a_{key}.txt"; open(al,"w",encoding="utf-8").write(chr(10).join(f"file '{a}'" for a in auds))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",f"{FR}/_a_{key}.mp3"])
    out=f"{RENDER}/{key}.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{FR}/_v_{key}.mp4","-i",f"{FR}/_a_{key}.mp3",
         "-filter_complex",f"[1:a]apad=pad_dur={TAIL}[a]","-map","0:v","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    poster=f"{RENDER}/{key}-poster.jpg"
    try: run([FF,"-hide_banner","-loglevel","error","-y","-ss","1","-i",out,"-frames:v","1","-q:v","3",poster])
    except Exception: poster=""
    print(f"쇼츠 완성: {key} {dur(out):.1f}s -> {out}")
    register_to_studio(sh, out, poster if poster and os.path.exists(poster) else "")
    return out

if __name__=="__main__":
    only=sys.argv[1] if len(sys.argv)>1 else None
    for si,sh in enumerate(PLAN["shorts"]):
        if only and sh["id"]!=only: continue
        build_one(sh, 8300+si*20)
