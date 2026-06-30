# -*- coding: utf-8 -*-
"""1편 쇼츠 — 검수 통과 음성(door-sign-short-01.tail2s.wav)을 그대로 쓰고 화면 컷만 내레이션에 맞춤.
긴급 정정 원칙: TTS 재생성 금지 / MeloTTS 재실행 금지 / 컷별 wav 생성 금지 / 음성 자르지 않음.
컷 경계 = silencedetect로 잡은 문장 사이 무음 시작점(이미지가 다음 문장보다 살짝 먼저 뜸).
영상 길이 = 오디오(38.29s) + 2초 여유. v1/v2/sync_fixed 보존, 별도 파일로 출력."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
AUDIO = os.path.join(ROOT, "assets", "audio", "door-sign-short-01.tail2s.wav")  # 기준 음성(재생성 금지)
OUTDIR = os.path.join(ROOT, "assets", "video"); os.makedirs(OUTDIR, exist_ok=True)
TMP = os.path.join(OUTDIR, "_frames_tailsync"); os.makedirs(TMP, exist_ok=True)
FB = r"C:\Windows\Fonts\malgunbd.ttf"; FR = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1080, 1920
AUDIO_LEN = 38.291
VIDEO_END = AUDIO_LEN + 2.0   # 오디오 끝 + 2초 여유

def f(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()

def grad(top, bot):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3)))
    return im

def ctext(d, cx, y, lines, font, fill, lh):
    for ln in lines:
        w = d.textlength(ln, font=font); d.text((cx - w/2, y), ln, font=font, fill=fill); y += lh

def contained(canvas, path, box):
    im = Image.open(path).convert("RGBA"); x0,y0,x1,y1 = box
    sc = min((x1-x0)/im.width, (y1-y0)/im.height)
    im = im.resize((max(1,int(im.width*sc)), max(1,int(im.height*sc))), Image.LANCZOS)
    px = int(x0+((x1-x0)-im.width)/2); py = int(y0+((y1-y0)-im.height)/2)
    canvas.paste(im, (px, py), im)
    return (px, py, im.width, im.height)

THEME = [(255,243,228),(253,246,238)]
ORANGE = (224,138,78)

# ── 화면 비주얼 ─────────────────────────────────────────────
def v_beforeafter(im, d, card):
    half = (card[2]-card[0]-60)/2
    lb = (card[0]+40, card[1]+70, card[0]+40+half-30, card[3]-130)
    rb = (card[2]-40-half+30, card[1]+70, card[2]-40, card[3]-130)
    contained(im, os.path.join(ROOT,"assets","example_photo.png"), lb)
    contained(im, os.path.join(ROOT,"assets","door-sign-sample.png"), rb)
    cy = (card[1]+card[3])/2 - 40
    d.line([(card[0]+40+half-18, cy),(card[2]-40-half+18, cy)], fill=ORANGE, width=10)
    d.polygon([(card[2]-40-half+18, cy-22),(card[2]-40-half+18, cy+22),(card[2]-40-half+52, cy)], fill=ORANGE)
    fnt = f(FB,42)
    ctext(d, (lb[0]+lb[2])/2, card[3]-110, ["사진"], fnt, (120,110,100), 50)
    ctext(d, (rb[0]+rb[2])/2, card[3]-110, ["문패"], fnt, (120,110,100), 50)

def v_img(im, d, card, name):
    contained(im, os.path.join(ROOT,"assets",name), (card[0]+50, card[1]+50, card[2]-50, card[3]-50))

def v_photo(im, d, card):
    pb = (card[0]+220, card[1]+60, card[2]-220, card[3]-60)
    contained(im, os.path.join(ROOT,"assets","example_photo.png"), pb)

def v_pick(im, d, card):
    px,py,pw,ph = contained(im, os.path.join(ROOT,"assets","example_emotion_sheet.png"),
                            (card[0]+50, card[1]+50, card[2]-50, card[3]-120))
    # 첫 칸 근처에 '이 그림!' 강조(시트 5열4행 기준 좌상단 셀 위치 근사)
    cx0 = px + pw*0.025; cy0 = py + ph*0.205; cx1 = px + pw*0.195; cy1 = py + ph*0.45
    d.rounded_rectangle([cx0,cy0,cx1,cy1], radius=16, outline=ORANGE, width=8)
    t = "이 그림 → 출력"; fnt = f(FB,46); tw = d.textlength(t, font=fnt); bw = tw+70
    bx = (card[0]+card[2])/2 - bw/2; by = card[3]-128
    d.rounded_rectangle([bx,by,bx+bw,by+96], radius=30, fill=ORANGE)
    d.text((bx+35, by+96/2-31), t, font=fnt, fill=(255,255,255))

def v_step(im, d, card, num, lines):
    cx = (card[0]+card[2])/2; cyc = card[1]+260; r = 110
    d.ellipse([cx-r, cyc-r, cx+r, cyc+r], fill=ORANGE)
    nf = f(FB,120); nw = d.textlength(str(num), font=nf)
    d.text((cx-nw/2, cyc-78), str(num), font=nf, fill=(255,255,255))
    sf = f(FB,62); lh = 84; y = cyc + r + 70
    ctext(d, cx, y, lines, sf, (70,60,52), lh)

def v_message(im, d, card, lines):
    cx = (card[0]+card[2])/2; mf = f(FB,72); lh = 100
    total = len(lines)*lh; y = (card[1]+card[3])/2 - total/2
    ctext(d, cx, y, lines, mf, (150,110,80), lh)

# ── 컷 정의: 검수음성 문장경계(silencedetect)에 정렬 ───────────────
# start = 직전 문장 음성이 끝나는 무음 시작점(이미지가 다음 문장보다 살짝 먼저 뜸)
CUTS = [
    dict(n=1, start=0.000,  kind="beforeafter", cap="사진 한 장으로 오늘 마음 문패",
         line="사진 한 장으로 오늘 마음 문패를 만들어볼게요.", vis="사진→문패 before/after"),
    dict(n=2, start=3.270,  kind="photo", cap="1단계 · 사진(또는 캐릭터) 준비",
         line="먼저 아이 사진이나 캐릭터 이미지를 준비합니다.", vis="example_photo.png"),
    dict(n=3, start=7.382,  kind="img", img="example_emotion_sheet.png", cap="2단계 · 생성형 AI로 감정 캐릭터",
         line="생성형 AI로 감정 캐릭터를 만들고,", vis="감정 캐릭터 20종 시트"),
    dict(n=4, start=11.112, kind="pick", cap="3단계 · 마음에 드는 그림 출력",
         line="마음에 드는 그림을 프린터로 출력해 주세요.", vis="시트에서 선택+출력"),
    dict(n=5, start=14.822, kind="step", num=4, steplines=["손코팅지로","감싸기"], cap="4단계 · 손코팅지로 감싸기",
         line="출력한 그림은 손코팅지로 감싸고,", vis="단계카드 4"),
    dict(n=6, start=18.362, kind="step", num=5, steplines=["폼보드에 붙여","단단하게"], cap="5단계 · 폼보드에 붙이기",
         line="폼보드에 붙여 단단하게 만들어줍니다.", vis="단계카드 5"),
    dict(n=7, start=21.697, kind="step", num=6, steplines=["모양 따라","자르기"], cap="6단계 · 자르기",
         line="가위로 모양을 따라 자르면,", vis="단계카드 6"),
    dict(n=8, start=24.368, kind="img", img="door-sign-sample.png", cap="완성! 오늘 마음 문패",
         line="아이 방 앞에 붙일 수 있는 오늘 마음 문패 완성.", vis="완성 문패"),
    dict(n=9, start=28.471, kind="message", msg=["어렵게 배우는","AI 말고"], cap="어렵게 배우는 AI 말고",
         line="어렵게 배우는 AI 말고,", vis="메시지"),
    dict(n=10, start=31.237, kind="img", img="hero-art.png", cap="아이와 함께 만들어보는 AI",
         line="아이와 함께 만들어보는 AI부터 시작해보세요.", vis="hero + CTA", sub="프롬프트는 홈페이지에"),
]
# 컷 길이 = 다음 컷 start - 이 컷 start (마지막은 VIDEO_END까지)
for i, c in enumerate(CUTS):
    nxt = CUTS[i+1]["start"] if i+1 < len(CUTS) else VIDEO_END
    c["dur"] = round(nxt - c["start"], 3)
    c["end"] = round(nxt, 3)

def base_frame(c):
    im = grad(*THEME); d = ImageDraw.Draw(im)
    ctext(d, W/2, 110, ["아이와 함께 배우는 생성형 AI"], f(FB,40), (200,150,90), 50)
    card = [90, 360, W-90, 1180]
    d.rounded_rectangle(card, radius=40, fill=(255,255,255))
    k = c["kind"]
    if k == "beforeafter": v_beforeafter(im, d, card)
    elif k == "photo": v_photo(im, d, card)
    elif k == "img": v_img(im, d, card, c["img"])
    elif k == "pick": v_pick(im, d, card)
    elif k == "step": v_step(im, d, card, c["num"], c["steplines"])
    elif k == "message": v_message(im, d, card, c["msg"])
    # 자막(제목)
    title = [c["cap"]]
    size = 70; maxw = W - 96
    while size > 42 and d.textlength(c["cap"], font=f(FB, size)) > maxw:
        size -= 3
    lh = int(size*1.24)
    ctext(d, W/2, 1448, title, f(FB,size), (58,50,44), lh)
    if c.get("sub"):
        ctext(d, W/2, 1448+lh+12, [c["sub"]], f(FR,46), (150,120,90), 56)
    return im, d

def add_debug(im, d, c):
    # 상단 바: CUT NN | 자막 | 화면설명 | 구간
    d.rectangle([0,0,W,64], fill=(20,20,20))
    top = f"CUT {c['n']:02d} | {c['cap']} | {c['vis']} | {c['start']:.2f}~{c['end']:.2f}s"
    fnt = f(FB,34); s = 34
    while s > 20 and d.textlength(top, font=f(FB,s)) > W-20: s -= 2
    d.text((10, 32-s/2-2), top, font=f(FB,s), fill=(255,255,255))
    # 하단 바: 예상 대사
    d.rectangle([0,H-66,W,H], fill=(20,20,20))
    bot = f"예상 대사: {c['line']}"
    s = 34
    while s > 18 and d.textlength(bot, font=f(FB,s)) > W-20: s -= 2
    d.text((10, H-66+(66-s)/2-4), bot, font=f(FB,s), fill=(255,235,200))

def render_all(debug):
    paths = []
    for c in CUTS:
        im, d = base_frame(c)
        if debug: add_debug(im, d, c)
        p = os.path.join(TMP, f"{'dbg' if debug else 'fin'}_{c['n']}.png")
        im.save(p); paths.append(p)
    return paths

def assemble(debug, outname):
    frames = render_all(debug)
    lst = os.path.join(TMP, ("dbg" if debug else "fin")+"_list.txt")
    with open(lst, "w", encoding="utf-8") as fh:
        for i, c in enumerate(CUTS):
            fh.write(f"file '{frames[i].replace(os.sep,'/')}'\nduration {c['dur']}\n")
        fh.write(f"file '{frames[-1].replace(os.sep,'/')}'\n")
    vonly = os.path.join(OUTDIR, "_vonly_"+("dbg" if debug else "fin")+".mp4")
    out = os.path.join(OUTDIR, outname)
    subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,"-t",str(VIDEO_END),
                    "-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast",vonly],
                   check=True, capture_output=True)
    # -shortest 없이: 영상(40.29s) > 오디오(38.29s) → 오디오 끝 + 2초 여유 유지, 음성은 자르지 않음
    subprocess.run([FF,"-y","-i",vonly,"-i",AUDIO,"-c:v","copy","-c:a","aac","-b:a","192k",out],
                   check=True, capture_output=True)
    print("[OK]", out, os.path.getsize(out), "B")
    return out

if __name__ == "__main__":
    print("기준 음성:", AUDIO, "(재생성 안 함)")
    print("컷 시간표:")
    for c in CUTS:
        print(f"  CUT {c['n']:02d}  {c['start']:6.2f}~{c['end']:6.2f}  dur {c['dur']:5.2f}  {c['cap']}")
    assemble(True,  "ep01_door_sign_tail_audio_sync_debug.mp4")
    assemble(False, "ep01_door_sign_tail_audio_sync_fixed.mp4")
    print("DONE / video end =", VIDEO_END, "s (audio", AUDIO_LEN, "+2s)")
