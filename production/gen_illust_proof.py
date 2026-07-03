#!/usr/bin/env python3
"""참고영상 스타일 증명: 로컬 SDXL(RealVisXL, ComfyUI)로 개념 일러스트 1장 생성(텍스트 없이).
주제=AI를 아이에게 어떻게: 부모가 옆에서 함께(판단은 사람). 16:9. 이후 Pillow로 한글 오버레이."""
import json, time, uuid, os, urllib.request, urllib.parse
SRV="http://127.0.0.1:8188"
OUT="assets/world-ai-education-5min/illust"; os.makedirs(OUT,exist_ok=True)
POS=("editorial storybook illustration, warm muted color palette, thick clean black outlines, "
 "semi-realistic cartoon style, flat shading, a Korean parent and a young child sitting together "
 "at a cozy home study desk, looking at a friendly glowing AI assistant screen and small robot, "
 "the parent gently pointing and guiding the child who is curious, warm bookshelves, soft window light, "
 "wide cinematic composition, detailed background, hand-drawn look, framed illustration")
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, signature, "
 "ugly, deformed, extra fingers, bad hands, blurry, low quality, creepy, scary")
def graph(seed):
    return {
 "4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
 "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
 "6":{"class_type":"CLIPTextEncode","inputs":{"text":POS,"clip":["4",1]}},
 "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
 "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m",
      "scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
 "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
 "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"aiedu_illust","images":["8",0]}}}
def post(path,data):
    r=urllib.request.urlopen(urllib.request.Request(SRV+path,data=json.dumps(data).encode(),
      headers={"Content-Type":"application/json"}),timeout=30); return json.load(r)
def get(path):
    return json.load(urllib.request.urlopen(SRV+path,timeout=30))
if __name__=="__main__":
    cid=uuid.uuid4().hex; seed=20260704
    pid=post("/prompt",{"prompt":graph(seed),"client_id":cid})["prompt_id"]
    print("queued",pid,"· 생성 대기(SDXL)...")
    t0=time.time()
    while time.time()-t0<600:
        h=get(f"/history/{pid}")
        if pid in h: break
        time.sleep(3)
    else: raise SystemExit("타임아웃")
    outs=h[pid]["outputs"]["9"]["images"][0]
    q=urllib.parse.urlencode({"filename":outs["filename"],"subfolder":outs.get("subfolder",""),"type":outs["type"]})
    data=urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read()
    p=os.path.join(OUT,"aiedu-concept-raw.png"); open(p,"wb").write(data)
    print(f"생성 완료 {time.time()-t0:.0f}s ->",p, len(data),"bytes")
