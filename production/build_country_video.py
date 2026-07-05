#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""영국·싱가포르·한국 AI교육 롱폼 — 세계영상(build_illust_video_v2) 정본 방식.
RealVisXL 스토리북 그림체 + 문장매칭 그림 + 타이틀배너 + 차분한 내레이션 + 디졸브. 16:9.
★그나라→한국가정→아이효과 3단 완결. Ollama 언로드 후 실행(VRAM).
산출: assets/{c}-ai-education/render/{c}-ai-longform.mp4 · 사용: python build_country_video.py [uk singapore korea]"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
EDGE=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"; HERE=f"{BASE}/production"
TMP="C:/Users/admin/AppData/Local/Temp/claude/cvid"
KB=r"C:\Windows\Fonts\malgunbd.ttf"; VOICE="ko-KR-InJoonNeural"; SPEED=1.12
STYLE=("editorial storybook illustration, warm muted color palette, thick clean black outlines, "
 "semi-realistic cartoon style, flat shading, soft warm lighting, detailed cozy background, hand-drawn look, wide cinematic composition")
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, signature, logo, "
 "ugly, deformed, extra fingers, bad hands, blurry, low quality, creepy, scary, surveillance, weapon")
GB="British, diverse ethnicities, "; SG="Singaporean, multicultural Asian, "; KR="Korean, black hair, "
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

# 나라별: (key, title, accent, [ (sec_title, narration, [(subfile,seed,scene,caption)]) ])
COUNTRIES={
"uk": ("영국은 왜 안전과 책임을 먼저 말했나",[
  ("영국 · 안전과 책임을 먼저","영국은 AI를 강제 과목으로 밀지 않았습니다. 대신 안전하게 쓰는 규칙과, 최종 판단과 책임은 사람에게 남기는 원칙을 먼저 세웠죠.",
   [("uk_l1",6101,"a "+GB+"teacher gently guiding a child using a friendly AI tablet in a warm classroom, safe and calm, storybook","영국은 안전한 규칙을 먼저 세웠습니다"),
    ("uk_l2",6102,"a "+GB+"person's hand thoughtfully signing a decision while a polite AI robot waits beside, responsibility stays with people, warm office, storybook","최종 판단과 책임은 사람에게")]),
  ("그럼, 한국 가정은","한국 가정도 같습니다. 쓰는 법보다, 결정을 아이가 하게 하는 습관이 먼저입니다.",
   [("uk_l3",6103,"a "+KR+"parent and child looking at an AI answer together, the child pointing and deciding, warm home, storybook","결정은 아이가 하게")]),
  ("그럼 아이는","그러면 아이는, AI 말을 그대로 따르지 않고 '내 생각은 어때?'를 먼저 묻는, 스스로 판단하는 아이로 자랍니다.",
   [("uk_l4",6104,"a "+KR+"child thoughtfully comparing two ideas with a small glowing AI helper, confident and curious, storybook","스스로 판단하는 아이로")]),
]),
"singapore": ("싱가포르는 왜 AI 가드레일을 먼저 채웠나",[
  ("싱가포르 · 안전한 틀(가드레일)","싱가포르는 AI를 빨리 쓰게 하기보다, 아이 생각이 AI 뒤로 숨지 않도록 네 원칙으로 균형을 먼저 잡았습니다.",
   [("sg_l1",6201,"a "+SG+"child learning with an AI tablet inside a gentle safe railing, balanced and protected, bright classroom, storybook","네 원칙으로 균형을 먼저"),
    ("sg_l2",6202,"a bright thought bubble glowing above a "+SG+"child, the child's own idea staying visible in front of the AI screen, storybook","아이 생각이 AI 뒤로 숨지 않게")]),
  ("그럼, 한국 가정은","한국 가정도 '많이'보다 '알맞게', 그리고 '네 생각 먼저'를 앞에 둘 수 있습니다.",
   [("sg_l3",6203,"a "+KR+"parent and child setting a gentle timer and talking before using AI together, balanced use, warm home, storybook","많이보다 알맞게, 네 생각 먼저")]),
  ("그럼 아이는","그러면 아이는, AI를 쓰되 자기 생각을 잃지 않는, 균형 잡힌 아이로 자랍니다.",
   [("sg_l4",6204,"a "+KR+"balanced happy child holding both a book and a small AI device, keeping their own voice, storybook","자기 생각을 잃지 않는 아이로")]),
]),
"korea": ("한국은 AI교과서를 넣었다 뺐다, 그래서 가정이 답이다",[
  ("한국 · AI교과서, 넣었다 뺐다","한국은 AI 디지털교과서를 학교에 넣었다가, 넉 달 만에 보조교재로 물러섰습니다. 정책은 요동쳤죠.",
   [("kr_l1",6301,"a "+KR+"school classroom introducing glowing AI digital textbooks on tablets, hopeful but uncertain, storybook","AI 디지털교과서가 학교에 들어왔다가"),
    ("kr_l2",6302,"a "+KR+"scene of the AI tablet being gently set aside back to a paper book, a step back, thoughtful mood, storybook","넉 달 만에 보조교재로 물러섰습니다")]),
  ("그래서, 가정이 답이다","하지만 어떤 교과서 논쟁과도 무관하게, 아이의 '다시 묻는 힘'은 가정이 지킬 수 있습니다.",
   [("kr_l3",6303,"a warm "+KR+"home evening, a parent and child talking about an AI answer together, steady and cozy, storybook","'다시 묻는 힘'은 가정이 지킨다")]),
  ("그럼 아이는","그러면 아이는, 학교 정책이 흔들려도 스스로 확인하고 다시 묻는 힘을 잃지 않는 아이로 자랍니다.",
   [("kr_l4",6304,"a "+KR+"child confidently checking and re-asking, finding a mistake in an AI answer with a smile, storybook","스스로 확인하고 다시 묻는 아이로")]),
]),
}
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
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"cvid","images":["8",0]}}}
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
        except Exception as e: print(f"  [재시도 {attempt+1}/3] {out}: {repr(e)[:60]}"); time.sleep(6)
    raise RuntimeError("sdxl 실패: "+out)
def overlay_png(title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); b=16
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
def build_one(key):
    title,SEC=COUNTRIES[key]
    A=f"{BASE}/assets/{key}-ai-education"; ILL=f"{A}/illust/scenes"; OVL=f"{A}/illust/overlays"; RND=f"{A}/render"
    for p in (ILL,OVL,RND,f"{TMP}/{key}"): os.makedirs(p,exist_ok=True)
    sys.path.insert(0,HERE); import reassemble_dissolve as RD
    beats_all=[]; auds=[]
    for sec_title,narr,beats in SEC:
        raw=f"{TMP}/{key}/{beats[0][0]}_raw.mp3"; tts(narr,raw)
        sa=f"{TMP}/{key}/{beats[0][0]}.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={SPEED}",sa])
        sd=dur(sa); auds.append(sa); per=sd/len(beats)
        for subfile,seed,scene,cap in beats:
            ip=f"{ILL}/{subfile}.png"
            if not os.path.exists(ip): print("  gen",subfile); sdxl(scene,seed,ip)
            op=f"{OVL}/{subfile}.png"; overlay_png(sec_title,cap,op)
            beats_all.append((ip,op,per))
        print(" sec",sec_title[:16],round(sd,2),"s")
    out=f"{RND}/{key}-ai-longform.mp4"
    RD.assemble(beats_all,auds,out,f"{TMP}/{key}/dtmp")
    print(f"[{key}] {title} · {round(dur(out),1)}s -> {out}")
    return out
if __name__=="__main__":
    for k in (sys.argv[1:] or ["uk","singapore","korea"]):
        build_one(k)
