# -*- coding: utf-8 -*-
"""1편 영상 오프닝(0~약8초) — 실사 이미지 A/B/C + 메인 문구 타이틀.
사용자 1번 승인: 오프닝용 새 TTS 생성 허용(craft_narrator, 본편과 동일 보이스).
본편(ep01_door_sign_tail_audio_sync_fixed.mp4, 검수 통과 음성)은 건드리지 않고 앞에만 붙임.
산출: assets/audio/ep01/op01~04.wav, opening_full.wav,
      assets/video/ep01_door_sign_opening_candidate.mp4 (오프닝+본편)
기존 파일 전부 보존. 자동 업로드 없음."""
import os, wave, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
AUD = os.path.join(ROOT, "assets", "audio", "ep01"); os.makedirs(AUD, exist_ok=True)
VID = os.path.join(ROOT, "assets", "video")
TMP = os.path.join(VID, "_frames_opening"); os.makedirs(TMP, exist_ok=True)
BODY = os.path.join(VID, "ep01_door_sign_tail_audio_sync_fixed.mp4")  # 검수 통과 본편
FB = r"C:\Windows\Fonts\malgunbd.ttf"; FR = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1080, 1920
PAUSE = 0.25
SPEED = 1.08  # craft_narrator preset (본편과 동일)

# 오프닝 컷: A/B/C 실사 + 메인 타이틀
CUTS = [
    dict(n=1, kind="photo", img="process-a-ask.png",
         narration="아이 혼자 AI에게 물어봐요.", caption="아이 혼자 AI에게 물어봐요"),
    dict(n=2, kind="photo", img="process-b-together.png",
         narration="엄마와 함께 결과를 보고,", caption="엄마와 함께 결과를 보고"),
    dict(n=3, kind="photo", img="process-c-result.png",
         narration="마음에 드는 결과를 골라요.", caption="마음에 드는 결과를 골라요"),
    dict(n=4, kind="title",
         narration="생성형 AI, 어렵게 배우지 말고, 아이와 함께 대화하며 시작해 보세요.",
         title=["생성형 AI, 어렵게 배우지 말고", "아이와 함께 대화하며 시작해 보세요"]),
]

def f(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()
def grad(top, bot):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y/H; d.line([(0,y),(W,y)], fill=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3)))
    return im
def ctext(d, cx, y, lines, font, fill, lh):
    for ln in lines:
        w = d.textlength(ln, font=font); d.text((cx-w/2, y), ln, font=font, fill=fill); y += lh
def contained(canvas, path, box):
    im = Image.open(path).convert("RGBA"); x0,y0,x1,y1 = box
    sc = min((x1-x0)/im.width, (y1-y0)/im.height)
    im2 = im.resize((max(1,int(im.width*sc)), max(1,int(im.height*sc))), Image.LANCZOS)
    canvas.paste(im2, (int(x0+((x1-x0)-im2.width)/2), int(y0+((y1-y0)-im2.height)/2)), im2)

# ---------- 1) 오프닝 TTS (승인된 신규 생성 / 이미 있으면 재사용) ----------
def gen_audio():
    full = os.path.join(AUD, "opening_full.wav")
    existing = [os.path.join(AUD, f"op{c['n']:02d}.wav") for c in CUTS]
    if os.path.exists(full) and all(os.path.exists(p) for p in existing):
        durs = []
        for p in existing:
            with wave.open(p) as w:
                durs.append(round(w.getnframes()/float(w.getframerate()), 3))
        print("  (기존 오프닝 음성 재사용 — TTS 재생성 안 함)")
        return durs, full
    from melo.api import TTS
    model = TTS(language="KR", device="cpu")
    spk = model.hps.data.spk2id
    sid = spk["KR"] if "KR" in spk else list(spk.values())[0]
    durs = []
    for c in CUTS:
        raw = os.path.join(AUD, f"op{c['n']:02d}_raw.wav")
        out = os.path.join(AUD, f"op{c['n']:02d}.wav")
        model.tts_to_file(c["narration"], sid, raw, speed=SPEED)
        subprocess.run([FF,"-y","-i",raw,"-af",f"apad=pad_dur={PAUSE}",out],
                       check=True, capture_output=True)
        with wave.open(out) as w:
            d = w.getnframes()/float(w.getframerate())
        durs.append(round(d,3)); os.remove(raw)
        print(f"  op{c['n']:02d}: {d:.3f}s  {c['narration'][:22]}")
    lst = os.path.join(AUD, "op_concat.txt")
    with open(lst,"w",encoding="utf-8") as fh:
        for c in CUTS:
            fh.write(f"file '{os.path.join(AUD, f'op{c[chr(0x6e)]:02d}.wav').replace(os.sep,'/')}'\n")
    full = os.path.join(AUD, "opening_full.wav")
    subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,full], check=True, capture_output=True)
    return durs, full

# ---------- 2) 렌더 ----------
def render(c):
    im = grad((255,243,228),(253,246,238)); d = ImageDraw.Draw(im)
    ctext(d, W/2, 110, ["아이와 함께 배우는 생성형 AI"], f(FB,40), (200,150,90), 50)
    if c["kind"] == "photo":
        card = [90,360,W-90,1180]; d.rounded_rectangle(card, radius=40, fill=(255,255,255))
        contained(im, os.path.join(ROOT,"assets",c["img"]), (card[0]+40,card[1]+40,card[2]-40,card[3]-40))
        size = 70; maxw = W-96
        while size>44 and d.textlength(c["caption"], font=f(FB,size))>maxw: size -= 3
        cw = d.textlength(c["caption"], font=f(FB,size)); d.text((W/2-cw/2,1448), c["caption"], font=f(FB,size), fill=(58,50,44))
    else:  # title
        size = 66; maxw = W-110
        while size>40 and max(d.textlength(ln, font=f(FB,size)) for ln in c["title"])>maxw: size -= 2
        lh = int(size*1.42); total = len(c["title"])*lh
        ctext(d, W/2, H/2-total/2-40, c["title"], f(FB,size), (58,50,44), lh)
        sub = "사진 한 장으로 감정 캐릭터를 만들고, 함께 대화하며"
        ctext(d, W/2, H/2-total/2-40+total+24, [sub], f(FR,40), (150,120,90), 50)
    p = os.path.join(TMP, f"op_{c['n']}.png"); im.save(p); return p

def assemble(durs, audio):
    frames = [render(c) for c in CUTS]
    lst = os.path.join(TMP, "op_list.txt")
    with open(lst,"w",encoding="utf-8") as fh:
        for i,c in enumerate(CUTS):
            fh.write(f"file '{frames[i].replace(os.sep,'/')}'\nduration {durs[i]}\n")
        fh.write(f"file '{frames[-1].replace(os.sep,'/')}'\n")
    total = round(sum(durs), 3)
    opvonly = os.path.join(TMP, "_opening_vonly.mp4")
    opening = os.path.join(VID, "_opening_only.mp4")
    subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,"-t",str(total),
                    "-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast",opvonly],
                   check=True, capture_output=True)
    subprocess.run([FF,"-y","-i",opvonly,"-i",audio,"-c:v","copy","-c:a","aac","-b:a","192k",
                    "-shortest",opening], check=True, capture_output=True)
    print("[OK] opening", os.path.getsize(opening), "B,", total, "s")
    # 본편과 이어붙이기(필터 concat: 본편 음성은 그대로 사용, 컨테이너만 재인코딩)
    out = os.path.join(VID, "ep01_door_sign_opening_candidate.mp4")
    subprocess.run([FF,"-y","-i",opening,"-i",BODY,"-filter_complex",
                    "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                    "-map","[v]","-map","[a]","-r","30","-c:v","libx264","-preset","veryfast",
                    "-c:a","aac","-b:a","192k",out], check=True, capture_output=True)
    print("[OK]", out, os.path.getsize(out), "B")
    return out

if __name__ == "__main__":
    print("1) 오프닝 TTS 생성(승인됨)...")
    durs, full = gen_audio()
    print("2) 오프닝 렌더 + 본편 결합...")
    assemble(durs, full)
    print("DONE")
