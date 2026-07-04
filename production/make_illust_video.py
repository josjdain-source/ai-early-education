#!/usr/bin/env python3
"""★무인 양산기: 주제 → 영상.
 로컬 LLM(Ollama gemma2:9b)이 대본·영어이미지프롬프트·한글자막 생성
 → 로컬 SDXL(ComfyUI) 일러스트 → Pillow 오버레이 → edge-tts(1.3배속) → ffmpeg 조립.
사용: python make_illust_video.py "AI가 숙제를 대신 해줄 때, 부모가 해야 할 일"
"""
import sys, os, json, time, uuid, re, subprocess, urllib.request, urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OLLAMA="http://127.0.0.1:11435"; OLLAMA_MODEL="gemma2:9b"
COMFY="http://127.0.0.1:8188"; CKPT="RealVisXL_V5.0_fp16.safetensors"
VENV=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"; A=f"{BASE}/assets/world-ai-education-5min"
HERE=os.path.dirname(os.path.abspath(__file__)); KB=r"C:\Windows\Fonts\malgunbd.ttf"
SPEED=1.3; N_SEC=6; N_BEAT=3
STYLE=("editorial storybook illustration, warm muted color palette, thick clean black outlines, "
 "semi-realistic cartoon style, flat shading, soft warm lighting, detailed cozy background, hand-drawn look, wide cinematic composition")
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, signature, logo, "
 "ugly, deformed, extra fingers, bad hands, blurry, low quality, creepy, scary, weapon")
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

def plan(topic):
    schema=('{"sections":[{"title":"한글 14자 이내 강한 제목","narration":"한글 2~3문장 내레이션(구어체, 성우가 읽음)",'
      '"beats":[{"prompt":"english scene description of a warm storybook illustration, people and setting and a visual metaphor, NO text",'
      '"caption":"한글 22자 이내 핵심 한 줄"}]}]}')
    p=(f"너는 부모 대상 교육영상 기획자다. 주제: '{topic}'.\n"
      f"정확히 {N_SEC}개 섹션, 각 섹션마다 정확히 {N_BEAT}개 beat로 구성해라.\n"
      "1번 섹션=강한 후크(질문), 마지막 섹션=오늘 부모가 할 행동+마무리.\n"
      "각 beat.prompt는 영어로, 따뜻한 스토리북 일러스트의 '장면'만 묘사(인물·배경·은유). 화면에 글자/텍스트는 넣지 마라.\n"
      "각 beat.caption은 한글 한 줄. narration은 그 섹션 자막들을 자연스러운 구어체로 이은 것.\n"
      "과장/공포/특정국 비하 금지. 정직하고 따뜻하게.\n"
      f"아래 JSON 스키마로만 출력:\n{schema}")
    body={"model":OLLAMA_MODEL,"prompt":p,"format":"json","stream":False,
          "keep_alive":0,   # ★기획 끝나면 즉시 VRAM에서 언로드(SDXL 자리 확보)
          "options":{"temperature":0.7,"num_predict":4096}}
    r=urllib.request.urlopen(urllib.request.Request(OLLAMA+"/api/generate",
        data=json.dumps(body).encode(),headers={"Content-Type":"application/json"}),timeout=300)
    resp=json.load(r)["response"]
    try: data=json.loads(resp)
    except Exception:
        m=re.search(r"\{.*\}",resp,re.S); data=json.loads(m.group(0))
    secs=data["sections"][:N_SEC]
    for s in secs:
        s["beats"]=(s.get("beats") or [])[:N_BEAT]
        while len(s["beats"])<N_BEAT: s["beats"].append(s["beats"][-1] if s["beats"] else {"prompt":"a warm classroom","caption":s.get("title","")})
    while len(secs)<N_SEC: secs.append(secs[-1])
    return secs

def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":28,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"auto","images":["8",0]}}}
    cid=uuid.uuid4().hex
    pid=json.load(urllib.request.urlopen(urllib.request.Request(COMFY+"/prompt",data=json.dumps({"prompt":g,"client_id":cid}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
    t0=time.time()
    while time.time()-t0<300:
        h=json.load(urllib.request.urlopen(COMFY+f"/history/{pid}",timeout=30))
        if pid in h: break
        time.sleep(3)
    im=h[pid]["outputs"]["9"]["images"][0]
    q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
    open(out,"wb").write(urllib.request.urlopen(COMFY+"/view?"+q,timeout=30).read())

def overlay_png(title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); b=16
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

def tts(text,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([VENV,os.path.join(HERE,"_tts_synth.py"),tf,out])

def main(topic):
    stamp=time.strftime("%m%d-%H%M"); slug=re.sub(r"[^A-Za-z0-9]+","",topic)[:16] or "topic"
    work=f"C:/Users/admin/AppData/Local/Temp/claude/auto_{stamp}"
    for sub in ("img","ovl","aud","seg"): os.makedirs(f"{work}/{sub}",exist_ok=True)
    print(f"[1/4] 기획(LLM)… 주제='{topic}'")
    secs=plan(topic)
    outdir=f"{A}/auto/{slug}-{stamp}"; os.makedirs(outdir,exist_ok=True)
    json.dump({"topic":topic,"sections":secs},open(f"{outdir}/plan.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"  섹션 {len(secs)}개 · 컷 {len(secs)*N_BEAT}개")
    for si,s in enumerate(secs):
        title=s["title"][:16]
        raw=f"{work}/aud/s{si}_raw.mp3"; tts(s["narration"],raw)
        sa=f"{work}/aud/s{si}.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={SPEED}",sa])
        sd=dur(sa); print(f"  [{si+1}/{len(secs)}] {title} · {sd:.1f}s")
        for bi,bt in enumerate(s["beats"]):
            ip=f"{work}/img/s{si}b{bi}.png"; sdxl(bt["prompt"],7000+si*10+bi,ip)
            op=f"{work}/ovl/s{si}b{bi}.png"; overlay_png(title,bt["caption"][:24],op)
        # 대표 이미지 보관
        if os.name=="nt":
            run(["cmd","/c","copy","/y",f"{work}/img/s{si}b0.png".replace("/","\\"),f"{outdir}/s{si}.png".replace("/","\\")])
    # ★조립 = 정적 이미지 + 크로스페이드 디졸브(zoompan 지진 제거)
    out=f"{A}/render/auto-{slug}-{stamp}.mp4"
    import reassemble_dissolve as RD
    RD.build(work, out)
    print(f"[4/4] 완성: {out} · {dur(out):.1f}s · plan={outdir}/plan.json")
    return out

if __name__=="__main__":
    topic=" ".join(sys.argv[1:]) or "AI가 숙제를 대신 해줄 때, 부모가 해야 할 일"
    main(topic)
