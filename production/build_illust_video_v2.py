#!/usr/bin/env python3
"""일러스트형 본편 v2: 섹션당 3장(촘촘) + 내레이션 1.3배속(30%↑).
beat1=기존 scenes/{key}.png 재사용, beat2/3 신규 생성. 타이틀배너 유지·자막 교체.
산출: world-ai-education-illust-v2.mp4"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"; A=f"{BASE}/assets/world-ai-education-5min"
AUD=f"{A}/audio/sections"; ILL=f"{A}/illust/scenes"; OVL=f"{A}/illust/overlays"
TMP="C:/Users/admin/AppData/Local/Temp/claude/illv2"
for p in (ILL,OVL,TMP,f"{TMP}/seg",f"{TMP}/aud"): os.makedirs(p,exist_ok=True)
KB=r"C:\Windows\Fonts\malgunbd.ttf"
SPEED=1.3
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())
STYLE=("editorial storybook illustration, warm muted color palette, thick clean black outlines, "
 "semi-realistic cartoon style, flat shading, soft warm lighting, detailed cozy background, hand-drawn look, wide cinematic composition")
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, signature, logo, "
 "ugly, deformed, extra fingers, bad hands, blurry, low quality, creepy, scary, surveillance, headband, weapon")
# 섹션: key,title,accent, 3 beats [(subfile, seed, scene, caption)]  beat1 subfile=기존 {key}.png
SEC=[
 ("opening","세계는 아이에게 AI를 어떻게?",(124,108,255),[
   ("opening",7001,None,"세계는 아이에게 AI를 어떻게 가르칠까?"),
   ("opening_b2",7101,"a world map with five glowing location pins connecting China USA UK Singapore Korea with soft light lines, children silhouettes","중국·미국·영국·싱가포르·한국"),
   ("opening_b3",7201,"a curious child looking up at floating question marks and soft AI light, sense of wonder, warm","방식은 달라도, 향하는 곳은 같습니다")]),
 ("china","중국 · 학교 안으로 AI",(230,70,80),[
   ("china",7002,None,"중국, 학교 안으로 AI가 들어옵니다"),
   ("china_b2",7102,"a Chinese classroom full of students each using a small AI tablet, a teacher walking between desks, orderly and bright","교실마다 AI 도구와 로봇 수업"),
   ("china_b3",7202,"a gentle giant hand pausing near a friendly AI robot, a balance feeling, thoughtful caution, warm","그래도, 다 맡기진 않습니다")]),
 ("usa","미국 · 의심하는 힘",(70,120,210),[
   ("usa",7003,None,"미국은 AI 리터러시를 말합니다"),
   ("usa_b2",7103,"a close up of a child's hand holding a magnifying glass over a glowing AI answer with a question mark, inspecting carefully","많이 쓰기가 아니라, 이해하고 의심하기"),
   ("usa_b3",7203,"a student erasing and rewriting on paper next to a glowing AI screen, correcting and improving, focused","그리고, 고쳐 쓰는 힘")]),
 ("uk","영국 · 판단은 사람",(90,110,180),[
   ("uk",7004,None,"영국은 분명히 선을 긋습니다"),
   ("uk_b2",7104,"a large balance scale, one side a small AI chip, the other side a glowing human head silhouette that is heavier and lower, thoughtful","AI는 도구, 판단은 사람"),
   ("uk_b3",7204,"a human hand signing a document deciding, while a polite AI robot waits beside, responsibility, warm office","최종 책임은 사람에게 남습니다")]),
 ("sg","싱가포르 · 가드레일",(230,110,70),[
   ("sg",7005,None,"싱가포르는 가드레일을 둡니다"),
   ("sg_b2",7105,"students using tablets calmly inside a soft glowing rounded fence guardrail, a teacher supervising with a gentle smile, tidy classroom","쓰게 하되, 안전한 틀 안에서"),
   ("sg_b3",7205,"a bright thought bubble above a child staying visible and glowing, not hidden behind an AI screen, protected imagination","아이 생각이 AI 뒤로 숨지 않게")]),
 ("kr","한국 · AI 디지털교과서",(70,140,210),[
   ("kr",7006,None,"한국, AI 디지털교과서가 학교로"),
   ("kr_b2",7106,"close up of a tablet showing a friendly AI digital textbook interface with a child's hands, bright modern classroom","학교가 AI를 들여오기 시작했습니다"),
   ("kr_b3",7206,"a split warm scene, left a school classroom with AI, right a home where a child uses an AI tablet alone, gentle contrast","하지만 학교 도입과 아이 습관은 다릅니다")]),
 ("common","공통점은 하나",(20,150,110),[
   ("common",7007,None,"다섯 나라의 공통점은 하나"),
   ("common_b2",7107,"a child confidently asking a glowing friendly AI a question, a speech bubble with a question mark, not afraid, warm","AI를 막는 게 아니라"),
   ("common_b3",7207,"an adult and a child looking at an AI answer together and nodding thoughtfully, guiding hand, cozy","질문하고, 판단하고, 다시 쓰는 힘")]),
 ("parent","AI는 도구, 곁엔 사람",(124,108,255),[
   ("parent",7008,None,"오늘, 집에서 시작할 수 있습니다"),
   ("parent_b2",7108,"a warm close up of a parent gently pointing at an AI screen and asking the child a question, cozy home evening","\"이상한 부분, 찾아볼까?\""),
   ("parent_b3",7208,"a parent and child smiling together in the warm evening, an AI device dimmed beside them, human warmth first","정답이 아니라, 다시 묻는 힘")]),
]
def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"aiedu2","images":["8",0]}}}
    cid=uuid.uuid4().hex
    pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":cid}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
    t0=time.time()
    while time.time()-t0<300:
        h=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
        if pid in h: break
        time.sleep(3)
    im=h[pid]["outputs"]["9"]["images"][0]
    q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
    open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read())
def overlay_png(title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    b=16
    for r in [(0,0,W,b),(0,H-b,W,H),(0,0,b,H),(W-b,0,W,H)]: d.rectangle(r,fill=(28,18,12,235))
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle([b,b,W-b,H-b],outline=(0,0,0,120),width=22)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    fs=46; f=F(fs)
    while d.textlength(title,font=f)>W-360 and fs>26: fs-=2; f=F(fs)
    tw=d.textlength(title,font=f); cx=W//2; y=34; pad=34; h=fs+28; x0,x1=cx-tw/2-pad,cx+tw/2+pad
    d.polygon([(x0-24,y+h/2),(x0,y+6),(x0,y+h-6)],fill=(150,96,52)); d.polygon([(x1+24,y+h/2),(x1,y+6),(x1,y+h-6)],fill=(150,96,52))
    d.rounded_rectangle([x0,y,x1,y+h],radius=12,fill=(245,232,205),outline=(150,96,52),width=4); d.text((cx-tw/2,y+13),title,font=f,fill=(60,40,20))
    cfs=42; cf=F(cfs)
    while d.textlength(caption,font=cf)>W-80 and cfs>24: cfs-=2; cf=F(cfs)
    cw=d.textlength(caption,font=cf); cxx=(W-cw)/2; cyy=H-cfs-48
    for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]: d.text((cxx+dx,cyy+dy),caption,font=cf,fill=(0,0,0))
    d.text((cxx,cyy),caption,font=cf,fill=(255,255,255)); im.save(out)
def segment(illust,ovl,d,out):
    run([FF,"-hide_banner","-loglevel","error","-y","-loop","1","-i",illust,"-loop","1","-i",ovl,"-t",f"{d}",
      "-filter_complex",f"[0:v]scale=1400:800,zoompan=z='min(zoom+0.0008,1.06)':d={int(d*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30[bg];[bg][1:v]overlay=0:0,format=yuv420p",
      "-c:v","libx264","-preset","veryfast","-crf","20","-r","30",out])
if __name__=="__main__":
    segs=[]; auds=[]
    for key,title,accent,beats in SEC:
        # 1.3배속 섹션 오디오
        sa=f"{TMP}/aud/{key}.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{AUD}/{key}.mp3","-filter:a",f"atempo={SPEED}",sa])
        sd=dur(sa); auds.append(sa); per=sd/len(beats)
        for subfile,seed,scene,cap in beats:
            ip=f"{ILL}/{subfile}.png"
            if scene and not os.path.exists(ip): print("  gen",subfile); sdxl(scene,seed,ip)
            op=f"{OVL}/v2_{subfile}.png"; overlay_png(title,cap,op)
            sp=f"{TMP}/seg/{subfile}.mp4"; segment(ip,op,per,sp); segs.append(sp)
        print(" sec",key,round(sd,2),"s ·",len(beats),"컷")
    vl=f"{TMP}/vlist.txt"; open(vl,"w",encoding="utf-8").write("\n".join(f"file '{s}'" for s in segs))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",vl,"-c:v","libx264","-preset","veryfast","-crf","20","-r","30",f"{TMP}/video.mp4"])
    al=f"{TMP}/alist.txt"; open(al,"w",encoding="utf-8").write("\n".join(f"file '{a}'" for a in auds))
    run([FF,"-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",al,"-c","copy",f"{TMP}/audio.mp3"])
    out=f"{A}/render/world-ai-education-illust-v2.mp4"
    run([FF,"-hide_banner","-loglevel","error","-y","-i",f"{TMP}/video.mp4","-i",f"{TMP}/audio.mp3",
      "-filter_complex","[0:v]tpad=stop_mode=clone:stop_duration=1.5[v];[1:a]apad=pad_dur=1.5[a]",
      "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","21","-c:a","aac","-b:a","192k","-shortest",out])
    print("illust-v2:",dur(out),"s ->",out)
