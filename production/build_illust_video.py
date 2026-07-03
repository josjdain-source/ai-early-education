#!/usr/bin/env python3
"""일러스트형 본편 파이프라인: 개념별 은유 일러스트(SDXL, 고정스타일) → Pillow 오버레이(액자+배너+자막)
→ 켄번즈(일러스트만 줌, 텍스트는 줌 위 정적합성=안 잘림) → 섹션 내레이션 조립.
산출: world-ai-education-illust-v1.mp4"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"; A=f"{BASE}/assets/world-ai-education-5min"
AUD=f"{A}/audio/sections"; ILL=f"{A}/illust/scenes"; OVL=f"{A}/illust/overlays"
TMP="C:/Users/admin/AppData/Local/Temp/claude/illustvid"
for p in (ILL,OVL,TMP,f"{TMP}/seg"): os.makedirs(p,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

STYLE=("editorial storybook illustration, warm muted color palette, thick clean black outlines, "
 "semi-realistic cartoon style, flat shading, soft warm lighting, detailed cozy background, "
 "hand-drawn look, wide cinematic composition")
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, signature, logo, "
 "ugly, deformed, extra fingers, bad hands, blurry, low quality, creepy, scary, surveillance, headband, weapon")
# key, seed, scene, accent(RGB), title, caption
CONS=[
 ("opening",7001,"a giant friendly glowing globe of the earth, curious happy children of different countries gathered around it reaching toward soft floating AI light symbols, sense of wonder",(124,108,255),"세계는 아이에게 AI를 어떻게?","세계 5개국이 아이에게 AI를 가르치는 법"),
 ("china",7002,"a bright Chinese kindergarten classroom, a small child happily interacting with a friendly rounded white educational AI robot, a kind teacher watching nearby, colorful books",(230,70,80),"중국 · 학교 안으로 AI","학교 안으로 AI, 그래도 다 맡기진 않는다"),
 ("usa",7003,"an American elementary classroom, diverse students using laptops, a teacher guiding them, a big glowing thought bubble showing a magnifying glass inspecting a question mark, critical thinking",(70,120,210),"미국 · 의심하는 힘","많이 쓰기보다, 이해하고 의심하고 고쳐 쓰기"),
 ("uk",7004,"a British classroom, a teacher and a student together at a desk, a large balance scale between them weighing a small AI chip versus a human head silhouette, the human side heavier, thoughtful",(90,110,180),"영국 · 판단은 사람","AI는 도구, 판단과 책임은 사람에게"),
 ("sg",7005,"a tidy Singapore classroom, students using tablets while sitting inside a friendly glowing rounded guardrail fence, a teacher calmly supervising, safe and orderly",(230,110,70),"싱가포르 · 가드레일","쓰게 하되, 안전한 틀 안에서"),
 ("kr",7006,"a modern Korean smart classroom, students using digital tablets showing friendly AI textbook interface, a teacher explaining at a smart board, bright and warm",(70,140,210),"한국 · AI 디지털교과서","학교가 AI를 들여오기 시작했다"),
 ("common",7007,"five happy children of five different countries standing together holding hands in a row, each holding a small friendly AI device, a shared glowing lightbulb of understanding above them, unity and warmth",(20,150,110),"공통점은 하나","AI를 막는 게 아니라, 다루는 힘"),
 ("parent",7008,"a warm home evening scene, a parent and a young child sitting together at a desk looking at a friendly glowing AI screen, the parent gently pointing and asking a question, cozy bookshelves",(124,108,255),"AI는 도구, 곁엔 사람","정답이 아니라, 다시 묻는 힘"),
]

def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"aiedu","images":["8",0]}}}
    cid=uuid.uuid4().hex
    r=urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":cid}).encode(),headers={"Content-Type":"application/json"}),timeout=30)
    pid=json.load(r)["prompt_id"]; t0=time.time()
    while time.time()-t0<300:
        h=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
        if pid in h: break
        time.sleep(3)
    im=h[pid]["outputs"]["9"]["images"][0]
    q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
    open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read())

def overlay_png(accent,title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    # 액자 비네트
    b=16
    for r in [(0,0,W,b),(0,H-b,W,H),(0,0,b,H),(W-b,0,W,H)]: d.rectangle(r,fill=(28,18,12,235))
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle([b,b,W-b,H-b],outline=(0,0,0,120),width=22)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d=ImageDraw.Draw(im)
    # 상단 리본 배너
    fs=46; f=F(fs)
    while d.textlength(title,font=f)>W-360 and fs>26: fs-=2; f=F(fs)
    tw=d.textlength(title,font=f); cx=W//2; y=34; pad=34; h=fs+28
    x0,x1=cx-tw/2-pad,cx+tw/2+pad
    d.polygon([(x0-24,y+h/2),(x0,y+6),(x0,y+h-6)],fill=(150,96,52))
    d.polygon([(x1+24,y+h/2),(x1,y+6),(x1,y+h-6)],fill=(150,96,52))
    d.rounded_rectangle([x0,y,x1,y+h],radius=12,fill=(245,232,205),outline=(150,96,52),width=4)
    d.text((cx-tw/2,y+13),title,font=f,fill=(60,40,20))
    # 하단 자막(흰+외곽선)
    cfs=42; cf=F(cfs)
    while d.textlength(caption,font=cf)>W-80 and cfs>24: cfs-=2; cf=F(cfs)
    cw=d.textlength(caption,font=cf); cxx=(W-cw)/2; cyy=H-cfs-48
    for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]: d.text((cxx+dx,cyy+dy),caption,font=cf,fill=(0,0,0))
    d.text((cxx,cyy),caption,font=cf,fill=(255,255,255))
    im.save(out)

def segment(illust,ovl,d,out):
    run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",illust,"-loop","1","-i",ovl,"-t",f"{d}",
      "-filter_complex",f"[0:v]scale=1400:800,zoompan=z='min(zoom+0.0006,1.05)':d={int(d*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[bg];[bg][1:v]overlay=0:0,format=yuv420p",
      "-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])

if __name__=="__main__":
    segs=[]
    for key,seed,scene,accent,title,cap in CONS:
        ip=f"{ILL}/{key}.png"
        if not os.path.exists(ip): print(" gen",key,"..."); sdxl(scene,seed,ip)
        op=f"{OVL}/{key}.png"; overlay_png(accent,title,cap,op)
        d=dur(f"{AUD}/{key}.mp3"); sp=f"{TMP}/seg/{key}.mp4"; segment(ip,op,d,sp); segs.append(sp)
        print(" seg",key,round(d,2),"s")
    # concat video
    vl=f"{TMP}/vlist.txt"; open(vl,"w",encoding="utf-8").write("\n".join(f"file '{s}'" for s in segs))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",vl,"-c:v","libx264","-preset","veryfast","-crf","20","-r","30",f"{TMP}/video.mp4"])
    al=f"{TMP}/alist.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{AUD}/{k}.mp3'" for k,*_ in CONS))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",f"{TMP}/audio.mp3"])
    out=f"{A}/render/world-ai-education-illust-v1.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{TMP}/video.mp4","-i",f"{TMP}/audio.mp3",
      "-filter_complex","[0:v]tpad=stop_mode=clone:stop_duration=2[v];[1:a]apad=pad_dur=2[a]",
      "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    print("illust-v1:",dur(out),"s ->",out)
