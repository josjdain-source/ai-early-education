# -*- coding: utf-8 -*-
"""2편 최종본 — "AI는 더 많은 아이에게 창작의 문을 열어줍니다" (약 60초, 1080x1920).
원칙: 제공된 GPT 이미지 7장을 원본 그대로 사용(사용자 지시: 크롭/삭제 금지).
      원본 보존 → 영상용 복사본만 사용. AI 재생성 X / 피사체 변형 X.
음성: craft_narrator(MeloTTS KR, speed 1.08) — 1편과 동일 보이스. 컷별 생성→측정→그 길이로 영상.
자막: 사용자 '화면 자막 최종본'을 컷별로 burn-in. 내레이션은 '추천 최종본' 버베이텀.
산출: assets/audio/ep02/seg01~11.wav, ep02_full.wav
      assets/video/ep02/ 각 컷 mp4, assets/video/ep02_creation_final.mp4
자동 업로드 없음. 기존 파일 전부 보존."""
import os, wave, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF   = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
SRC  = r"C:\Users\admin\AppData\Local\Temp\claude\C--Users-admin-Desktop----------\1fb996f8-0fab-4421-a9f4-ebdd18ff477c\scratchpad\ep2img"

AUD  = os.path.join(ROOT, "assets", "audio", "ep02"); os.makedirs(AUD, exist_ok=True)
IMGM = os.path.join(ROOT, "assets", "images", "ep02", "master"); os.makedirs(IMGM, exist_ok=True)
VID  = os.path.join(ROOT, "assets", "video", "ep02"); os.makedirs(VID, exist_ok=True)
TMP  = os.path.join(VID, "_frames"); os.makedirs(TMP, exist_ok=True)
OUT  = os.path.join(ROOT, "assets", "video", "ep02_creation_final.mp4")

FB = r"C:\Windows\Fonts\malgunbd.ttf"   # bold
FR = r"C:\Windows\Fonts\malgun.ttf"     # regular
SCALE = 1
W, H = 1080*SCALE, 1920*SCALE
FPS = 30
PAUSE = 0.30      # 컷 사이 호흡
TAIL  = 2.0       # 엔딩 무음 tail(2초 규칙)
SPEED = 1.08      # craft_narrator

# 8컷 구조 → 11세그(내레이션 호흡 단위). img = scratchpad 파일명(원본 보존 복사).
SEGS = [
    dict(n=1,  img="img7.png", zin=True,
         narration="모든 아이가 같은 재능으로 시작하지는 않습니다.",
         caption=["모든 아이가 같은 재능으로", "시작하지는 않습니다"]),
    dict(n=2,  img="img1.png", zin=False,
         narration="누군가는 영화를 꿈꾸고,",
         caption=["누군가는 영화를 꿈꿉니다"]),
    dict(n=3,  img="img2.png", zin=True,
         narration="누군가는 무대를 꿈꾸고,",
         caption=["누군가는 무대를 꿈꿉니다"]),
    dict(n=4,  img="img3.png", zin=False,
         narration="누군가는 사람을 돕는 미래를 꿈꿉니다.",
         caption=["누군가는 사람을 돕는", "미래를 꿈꿉니다"]),
    dict(n=5,  img="img7.png", zin=False,
         narration="예전에는 재능과 장비와 기회가 먼저 필요해 보였습니다.",
         caption=["예전엔 재능·장비·기회가", "먼저 필요해 보였습니다"]),
    dict(n=6,  img="img4.png", zin=True,
         narration="하지만 이제 아이는 AI에게 말하면서 시작할 수 있습니다.",
         caption=["이제 아이는 AI에게 말하면서", "시작할 수 있습니다"]),
    dict(n=7,  img="img5.png", zin=True,
         narration="이 장면을 더 밝게 해줘. 처음 3초를 더 재미있게 해줘. 다시 만들어줘.",
         caption=["“더 밝게 해줘”  “다시 만들어줘”"]),
    dict(n=8,  img="img5.png", zin=False,
         narration="중요한 것은 완성된 영상이 아닙니다.",
         caption=["중요한 건 완성된 영상이 아닙니다"]),
    dict(n=9,  img="img5.png", zin=True,
         narration="결과를 보고, 부족한 부분을 찾고, 다시 요청하는 과정입니다.",
         caption=["보고, 생각하고,", "다시 요청하는 과정입니다"]),
    dict(n=10, img="img6.png", zin=False,
         narration="처음에는 무료 크레딧으로 하루 한 편이면 충분합니다.",
         caption=["처음엔 무료 크레딧으로", "하루 한 편이면 충분합니다"]),
    dict(n=11, img="img7.png", zin=True,
         narration="모든 아이에게 같은 재능은 없지만, AI는 더 많은 아이에게 창작의 문을 열어줍니다.",
         caption=["AI는 더 많은 아이에게", "창작의 문을 열어줍니다"]),
]

# 이미지별 '아이' 초점(원본 가로/세로 비율). 클로즈업이 아이 쪽으로 수렴.
FOCAL = {
    "img1.png": (0.42, 0.55),  # 영화: 빈백 소년(뒤통수) 중앙
    "img2.png": (0.34, 0.55),  # 무대: 춤추는 소년 중앙좌
    "img3.png": (0.20, 0.52),  # 의료: 가운 소년 좌측
    "img4.png": (0.30, 0.45),  # 가족컴퓨터: 딸(좌측)
    "img5.png": (0.43, 0.44),  # 가리키는 소년 중앙
    "img6.png": (0.70, 0.42),  # 무료크레딧: 소년 우측
    "img7.png": (0.50, 0.60),  # 문 앞 소년 중앙(서있는 몸 중심)
}
ZOOM_RATE = 0.016   # 초당 줌 증가(천천히)
ZOOM_CAP  = 1.20    # 최대 클로즈업

def font(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()

# ---------- 0) 원본 보존 복사 ----------
def stage_images():
    used = sorted({s["img"] for s in SEGS})
    for fn in used:
        src = os.path.join(SRC, fn)
        dst = os.path.join(IMGM, fn)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    print(f"[img] master 보존 복사 {len(used)}장 → {IMGM}")

# ---------- 1) 컷별 TTS(이미 있으면 재사용) ----------
def gen_audio():
    full = os.path.join(AUD, "ep02_full.wav")
    paths = [os.path.join(AUD, f"seg{s['n']:02d}.wav") for s in SEGS]
    if os.path.exists(full) and all(os.path.exists(p) for p in paths):
        durs = []
        for p in paths:
            with wave.open(p) as w: durs.append(round(w.getnframes()/float(w.getframerate()), 3))
        print("  (기존 ep02 음성 재사용 — TTS 재생성 안 함)")
        return durs, full
    from melo.api import TTS
    model = TTS(language="KR", device="cpu")
    spk = model.hps.data.spk2id
    sid = spk["KR"] if "KR" in spk else list(spk.values())[0]
    durs = []
    for s in SEGS:
        raw = os.path.join(AUD, f"seg{s['n']:02d}_raw.wav")
        out = os.path.join(AUD, f"seg{s['n']:02d}.wav")
        model.tts_to_file(s["narration"], sid, raw, speed=SPEED)
        subprocess.run([FF,"-y","-i",raw,"-af",f"apad=pad_dur={PAUSE}",out],
                       check=True, capture_output=True)
        with wave.open(out) as w:
            d = w.getnframes()/float(w.getframerate())
        durs.append(round(d,3)); os.remove(raw)
        print(f"  seg{s['n']:02d}: {d:5.2f}s  {s['narration'][:24]}")
    # 본 음성 concat + 엔딩 tail
    lst = os.path.join(AUD, "ep02_concat.txt")
    with open(lst,"w",encoding="utf-8") as fh:
        for p in paths: fh.write(f"file '{p.replace(os.sep,'/')}'\n")
    body = os.path.join(AUD, "_ep02_body.wav")
    subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,body], check=True, capture_output=True)
    subprocess.run([FF,"-y","-i",body,"-af",f"apad=pad_dur={TAIL}",full], check=True, capture_output=True)
    os.remove(body)
    print(f"  full: {round(sum(durs)+TAIL,2)}s (+tail {TAIL}s)")
    return durs, full

# ---------- 2) 합성 자산: 정지 배경 PNG + 자막 오버레이 PNG + 전경 박스 좌표 ----------
def compose(s):
    img = os.path.join(IMGM, s["img"])
    src = Image.open(img).convert("RGB")
    # 배경(정지): cover→블러→어둡게
    sc = max(W/src.width, H/src.height)
    bg = src.resize((int(src.width*sc), int(src.height*sc)), Image.LANCZOS)
    bx, by = (bg.width-W)//2, (bg.height-H)//2
    bg = bg.crop((bx,by,bx+W,by+H)).filter(ImageFilter.GaussianBlur(60))
    bg = Image.eval(bg, lambda p:int(p*0.78))
    bg_p = os.path.join(TMP, f"seg{s['n']:02d}_bg.png"); bg.convert("RGB").save(bg_p)
    # 전경 박스: 원본 전체 폭 96% contain(잘림 없음), 세로 중앙
    fw = int(W*0.96); fh = int(fw*src.height/src.width)
    if fh > int(H*0.74):
        fh = int(H*0.74); fw = int(fh*src.width/src.height)
    fw -= fw % 2; fh -= fh % 2
    fx = (W-fw)//2; fy = (H-fh)//2
    # 오버레이(정지·투명): 상단 브랜드 + 하단 스크림 + 자막(조금 위로)
    ov = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(ov)
    d.text((W/2, int(H*0.032)), "아이와 함께 배우는 생성형 AI",
           font=font(FB, 30), fill=(255,255,255,215), anchor="mm")
    band_top = int(H*0.74)
    for y in range(band_top, H):
        t = (y-band_top)/(H-band_top); a = int(220*t)
        d.line([(0,y),(W,y)], fill=(8,8,12,a))
    lines = s["caption"]
    size = 58; maxw = int(W*0.90)
    while size > 34 and max(d.textlength(ln, font=font(FB,size)) for ln in lines) > maxw:
        size -= 2
    fnt = font(FB, size); lh = int(size*1.34)
    total = len(lines)*lh
    y0 = int(H*0.85) - total//2   # 0.905 → 0.85 (조금 더 위로)
    for i, ln in enumerate(lines):
        y = y0 + i*lh
        d.text((W/2+3, y+3), ln, font=fnt, fill=(0,0,0,180), anchor="mm")
        d.text((W/2, y), ln, font=fnt, fill=(255,255,255,255), anchor="mm")
    ov_p = os.path.join(TMP, f"seg{s['n']:02d}_ov.png"); ov.save(ov_p)
    return dict(bg=bg_p, ov=ov_p, src=img, fw=fw, fh=fh, fx=fx, fy=fy)

# ---------- 3) 컷별 클립: 배경 정지 + 아이 초점 천천히 클로즈업(줌인) ----------
def render_clip(s, dur, tail=0.0):
    c = compose(s)
    clip = os.path.join(VID, f"seg{s['n']:02d}.mp4")
    d = round(dur + tail, 3)
    N = max(2, int(round(FPS*d)))
    fx_f, fy_f = FOCAL.get(s["img"], (0.5, 0.5))
    zs, ze = s["zstart"], s["zend"]
    step = (ze - zs)/(N-1) if N > 1 else 0.0
    # 전경 2배 업스케일 → 줌 시 서브픽셀 이동(지터 제거). 아이 초점으로 크롭창 수렴.
    zexp = f"min({zs:.5f}+{step:.7f}*on\\,{ze:.5f})"
    xexp = f"max(0\\,min(iw-iw/zoom\\,{fx_f}*iw-(iw/zoom)/2))"
    yexp = f"max(0\\,min(ih-ih/zoom\\,{fy_f}*ih-(ih/zoom)/2))"
    fc = (
        f"[1:v]scale=iw*2:ih*2,zoompan=z='{zexp}':d={N}:x='{xexp}':y='{yexp}':"
        f"s={c['fw']}x{c['fh']}:fps={FPS}[fg];"
        f"[0:v][fg]overlay={c['fx']}:{c['fy']}[b];"
        f"[b][2:v]overlay=0:0,format=yuv420p[v]"
    )
    subprocess.run([FF,"-y",
                    "-loop","1","-i",c["bg"],     # 0: 정지 배경
                    "-loop","1","-i",c["src"],    # 1: 전경 원본(줌 대상)
                    "-loop","1","-i",c["ov"],     # 2: 정지 자막 오버레이
                    "-filter_complex",fc,"-map","[v]","-t",str(d),"-r",str(FPS),
                    "-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p",clip],
                   check=True, capture_output=True)
    return clip

# 줌 플랜: 같은 이미지가 연속이면 줌을 이어붙여(컷 경계 튐 방지), 이미지 바뀌면 1.0부터.
def plan_zoom(durs):
    prev, cur = None, 1.0
    for i, s in enumerate(SEGS):
        if s["img"] != prev: cur = 1.0
        zs = cur
        ze = min(cur + ZOOM_RATE*durs[i], ZOOM_CAP)
        s["zstart"], s["zend"] = zs, ze
        cur, prev = ze, s["img"]

# ---------- 4) 조립 ----------
def assemble(durs, audio):
    plan_zoom(durs)
    clips = []
    for i, s in enumerate(SEGS):
        tail = TAIL if i == len(SEGS)-1 else 0.0
        clips.append(render_clip(s, durs[i], tail))
        print(f"  clip seg{s['n']:02d} done")
    lst = os.path.join(VID, "ep02_vlist.txt")
    with open(lst,"w",encoding="utf-8") as fh:
        for c in clips: fh.write(f"file '{c.replace(os.sep,'/')}'\n")
    vonly = os.path.join(VID, "_ep02_vonly.mp4")
    subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,"-c","copy",vonly],
                   check=True, capture_output=True)
    subprocess.run([FF,"-y","-i",vonly,"-i",audio,"-map","0:v","-map","1:a",
                    "-c:v","copy","-c:a","aac","-b:a","192k","-shortest",OUT],
                   check=True, capture_output=True)
    os.remove(vonly)
    vtot = round(sum(durs)+TAIL, 2)
    print(f"[OK] {OUT}  {os.path.getsize(OUT)} B  ~{vtot}s")
    return OUT

if __name__ == "__main__":
    print("0) 원본 보존 복사...");  stage_images()
    print("1) 컷별 TTS(craft_narrator)..."); durs, full = gen_audio()
    print("2) 컷 합성 + Ken Burns + 자막..."); assemble(durs, full)
    print("DONE")
