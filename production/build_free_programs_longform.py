#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""무료 프로그램 소개 롱폼 빌드 — 플랜(free_programs_longform_plan.json) 기반.
build_us_ai_longform 계열(1280x720, SDXL 일러스트+한글 오버레이+켄번즈+디졸브). 로고/텍스트 없음(NEG).
산출: assets/free-programs-longform/render/free-programs-longform.mp4. 완료 시 8971 스튜디오 자동 등록(private).
전제: Ollama 언로드 후 ComfyUI(8188). 사용: python build_free_programs_longform.py"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
A=f"{REPO}/assets/free-programs-longform"; RENDER=f"{A}/render"; IMG=f"{A}/img"; OVL=f"{A}/ovl"; AUD=f"{A}/audio"
for d in (RENDER,IMG,OVL,AUD): os.makedirs(d,exist_ok=True)
sys.path.insert(0,HERE); import reassemble_dissolve as RD
KB=r"C:\Windows\Fonts\malgunbd.ttf"
PLAN=json.load(open(f"{HERE}/free_programs_longform_plan.json",encoding="utf-8")); STYLE=PLAN["style"]
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, chinese text, watermark, logo, brand logo, ui screenshot, "
 "scary, dark, ugly, deformed, extra fingers, blurry, western caucasian people")
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
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"fpLF","images":["8",0]}}}
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

def register_to_studio(mp4, poster):
    """완성 롱폼을 8971 스튜디오(아이와 AI교실 채널)에 등록. private·ready_to_upload(자동 공개 없음)."""
    QF=os.path.join(REPO,"youtube","upload_queue.json")
    try: q=json.load(open(QF,encoding="utf-8"))
    except Exception: return
    vid="aiedu-free-programs-longform"
    rel=os.path.relpath(mp4,REPO).replace("\\","/"); prel=os.path.relpath(poster,REPO).replace("\\","/") if poster else ""
    desc=("아이와 AI교실이 콘텐츠 제작에 쓰는 무료·로컬 프로그램을 용도별로 소개합니다. "
          "TTS·영상 조립·이미지 생성·자막/오디오 편집·로컬 AI·개발 도구. 각 도구의 무료 범위·라이선스는 바뀔 수 있으니 공식 사이트를 확인하세요.\\n\\n"
          "전체 목록·링크 ▶ https://ai-early-education.pages.dev/free-programs\\n\\n#AI교육 #무료프로그램 #영상제작 #TTS")
    entry={"video_id":vid,"title":"아이와 AI교실이 쓰는 무료 프로그램 (제작 도구 총정리)","video_type":"longform",
           "series":"S07_free_programs","mp4_path":rel,"poster_path":prel,"thumbnail_path":prel,
           "tags":["AI교육","무료프로그램","영상제작","TTS","콘텐츠제작"],"shorts":False,"category":"27",
           "status":"ready_to_upload","upload_status":"ready_to_upload","public":False,"public_status":"none",
           "youtube_id":"","youtube_url":"","created_at":"2026-07-06","description":desc,
           "source":"production/free_programs_longform_plan.json","note":"무료 프로그램 소개 롱폼. 업로드는 사람 승인(자동 공개 금지)."}
    for i,it in enumerate(q["queue"]):
        if it.get("video_id")==vid: q["queue"][i]={**it,**entry}; break
    else: q["queue"].append(entry)
    json.dump(q,open(QF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"  → 스튜디오(8971) 등록: {vid}")

if __name__=="__main__":
    beats=[]; auds=[]; si=0
    for s in PLAN["sections"]:
        na=f"{AUD}/{s['key']}.mp3"; tts(s["narration"],na); auds.append(na)
        per=dur(na)/len(s["beats"]); title=s["title"]
        for bi,bt in enumerate(s["beats"]):
            ip=f"{IMG}/{s['key']}_{bi}.png"
            if not os.path.exists(ip): sdxl(bt["prompt"],9300+si*10+bi,ip)
            op=f"{OVL}/{s['key']}_{bi}.png"; overlay(title,bt["caption"],op)
            beats.append((ip,op,per))
        print(f" [{si+1}/{len(PLAN['sections'])}] {s['key']} {dur(na):.1f}s")
        si+=1
    out=f"{RENDER}/free-programs-longform.mp4"
    RD.assemble(beats,auds,out,f"{A}/_dtmp")
    poster=f"{RENDER}/free-programs-poster.jpg"
    try: run([FF,"-hide_banner","-loglevel","error","-y","-ss","3","-i",out,"-frames:v","1","-q:v","3",poster])
    except Exception: poster=""
    print("롱폼 완성:",round(dur(out),1),"s ->",out)
    register_to_studio(out, poster if poster and os.path.exists(poster) else "")
