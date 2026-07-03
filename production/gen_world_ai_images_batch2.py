#!/usr/bin/env python3
"""pending 13개: 인포그래픽 IMG-05~16(8개) + 부모 해석 카드 5개.
IMG-01~04와 톤 통일(사이트 팔레트, 드로잉 아이콘, 텍스트 최소). 무료 Pillow. 16:9 1280x720."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IMG="assets/world-ai-education-5min/images"
CARD="assets/world-ai-education-5min/interpretation-cards"
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
W,H=1280,720
BG1,BG2=(243,240,255),(238,246,255)
PUR,BLUE,GREEN,ORG=(124,108,255),(47,107,216),(10,138,74),(192,81,43)
INK,GRAY,CARDC,SOFT=(36,36,51),(150,150,170),(255,255,255),(225,222,240)

def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def bg():
    im=Image.new("RGB",(W,H),BG1); top=Image.new("RGB",(W,H),BG2); m=Image.new("L",(W,H)); md=ImageDraw.Draw(m)
    for y in range(H): md.line([(0,y),(W,y)],fill=int(255*(y/H)))
    im=Image.composite(top,im,m); d=ImageDraw.Draw(im,"RGBA")
    for cx,cy,r,c in [(260,160,240,(124,108,255,26)),(1080,600,300,(47,107,216,20)),(1120,120,150,(192,81,43,16))]:
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)
    return im,ImageDraw.Draw(im)
def scard(im,xy,r=28,fill=CARDC,outline=None,ow=0):
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle([xy[0]+6,xy[1]+10,xy[2]+6,xy[3]+12],radius=r,fill=(80,70,140,55))
    sh=sh.filter(ImageFilter.GaussianBlur(12))
    im.paste(Image.alpha_composite(im.convert("RGBA"),sh).convert("RGB"),(0,0))
    d=ImageDraw.Draw(im); d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=ow); return d
def ctext(d,t,f,y,fill,w=W):
    bb=d.textbbox((0,0),t,font=f); d.text(((w-(bb[2]-bb[0]))/2,y),t,font=f,fill=fill)
def kicker(d,t,col):
    f=F(KB,34); bb=d.textbbox((0,0),t,font=f); tw=bb[2]-bb[0]
    d.rounded_rectangle([(W-tw)/2-22,60,(W-tw)/2+tw+22,112],radius=26,fill=col)
    d.text(((W-tw)/2,68),t,font=f,fill=CARDC)

# ── 아이콘(batch1과 동일 계열) ──
def ic_person(d,cx,cy,s,col):
    d.ellipse([cx-s*0.28,cy-s*0.6,cx+s*0.28,cy-s*0.04],fill=col)
    d.rounded_rectangle([cx-s*0.5,cy+s*0.05,cx+s*0.5,cy+s*0.7],radius=20,fill=col)
def ic_tablet(d,cx,cy,s,col):
    d.rounded_rectangle([cx-s*0.5,cy-s*0.68,cx+s*0.5,cy+s*0.68],radius=10,fill=col)
    d.rounded_rectangle([cx-s*0.36,cy-s*0.52,cx+s*0.36,cy+s*0.42],radius=5,fill=CARDC)
    d.ellipse([cx-s*0.06,cy+s*0.5,cx+s*0.06,cy+s*0.62],fill=CARDC)
def ic_spark(d,cx,cy,s,col):
    pts=[];
    for i in range(8):
        a=math.pi/4*i; rr=s*0.7 if i%2==0 else s*0.28; pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    d.polygon(pts,fill=col)
def ic_check(d,cx,cy,s,col):
    d.ellipse([cx-s*0.7,cy-s*0.7,cx+s*0.7,cy+s*0.7],fill=col)
    d.line([(cx-s*0.28,cy),(cx-s*0.05,cy+s*0.28),(cx+s*0.35,cy-s*0.3)],fill=CARDC,width=9,joint="curve")
def ic_shield(d,cx,cy,s,col):
    d.polygon([(cx,cy-s*0.7),(cx+s*0.6,cy-s*0.4),(cx+s*0.6,cy+s*0.2),(cx,cy+s*0.7),(cx-s*0.6,cy+s*0.2),(cx-s*0.6,cy-s*0.4)],fill=col)
    d.line([(cx-s*0.2,cy),(cx-s*0.02,cy+s*0.22),(cx+s*0.3,cy-s*0.2)],fill=CARDC,width=7,joint="curve")
def ic_fence(d,cx,cy,s,col):
    for dx in (-s*0.5,-s*0.17,s*0.17,s*0.5):
        d.rounded_rectangle([cx+dx-s*0.07,cy-s*0.5,cx+dx+s*0.07,cy+s*0.6],radius=6,fill=col)
    d.rounded_rectangle([cx-s*0.62,cy-s*0.28,cx+s*0.62,cy-s*0.14],radius=6,fill=col)
    d.rounded_rectangle([cx-s*0.62,cy+s*0.06,cx+s*0.62,cy+s*0.2],radius=6,fill=col)
def ic_book(d,cx,cy,s,col):
    d.rounded_rectangle([cx-s*0.7,cy-s*0.55,cx+s*0.7,cy+s*0.55],radius=8,fill=col)
    d.line([(cx,cy-s*0.5),(cx,cy+s*0.5)],fill=CARDC,width=5)
def ic_bubble(d,cx,cy,s,col):
    d.rounded_rectangle([cx-s*0.8,cy-s*0.55,cx+s*0.8,cy+s*0.35],radius=16,fill=col)
    d.polygon([(cx-s*0.3,cy+s*0.3),(cx-s*0.5,cy+s*0.62),(cx-s*0.05,cy+s*0.32)],fill=col)
def ic_home(d,cx,cy,s,col):
    d.polygon([(cx-s*0.7,cy),(cx,cy-s*0.6),(cx+s*0.7,cy)],fill=col)
    d.rounded_rectangle([cx-s*0.5,cy,cx+s*0.5,cy+s*0.6],radius=8,fill=col)
def ic_arrows(d,cx,cy,s,col):  # 다시 묻기(순환)
    d.arc([cx-s*0.6,cy-s*0.6,cx+s*0.6,cy+s*0.6],30,300,fill=col,width=int(s*0.16))
    d.polygon([(cx+s*0.5,cy-s*0.55),(cx+s*0.72,cy-s*0.2),(cx+s*0.3,cy-s*0.25)],fill=col)

def sub(d,t,col=GRAY,y=920):  # 하단 자막(짧게)
    ctext(d,t,F(KF,42),y,col)

def save_img(im,name,folder=IMG):
    os.makedirs(folder,exist_ok=True); im.convert("RGB").save(os.path.join(folder,name)); print("saved",name)

# ── 인포그래픽 8개 ──
def img05():  # 미국 AI 리터러시
    im,d=bg(); kicker(d,"미국: AI 리터러시",BLUE)
    for i,(lab,col) in enumerate([("이해",BLUE),("의심",PUR),("고쳐 쓰기",GREEN)]):
        x=340+i*300; scard(im,[x-120,300,x+120,520],26)
        dd=ImageDraw.Draw(im); [ic_book,ic_check,ic_bubble][i](dd,x,400,78,col)
        ctext(dd,lab,F(KB,40),540,col,w=1) if False else dd.text((x-dd.textlength(lab,font=F(KB,40))/2,540),lab,font=F(KB,40),fill=col)
        if i<2: d.text((x+150,380),"→",font=F(KB,60),fill=SOFT)
    sub(d,"미래 인재는 AI를 이해한다")
    save_img(im,"IMG-05-usa-literacy.png")
def img06():  # 미국 교사 훈련
    im,d=bg(); kicker(d,"미국: 교사 훈련",BLUE)
    ic_person(d,520,430,150,BLUE); ic_person(d,760,470,110,PUR)
    dd=ImageDraw.Draw(im); ic_spark(dd,900,330,70,ORG)
    sub(d,"교사가 먼저 배우고, 아이를 안내한다")
    save_img(im,"IMG-06-usa-teacher-training.png")
def img07():  # 영국 교사 판단(확인)
    im,d=bg(); kicker(d,"영국: AI는 도구",BLUE)
    scard(im,[430,290,850,560],26); dd=ImageDraw.Draw(im)
    ic_tablet(dd,560,420,110,GRAY); ic_check(dd,760,420,80,GREEN)
    ic_person(dd,900,440,120,BLUE)
    sub(d,"AI가 만든 것, 사람이 확인한다")
    save_img(im,"IMG-07-uk-teacher-check.png")
def img08():  # 영국 사람의 책임
    im,d=bg(); kicker(d,"영국: 판단은 사람",BLUE)
    ic_person(d,560,430,150,BLUE); dd=ImageDraw.Draw(im)
    ic_spark(dd,820,360,80,PUR); ic_shield(dd,820,470,80,GREEN)
    sub(d,"최종 판단과 책임은 사람에게")
    save_img(im,"IMG-08-uk-human-judgment.png")
def img09():  # 싱가포르 플랫폼
    im,d=bg(); kicker(d,"싱가포르: 학습 플랫폼",ORG)
    scard(im,[420,290,860,560],26,fill=(255,255,255)); dd=ImageDraw.Draw(im)
    ic_tablet(dd,640,420,150,ORG); ic_fence(dd,980,430,150,GREEN)
    sub(d,"국가 학습 플랫폼(SLS) 안에서")
    save_img(im,"IMG-09-singapore-platform.png")
def img10():  # 싱가포르 가드레일
    im,d=bg(); kicker(d,"싱가포르: 가드레일",ORG)
    ic_fence(d,500,420,170,GREEN); dd=ImageDraw.Draw(im)
    ic_person(dd,780,440,130,BLUE); ic_spark(dd,980,340,60,ORG)
    sub(d,"자유 사용보다 안전한 틀 먼저")
    save_img(im,"IMG-10-singapore-guardrail.png")
def img11():  # 한국 디지털교과서
    im,d=bg(); kicker(d,"한국: AI 디지털교과서",BLUE)
    scard(im,[430,290,850,560],26); dd=ImageDraw.Draw(im)
    ic_tablet(dd,640,420,150,BLUE)
    for i,(t,c) in enumerate([("수학",PUR),("영어",GREEN),("정보",ORG)]):
        x=380+i*220;
        if i==0: continue
    for i,t in enumerate(["수학","영어","정보"]):
        x=980; dd.text((900,340+i*70),"· "+t,font=F(KB,40),fill=INK)
    sub(d,"영어·수학·정보 교과 중심 도입")
    save_img(im,"IMG-11-korea-digital-textbook.png")
def img12():  # 한국 가정 내 다시 묻기
    im,d=bg(); kicker(d,"한국: 집에서 다시 묻기",BLUE)
    ic_home(d,470,410,150,PUR); dd=ImageDraw.Draw(im)
    ic_person(dd,700,440,120,BLUE); ic_arrows(dd,930,410,110,GREEN)
    sub(d,"학교 도입은 시작, 습관은 집에서")
    save_img(im,"IMG-12-korea-parent-home.png")

# ── 인포그래픽 나머지(13~16, 부모핵심용 이미 batch에 없던 것 확인) ──
def img13():  # 5국 요약
    im,d=bg(); kicker(d,"방식은 다르다",PUR)
    labs=[("중국","학교 안으로",BLUE),("미국","리터러시",GREEN),("영국","책임",ORG),("싱가포르","가드레일",PUR),("한국","디지털교과서",(90,73,214))]
    n=5; cw=210; gap=18; x0=(W-(cw*n+gap*(n-1)))//2
    for i,(a,b,c) in enumerate(labs):
        x=x0+i*(cw+gap); scard(im,[x,320,x+cw,520],22)
        dd=ImageDraw.Draw(im); dd.text((x+(cw-dd.textlength(a,font=F(KB,38)))/2,352),a,font=F(KB,38),fill=c)
        for j,ln in enumerate([b]): dd.text((x+(cw-dd.textlength(ln,font=F(KF,26)))/2,430),ln,font=F(KF,26),fill=INK)
    save_img(im,"IMG-13-five-country-summary.png")
def img14():  # 질문·판단·수정
    im,d=bg(); kicker(d,"공통점: AI를 다루는 힘",GREEN)
    for i,(t,c) in enumerate([("질문",BLUE),("판단",PUR),("수정",GREEN)]):
        x=390+i*250; scard(im,[x-110,300,x+110,520],26)
        dd=ImageDraw.Draw(im); [ic_bubble,ic_check,ic_arrows][i](dd,x,400,78,c)
        dd.text((x-dd.textlength(t,font=F(KB,44))/2,540),t,font=F(KB,44),fill=c)
        if i<2: d.text((x+130,380),"·",font=F(KB,70),fill=SOFT)
    save_img(im,"IMG-14-question-judgment-revise.png")
def img15():  # 부모+아이 다시 말하기
    im,d=bg(); kicker(d,"오늘 우리 집",PUR)
    ic_person(d,520,430,140,BLUE); ic_person(d,720,450,100,PUR)
    dd=ImageDraw.Draw(im); ic_bubble(dd,940,360,90,GREEN)
    sub(d,"묻기 · 보기 · 다시 말하기")
    save_img(im,"IMG-15-parent-child-retry.png")
def img16():  # 엔드카드
    im,d=bg(); ctext(d,"AI 조기교육의 시작은",F(KB,52),260,INK)
    ctext(d,"정답이 아니라 다시 묻는 힘",F(KB,60),340,PUR)
    scard(im,[300,470,620,590],24,fill=(124,108,255)); scard(im,[660,470,980,590],24,fill=(255,255,255),outline=PUR,ow=3)
    dd=ImageDraw.Draw(im)
    dd.text((330,505),"다음 영상: 중국 편",font=F(KB,32),fill=CARDC)
    dd.text((690,505),"AI 대화 카드 받기",font=F(KB,32),fill=PUR)
    save_img(im,"IMG-16-final-cta.png")

# ── 부모 해석 카드 5개 ──
def card(name,kick,lines,accent):
    im=Image.new("RGB",(W,H),(250,249,255))
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([0,0,W,14],fill=accent)  # 상단 얇은 국가색
    d.ellipse([-160,-160,220,220],fill=(accent[0],accent[1],accent[2],20))
    d.ellipse([W-220,H-220,W+160,H+160],fill=(accent[0],accent[1],accent[2],16))
    d=ImageDraw.Draw(im)
    kf=F(KB,34); bb=d.textbbox((0,0),kick,font=kf); tw=bb[2]-bb[0]
    d.rounded_rectangle([(W-tw)/2-20,120,(W-tw)/2+tw+20,172],radius=24,fill=accent)
    d.text(((W-tw)/2,128),kick,font=kf,fill=(255,255,255))
    fs=64 if len(lines)<=2 else 56
    total=len(lines)*(fs+22); y=(H-total)//2+40
    for ln in lines:
        f=F(KB,fs); bb=d.textbbox((0,0),ln,font=f)
        d.text(((W-(bb[2]-bb[0]))/2,y),ln,font=f,fill=INK); y+=fs+22
    save_img(im,name,CARD)

if __name__=="__main__":
    for fn in [img05,img06,img07,img08,img09,img10,img11,img12,img13,img14,img15,img16]:
        fn()
    card("CN-parent-interpretation.png","중국",["빨리 접하게 하되,","그냥 맡기지는 않는다."],BLUE)
    card("US-parent-interpretation.png","미국",["많이 쓰는 능력보다,","이해하고 의심하고 고쳐 쓰는 힘."],GREEN)
    card("UK-parent-interpretation.png","영국",["AI는 도구입니다.","판단은 사람이 해야 합니다."],ORG)
    card("SG-parent-interpretation.png","싱가포르",["AI를 쓰게 하는 것보다,","아이의 생각이 숨지 않게 하는 틀."],PUR)
    card("KR-parent-interpretation.png","한국",["학교 도입과 아이의 AI 습관은 다릅니다.","다시 묻는 힘은 집에서 시작됩니다."],(90,73,214))
    print("done · 인포그래픽 12(05~16) + 해석카드 5")
