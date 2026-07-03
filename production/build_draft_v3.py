#!/usr/bin/env python3
"""가로 다이내믹 draft-v3 조립.
섹션별: [지도 줌인] → [프리미엄 카드 켄번즈] → [뉴스 b-roll 켄번즈 + 굵은 자막].
섹션 오디오(assets/.../audio/sections)에 정확히 싱크. 1280x720/30fps.
※ 본편 final candidate는 건드리지 않음. 산출=world-ai-education-dynamic-draft-v3.mp4"""
import os, subprocess, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_map_zoom as MZ

FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"
A=f"{BASE}/assets/world-ai-education-5min"
CARD=f"{A}/premium-cards"; VS=f"{A}/video-scenes/final"; DOC=f"{A}/evidence-screenshots/final"
AUD=f"{A}/audio/sections"; MAP=f"{A}/map/world-map-base.png"
TMP="C:/Users/admin/AppData/Local/Temp/claude/v3"; os.makedirs(TMP,exist_ok=True)
SEG=f"{TMP}/seg"; os.makedirs(SEG,exist_ok=True)
BOLD="C\\:/Windows/Fonts/malgunbd.ttf"
def run(cmd): subprocess.run(cmd,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

def kb_in(img,out,d,zmax=1.18):  # 켄번즈 줌인
    run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",img,"-t",f"{d}",
      "-vf",f"scale=1600:900,zoompan=z='min(zoom+0.0010,{zmax})':d={int(d*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30,format=yuv420p",
      "-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])
def kb_out(img,out,d,sub=None):  # 켄번즈 줌아웃(+자막)
    vf=f"scale=1600:900,zoompan=z='if(lte(zoom,1.0),1.18,max(1.001,zoom-0.0010))':d={int(d*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30"
    if sub: vf+=f",drawtext=fontfile='{BOLD}':text='{sub}':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.55:boxborderw=16:x=(w-tw)/2:y=84"
    vf+=",format=yuv420p"
    run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",img,"-t",f"{d}","-vf",vf,"-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])
def mapzoom(key,out):
    fr=f"{TMP}/mz_{key}"; MZ.gen(key,fr)
    run([FF,"-hide_banner","-loglevel","error","-y","-framerate","30","-i",f"{fr}/z%03d.png","-vf","format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])
    return dur(out)
def concat(parts,out):
    lst=f"{TMP}/cc_{os.path.basename(out)}.txt"
    open(lst,"w",encoding="utf-8").write("\n".join(f"file '{p}'" for p in parts))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",lst,"-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])

# 나라별: (map_key, card, media_img, subtitle)
CO={"china":("cn",f"{CARD}/01-china.png",f"{VS}/CN-video-scene-final.png","중국 · 학교 안으로 AI"),
    "usa":("us",f"{CARD}/02-usa.png",f"{VS}/US-video-scene-final.png","미국 · 이해하고 의심하는 힘"),
    "uk":("uk",f"{CARD}/03-uk.png",f"{DOC}/UK-01-dfe-genai-guidance-evidence.png","영국 · 판단은 사람에게"),
    "sg":("sg",f"{CARD}/04-singapore.png",f"{VS}/SG-video-scene-final.png","싱가포르 · 안전한 틀 안에서"),
    "kr":("kr",f"{CARD}/05-korea.png",f"{VS}/KR-video-scene-final.png","한국 · AI 디지털교과서")}
CARD_D=6.0

def build_country(name):
    d=dur(f"{AUD}/{name}.mp3"); key,card,media,sub=CO[name]
    mz=f"{SEG}/{name}_mz.mp4"; mzd=mapzoom(key,mz)
    cd=f"{SEG}/{name}_card.mp4"; kb_in(card,cd,CARD_D)
    bd=f"{SEG}/{name}_broll.mp4"; brl=d-mzd-CARD_D
    kb_out(media,bd,brl,sub)
    out=f"{SEG}/S_{name}.mp4"; concat([mz,cd,bd],out); return out

def build_opening():
    d=dur(f"{AUD}/opening.mp3")
    oc=f"{SEG}/open_card.mp4"; kb_in(f"{CARD}/00-opening.png",oc,d*0.5)
    om=f"{SEG}/open_map.mp4"; kb_in(MAP,om,d-d*0.5,zmax=1.10)
    out=f"{SEG}/S_opening.mp4"; concat([oc,om],out); return out
def build_common():
    d=dur(f"{AUD}/common.mp3")
    cc=f"{SEG}/common_card.mp4"; kb_in(f"{CARD}/06-common.png",cc,d*0.5)
    cm=f"{SEG}/common_map.mp4"; kb_out(MAP,cm,d-d*0.5)
    out=f"{SEG}/S_common.mp4"; concat([cc,cm],out); return out
def build_parent():
    d=dur(f"{AUD}/parent.mp3")
    pc=f"{SEG}/parent_card.mp4"; kb_in(f"{CARD}/07-conclusion.png",pc,d)
    return pc

if __name__=="__main__":
    print("빌드 시작...")
    order=["opening","china","usa","uk","sg","kr","common","parent"]
    segs={}
    segs["opening"]=build_opening(); print(" opening OK")
    for c in ["china","usa","uk","sg","kr"]: segs[c]=build_country(c); print(f" {c} OK")
    segs["common"]=build_common(); print(" common OK")
    segs["parent"]=build_parent(); print(" parent OK")
    # 비디오 concat
    vtrack=f"{TMP}/video_all.mp4"; concat([segs[o] for o in order],vtrack)
    # 오디오 concat(섹션 mp3 순서대로) — 완벽 싱크
    alst=f"{TMP}/audio.txt"; open(alst,"w",encoding="utf-8").write("\n".join(f"file '{AUD}/{o}.mp3'" for o in order))
    atrack=f"{TMP}/audio_all.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",alst,"-c","copy",atrack])
    # 최종 mux + 2s tail
    out=f"{A}/render/world-ai-education-dynamic-draft-v3.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",vtrack,"-i",atrack,
      "-filter_complex","[0:v]tpad=stop_mode=clone:stop_duration=2[v];[1:a]apad=pad_dur=2[a]",
      "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    print("draft-v3:",dur(out),"s ->",out)
