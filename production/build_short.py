#!/usr/bin/env python3
"""세로 숏폼(9:16, 1080x1920) 펀치판. 문장별 TTS로 싱크.
구조: 훅카드 → 5국(뉴스클립+큰 자막) → 공통 카드 → CTA 카드. 켄번즈 모션. ~46s."""
import os, subprocess, asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"; A=f"{BASE}/assets/world-ai-education-5min"
VS=f"{A}/video-scenes/final"; DOC=f"{A}/evidence-screenshots/final"
SA=f"{A}/audio/short"; os.makedirs(SA,exist_ok=True)
FR=f"{A}/short-frames"; os.makedirs(FR,exist_ok=True)
TMP="C:/Users/admin/AppData/Local/Temp/claude/short"; os.makedirs(TMP,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
W,H=1080,1920; GOLD=(255,224,130); PUR=(124,108,255); WHITE=(245,247,255)
def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

SENT=[
 ("hook","세계는 아이에게 AI를 어떻게 가르칠까요?"),
 ("china","중국은 학교 안으로 AI를 들여옵니다. 그래도 다 맡기진 않죠."),
 ("usa","미국은 많이 쓰기보다, 이해하고 의심하는 힘을 가르칩니다."),
 ("uk","영국은 말합니다. AI는 도구고, 판단은 사람이라고."),
 ("sg","싱가포르는 안전한 틀 안에서만 쓰게 하고,"),
 ("kr","한국은 AI 디지털교과서를 학교에 들입니다."),
 ("common","방식은 달라도 공통점은 하나. 정답을 맡기는 게 아니라, 다시 묻는 힘이죠."),
 ("cta","오늘 아이에게 물어보세요. AI 답에서 이상한 부분, 찾아볼까?"),
]
CLIP={"china":(f"{VS}/CN-video-scene-final.png",(230,70,80),"중국",["학교 안으로 AI","그래도 다 맡기진 않는다"]),
      "usa":(f"{VS}/US-video-scene-final.png",(70,120,210),"미국",["많이 쓰기보다","이해하고 의심하는 힘"]),
      "uk":(f"{DOC}/UK-01-dfe-genai-guidance-evidence.png",(90,110,180),"영국",["AI는 도구,","판단은 사람"]),
      "sg":(f"{VS}/SG-video-scene-final.png",(230,110,70),"싱가포르",["쓰게 하되","안전한 틀 안에서"]),
      "kr":(f"{VS}/KR-video-scene-final.png",(70,140,210),"한국",["AI 디지털교과서를","학교 안으로"])}
CARD={"hook":(PUR,"세계 5개국·AI교육",["세계는 아이에게","AI를 어떻게","가르칠까?"]),
      "common":((20,150,110),"공통점은 하나",["AI를 막는 게 아니라","다루는 힘"]),
      "cta":(PUR,"오늘, 우리 집",["정답이 아니라,","다시 묻는 힘"])}

def bg(accent):
    im=Image.new("RGB",(W,H),(13,15,26)); d=ImageDraw.Draw(im,"RGBA")
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=(13+int(9*t),15+int(12*t),26+int(26*t)))
    for x,y,r in [(250,520,220),(820,700,180),(300,1300,200),(800,1500,220)]:
        d.ellipse([x-r,y-r,x+r,y+r],fill=(60,80,140,40))
    d.ellipse([-150,H-150,220,H+150],fill=(accent[0],accent[1],accent[2],26))
    return im
def pill(d,x,y,txt,accent,fs=44):
    f=F(KB,fs); tw=d.textlength(txt,font=f)
    d.rounded_rectangle([x,y,x+tw+40,y+fs+26],radius=(fs+26)//2,fill=accent)
    d.text((x+20,y+12),txt,font=f,fill=(255,255,255)); return tw+40

def card_frame(key):
    accent,kick,lines=CARD[key]; im=bg(accent); d=ImageDraw.Draw(im,"RGBA")
    pill(d,80,180,kick,accent,fs=40)
    y=760
    for i,ln in enumerate(lines):
        fs=110 if len(ln)<=9 else 92; f=F(KB,fs)
        col=GOLD if i==len(lines)-1 else WHITE
        d.text((80,y),ln,font=f,fill=col); y+=fs+20
    if key=="cta":
        d.rounded_rectangle([80,1360,W-80,1560],radius=28,fill=(255,255,255))
        d.text((120,1390),"오늘 아이에게",font=F(KB,40),fill=(90,73,214))
        d.text((120,1450),"\"이상한 부분 찾아볼까?\"",font=F(KF,46),fill=(36,36,51))
    p=f"{FR}/card_{key}.png"; im.convert("RGB").save(p); return p
def country_frame(key):
    img,accent,pilltxt,lines=CLIP[key]; im=bg(accent); d=ImageDraw.Draw(im,"RGBA")
    # 상단 큰 자막
    px=pill(d,80,200,pilltxt,accent,fs=46)
    y=320
    for ln in lines:
        fs=84 if len(ln)<=11 else 70; f=F(KB,fs)
        d.text((80,y),ln,font=f,fill=WHITE if y==320 else GOLD); y+=fs+16
    # 뉴스 클립(1080폭, 16:9 → 1080x608) 중앙
    clip=Image.open(img).convert("RGB").resize((1080,608))
    cy=760; im.paste(clip,(0,cy))
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([0,cy,W,cy+6],fill=accent); d.rectangle([0,cy+602,W,cy+608],fill=accent)
    # 하단 진행 점(5국)
    order=["china","usa","uk","sg","kr"]; bx=W//2-5*40//1-40
    x0=W//2-(5*46)//2
    for i,k in enumerate(order):
        cc=CLIP[k][1] if k==key else (90,95,120)
        d.ellipse([x0+i*46,1760,x0+i*46+22,1782],fill=cc)
    p=f"{FR}/co_{key}.png"; im.convert("RGB").save(p); return p

def kb(img,out,d,zin=True):
    z=("min(zoom+0.0011,1.16)" if zin else "if(lte(zoom,1.0),1.16,max(1.001,zoom-0.0011))")
    run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",img,"-t",f"{d}",
      "-vf",f"scale=1300:2311,zoompan=z='{z}':d={int(d*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p",
      "-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])

async def tts_one(text,out):
    import edge_tts
    c=edge_tts.Communicate(text,"ko-KR-SunHiNeural",rate="-8%"); await c.save(out)

if __name__=="__main__":
    # 문장별 오디오는 venv로 미리 합성됨({TMP}/a_<key>.mp3). 여기선 재사용.
    order=[k for k,_ in SENT]; segs=[]; auds=[]
    for key,text in SENT:
        ap=f"{TMP}/a_{key}.mp3"
        if not os.path.exists(ap): raise SystemExit(f"오디오 없음: {ap} (venv로 먼저 합성)")
        auds.append(ap)
        d=dur(ap)
        if key in CARD: fp=card_frame(key); kb(fp,f"{TMP}/v_{key}.mp4",d,zin=(key!="common"))
        else: fp=country_frame(key); kb(fp,f"{TMP}/v_{key}.mp4",d,zin=True)
        segs.append(f"{TMP}/v_{key}.mp4"); print(" seg",key,round(d,2),"s")
    # concat video
    vl=f"{TMP}/vlist.txt"; open(vl,"w",encoding="utf-8").write("\n".join(f"file '{s}'" for s in segs))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",vl,"-c:v","libx264","-preset","veryfast","-crf","20","-r","30",f"{TMP}/video.mp4"])
    # concat audio
    al=f"{TMP}/alist.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{a}'" for a in auds))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",f"{TMP}/audio.mp3"])
    out=f"{A}/render/world-ai-education-short-v1.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{TMP}/video.mp4","-i",f"{TMP}/audio.mp3",
      "-filter_complex","[0:v]tpad=stop_mode=clone:stop_duration=1.2[v];[1:a]apad=pad_dur=1.2[a]",
      "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    print("short-v1:",dur(out),"s ->",out)
