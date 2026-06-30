# -*- coding: utf-8 -*-
"""ep01 싱크 복구 — 타임라인 기반 결정론적 조립.
원칙: 컷별 TTS(craft_narrator)를 생성 → 각 컷 이미지를 그 컷 음성 길이만큼만 표시.
=> 이미지와 내레이션이 '구조적으로' 일치(감으로 맞추지 않음).
산출: ep01_timeline_sync.json / assets/audio/ep01/cutNN.wav / ep01_sync_full.wav /
      ep01_door_sign_sync_debug.mp4 / ep01_door_sign_sync_fixed.mp4
v1/v2/v3 보존. 자동 업로드 없음."""
import os, sys, json, wave, subprocess

ROOT = r"C:\Users\admin\Desktop\ai-craft-kids"
FF = r"C:\Users\admin\Desktop\유튜브쇼츠\동영상제작\ffmpeg.exe"
AUD = os.path.join(ROOT, "assets", "audio", "ep01"); os.makedirs(AUD, exist_ok=True)
VID = os.path.join(ROOT, "assets", "video")
TMP = os.path.join(VID, "_frames_sync"); os.makedirs(TMP, exist_ok=True)
TL = os.path.join(ROOT, "content", "video", "ep01_timeline_sync.json")
FB = r"C:\Windows\Fonts\malgunbd.ttf"; FR = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1080, 1920
PAUSE = 0.25          # 컷 사이 쉼
TAIL = 2.0            # 끝 무음
SPEED = 1.08          # craft_narrator preset

CUTS = [
    dict(cut=1, kind="beforeafter", intent="before_after_hook",
         narration="사진 한 장이 감정 캐릭터 20종으로 바뀝니다.",
         caption="사진 한 장 → 감정 캐릭터 20종",
         visual="example_photo.png + example_emotion_sheet.png",
         check="실사 사진과 감정 캐릭터 20종이 같이 보이는가?"),
    dict(cut=2, kind="promptcard", intent="prompt_retry",
         narration="GPT 프롬프트를 넣고, 원하는 결과가 나올 때까지 다시 말해봅니다.",
         caption="AI에게 다시 말해보기",
         visual="prompt_card",
         check="프롬프트 카드가 보이는가?"),
    dict(cut=3, kind="say3", intent="retry_examples",
         narration="더 귀엽게, 번호는 빼줘, 5열 4행으로 정리해줘처럼 말할 수 있어요.",
         caption="말이 바뀌면 결과도 바뀌어요",
         visual="say_bubbles(더 귀엽게/번호는 빼줘/5열 4행)",
         check="다시 말하기 말풍선 3개가 보이는가?"),
    dict(cut=4, kind="select", intent="select_character",
         narration="마음에 드는 감정 캐릭터를 고릅니다.",
         caption="마음에 드는 표정 고르기",
         visual="example_emotion_sheet.png + 선택표시",
         check="시트에서 한 표정을 고르는 표시가 보이는가?"),
    dict(cut=5, kind="doorimg", intent="use_case_doorsign",
         narration="오늘은 그 결과를 문패로 활용해볼게요.",
         caption="첫 활용: 오늘 마음 문패",
         visual="door-sign-sample.png",
         check="완성된 문패가 보이는가?"),
    dict(cut=6, kind="talk", intent="education_core",
         narration="중요한 건 출력물이 아니라, 아이가 AI에게 어떻게 말해야 결과가 나오는지 배우는 과정입니다.",
         caption="첫 AI 조기교육은 대화부터",
         visual="talk_card(아이 ↔ AI)",
         check="아이와 AI가 대화하는 느낌이 보이는가?"),
    dict(cut=7, kind="apply3", intent="series_application",
         narration="한 번 해보면, 같은 방식으로 스티커와 키링도 만들어볼 수 있어요.",
         caption="같은 방법으로 더 만들어보세요",
         visual="apply_cards(스티커/키링/이름표)",
         check="스티커·키링·이름표 응용 카드가 보이는가?"),
]

# ---------- 1) 컷별 TTS ----------
def gen_audio():
    from melo.api import TTS
    model = TTS(language="KR", device="cpu")
    spk = model.hps.data.spk2id
    sid = spk["KR"] if "KR" in spk else list(spk.values())[0]
    durs = []
    for c in CUTS:
        raw = os.path.join(AUD, f"cut{c['cut']:02d}_raw.wav")
        out = os.path.join(AUD, f"cut{c['cut']:02d}.wav")
        model.tts_to_file(c["narration"], sid, raw, speed=SPEED)
        # 끝 120ms 페이드 + PAUSE 무음
        subprocess.run([FF, "-y", "-i", raw, "-af",
                        f"afade=t=out:st=0:d=0:curve=tri,apad=pad_dur={PAUSE}", out],
                       check=True, capture_output=True)
        with wave.open(out) as w:
            d = w.getnframes() / float(w.getframerate())
        durs.append(round(d, 3))
        os.remove(raw)
        print(f"  cut{c['cut']:02d}: {d:.3f}s  {c['narration'][:24]}")
    # 전체 합치고 끝 2초 tail
    lst = os.path.join(AUD, "concat.txt")
    with open(lst, "w", encoding="utf-8") as fh:
        for c in CUTS:
            p = os.path.join(AUD, f"cut{c['cut']:02d}.wav").replace(os.sep, "/")
            fh.write(f"file '{p}'\n")
    full = os.path.join(AUD, "ep01_sync_full.wav")
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", f"apad=pad_dur={TAIL}", full], check=True, capture_output=True)
    return durs, full

# ---------- 2) 타임라인 ----------
def build_timeline(durs):
    cuts = []
    t = 0.0
    for i, c in enumerate(CUTS):
        d = durs[i] + (TAIL if i == len(CUTS) - 1 else 0.0)  # 마지막 컷은 tail 포함 표시
        cuts.append({"cut": c["cut"], "start": round(t, 3), "end": round(t + d, 3),
                     "duration": round(d, 3), "narration": c["narration"],
                     "visual": c["visual"], "caption": c["caption"],
                     "intent": c["intent"], "check_question": c["check"]})
        t += d
    tl = {"project": "ep01_door_sign", "version": "sync_fix",
          "audio_policy": {"tail_silence_seconds": TAIL, "no_cut_at_audio_end": True,
                           "per_cut_tts": True, "preset": "craft_narrator", "pause_between_cuts": PAUSE},
          "total_seconds": round(t, 3), "cut_count": len(cuts), "cuts": cuts}
    json.dump(tl, open(TL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return tl

# ---------- 3) 렌더 ----------
from PIL import Image, ImageDraw, ImageFont
GRID_COLS = [22, 301, 583, 860, 1138, 1422]; GRID_ROWS = [153, 369, 594, 811, 1053]
def f(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()
def grad(top, bot):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        tt = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i]*(1-tt)+bot[i]*tt) for i in range(3)))
    return im
def ctext(d, cx, y, lines, font, fill, lh):
    for ln in lines:
        w = d.textlength(ln, font=font); d.text((cx-w/2, y), ln, font=font, fill=fill); y += lh
def contained(canvas, path, box):
    im = Image.open(path).convert("RGBA"); x0, y0, x1, y1 = box
    sc = min((x1-x0)/im.width, (y1-y0)/im.height)
    im2 = im.resize((max(1,int(im.width*sc)), max(1,int(im.height*sc))), Image.LANCZOS)
    px, py = int(x0+((x1-x0)-im2.width)/2), int(y0+((y1-y0)-im2.height)/2)
    canvas.paste(im2, (px, py), im2); return px, py, im2.width, im2.height, sc

def v_beforeafter(im, d, card):
    pbox = (card[0]+30, 470, card[0]+360, 1010); sbox = (card[0]+470, 470, card[2]-30, 1010)
    contained(im, os.path.join(ROOT,"assets","example_photo.png"), pbox)
    contained(im, os.path.join(ROOT,"assets","example_emotion_sheet.png"), sbox)
    ax=(pbox[2]+sbox[0])/2; aw=d.textlength("→",font=f(FB,110)); d.text((ax-aw/2,690),"→",font=f(FB,110),fill=(224,138,78))
    ctext(d,(pbox[0]+pbox[2])/2,1030,["사진"],f(FB,40),(138,125,112),48)
    ctext(d,(sbox[0]+sbox[2])/2,1030,["감정 캐릭터 20종"],f(FB,38),(138,125,112),48)
def v_promptcard(im, d, card):
    bx=(card[0]+70,card[1]+70,card[2]-70,card[3]-110)
    d.rounded_rectangle(bx,radius=28,fill=(255,253,248),outline=(236,226,214),width=4)
    d.text((bx[0]+34,bx[1]+30),"GPT 프롬프트",font=f(FB,40),fill=(201,116,58))
    ys=bx[1]+110
    for w in [0.86,0.72,0.9,0.64,0.8,0.7,0.58]:
        d.rounded_rectangle([bx[0]+34,ys,bx[0]+34+(bx[2]-bx[0]-68)*w,ys+26],radius=13,fill=(229,222,212)); ys+=52
    pill=[bx[2]-300,bx[3]-90,bx[2]-34,bx[3]-30]; d.rounded_rectangle(pill,radius=30,fill=(224,138,78))
    t="프롬프트 복사"; tw=d.textlength(t,font=f(FB,40)); d.text(((pill[0]+pill[2])/2-tw/2,pill[1]+8),t,font=f(FB,40),fill=(255,255,255))
def v_say3(im, d, card):
    texts=["더 귀엽게 해줘","번호는 빼줘","5열 4행으로 정리해줘"]; fnt=f(FB,52); bh=104; gap=30
    total=len(texts)*bh+(len(texts)-1)*gap; y=(card[1]+card[3])/2-total/2
    for t in texts:
        tw=d.textlength(t,font=fnt); bw=tw+80; x0=(card[0]+card[2])/2-bw/2
        d.rounded_rectangle([x0,y,x0+bw,y+bh],radius=34,fill=(224,138,78)); d.text((x0+40,y+bh/2-34),t,font=fnt,fill=(255,255,255)); y+=bh+gap
def v_select(im, d, card):
    box=(card[0]+50,card[1]+50,card[2]-50,card[3]-50)
    px,py,w,h,sc=contained(im,os.path.join(ROOT,"assets","example_emotion_sheet.png"),box)
    # 첫 칸(좋아) 하이라이트
    x0=px+GRID_COLS[0]*sc; y0=py+GRID_ROWS[0]*sc; x1=px+GRID_COLS[1]*sc; y1=py+GRID_ROWS[1]*sc
    d.rounded_rectangle([x0,y0,x1,y1],radius=14,outline=(224,138,78),width=10)
    lab="이 표정!"; fnt=f(FB,44); tw=d.textlength(lab,font=fnt)
    d.rounded_rectangle([x0,y0-66,x0+tw+40,y0-8],radius=24,fill=(224,138,78)); d.text((x0+20,y0-60),lab,font=fnt,fill=(255,255,255))
def v_doorimg(im, d, card):
    contained(im,os.path.join(ROOT,"assets","door-sign-sample.png"),(card[0]+50,card[1]+50,card[2]-50,card[3]-50))
def v_talk(im, d, card):
    fnt=f(FB,48); rows=[("아이","이렇게 만들어줘",False),("AI","네, 그릴게요!",True),("아이","더 귀엽게 해줘!",False)]
    y=card[1]+120
    for who,t,right in rows:
        tw=d.textlength(t,font=fnt); bw=tw+70; bh=98
        if right: x0=card[2]-90-bw; col=(224,138,78)
        else: x0=card[0]+90; col=(111,174,142)
        d.rounded_rectangle([x0,y,x0+bw,y+bh],radius=30,fill=col); d.text((x0+35,y+bh/2-32),t,font=fnt,fill=(255,255,255))
        lab=f(FR,30); d.text((x0+ (bw-10 if right else 2), y-34) if False else (x0+2,y-34),who,font=lab,fill=(150,140,128))
        y+=bh+44
def v_apply3(im, d, card):
    items=[("감정 스티커",(224,138,78)),("감정 키링",(111,174,142)),("이름표",(122,111,154))]
    n=3; gap=30; cw=(card[2]-card[0]-2*gap)/n; cy0=card[1]+200; ch=380
    for i,(lab,col) in enumerate(items):
        x0=card[0]+i*(cw+gap)+ (gap if i>0 else 0)*0
        x0=card[0]+i*(cw+gap);
        d.rounded_rectangle([x0,cy0,x0+cw,cy0+ch],radius=24,fill=(255,255,255),outline=(236,226,214),width=3)
        d.ellipse([x0+cw/2-50,cy0+50,x0+cw/2+50,cy0+150],fill=col)
        t=lab; fnt=f(FB,40); tw=d.textlength(t,font=fnt); d.text((x0+cw/2-tw/2,cy0+210),t,font=fnt,fill=(58,50,44))

VIS={"beforeafter":v_beforeafter,"promptcard":v_promptcard,"say3":v_say3,"select":v_select,"doorimg":v_doorimg,"talk":v_talk,"apply3":v_apply3}

def render(cut_meta, tl_cut, debug):
    im=grad((255,243,228),(253,246,238)); d=ImageDraw.Draw(im)
    ctext(d,W/2,110,["아이와 함께 배우는 생성형 AI"],f(FB,40),(200,150,90),50)
    card=[90,360,W-90,1180]; d.rounded_rectangle(card,radius=40,fill=(255,255,255))
    VIS[cut_meta["kind"]](im,d,card)
    # 캡션(자막)
    size=72; maxw=W-96
    while size>44 and d.textlength(tl_cut["caption"],font=f(FB,size))>maxw: size-=3
    cw=d.textlength(tl_cut["caption"],font=f(FB,size)); d.text((W/2-cw/2,1440),tl_cut["caption"],font=f(FB,size),fill=(58,50,44))
    if debug:
        bar=f"CUT {cut_meta['cut']:02d} | {tl_cut['caption']} | {cut_meta['kind']} | {tl_cut['start']:.2f}~{tl_cut['end']:.2f}s"
        d.rectangle([0,0,W,46],fill=(20,20,20)); d.text((12,6),bar,font=f(FR,30),fill=(255,235,180))
        nr=cut_meta["narration"]; d.rectangle([0,H-54,W,H],fill=(20,20,20)); d.text((12,H-48),("🗣 "+nr)[:54],font=f(FR,28),fill=(180,220,255))
    p=os.path.join(TMP,f"{'dbg' if debug else 'fin'}_{cut_meta['cut']:02d}.png"); im.save(p); return p

def assemble(tl, debug, audio, outname):
    frames=[render(CUTS[i],tl["cuts"][i],debug) for i in range(len(CUTS))]
    lst=os.path.join(TMP,f"list_{'dbg' if debug else 'fin'}.txt")
    with open(lst,"w",encoding="utf-8") as fh:
        for i,c in enumerate(tl["cuts"]):
            fh.write(f"file '{frames[i].replace(os.sep,'/')}'\nduration {c['duration']}\n")
        fh.write(f"file '{frames[-1].replace(os.sep,'/')}'\n")
    vonly=os.path.join(TMP,f"_v_{'dbg' if debug else 'fin'}.mp4"); out=os.path.join(VID,outname)
    subprocess.run([FF,"-y","-f","concat","-safe","0","-i",lst,"-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","veryfast",vonly],check=True,capture_output=True)
    subprocess.run([FF,"-y","-i",vonly,"-i",audio,"-c:v","copy","-c:a","aac","-b:a","192k","-shortest",out],check=True,capture_output=True)
    print("[OK]",out,os.path.getsize(out),"B")
    return out

if __name__=="__main__":
    print("1) 컷별 TTS 생성...")
    durs,full=gen_audio()
    print("2) 타임라인...")
    tl=build_timeline(durs); print("   total",tl["total_seconds"],"s,",tl["cut_count"],"컷")
    print("3) debug 렌더...")
    assemble(tl,True,full,"ep01_door_sign_sync_debug.mp4")
    print("4) final 렌더...")
    assemble(tl,False,full,"ep01_door_sign_sync_fixed.mp4")
    print("DONE")
