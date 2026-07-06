#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""광주 군공항 반도체 시나리오 롱폼 — 평택 대비 긍정 시나리오(공식예측 아님). 속도 1.2.
build_free_programs_longform 계열(1280x720, SDXL 다큐 일러스트+한글오버레이+켄번즈+디졸브). 숫자는 자막으로만(이미지 NEG 차단).
산출: assets/gwangju-semi/render/gwangju-semi-longform.mp4. 완료 시 8971 자동 등록(private)."""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
A=f"{REPO}/assets/ai-talent"; RENDER=f"{A}/render"; IMG=f"{A}/img"; OVL=f"{A}/ovl"; AUD=f"{A}/audio"
for d in (RENDER,IMG,OVL,AUD): os.makedirs(d,exist_ok=True)
sys.path.insert(0,HERE); import reassemble_dissolve as RD
KB=r"C:\Windows\Fonts\malgunbd.ttf"
PLAN=json.load(open(f"{HERE}/ai_talent_longform_plan.json",encoding="utf-8")); STYLE=PLAN["style"]
SPEED=PLAN.get("speed",1.2)
NEG=("photo, photorealistic, 3d render, text, letters, words, numbers, korean text, watermark, logo, brand logo, ui screenshot, "
 "scary, dark, ugly, deformed, extra fingers, blurry, western caucasian people")
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())
def tts(text,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([VENV,os.path.join(HERE,"_tts_param.py"),tf,out,"ko-KR-InJoonNeural","+0%","+0Hz"])  # 울분/임팩트 확정 음성
def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"talentLF","images":["8",0]}}}
    for attempt in range(3):
        try:
            pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":uuid.uuid4().hex}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
            t0=time.time(); ok=False
            while time.time()-t0<300:
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
def overlay(title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); b=16
    for r in [(0,0,W,b),(0,H-b,W,H),(0,0,b,H),(W-b,0,W,H)]: d.rectangle(r,fill=(24,20,16,235))
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle([b,b,W-b,H-b],outline=(0,0,0,120),width=22)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    fs=44; f=F(KB,fs)
    while d.textlength(title,font=f)>W-360 and fs>24: fs-=2; f=F(KB,fs)
    tw=d.textlength(title,font=f); cx=W//2; y=34; pad=34; h=fs+28; x0,x1=cx-tw/2-pad,cx+tw/2+pad
    d.polygon([(x0-24,y+h/2),(x0,y+6),(x0,y+h-6)],fill=(40,90,150)); d.polygon([(x1+24,y+h/2),(x1,y+6),(x1,y+h-6)],fill=(40,90,150))
    d.rounded_rectangle([x0,y,x1,y+h],radius=12,fill=(240,236,226),outline=(40,90,150),width=4); d.text((cx-tw/2,y+13),title,font=f,fill=(30,44,66))
    cfs=44; cf=F(KB,cfs)
    while d.textlength(caption,font=cf)>W-70 and cfs>22: cfs-=2; cf=F(KB,cfs)
    cw=d.textlength(caption,font=cf); cxx=(W-cw)/2; cyy=H-cfs-46
    for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]: d.text((cxx+dx,cyy+dy),caption,font=cf,fill=(0,0,0))
    d.text((cxx,cyy),caption,font=cf,fill=(255,236,180)); im.save(out)

def register_to_studio(mp4, poster):
    QF=os.path.join(REPO,"youtube","upload_queue.json")
    try: q=json.load(open(QF,encoding="utf-8"))
    except Exception: return
    vid="ai-talent-longform"
    rel=os.path.relpath(mp4,REPO).replace("\\","/"); prel=os.path.relpath(poster,REPO).replace("\\","/") if poster else ""
    desc=("스펙 쌓아도 떨어지는 이유 — 기업이 사람을 뽑는 기준이 바뀌었습니다. 싱가포르 AIAP(실전 도제·90%+ 취업)·미국(포트폴리오=학위 49%·학위우선 6%·AI스킬 임금 +56%)·영국(기업이 등록금+월급·£32k). 공통 공식: 포트폴리오>학위, 활용>제작, 현장>강의, 도메인×AI. 고등학생·대학생이 오늘 할 일까지."
          +chr(10)+chr(10)+"🏆 공개 대회로 시작 https://ai-early-education.pages.dev/competitions"
          +chr(10)+chr(10)+"#AI취업 #포트폴리오 #미래직업 #AI교육")
    entry={"video_id":vid,"title":"기업이 뽑는 AI 인재 — 3개국에서 확인했다 (스펙이 아니라 증거다)","video_type":"longform",
           "series":"S10_edu_to_jobs","mp4_path":rel,"poster_path":prel,"thumbnail_path":prel,
           "tags":["AI취업","포트폴리오","미래직업","AI교육","도제"],"shorts":False,"category":"25",
           "status":"ready_to_upload","upload_status":"ready_to_upload","public":False,"public_status":"none",
           "youtube_id":"","youtube_url":"","created_at":"2026-07-07","description":desc,
           "source":"production/ai_talent_longform_plan.json","note":"3개국 실측(출처 있는 수치만). 인물·정당 없음. 업로드는 사람 승인."}
    for i,it in enumerate(q["queue"]):
        if it.get("video_id")==vid: q["queue"][i]={**it,**entry}; break
    else: q["queue"].append(entry)
    json.dump(q,open(QF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"  → 스튜디오(8971) 등록: {vid}")

if __name__=="__main__":
    beats=[]; auds=[]; si=0
    for s in PLAN["sections"]:
        raw=f"{AUD}/{s['key']}_raw.mp3"; tts(s["narration"],raw)
        na=f"{AUD}/{s['key']}.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={SPEED}",na])
        auds.append(na); per=dur(na)/len(s["beats"]); title=s["title"]
        for bi,bt in enumerate(s["beats"]):
            ip=f"{IMG}/{s['key']}_{bi}.png"
            if not os.path.exists(ip): sdxl(bt["prompt"],9500+si*10+bi,ip)
            op=f"{OVL}/{s['key']}_{bi}.png"; overlay(title,bt["caption"],op)
            beats.append((ip,op,per))
        print(f" [{si+1}/{len(PLAN['sections'])}] {s['key']} {dur(na):.1f}s")
        si+=1
    out=f"{RENDER}/ai-talent-longform.mp4"
    RD.assemble(beats,auds,out,f"{A}/_dtmp")
    poster=f"{RENDER}/ai-talent-poster.jpg"
    try: run([FF,"-hide_banner","-loglevel","error","-y","-ss","3","-i",out,"-frames:v","1","-q:v","3",poster])
    except Exception: poster=""
    print("롱폼 완성:",round(dur(out),1),"s ->",out)
    register_to_studio(out, poster if poster and os.path.exists(poster) else "")
