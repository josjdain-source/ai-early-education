#!/usr/bin/env python3
"""정적 이미지 + 크로스페이드(디졸브) 재조립 — zoompan 지터('지진') 제거.
사용: python reassemble_dissolve.py <work_dir> <out.mp4>
work_dir = make_illust_video.py의 작업폴더(img/ovl/aud 포함)."""
import os, sys, subprocess
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
XF=0.6  # 디졸브 길이(초)
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

def static_seg(img,ovl,length,out):
    # 정적: 이미지 스케일 + 오버레이, 줌 없음 → 흔들림 0
    run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",img,"-loop","1","-i",ovl,"-t",f"{length}",
      "-filter_complex","[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720[b];[b][1:v]overlay=0:0,format=yuv420p",
      "-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])

def build(work,out):
    segs=[]; durs=[]; auds=[]
    for si in range(20):
        sa=f"{work}/aud/s{si}.mp3"
        if not os.path.exists(sa): break
        auds.append(sa); per=dur(sa)/3.0
        for bi in range(3):
            img=f"{work}/img/s{si}b{bi}.png"; ovl=f"{work}/ovl/s{si}b{bi}.png"
            if not os.path.exists(img): continue
            seg=f"{work}/dseg_s{si}b{bi}.mp4"; static_seg(img,ovl,per+XF,seg)
            segs.append(seg); durs.append(per)
    # 오디오 이어붙이기
    al=f"{work}/daudio.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{a}'" for a in auds))
    aout=f"{work}/dnarration.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",aout])
    # xfade 체인(디졸브)
    args=[FF,"-hide_banner","-loglevel","error","-y"]
    for s in segs: args+=["-i",s]
    args+=["-i",aout]
    aidx=len(segs)
    chain=[]; prev="[0:v]"; cum=0.0
    for k in range(1,len(segs)):
        cum+=durs[k-1]  # offset = sum_{j<k} d_j
        lbl=f"[vx{k}]"
        chain.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cum:.3f}{lbl}")
        prev=lbl
    fc=";".join(chain)
    args+=["-filter_complex",fc,"-map",prev,"-map",f"{aidx}:a",
           "-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out]
    run(args)
    return dur(out)

if __name__=="__main__":
    work=sys.argv[1]; out=sys.argv[2]
    print("dissolve 재조립:",build(work,out),"s ->",out)
