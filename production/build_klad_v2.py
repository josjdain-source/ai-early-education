#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""한국의 잃어버린 AI 10년 v2 — 격정 연설형. speech_pacing.json 기반.
문장별 pause/속도/음량, 단어 슬램(검은 화면), 화면 흔들림, 붐/타격/틱 SFX, 침묵 설계. 이미지 캐시 재사용.
산출: assets/korea-lost-decade/render/shorts/korea-lost-decade-v2.mp4"""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
A=f"{REPO}/assets/korea-lost-decade"; SIMG=f"{A}/simg"; T=f"{A}/v2tmp"; os.makedirs(T,exist_ok=True)
os.makedirs(f"{A}/render/shorts",exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"
PACE=json.load(open(f"{HERE}/speech_pacing.json",encoding="utf-8")); VOICE=PACE["voice"]
W, H=1080,1920
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip() or 0)
def wrap(d,t,f,mw):
    out=[]; ln=""
    for w in t.split():
        s=(ln+" "+w).strip()
        if d.textlength(s,font=f)<=mw: ln=s
        else:
            if ln: out.append(ln)
            ln=w
    if ln: out.append(ln)
    return out or [t]
# ---------- 프레임 ----------
def frame_img(idx,text,accent,out):
    base=Image.open(f"{SIMG}/main_{idx}.png").convert("RGB")
    r=max(W/base.width,H/base.height); base=base.resize((int(base.width*r),int(base.height*r)))
    base=base.crop(((base.width-W)//2,(base.height-H)//2,(base.width-W)//2+W,(base.height-H)//2+H))
    base=Image.blend(base,Image.new("RGB",(W,H),(0,0,0)),0.42)
    sc=Image.new("L",(W,H),0); sd=ImageDraw.Draw(sc)
    for y in range(int(H*0.5),H): sd.line([(0,y),(W,y)],fill=int(235*(y-H*0.5)/(H*0.5)))
    base=Image.composite(Image.new("RGB",(W,H),(5,7,12)),base,sc)
    d=ImageDraw.Draw(base)
    cf=F(30); tt="잃어버린 AI 10년"; cw=d.textlength(tt,font=cf)
    d.rounded_rectangle([(W-cw)/2-22,58,(W+cw)/2+22,108],radius=25,fill=(150,40,34)); d.text(((W-cw)/2,68),tt,font=cf,fill=(240,225,215))
    fs=64; f=F(fs); lines=wrap(d,text,f,W-130)
    while len(lines)>3 and fs>40: fs-=4; f=F(fs); lines=wrap(d,text,f,W-130)
    col=(232,86,66) if accent else (238,228,205); ly=H-330-(len(lines)-1)*(fs+10)
    for ln in lines:
        lw=d.textlength(ln,font=f)
        for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]: d.text(((W-lw)/2+dx,ly+dy),ln,font=f,fill=(0,0,0))
        d.text(((W-lw)/2,ly),ln,font=f,fill=col); ly+=fs+10
    base.save(out)
def frame_word(word,red,out):
    im=Image.new("RGB",(W,H),(10,12,18)); d=ImageDraw.Draw(im)
    fs=176; f=F(fs); lines=wrap(d,word,f,W-110)
    while (len(lines)>2 or max(d.textlength(l,font=f) for l in lines)>W-110) and fs>60: fs-=10; f=F(fs); lines=wrap(d,word,f,W-110)
    col=(216,58,48) if red else (233,206,140); ty=(H-len(lines)*(fs+16))//2
    for ln in lines:
        lw=d.textlength(ln,font=f)
        for dx,dy in [(-4,-4),(4,4),(4,-4),(-4,4)]: d.text(((W-lw)/2+dx,ty+dy),ln,font=f,fill=(0,0,0))
        d.text(((W-lw)/2,ty),ln,font=f,fill=col); ty+=fs+16
    im.save(out)
def frame_black(text,out):
    im=Image.new("RGB",(W,H),(6,7,11)); d=ImageDraw.Draw(im)
    fs=76; f=F(fs); lw=d.textlength(text,font=f); d.text(((W-lw)/2,(H-fs)//2),text,font=f,fill=(198,188,168)); im.save(out)
# ---------- SFX 합성 ----------
def synth():
    run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i","sine=frequency=52:duration=1.5","-af","afade=t=out:st=0.25:d=1.2,volume=3.2","-ar","44100","-ac","1",f"{T}/boom.wav"])
    run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i","sine=frequency=66:duration=0.5","-af","afade=t=out:st=0.05:d=0.44,volume=4.6","-ar","44100","-ac","1",f"{T}/hit.wav"])
    run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i","sine=frequency=210:duration=0.1","-af","afade=t=out:st=0.02:d=0.08,volume=1.6","-ar","44100","-ac","1",f"{T}/tick.wav"])
def tts(text,rate,pitch,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([VENV,os.path.join(HERE,"_tts_param.py"),tf,out+".raw.mp3",VOICE,rate,pitch])
    # 피치 다운(깊이) 유지 + 전체 속도 살짝 빠르게(atempo 1.28) + 앞뒤 여백 제거로 타격감
    filt=("aresample=44100,asetrate=41000,aresample=44100,atempo=1.28,"
          "equalizer=f=110:t=q:w=1.0:g=4,equalizer=f=2800:t=q:w=1.4:g=2.5,"
          "acompressor=threshold=-16dB:ratio=4:attack=5:release=100:makeup=4,"
          "silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.03,"
          "areverse,silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.08,areverse")
    run([FF,"-hide_banner","-loglevel","error","-y","-i",out+".raw.mp3","-af",filt,"-ar","44100","-ac","1",out])

if __name__=="__main__":
    synth()
    lines=PACE["lines"]; segs=[]; blocks=[]; sfx_ev=[]; t=0.0; q_start=None
    for i,L in enumerate(lines):
        rate=L.get("rate","-12%"); pitch=L.get("pitch","+0Hz"); gap=max(0.02,L.get("gap",0.25)); hold=max(0.02,L.get("hold",0.15)); vol=L.get("vol",1.0)
        vo=f"{T}/v{i}.wav"; tts(L["t"],rate,pitch,vo)
        vp=f"{T}/vp{i}.wav"; run([FF,"-hide_banner","-loglevel","error","-y","-i",vo,"-af",f"volume={vol*1.5}","-ar","44100","-ac","1",vp])
        vd=dur(vp)
        blk=f"{T}/b{i}.wav"
        run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i",f"anullsrc=r=44100:cl=mono:d={gap}","-i",vp,"-f","lavfi","-i",f"anullsrc=r=44100:cl=mono:d={hold}","-filter_complex","[0][1][2]concat=n=3:v=0:a=1[a]","-map","[a]","-ar","44100","-ac","1",blk])
        bd=gap+vd+hold; blocks.append(blk)
        # 프레임
        fr=f"{T}/f{i}.png"; v=L["v"]; accent=(vol>=1.18 or L.get("shake"))
        if v.startswith("img:"): frame_img(int(v.split(":")[1]),L["t"],accent,fr)
        elif v.startswith("word:"): frame_word(v.split(":",1)[1], (L.get("sfx")=="hit" or L.get("shake")), fr)
        else: frame_black(L["t"],fr)
        # 비디오 세그(흔들림 옵션)
        seg=f"{T}/s{i}.mp4"
        if L.get("shake"): vf="scale=1188:2112,crop=1080:1920:x='(iw-ow)/2+18*sin(t*46)':y='(ih-oh)/2+16*sin(t*40)',format=yuv420p"
        else: vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p"
        run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",fr,"-t",f"{bd}","-vf",vf,"-r","30","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",seg])
        segs.append(seg)
        if L.get("sfx"): sfx_ev.append((t+gap, f"{T}/{L['sfx']}.wav"))
        if "뭐 했습니까!" in L["t"] and q_start is None: q_start=t
        t+=bd
    total=t
    if q_start is None: q_start=total*0.55
    # 오디오 concat
    lst=f"{T}/blist.txt"; open(lst,"w",encoding="utf-8").write("\n".join(f"file '{b}'" for b in blocks))
    narr=f"{T}/narr.wav"; run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",lst,"-c","copy",narr])
    # 드론(Act1~2 긴장, 질문 직전 페이드아웃)
    drone=f"{T}/drone.wav"; run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i",f"sine=frequency=48:duration={q_start:.2f}","-af","tremolo=f=0.25:d=0.35,volume=0.42","-ar","44100","-ac","1",drone])
    # 믹스
    inp=["-i",narr]; filt=[]; amix=["[0:a]"]; k=1
    for (tt,sf) in sfx_ev:
        inp+=["-i",sf]; ms=int(tt*1000); filt.append(f"[{k}:a]adelay={ms}|{ms}[s{k}]"); amix.append(f"[s{k}]"); k+=1
    inp+=["-i",drone]; filt.append(f"[{k}:a]afade=t=out:st={max(0,q_start-0.6):.2f}:d=0.6[dr]"); amix.append("[dr]")
    filt.append("".join(amix)+f"amix=inputs={len(amix)}:normalize=0,alimiter=limit=0.96,loudnorm=I=-13:TP=-1.2[m]")
    mixed=f"{T}/mixed.wav"; run([FF,"-hide_banner","-loglevel","error","-y",*inp,"-filter_complex",";".join(filt),"-map","[m]","-ar","44100","-ac","2",mixed])
    # 비디오 concat
    vlst=f"{T}/vlist.txt"; open(vlst,"w",encoding="utf-8").write("\n".join(f"file '{s}'" for s in segs))
    vid=f"{T}/video.mp4"; run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",vlst,"-c","copy",vid])
    out=f"{A}/render/shorts/korea-lost-decade-v2.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",vid,"-i",mixed,"-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    print(f"v2 완성: {dur(out):.1f}s -> {out}")
