#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""잃어버린 AI 10년 v3 — 격정 보이스 자동생성(엔진/보이스/감정 DSP 시스템화).
사용: python build_klad_v3.py <A|B|C>  (voice_profiles.json test_options)
실존 인물 성대복제 금지. civic_rage_speaker = DSP 캐릭터. 산출: comparison/voice_test_{P}.mp4"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
EDGE_VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
REPO="C:/Users/admin/Desktop/ai-craft-kids"; HERE=os.path.join(REPO,"production")
A=f"{REPO}/assets/korea-lost-decade"; SIMG=f"{A}/simg"; CMP=f"{A}/comparison"
KB=r"C:\Windows\Fonts\malgunbd.ttf"; W,H=1080,1920
PROF=sys.argv[1] if len(sys.argv)>1 else "B"
VP=json.load(open(f"{HERE}/voice_profiles.json",encoding="utf-8"))
PACE=json.load(open(f"{HERE}/speech_pacing.json",encoding="utf-8"))
opt=VP["test_options"][PROF]; ENGINE=opt["engine"]; VOICE=opt["voice"]; RAGE=opt["rage"]; EMO=VP["emotion_dsp"]
ST_PY=VP["engines"]["supertonic"]["py"]; ST_CLI=VP["engines"]["supertonic"]["cli"]
T=f"{A}/v3tmp_{PROF}"; os.makedirs(T,exist_ok=True); os.makedirs(CMP,exist_ok=True)
SPEEDFIX=1.12 if ENGINE=="edge" else 0.88  # Supertonic은 빨라서 느리게(70초)
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
def frame_img(idx,text,accent,out):
    base=Image.open(f"{SIMG}/main_{idx}.png").convert("RGB")
    r=max(W/base.width,H/base.height); base=base.resize((int(base.width*r),int(base.height*r)))
    base=base.crop(((base.width-W)//2,(base.height-H)//2,(base.width-W)//2+W,(base.height-H)//2+H))
    base=Image.blend(base,Image.new("RGB",(W,H),(0,0,0)),0.22)
    sc=Image.new("L",(W,H),0); sd=ImageDraw.Draw(sc)
    for y in range(int(H*0.55),H): sd.line([(0,y),(W,y)],fill=int(205*(y-H*0.55)/(H*0.45)))
    base=Image.composite(Image.new("RGB",(W,H),(20,15,26)),base,sc); d=ImageDraw.Draw(base)
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
    im=Image.new("RGB",(W,H),(6,7,11)); d=ImageDraw.Draw(im); fs=76; f=F(fs)
    lw=d.textlength(text,font=f); d.text(((W-lw)/2,(H-fs)//2),text,font=f,fill=(198,188,168)); im.save(out)
def synth(text,speed,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    if ENGINE=="edge":
        pc=int(round((speed-1)*100)); rate=(f"+{pc}%" if pc>=0 else f"{pc}%")
        run([EDGE_VENV,os.path.join(HERE,"_tts_param.py"),tf,out,VOICE,rate,"+0Hz"])
    else:
        run([ST_PY,ST_CLI,"--input",tf,"--output",out,"--voice",VOICE,"--lang","ko","--speed",f"{max(0.7,min(2.0,speed)):.2f}"])
def emo_dsp(raw,emotion,intens,vol,out):
    E=EMO[emotion]; k=RAGE*(0.6+0.4*intens/5)
    ratio=2**((E["pitch"]*k)/12.0)  # 피치 다운
    at=(1.0/ratio)*SPEEDFIX*E["speed"]; at=max(0.5,min(2.0,at))
    gain=(1+(E["gain"]-1)*k)*vol*1.5; sat=E["sat"]*k
    ch=[f"aresample=44100",f"asetrate={int(44100*ratio)}","aresample=44100",f"atempo={at:.4f}",
        f"equalizer=f=110:t=q:w=1.0:g={4+sat*4:.1f}","equalizer=f=2800:t=q:w=1.4:g=2.5",
        "acompressor=threshold=-16dB:ratio=4:attack=5:release=100:makeup=4"]
    if sat>0.05: ch+=[f"volume={1+sat*0.8:.2f}","asoftclip=type=atan"]
    ch+=[f"volume={gain:.2f}",
         "silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.03","areverse",
         "silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.08","areverse"]
    run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-af",",".join(ch),"-ar","44100","-ac","1",out])
def synth_sfx():
    run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i","sine=frequency=52:duration=1.5","-af","afade=t=out:st=0.25:d=1.2,volume=3.2","-ar","44100","-ac","1",f"{T}/boom.wav"])
    run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i","sine=frequency=66:duration=0.5","-af","afade=t=out:st=0.05:d=0.44,volume=4.6","-ar","44100","-ac","1",f"{T}/hit.wav"])
    run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i","sine=frequency=210:duration=0.1","-af","afade=t=out:st=0.02:d=0.08,volume=1.6","-ar","44100","-ac","1",f"{T}/tick.wav"])

if __name__=="__main__":
    synth_sfx(); lines=PACE["lines"]; segs=[]; blocks=[]; sfx_ev=[]; t=0.0; q_start=None
    for i,L in enumerate(lines):
        rate=L.get("rate","-12%"); base_speed=1+int(rate.replace("%",""))/100.0
        gap=max(0.02,L.get("gap",0.25)); hold=max(0.02,L.get("hold",0.15)); vol=L.get("vol",1.0)
        emotion=L.get("emotion","calm"); intens=L.get("intensity",2)
        raw=f"{T}/r{i}.wav"; synth(L["t"],base_speed,raw)
        vp=f"{T}/v{i}.wav"; emo_dsp(raw,emotion,intens,vol,vp); vd=dur(vp)
        blk=f"{T}/b{i}.wav"
        run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i",f"anullsrc=r=44100:cl=mono:d={gap}","-i",vp,"-f","lavfi","-i",f"anullsrc=r=44100:cl=mono:d={hold}","-filter_complex","[0][1][2]concat=n=3:v=0:a=1[a]","-map","[a]","-ar","44100","-ac","1",blk])
        bd=gap+vd+hold; blocks.append(blk)
        fr=f"{T}/f{i}.png"; v=L["v"]; accent=(vol>=1.18 or L.get("shake") or emotion in("anger","climax"))
        if v.startswith("img:"): frame_img(int(v.split(":")[1]),L["t"],accent,fr)
        elif v.startswith("word:"): frame_word(v.split(":",1)[1],(L.get("sfx")=="hit" or L.get("shake")),fr)
        else: frame_black(L["t"],fr)
        seg=f"{T}/s{i}.mp4"
        vf=("scale=1188:2112,crop=1080:1920:x='(iw-ow)/2+18*sin(t*46)':y='(ih-oh)/2+16*sin(t*40)',format=yuv420p" if L.get("shake")
            else "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p")
        run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",fr,"-t",f"{bd}","-vf",vf,"-r","30","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p",seg])
        segs.append(seg)
        if L.get("sfx"): sfx_ev.append((t+gap,f"{T}/{L['sfx']}.wav"))
        if "뭐 했습니까!" in L["t"] and q_start is None: q_start=t
        t+=bd
    total=t; q_start=q_start or total*0.55
    lst=f"{T}/bl.txt"; open(lst,"w",encoding="utf-8").write("\n".join(f"file '{b}'" for b in blocks))
    narr=f"{T}/narr.wav"; run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",lst,"-c","copy",narr])
    drone=f"{T}/drone.wav"; run([FF,"-hide_banner","-loglevel","error","-y","-f","lavfi","-i",f"sine=frequency=48:duration={q_start:.2f}","-af","tremolo=f=0.25:d=0.35,volume=0.42","-ar","44100","-ac","1",drone])
    inp=["-i",narr]; filt=[]; amix=["[0:a]"]; k=1
    for (tt,sf) in sfx_ev:
        inp+=["-i",sf]; ms=int(tt*1000); filt.append(f"[{k}:a]adelay={ms}|{ms}[s{k}]"); amix.append(f"[s{k}]"); k+=1
    inp+=["-i",drone]; filt.append(f"[{k}:a]afade=t=out:st={max(0,q_start-0.6):.2f}:d=0.6[dr]"); amix.append("[dr]")
    filt.append("".join(amix)+f"amix=inputs={len(amix)}:normalize=0,alimiter=limit=0.97,loudnorm=I=-12:TP=-1.0[m]")
    mixed=f"{T}/mix.wav"; run([FF,"-hide_banner","-loglevel","error","-y",*inp,"-filter_complex",";".join(filt),"-map","[m]","-ar","44100","-ac","2",mixed])
    vlst=f"{T}/vl.txt"; open(vlst,"w",encoding="utf-8").write("\n".join(f"file '{s}'" for s in segs))
    vid=f"{T}/video.mp4"; run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",vlst,"-c","copy",vid])
    out=f"{CMP}/voice_test_{PROF}.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",vid,"-i",mixed,"-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    print(f"[{PROF}] {opt['label']} ({ENGINE}/{VOICE}/rage{RAGE}): {dur(out):.1f}s -> {out}")
