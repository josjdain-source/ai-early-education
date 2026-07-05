#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""잃어버린 AI 10년 — 세계영상(build_illust_video_v2) 방식으로 재제작.
문장마다 그 장면을 그린 일관된 스토리북 그림 + 타이틀배너 + 자막 + 차분한 내레이션 + 디졸브.
그림체/이미지/나레이션 연결성 = 세계 5개국 영상과 동일. ★Ollama 언로드 후 실행(VRAM).
산출: assets/korea-lost-decade/render/korea-lost-decade-illust.mp4"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
EDGE=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"; HERE=f"{BASE}/production"; A=f"{BASE}/assets/korea-lost-decade"
AUD=f"{A}/audio/sections"; ILL=f"{A}/illust/scenes"; OVL=f"{A}/illust/overlays"
TMP="C:/Users/admin/AppData/Local/Temp/claude/kladill"
for p in (AUD,ILL,OVL,TMP,f"{TMP}/aud",f"{TMP}/dtmp"): os.makedirs(p,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"; VOICE="ko-KR-InJoonNeural"; SPEED=1.12
STYLE=("editorial storybook illustration, warm muted color palette, thick clean black outlines, "
 "semi-realistic cartoon style, flat shading, soft warm lighting, detailed cozy background, hand-drawn look, wide cinematic composition")
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, signature, logo, "
 "ugly, deformed, extra fingers, bad hands, blurry, low quality, creepy, scary, horror, surveillance, weapon")
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())
# 섹션: key, title, accent, narration(전체 TTS), beats[(subfile,seed,scene,caption)]
KR="Korean, black hair, East Asian, "; CN="Chinese, black hair, East Asian, "
SEC=[
 ("open","AI 시대, 경고음은 서울에서",(150,60,54),
  "이천십육년, 알파고가 이세돌을 이긴 곳은 중국이 아니라 서울이었습니다. 인공지능 시대의 첫 경고음은, 우리 한복판에서 울렸습니다.",
  [("kl_open1",5101,"a calm scene of a person sitting at a wooden go board across from a soft glowing friendly AI light, a quiet hall in Seoul, "+KR+"thoughtful, warm storybook","2016년, 알파고가 이세돌을 이긴 곳은 서울"),
   ("kl_open2",5102,"a small warm warning bell glowing softly above a gentle Seoul city skyline at dawn, a quiet alarm, storybook","AI 시대의 첫 경고음이 울렸습니다")]),
 ("china","중국은 움직였습니다",(70,130,180),
  "그 사이 중국은 움직였습니다. 국가 전략으로, 학교로, 대학 전공으로, 기업과 산업으로. 아이가 배우기 시작해, 어른이 되어 산업을 만듭니다.",
  [("kl_cn1",5201,"a "+CN+"child in a bright cozy classroom starting to learn with a friendly white AI robot, hopeful, warm storybook","중국은 학교와 국가 전략으로 AI를 넣었고"),
   ("kl_cn2",5202,"a "+CN+"student growing into a confident young engineer walking toward a bright smart factory with friendly robots, upward hopeful, storybook","아이가 어른이 되어 산업을 만듭니다")]),
 ("korea","그러면, 한국은?",(200,120,40),
  "한국은 어땠을까요. 케이팝과 드라마로 조명은 화려했습니다. 하지만 그 이득은 일부에게만 돌아갔고, 새로운 산업이 오는 동안, 우리는 한 걸음 뒤처졌습니다.",
  [("kl_kr1",5301,"a dazzling warm K-pop concert stage with bright golden spotlights and a happy cheering crowd, glamorous, storybook","K팝과 드라마로 조명은 화려했지만"),
   ("kl_kr2",5302,"a gentle storybook metaphor, a few figures holding most of the golden light while many others stand in soft shadow, uneven sharing, warm","그 이득은 일부에게만 돌아갔고"),
   ("kl_kr3",5303,"a bright train of industry and AI moving ahead while one "+KR+"figure stands a step behind on the platform, thoughtful, warm storybook","새 산업에서 우리는 뒤처졌습니다")]),
 ("youth","잃어버린 것",(120,90,150),
  "그 대가는 지금, 청년들의 취업난과, 잃어버린 비전입니다. 화려한 조명 뒤에서, 정작 미래를 만들 힘은 밀려 있었습니다.",
  [("kl_yt1",5401,"a young "+KR+"job-seeker sitting quietly with application papers near a warm window at dusk, thoughtful and hopeful, storybook","그 대가는 청년들의 취업난과 잃어버린 비전")]),
 ("child","우리 아이는?",(60,150,90),
  "이제 물어야 합니다. 우리 아이는 인공지능을 소비만 할까요, 아니면 인공지능으로 자기 일을 만들까요. 지금 아이에게 필요한 건, 정답을 빨리 찾는 힘이 아니라, 인공지능으로 자기 일을 만드는 힘입니다.",
  [("kl_ch1",5501,"a "+KR+"child at a gentle sunny fork in a path, one side softly watching a glowing screen, the other side happily building and creating with friendly AI tools, hopeful, storybook","우리 아이는 AI를 소비할까요, 만들까요"),
   ("kl_ch2",5502,"a "+KR+"parent and child building something together with a friendly AI tablet in a warm evening room, guiding hand, cozy storybook","필요한 건, AI로 자기 일을 만드는 힘입니다")]),
]
def tts(text,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([EDGE,f"{HERE}/_tts_param.py",tf,out,VOICE,"+0%","+0Hz"])
def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"kladill","images":["8",0]}}}
    cid=uuid.uuid4().hex
    for attempt in range(3):
        try:
            pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":cid}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
            t0=time.time()
            while time.time()-t0<300:
                h=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
                if pid in h and h[pid].get("outputs"): break
                time.sleep(2)
            im=h[pid]["outputs"]["9"]["images"][0]
            q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
            open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read()); return
        except Exception as e:
            print(f"  [재시도 {attempt+1}/3] {out}: {repr(e)[:60]}"); time.sleep(6)
    raise RuntimeError("sdxl 3회 실패: "+out)
def overlay_png(title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    b=16
    for r in [(0,0,W,b),(0,H-b,W,H),(0,0,b,H),(W-b,0,W,H)]: d.rectangle(r,fill=(28,18,12,235))
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle([b,b,W-b,H-b],outline=(0,0,0,120),width=22)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    fs=46; f=F(fs)
    while d.textlength(title,font=f)>W-360 and fs>26: fs-=2; f=F(fs)
    tw=d.textlength(title,font=f); cx=W//2; y=34; pad=34; hh=fs+28; x0,x1=cx-tw/2-pad,cx+tw/2+pad
    d.polygon([(x0-24,y+hh/2),(x0,y+6),(x0,y+hh-6)],fill=(150,96,52)); d.polygon([(x1+24,y+hh/2),(x1,y+6),(x1,y+hh-6)],fill=(150,96,52))
    d.rounded_rectangle([x0,y,x1,y+hh],radius=12,fill=(245,232,205),outline=(150,96,52),width=4); d.text((cx-tw/2,y+13),title,font=f,fill=(60,40,20))
    cfs=42; cf=F(cfs)
    while d.textlength(caption,font=cf)>W-80 and cfs>24: cfs-=2; cf=F(cfs)
    cw=d.textlength(caption,font=cf); cxx=(W-cw)/2; cyy=H-cfs-48
    for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]: d.text((cxx+dx,cyy+dy),caption,font=cf,fill=(0,0,0))
    d.text((cxx,cyy),caption,font=cf,fill=(255,255,255)); im.save(out)
if __name__=="__main__":
    import sys; sys.path.insert(0,HERE); import reassemble_dissolve as RD
    beats_all=[]; auds=[]
    for key,title,accent,narr,beats in SEC:
        raw=f"{TMP}/aud/{key}_raw.mp3"; tts(narr,raw)
        sa=f"{TMP}/aud/{key}.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={SPEED}",sa])
        sd=dur(sa); auds.append(sa); per=sd/len(beats)
        for subfile,seed,scene,cap in beats:
            ip=f"{ILL}/{subfile}.png"
            if not os.path.exists(ip): print("  gen",subfile); sdxl(scene,seed,ip)
            op=f"{OVL}/{subfile}.png"; overlay_png(title,cap,op)
            beats_all.append((ip,op,per))
        print(" sec",key,round(sd,2),"s ·",len(beats),"컷")
    out=f"{A}/render/korea-lost-decade-illust.mp4"
    RD.assemble(beats_all,auds,out,f"{TMP}/dtmp")
    print("잃어버린10년 illust(연결성):",round(dur(out),1),"s ->",out)
