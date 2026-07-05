#!/usr/bin/env python3
"""정적 이미지 + 크로스페이드(디졸브) 조립 — zoompan 지터('지진') 제거.
- assemble(beats, audios, out, tmp): 범용. beats=[(img, ovl, dur)], audios=[mp3...].
- build(work, out): make_illust_video 작업폴더(img/ovl/aud) 재조립 래퍼.
CLI: python reassemble_dissolve.py <work_dir> <out.mp4>"""
import os, sys, subprocess
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
XF=0.6  # 디졸브 길이(초)
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

def _static_seg(img,ovl,length,out,size=(1280,720)):
    # 정적: 이미지 꽉차게 스케일+크롭 + 오버레이, 줌 없음 → 흔들림 0
    w,h=size
    run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",img,"-loop","1","-i",ovl,"-t",f"{length}",
      "-filter_complex",f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}[b];[b][1:v]overlay=0:0,format=yuv420p",
      "-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])

def assemble(beats, audios, out, tmp, size=(1280,720)):
    """beats=[(img,ovl,dur)], audios=[mp3...] → 디졸브 영상. size=(w,h) 세로쇼츠=(1080,1920)."""
    os.makedirs(tmp,exist_ok=True)
    segs=[]; durs=[]
    for i,(img,ovl,d) in enumerate(beats):
        seg=f"{tmp}/dseg_{i:03d}.mp4"; _static_seg(img,ovl,d+XF,seg,size); segs.append(seg); durs.append(d)
    al=f"{tmp}/daudio.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{a}'" for a in audios))
    aout=f"{tmp}/dnarration.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",aout])
    args=[FF,"-hide_banner","-loglevel","error","-y"]
    for s in segs: args+=["-i",s]
    args+=["-i",aout]; aidx=len(segs)
    chain=[]; prev="[0:v]"; cum=0.0
    for k in range(1,len(segs)):
        cum+=durs[k-1]
        lbl=f"[vx{k}]"; chain.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={cum:.3f}{lbl}"); prev=lbl
    args+=["-filter_complex",";".join(chain),"-map",prev,"-map",f"{aidx}:a",
           "-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out]
    run(args); return dur(out)

def build(work,out):
    beats=[]; audios=[]
    for si in range(20):
        sa=f"{work}/aud/s{si}.mp3"
        if not os.path.exists(sa): break
        audios.append(sa); per=dur(sa)/3.0
        for bi in range(3):
            img=f"{work}/img/s{si}b{bi}.png"; ovl=f"{work}/ovl/s{si}b{bi}.png"
            if os.path.exists(img): beats.append((img,ovl,per))
    return assemble(beats, audios, out, f"{work}/dtmp")

if __name__=="__main__":
    print("dissolve:",build(sys.argv[1],sys.argv[2]),"s ->",sys.argv[2])
