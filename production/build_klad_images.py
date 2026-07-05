#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""잃어버린 AI 10년 v3 배경을 '실사'에서 '그림체 일러스트'로 재생성.
장면: 이세돌·알파고 바둑(뒤모습·실루엣, 실존인물 얼굴 금지) / 중국 아이→성인 AI비전 / 한국 K팝→5차산업 뒤처짐→청년 비전상실.
ComfyUI(8188) SDXL. 산출: assets/korea-lost-decade/simg/main_{idx}.png (klad_v3가 읽음).
※Ollama 언로드 후 실행(VRAM). 사용: python build_klad_images.py [--force]"""
import json, os, sys, time, urllib.request, urllib.error
REPO="C:/Users/admin/Desktop/ai-craft-kids"; SIMG=f"{REPO}/assets/korea-lost-decade/simg"
SRV="http://127.0.0.1:8188"; CKPT="animagine-xl-3.1.safetensors"  # 일러스트 전용 모델(실사 방지)
os.makedirs(SIMG,exist_ok=True); FORCE="--force" in sys.argv
STYLE=("masterpiece, best quality, detailed illustration, semi-realistic anime art, painterly, "
       "muted serious color palette, cinematic dramatic lighting, thick clean outlines, "
       "dignified documentary poster illustration, hopeful undertone, no text, no watermark")
NEG=("lowres, worst quality, low quality, jpeg artifacts, photograph, photo, photorealistic, dslr, 3d render, "
     "chess, chess pieces, horror, creepy, scary, gore, bad anatomy, bad hands, extra digits, deformed, "
     "close-up, face portrait, character sheet, multiple panels, grid, collage, split image, "
     "text, letters, words, korean text, chinese text, watermark, logo, signature, blurry")
# region 민족 프롬프트 (뒤모습·소품 위주라 얼굴 최소)
KR="Korean, black hair, "; CN="Chinese, black hair, "
SCENES={
 0: "wide cinematic establishing shot, a lone young "+KR+"youth in a long coat seen from behind standing small on a rooftop at dusk, a vast city skyline fading into the dark ahead, ten years slipping away, solemn, scenery focus, no face",
 1: "wide night skyline of Seoul, tall towers, a single glowing red warning beacon high over the city, tiny people far below, symbolic alarm of the AI era, atmospheric, scenery focus, no face",
 2: "wide shot from behind, a "+KR+"man in a suit seen from behind (back of head, no face) sitting at a low table, a large square wooden go board with round black and white go stones filling the foreground, a cold blue machine glow across the table, single dramatic spotlight, solemn, scenery focus",
 3: "wide scene, a small "+CN+"child in school uniform seen from behind at a desk, a long bright road and a futuristic city stretching far ahead, hopeful determined first step, morning light, scenery focus, no face",
 6: "wide inspiring establishing shot, a "+CN+"student seen from behind looking up at an enormous glowing wall of AI screens, robots and a bright future city, rising staircase of growth, national effort, scenery focus, no face",
 7: "wide shot of a dazzling K-pop concert stage exploding with bright spotlights, tiny idol silhouettes on a huge stage, a vast cheering crowd seen from behind, glittering but hollow, scenery focus, no face",
 8: "wide scene, "+KR+"schoolchildren seen from behind in a dim classroom facing an old chalkboard, a bright AI future city glowing unreachable behind a tall wall, left behind, contrast of light and shadow, scenery focus, no face",
 9: "wide melancholic scene, a tired young "+KR+"job-seeker in a suit seen from behind sitting alone at night, a scattered stack of rejected papers, a dim room, a lost distant city horizon through the window, quiet despair, scenery focus, no face",
 10: "wide dramatic scene, a broken bridge over a dark chasm, a small lone "+KR+"figure seen from behind on the near side, a glowing AI future city on the far unreachable side, the gap of a lost decade, aching, scenery focus, no face",
 11: "wide symbolic scene, a "+KR+"child seen from behind at a fork in a road, one dim path of glowing screens to consume, one bright path of building and creating with AI, hopeful light on the bright path, scenery focus, no face",
}
def sdxl(scene,seed,out):
    wf={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":CKPT}},
        "5":{"class_type":"EmptyLatentImage","inputs":{"width":832,"height":1216,"batch_size":1}},
        "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+STYLE,"clip":["4",1]}},
        "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
        "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":32,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
        "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
        "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"klad","images":["8",0]}}}
    for attempt in range(3):
        try:
            data=json.dumps({"prompt":wf}).encode()
            pid=json.load(urllib.request.urlopen(urllib.request.Request(f"{SRV}/prompt",data=data,headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
            ok=None
            for _ in range(200):
                time.sleep(1.5)
                h=json.load(urllib.request.urlopen(f"{SRV}/history/{pid}",timeout=30))
                if pid in h and h[pid].get("outputs"):
                    im=h[pid]["outputs"]["9"]["images"][0]; ok=im; break
            if not ok: raise TimeoutError("comfy timeout")
            url=f"{SRV}/view?filename={urllib.parse.quote(ok['filename'])}&subfolder={ok.get('subfolder','')}&type={ok.get('type','output')}"
            open(out,"wb").write(urllib.request.urlopen(url,timeout=30).read())
            print(f"  [ok] main_{out.split('main_')[1].split('.')[0]}"); return
        except Exception as e:
            print(f"  [재시도 {attempt+1}/3] {out}: {repr(e)[:70]}"); time.sleep(6)
    raise RuntimeError(f"sdxl 3회 실패: {out}")
import urllib.parse
if __name__=="__main__":
    todo=[(i,SCENES[i]) for i in sorted(SCENES)]
    print(f"그림체 재생성 {len(todo)}장 (그림/일러스트, 실존인물 얼굴 없음)…")
    for i,scene in todo:
        out=f"{SIMG}/main_{i}.png"
        if os.path.exists(out) and not FORCE: print(f"  [skip] main_{i} (있음, --force로 덮어쓰기)"); continue
        sdxl(scene,3300+i*17,out)
    print("완료 — 이제 build_klad_v3.py C 로 영상 재조립")
