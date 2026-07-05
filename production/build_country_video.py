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
"uk": ("영국은 왜 커리큘럼보다 안전과 책임을 먼저 말했나",[
  ("영국 · 강제보다 안전과 책임","영국은 다른 나라처럼 AI를 강제 과목으로 밀어붙이지 않았습니다. 대신 아이가 AI를 안전하게 쓰는 규칙과, 최종 판단과 책임은 사람에게 남긴다는 원칙을 먼저 세웠습니다. 왜 이렇게 신중했을까요.",
   [("uk_s1a",6101,"a "+GB+"teacher gently guiding a young child using a friendly AI tablet in a warm bright classroom, safe and calm, storybook","영국은 안전한 규칙을 먼저"),
    ("uk_s1b",6102,"a warm glowing rulebook and a gentle shield beside a small friendly AI robot, safety first, storybook","판단과 책임은 사람에게")]),
  ("2023 · 첫 공식 입장","출발은 2023년입니다. 영국 교육부는 학교의 생성형 AI 사용에 대한 첫 공식 입장을 냈습니다. 막지도, 무작정 권하지도 않고, 투명하고 안전하게 쓰라는 방향이었죠.",
   [("uk_s2a",6103,"a "+GB+"education official placing a first friendly guidance document on a desk, a new beginning, warm office, storybook","2023 · 첫 생성형 AI 입장문"),
    ("uk_s2b",6104,"a "+GB+"teacher calmly reading a gentle guidance booklet in a staff room, thoughtful, storybook","막지도 권하지도 않고, 투명하게")]),
  ("2025 · 데이터와 평가를 챙기다","2025년 초, 가이드는 더 촘촘해졌습니다. 학생의 데이터를 보호하고, 시험에서 AI를 어떻게 다룰지, 교사의 업무 부담을 줄이는 방향까지 담겼습니다.",
   [("uk_s3a",6105,"a warm protective bubble around a child's personal data and notebook, data protection, gentle storybook","학생 데이터를 지키고"),
    ("uk_s3b",6106,"a fair balanced scale beside an exam paper and a small AI helper, honesty in tests, storybook","시험에서 AI를 어떻게 다룰지")]),
  ("2025 · 아이 안전을 먼저","같은 해, 아동 안전 지침에도 AI가 들어갔습니다. AI가 만든 유해한 콘텐츠나 괴롭힘으로부터 아이를 지키는 것이 먼저라는 뜻입니다.",
   [("uk_s4a",6107,"a big warm umbrella sheltering a "+GB+"child who is safely using a tablet, protection from harm, storybook","아이 안전이 먼저")]),
  ("경계 · 무엇이 내 것인가","시험 기관은 과제와 평가에서 AI 사용의 경계를 정했습니다. 핵심은 하나였습니다. 무엇이 아이가 한 것이고, 무엇이 AI가 한 것인지 구분하는 것.",
   [("uk_s5a",6108,"a "+GB+"child's drawing hand and a glowing AI hand clearly separated by a soft line, whose work is whose, storybook","무엇이 내 것, 무엇이 AI 것")]),
  ("현장의 과제 · 준비","물론 쉽지만은 않습니다. 아직 많은 교사가 AI 조언에 자신이 없고, AI가 어떻게 작동하는지 가르치는 학교는 다섯 곳 중 한 곳 정도였습니다. 그래서 영국은 속도보다 준비를 택했습니다.",
   [("uk_s6a",6109,"a "+GB+"teacher patiently learning how AI works, step by step, determined and warm, storybook","속도보다 준비를 택했습니다")]),
  ("그럼, 한국 가정은","한국 가정도 배울 게 있습니다. 쓰는 법을 서두르기보다, 결정을 아이가 하게 하고, 이 답에 대한 네 생각은 어떠냐고 한 번 더 묻는 습관입니다.",
   [("uk_s7a",6110,"a "+KR+"parent and child looking at an AI answer together, the child pointing and deciding, warm home, storybook","결정은 아이가, '네 생각은?'")]),
  ("그럼 아이는","그러면 아이는, AI 말을 그대로 따르지 않고 스스로 판단하는 아이, 무엇이 자기 생각인지 아는 아이로 자랍니다. 영국이 제도로 지키려 한 것을, 우리는 집에서 대화로 기릅니다.",
   [("uk_s8a",6111,"a confident "+KR+"child keeping their own idea while gently using AI, self-judging and calm, hopeful storybook","스스로 판단하는 아이로")]),
]),
"singapore": ("싱가포르는 왜 아이에게 AI 가드레일을 먼저 채웠나",[
  ("싱가포르 · 균형을 먼저","싱가포르는 AI를 빨리 쓰게 하기보다, 아이 생각이 AI 뒤로 숨지 않도록 균형을 먼저 설계했습니다. 그 균형을 나라 전체가 하나의 전략으로 묶었죠.",
   [("sg_s1a",6201,"a "+SG+"child learning with an AI tablet inside a gentle safe railing, balanced and protected, bright classroom, storybook","아이 생각이 AI 뒤로 숨지 않게"),
    ("sg_s1b",6202,"a bright thought bubble glowing above a "+SG+"child, their own idea staying visible in front of the AI screen, storybook","균형을 먼저 설계")]),
  ("2019 · 국가 AI 전략","시작은 2019년, 국가 AI 전략입니다. 싱가포르는 AI를 나라 경쟁력의 축으로 삼고, 교육을 그 전략의 한 부분으로 함께 설계했습니다.",
   [("sg_s2a",6203,"a friendly national blueprint of a smart city with AI, a hopeful rising plan, warm storybook","2019 · 국가 AI 전략")]),
  ("2023 · 전략 2.0","2023년에는 국가 AI 전략 2.0으로 확장했습니다. 더 빠른 기술만이 아니라, 사회 전체의 신뢰와 안전을 함께 키우겠다는 방향이었죠.",
   [("sg_s3a",6204,"an upgraded glowing plan with a heart of trust and a shield of safety at its center, storybook","2023 · 신뢰와 안전을 함께")]),
  ("EdTech 2030 · 교실로","그 전략은 교실로 내려옵니다. 에듀테크 마스터플랜 2030은 학습에 AI를 책임 있게 통합하는 로드맵입니다.",
   [("sg_s4a",6205,"a warm classroom of the future with gentle AI helpers guided by a teacher, storybook","교실로 내려온 로드맵")]),
  ("적응형 학습 · 개인화","학교에서는 적응형 학습 시스템이 쓰입니다. 아이마다 속도와 난이도를 맞춰주되, 교사가 늘 곁에서 안내합니다.",
   [("sg_s5a",6206,"a "+SG+"child following a personalized glowing learning path while a teacher watches warmly beside, storybook","아이마다 맞춤, 교사가 곁에")]),
  ("네 원칙 · 가드레일","그 중심에는 네 원칙이 있습니다. 주도성, 포용, 공정, 그리고 안전. 아이는 AI를 배우고, 쓰고, 함께 배우고, 그리고 넘어서는 힘까지 익힙니다.",
   [("sg_s6a",6207,"four warm guiding pillars around a happy "+SG+"child using AI safely, agency inclusivity fairness safety, storybook","주도성·포용·공정·안전"),
    ("sg_s6b",6208,"a "+SG+"child putting down the tablet to think on their own, going beyond AI, storybook","쓰고, 함께 배우고, 넘어서기")]),
  ("그럼, 한국 가정은","한국 가정도 배울 게 있습니다. 많이보다 알맞게, 그리고 네 생각 먼저를 앞에 두는 것. AI도 한쪽으로 치우칠 수 있다고 함께 이야기하는 것입니다.",
   [("sg_s7a",6209,"a "+KR+"parent and child setting a gentle timer and talking before using AI together, balanced, warm home, storybook","많이보다 알맞게, 네 생각 먼저")]),
  ("그럼 아이는","그러면 아이는, AI를 쓰되 자기 생각을 잃지 않는, 균형 잡힌 아이로 자랍니다. 싱가포르가 나라로 세운 가드레일을, 우리는 집에서 대화로 세웁니다.",
   [("sg_s8a",6210,"a balanced happy "+KR+"child holding both a book and a small AI device, keeping their own voice, hopeful storybook","자기 생각을 잃지 않는 아이로")]),
]),
"korea": ("한국은 AI교과서를 넣었다 뺐다, 그래서 가정이 답이다",[
  ("한국 · 서울에서 울린 경고음","2016년, 알파고가 이세돌을 이긴 곳은 서울이었습니다. AI 시대의 경고음은 우리 한복판에서 울렸고, 한국도 학교를 바꾸려 움직였습니다.",
   [("kr_s1a",6301,"a quiet solemn scene of a person facing a soft glowing AI light in Seoul, the alarm of the AI era, storybook","2016 · 서울에서 울린 경고음"),
    ("kr_s1b",6302,"a "+KR+"school preparing to change, hopeful morning light, storybook","한국도 학교를 바꾸려 움직였다")]),
  ("2023 · 디지털 교육혁신","2023년, 교육부는 디지털 기반 교육혁신 방안을 발표했습니다. 그 중심에 AI 디지털교과서가 있었습니다.",
   [("kr_s2a",6303,"a friendly national plan poster about digital education reform, hopeful, warm storybook","2023 · 디지털 교육혁신 방안")]),
  ("2024 · 도입 확정","2024년 말, 2025년부터 수학·영어·정보 과목에 AI 디지털교과서를 넣기로 확정했습니다. 다만 디지털 과몰입을 걱정하는 목소리도 함께 나왔죠.",
   [("kr_s3a",6304,"glowing AI digital textbooks on tablets ready for a "+KR+"classroom, hopeful but a small worry cloud above, storybook","2024 · 도입 확정, 과몰입 우려도")]),
  ("2025.3 · 교실에 들어오다","2025년 3월, AI 디지털교과서가 초등 3·4학년과 중1, 고1 교실에 들어왔습니다. 아이마다 맞춤 학습을 내세웠습니다.",
   [("kr_s4a",6305,"a "+KR+"classroom of children using new glowing AI tablets, personalized learning, bright, storybook","2025.3 · 교실에 들어오다")]),
  ("2025 여름 · 한 걸음 뒤로","그런데 넉 달 만에, 교사와 학부모의 반발 속에서 국회는 AI 디지털교과서를 핵심 교재에서 보조 교재로 되돌렸습니다.",
   [("kr_s5a",6306,"a "+KR+"AI tablet being gently set aside back beside a paper book, a step back, thoughtful mood, storybook","넉 달 만에 보조교재로")]),
  ("흔들린 도입 · 왜","채택률은 첫 학기 37퍼센트에서 다음 학기 19퍼센트로 떨어졌습니다. 준비보다 속도가 앞섰고, 과몰입 걱정이 컸기 때문입니다.",
   [("kr_s6a",6307,"a wobbly path with numbers falling, a "+KR+"school unsure, thoughtful muted storybook","채택률 37에서 19로")]),
  ("그래서, 가정이 답이다","하지만 어떤 교과서 논쟁과도 무관하게, 아이의 다시 묻는 힘은 가정이 지킬 수 있습니다. 학교 정책은 바뀌어도, 저녁의 대화는 바뀌지 않으니까요.",
   [("kr_s7a",6308,"a warm "+KR+"home evening, a parent and child talking about an AI answer together, steady and cozy, storybook","'다시 묻는 힘'은 가정이 지킨다")]),
  ("그럼 아이는","그러면 아이는, 학교가 흔들려도 스스로 확인하고 다시 묻는 힘을 잃지 않습니다. 나라가 못다 지킨 것을, 우리는 집에서 대화로 기릅니다.",
   [("kr_s8a",6309,"a "+KR+"child confidently finding a mistake in an AI answer and re-asking with a smile, hopeful storybook","스스로 확인하고 다시 묻는 아이로")]),
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
