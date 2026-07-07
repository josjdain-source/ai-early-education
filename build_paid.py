#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""유료 프로그램 상세페이지(/paid-programs) — 쇼핑몰형 신뢰 구조(직접 복제 없이 구조만 참고).
좌측 고정 카테고리(sticky·scroll-spy) + 상품별 상세 섹션(갤러리·핵심정보·설치·사용·주의) + 구매안내 + FAQ.
이미지=자체 제작 목업(PIL) + 우리 실물 결과컷. '사용 설명서'는 넣고 '제작 비법'은 넣지 않는다."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGD = os.path.join(ROOT, "assets", "paid")
os.makedirs(IMGD, exist_ok=True)
KB = r"C:\Windows\Fonts\malgunbd.ttf"; KF = r"C:\Windows\Fonts\malgun.ttf"
CREAM=(251,246,238); CARD=(255,253,248); NAVY=(43,58,85); CORAL=(224,104,74); LINE=(234,217,190); INK=(58,48,36); MUT=(155,138,110)

def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()

def _round(d,xy,r,**kw): d.rounded_rectangle(xy,radius=r,**kw)

def hero_img(pid, icon, name, tag, chips):
    W,H=1200,700; im=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(im)
    for i in range(H):
        t=i/H; d.line([(0,i),(W,i)],fill=(int(251-8*t),int(246-10*t),int(238-14*t)))
    _round(d,[60,80,W-60,H-80],28,fill=CARD,outline=LINE,width=3)
    _round(d,[110,H//2-110,330,H//2+110],36,fill=(253,236,229),outline=(240,201,187),width=3)
    try:
        ef=ImageFont.truetype(r"C:\Windows\Fonts\seguiemj.ttf",108)
        d.text((220,H//2),icon,font=ef,anchor="mm",embedded_color=True)
    except Exception:
        d.text((220,H//2),icon,font=F(KB,110),anchor="mm")
    d.text((390,H//2-92),name,font=F(KB,58),fill=NAVY)
    d.text((390,H//2-10),tag,font=F(KF,27),fill=INK)
    x=390
    for c in chips:
        f=F(KB,22); w=d.textlength(c,font=f)
        _round(d,[x,H//2+52,x+w+36,H//2+102],25,fill=(43,58,85))
        d.text((x+18,H//2+64),c,font=f,fill=(255,255,255)); x+=w+50
    d.text((W-84,H-104),"아이와 AI교실 · 직접 개발",font=F(KB,19),fill=MUT,anchor="rm")
    p=os.path.join(IMGD,f"{pid}-hero.png"); im.save(p,optimize=True); return p

def flow_img(pid, steps):
    W,H=1200,480; im=Image.new("RGB",(W,H),CARD); d=ImageDraw.Draw(im)
    d.text((70,54),"작동 흐름",font=F(KB,30),fill=NAVY)
    n=len(steps); bw=(W-140-40*(n-1))//n; y0,y1=160,360
    for i,(t,sub) in enumerate(steps):
        x=70+i*(bw+40)
        _round(d,[x,y0,x+bw,y1],20,fill=(251,246,238),outline=LINE,width=3)
        d.text((x+bw//2,y0+52),t,font=F(KB,30),fill=CORAL,anchor="mm")
        f=F(KF,21)
        for j,ln in enumerate(sub.split("\n")):
            d.text((x+bw//2,y0+110+j*30),ln,font=f,fill=INK,anchor="mm")
        if i<n-1:
            ax=x+bw+8; d.text((ax+12,(y0+y1)//2),"→",font=F(KB,40),fill=MUT,anchor="lm")
    p=os.path.join(IMGD,f"{pid}-flow.png"); im.save(p,optimize=True); return p

def files_img(pid, files):
    W,H=1200,480; im=Image.new("RGB",(W,H),CARD); d=ImageDraw.Draw(im)
    d.text((70,50),"받는 파일 구성 (zip)",font=F(KB,30),fill=NAVY)
    y=140
    for icon,nm,desc in files:
        _round(d,[70,y,W-70,y+68],14,fill=(251,246,238),outline=(240,230,210),width=2)
        try:
            d.text((100,y+34),icon,font=ImageFont.truetype(r"C:\Windows\Fonts\seguiemj.ttf",28),anchor="lm",embedded_color=True)
        except Exception:
            d.text((100,y+34),icon,font=F(KB,30),anchor="lm")
        d.text((160,y+34),nm,font=F(KB,25),fill=INK,anchor="lm")
        d.text((W-100,y+34),desc,font=F(KF,21),fill=MUT,anchor="rm")
        y+=82
    p=os.path.join(IMGD,f"{pid}-files.png"); im.save(p,optimize=True); return p

def result_copy(pid, src, vertical=False):
    """우리 실물 결과컷 → 축소 복사(자체 콘텐츠)."""
    dst=os.path.join(IMGD,f"{pid}-result.jpg")
    if not os.path.exists(src): return None
    im=Image.open(src).convert("RGB")
    if vertical:
        im.thumbnail((520,700)); canvas=Image.new("RGB",(1200,700),(24,20,16))
        canvas.paste(im,((1200-im.width)//2,(700-im.height)//2))
        d=ImageDraw.Draw(canvas); d.text((36,660),"실제 결과물 예시 (이 채널 쇼츠)",font=F(KB,22),fill=(255,236,180))
        canvas.save(dst,quality=82,optimize=True)
    else:
        im.thumbnail((1200,700)); im.save(dst,quality=82,optimize=True)
    return dst

def ensure_images():
    hero_img("shorts-builder","🎬","쇼츠 자동 빌더","대본 JSON 한 장 → 세로 쇼츠 mp4 완성",["대본만 쓰면 됨","1080×1920","음성·자막 자동"])
    flow_img("shorts-builder",[("① 대본","plans 폴더에\nJSON 작성"),("② 실행","명령 한 줄\npython …"),("③ 자동 처리","그림·음성·자막\n·화면 조립"),("④ 완성","output/render\nmp4 저장")])
    files_img("shorts-builder",[("🐍","shorts_builder.py","메인 프로그램"),("🗣","TTS 모듈 2종","음성 생성"),("📄","plan_template.json","대본 템플릿"),("📘","GUIDE.pdf","설치·사용 설명서"),("📜","LICENSE.txt","이용 조건")])
    result_copy("shorts-builder", os.path.join(ROOT,"assets/ai-edu-shorts/sframe/shorts-parent-001_0.png"), vertical=True)

    hero_img("video-maker","📽","영상 자동 생성기","주제 한 줄 → 롱폼 일러스트 영상",["주제만 입력","대본 자동","약 5분 제작"])
    flow_img("video-maker",[("① 주제","문장 하나로\n주제 입력"),("② 대본","로컬 AI가\n대본·자막 생성"),("③ 그림·음성","일러스트 18장\n내레이션"),("④ 완성","한 편의\nmp4 영상")])
    files_img("video-maker",[("🐍","make_illust_video.py","메인 파이프라인"),("🧩","조립 모듈","디졸브 합성"),("🗣","TTS 모듈 2종","음성 생성"),("📘","GUIDE.pdf","설치·사용 설명서"),("📜","LICENSE.txt","이용 조건")])
    result_copy("video-maker", os.path.join(ROOT,"assets/free-programs-longform/render/free-programs-poster.jpg"))

    hero_img("capcut-agent","✂️","캡컷 에이전트","말하는 영상 편집, 절반은 자동으로",["무음 구간 컷","자막 초안","점프컷 초안"])
    flow_img("capcut-agent",[("① 업로드","영상 파일을\n브라우저로"),("② 분석","무음·잔말\n자동 탐지"),("③ 초안","자막·컷 목록\n미리보기 mp4"),("④ 마무리","캡컷에서\n최종 편집")])
    files_img("capcut-agent",[("🐍","app.py + core","프로그램 본체"),("🖥","static","브라우저 화면"),("▶","run.bat","더블클릭 실행"),("📘","GUIDE.pdf","설치·사용 설명서"),("📜","LICENSE.txt","이용 조건")])

    hero_img("blog-radar","📝","네이버 블로그 레이더","붙여넣은 글을 5초 안에 진단",["점수 진단","제목 후보","10단 재구성"])
    flow_img("blog-radar",[("① 붙여넣기","내 글 텍스트\n복사·입력"),("② 진단","5초 이해 점수\n구조 분석"),("③ 제안","제목·이미지 위치\n재구성안"),("④ 저장","outputs에\n결과 저장")])
    files_img("blog-radar",[("🐍","분석기 5종 .py","진단·제안 엔진"),("📄","README","빠른 시작"),("📘","GUIDE.pdf","설치·사용 설명서"),("📜","LICENSE.txt","이용 조건")])

    hero_img("meme-cartoon","🎨","밈 카툰 변환기","사진 → 두꺼운 선 밈 카툰 패널",["말풍선 자동","GPU 불필요","PNG 출력"])
    flow_img("meme-cartoon",[("① 사진","input 폴더에\n사진 넣기"),("② 변환","선화·색 단순화\n자동 처리"),("③ 말풍선","대사·화자\n자동 배치"),("④ 완성","output에\nPNG 저장")])
    files_img("meme-cartoon",[("🐍","변환기 .py","메인 프로그램"),("⚙️","config·프리셋","패널 스타일"),("📘","GUIDE.pdf","설치·사용 설명서"),("📜","LICENSE.txt","이용 조건")])

    hero_img("workbook-guide","🃏","12주 워크북 부모 해설판","무료 워크북의 부모용 진행 대본",["주차별 해설","대화 스크립트","체크시트"])
    flow_img("workbook-guide",[("① 무료판","아이용 워크북\n(사이트 무료)"),("② 해설판","부모용 해설\n1분 읽기"),("③ 진행","대화 스크립트로\n아이와 활동"),("④ 체크","주차 체크시트\n기록")])
    files_img("workbook-guide",[("📕","12주_부모해설판.pdf","15쪽 · 인쇄 권장"),("📜","LICENSE.txt","이용 조건")])

MAIL="2011kstudentlife@gmail.com"

CATS=[
 ("video","🎬 영상 제작용",["shorts-builder","video-maker","capcut-agent","meme-cartoon"]),
 ("edu","🎓 교육용",["workbook-guide"]),
 ("ops","🗂 콘텐츠 운영용",["blog-radar"]),
]

P={
"shorts-builder":dict(icon="🎬",name="쇼츠 자동 빌더",price="9,900",core=True,
 one="대본 JSON 한 장을 넣으면, 그림·음성·자막·조립까지 끝난 세로 쇼츠 mp4가 나옵니다.",
 who="유튜브 쇼츠를 꾸준히 올리고 싶지만 편집 시간이 없는 분 · 얼굴 없이 채널을 운영하고 싶은 분",
 solve="쇼츠 1편에 들어가는 편집 노동(이미지 배치·자막·음성·컷 전환)을 명령 한 줄로 줄입니다.",
 inc=["shorts_builder.py (메인 프로그램)","TTS 모듈 2종","plans/plan_template.json (대본 템플릿)","GUIDE.pdf (한글 설치·사용 설명서)","LICENSE.txt"],
 env="Windows · Python 3.10+ · ffmpeg · (그림 자동 생성 시) ComfyUI+GPU — GPU가 없으면 그림만 따로 준비해 넣는 방식 지원(가이드 수록)",
 detail=[("어떤 상황에서 쓰나","매일 쇼츠를 올리고 싶은데 편집에 1~2시간씩 쓰고 있다면, 이 도구는 '대본 쓰는 시간'만 남기고 나머지를 자동화합니다. 이 채널의 쇼츠들이 실제로 이 프로그램으로 만들어집니다."),
  ("무엇이 쉬워지나","컷별 큰 제목·하단 자막·내레이션 싱크·컷 전환(디졸브)·느린 줌 연출이 전부 자동입니다. 완성본은 유튜브에 바로 올릴 수 있는 mp4입니다."),
  ("제한사항","그림 자동 생성은 GPU가 있어야 합니다(없으면 이미지 수동 투입 방식). 음성은 인터넷 연결이 필요합니다. 대본(내용)은 직접 쓰셔야 합니다 — 이 상품은 '조립 자동화'이지 '내용 생성기'가 아닙니다.")],
 install=["Python 설치 (python.org — 'Add to PATH' 체크)","명령창에서: pip install edge-tts","ffmpeg 설치 후 Path 등록 (가이드 1장에 그림 순서 수록)","zip을 원하는 폴더에 풀기 — 폴더 구조 그대로 유지","(선택) 그림 자동 생성용 ComfyUI 설치 — 가이드 수록"],
 usage=["plans/plan_template.json 을 복사해 내 대본으로 수정","명령창에서: python shorts_builder.py 대본이름","완성 mp4: output/render/ · 컷 이미지: output/sframe/ (썸네일용)"],
 caution="자동 생성 자막·음성은 업로드 전 한 번 확인하세요. 타인의 이미지·음원을 넣을 경우 저작권은 사용자 책임입니다.",
 imgs=["hero","result","flow","files"]),
"video-maker":dict(icon="📽",name="영상 자동 생성기",price="9,900",core=True,
 one="주제 한 줄을 넣으면 대본·그림·내레이션·조립까지, 한 편의 롱폼 영상이 나옵니다.",
 who="정보성 유튜브 롱폼을 시작하고 싶은 분 · 매일 1편 자동 제작 루틴을 만들고 싶은 분",
 solve="'대본 쓰고, 그림 찾고, 녹음하고, 편집하는' 4단계 전체를 로컬 PC 안에서 자동화합니다.",
 inc=["make_illust_video.py (메인 파이프라인)","디졸브 조립 모듈","TTS 모듈 2종","파이프라인 상세설명 txt","GUIDE.pdf","LICENSE.txt"],
 env="Windows · Python 3.10+ · ffmpeg · Ollama(로컬 대본 AI) · ComfyUI+GPU (그림 생성)",
 detail=[("어떤 상황에서 쓰나","'주제는 많은데 만들 시간이 없다'는 분께. 주제 한 줄만 넣으면 약 5분 뒤 45~55초 일러스트 영상이 나옵니다. 이 채널의 자동 제작 영상들이 이 파이프라인 산출물입니다."),
  ("무엇이 쉬워지나","대본 작성(로컬 AI)→장면별 그림→내레이션→자막·조립이 무인으로 이어집니다. 외부 유료 API 없이 전부 내 PC에서 돌아갑니다."),
  ("제한사항","GPU(그래픽카드)가 꼭 필요합니다. 생성된 대본·사실관계는 업로드 전 반드시 사람이 검수하세요.")],
 install=["Python 설치 ('Add to PATH' 체크)","pip install edge-tts","ffmpeg 설치 후 Path 등록","Ollama 설치 + 모델 1개 받기 (가이드 수록)","ComfyUI 설치 + 그림 모델 배치 (가이드 수록)","zip을 원하는 폴더에 풀기"],
 usage=["명령창에서: python make_illust_video.py \"주제 문장\"","약 5분 대기 (진행 상황이 콘솔에 표시)","완성 mp4와 대본 로그 위치가 마지막 줄에 출력"],
 caution="AI가 쓴 대본은 초안입니다 — 수치·사실은 반드시 검수 후 업로드하세요.",
 imgs=["hero","result","flow","files"]),
"capcut-agent":dict(icon="✂️",name="캡컷 에이전트",price="9,900",core=True,
 one="말하는 영상을 올리면 무음 구간 컷·자막 초안·점프컷 초안을 자동으로 만들어 줍니다.",
 who="얼굴/목소리로 말하는 영상을 만드는 분 · 편집에서 '자르기'에 시간을 다 쓰는 분",
 solve="토킹 영상 편집의 70%를 차지하는 '무음 자르기 + 자막 받아치기'를 자동 초안으로 대체합니다.",
 inc=["app.py + core 모듈 (프로그램 본체)","static (브라우저 화면)","run.bat (더블클릭 실행)","requirements.txt","GUIDE.pdf","LICENSE.txt"],
 env="Windows · Python 3.10+ · ffmpeg · (마무리 편집용) CapCut 선택",
 detail=[("어떤 상황에서 쓰나","10분 촬영본에서 무음·잔말만 잘라내는 데 1시간씩 쓰고 있다면 — 업로드 후 몇 분 안에 컷 목록·자막 초안·미리보기 mp4가 나옵니다."),
  ("무엇이 쉬워지나","브라우저 화면에서 파일만 올리면 됩니다. 명령창을 몰라도 run.bat 더블클릭으로 시작합니다."),
  ("제한사항","자동 전사(자막)는 초안 품질입니다 — 반드시 사람이 검수하세요. 한국어 음성 기준으로 조정되어 있습니다.")],
 install=["Python 설치 ('Add to PATH' 체크)","zip 풀기 → 폴더에서 명령창 열고: pip install -r requirements.txt","ffmpeg 설치 후 Path 등록"],
 usage=["run.bat 더블클릭 → 브라우저에서 127.0.0.1:8910 접속","영상 파일 업로드 → 분석 완료까지 대기","무음컷 목록·자막 초안·미리보기 확인 → 캡컷에서 마무리"],
 caution="개인정보가 담긴 영상은 외부에 올리지 말고 이 도구(로컬 처리)까지만 사용하세요.",
 imgs=["hero","flow","files"]),
"blog-radar":dict(icon="📝",name="네이버 블로그 레이더",price="9,900",core=False,
 one="붙여넣은 글을 '5초 이해 점수'로 진단하고 제목 후보·이미지 위치·10단 재구성을 제안합니다.",
 who="블로그 글이 잘 안 읽힌다고 느끼는 분 · 발행 전 구조 점검 루틴이 필요한 분",
 solve="감으로 고치던 글을 점수와 구조 제안으로 고치게 합니다. 크롤링·로그인 없이 텍스트만 분석합니다.",
 inc=["분석기 5종 .py","README","GUIDE.pdf","LICENSE.txt"],
 env="Windows · Python 3.10+ (그 외 설치 없음 · 인터넷 불필요)",
 detail=[("어떤 상황에서 쓰나","발행 직전 3분 점검용. 내 글을 붙여넣으면 어디서 읽다 떠나는지, 제목이 왜 약한지 근거와 함께 보여줍니다."),
  ("제한사항","분석 보조 도구입니다 — 자동 발행·네이버 접속 기능이 없습니다(계정 안전).")],
 install=["Python 설치 ('Add to PATH' 체크)","zip 풀기 (추가 설치 없음)"],
 usage=["명령창에서: python app.py","안내에 따라 글 붙여넣기","점수·제목 후보·재구성안 확인 (outputs/에 저장)"],
 caution="타인의 글을 분석·표절하는 용도로 사용하지 마세요.",
 imgs=["hero","flow","files"]),
"meme-cartoon":dict(icon="🎨",name="밈 카툰 변환기",price="9,900",core=False,
 one="사진 한 장을 두꺼운 선의 밈 카툰 패널(말풍선 포함) PNG로 바꿔 줍니다.",
 who="썸네일·SNS 짤을 직접 만들고 싶은 분 · 얼굴 사진을 만화풍으로 바꾸고 싶은 분",
 solve="포토샵 없이 '만화 한 컷' 스타일 이미지를 명령 한 줄로 만듭니다. 기본 모드는 GPU가 필요 없습니다.",
 inc=["변환기 .py 세트","config·프리셋","GUIDE.pdf","LICENSE.txt"],
 env="Windows · Python 3.10+ · pip 패키지 3개(가이드 수록) · GPU 불필요(기본 모드)",
 detail=[("어떤 상황에서 쓰나","영상 썸네일·커뮤니티 짤·프로필용 만화 컷을 빠르게. --compare 옵션으로 원본과 나란히 비교컷도 뽑습니다."),
  ("제한사항","실존 인물 사진을 희화화해 공개할 때의 초상권은 사용자 책임입니다.")],
 install=["Python 설치 ('Add to PATH' 체크)","pip install opencv-python pillow numpy","zip 풀기"],
 usage=["사진을 input/ 에 넣기","python run_cartoonize.py input/사진.jpg --preset meme_panel --text \"대사\"","결과 PNG는 output/ 에 저장"],
 caution="기본(cv) 모드 기준입니다. 고급 디퓨전 모드는 별도 GPU 환경이 필요합니다.",
 imgs=["hero","flow","files"]),
"workbook-guide":dict(icon="🃏",name="12주 워크북 부모 해설판",price="9,900",core=False,
 one="무료 12주 워크북(아이용)의 '부모용 진행 대본' — 주차별 해설·대화 스크립트·체크시트 15쪽 PDF.",
 who="무료 워크북을 시작했거나 시작하려는 부모 · 아이와 뭘 말해야 할지 막막한 분",
 solve="활동 전에 1분만 읽으면 이번 주에 무엇을 기르는지, 어떤 말을 건네야 하는지가 잡힙니다.",
 inc=["12주_부모해설판.pdf (15쪽 · 인쇄 권장)","LICENSE.txt"],
 env="PDF 뷰어만 있으면 됩니다 (프로그램 아님)",
 detail=[("어떤 상황에서 쓰나","무료 워크북으로 아이와 활동할 때 옆에 두는 부모용 커닝페이퍼입니다. 파트별 철학(1부 생각훈련→2부 만들기→3부 AI 의심하기)과 주차별 대화 3종, 체크 3항목."),
  ("제한사항","아이용 활동지 자체는 무료판(사이트)에 있습니다 — 이 상품은 부모용 해설·진행 자료입니다.")],
 install=["받은 PDF를 열기 (인쇄 권장)"],
 usage=["매주 활동 전 해당 주차 해설 1분 읽기","활동 중 '대화 스크립트' 그대로 사용","활동 후 체크시트 3항목 표시"],
 caution="교육 자료입니다 — 아이마다 속도가 다르니 12주는 목표가 아니라 리듬으로 쓰세요.",
 imgs=["hero","flow","files"]),
}

def _gal(pid, spec):
    imgs=[]
    for k in spec["imgs"]:
        ext="jpg" if k=="result" else "png"
        f=f"/assets/paid/{pid}-{k}.{ext}"
        local=os.path.join(IMGD,f"{pid}-{k}.{ext}")
        if os.path.exists(local): imgs.append(f)
    main=imgs[0]
    thumbs="".join(f'<img src="{u}" class="pp-th{" on" if i==0 else ""}" onclick="ppSwap(this,\'{pid}\')" loading="lazy" alt="">' for i,u in enumerate(imgs))
    return f'<div class="pp-gal"><img id="ppMain-{pid}" class="pp-main" src="{main}" alt="{spec["name"]}"><div class="pp-ths">{thumbs}</div></div>'

def _sec(pid, spec):
    s=spec
    mailto=f"mailto:{MAIL}?subject=[구매] {s['name']} (9,900원)&body=주문 상품: {s['name']} / 9,900원%0A입금 안내 부탁드립니다.%0A(파일 받을 이메일: )"
    inc="".join(f"<li>{x}</li>" for x in s["inc"])
    det="".join(f'<h4>{t}</h4><p>{b}</p>' for t,b in s["detail"])
    ins="".join(f"<li>{x}</li>" for x in s["install"])
    use="".join(f"<li>{x}</li>" for x in s["usage"])
    core_badge='<span class="pp-core">인기</span>' if s.get("core") else ''
    return f"""<section class="pp-item" id="{pid}">
<div class="pp-topgrid">
{_gal(pid,s)}
<div class="pp-buy">
<div class="pp-cat">{s['icon']} 직접 개발 · 디지털 상품 {core_badge}</div>
<h2>{s['name']}</h2>
<p class="pp-one">{s['one']}</p>
<div class="pp-price-row"><span class="pp-pr">₩{s['price']}</span><span class="pp-prnote">부담 없는 단일가</span></div>
<table class="pp-meta">
<tr><th>이런 분께</th><td>{s['who']}</td></tr>
<tr><th>포함 구성</th><td><ul class="pp-inc">{inc}</ul></td></tr>
<tr><th>필요 환경</th><td>{s['env']}</td></tr>
<tr><th>전달 방식</th><td>이메일로 zip 파일 + 한글 설치·사용 가이드(PDF)</td></tr>
</table>
<div class="pp-btns">
<a class="btn btn-primary pp-buybtn" href="{mailto}">📩 이메일 주문하기 · ₩{s['price']}</a>
<a class="btn" href="#{pid}-install">설치 방법 보기</a>
</div>
<p class="pp-mailnote">주문 흐름: 이메일 → 입금 안내 회신 → 파일 전달 (영업일 기준 24시간 내)</p>
</div></div>

<div class="pp-boxes">
<div class="pp-box"><b>🎯 무엇을 해결하나</b><p>{s['solve']}</p></div>
<div class="pp-box"><b>📦 받으면 오는 것</b><p>zip 1개 — 프로그램 파일 + GUIDE.pdf + LICENSE. 압축을 풀고 가이드 1장부터 따라가면 됩니다.</p></div>
</div>

<div class="pp-detail">{det}</div>

<h3 class="pp-h" id="{pid}-install">🔧 설치 방법 (Windows)</h3>
<ol class="pp-steps">{ins}</ol>
<p class="pp-tip">설치가 막히면 그 화면을 캡처해 이메일로 보내주세요 — 함께 해결해 드립니다.</p>

<h3 class="pp-h">▶ 기본 사용 방법</h3>
<ol class="pp-steps">{use}</ol>

<div class="pp-warn">⚠ <b>주의</b> · {s['caution']}</div>
</section>"""

def page_html(BS):
    ensure_images()
    # 좌측 카테고리 사이드바 (frsb 마커 = 공통 섹션랩 생략)
    nav=""
    for cid,label,pids in CATS:
        nav+=f'<div class="pp-navh">{label}</div>'
        for pid in pids:
            s=P[pid]
            nav+=f'<a class="pp-nava" href="#{pid}" data-p="{pid}">{s["icon"]} {s["name"]}<span class="pp-navpr">9,900</span></a>'
    nav+='<div class="pp-navh">ℹ️ 안내</div><a class="pp-nava" href="#order">주문·전달 안내</a><a class="pp-nava" href="#faq">자주 묻는 질문</a>'
    secs="".join(_sec(pid,P[pid]) for _,__,pids in CATS for pid in pids)
    faq=[("Mac에서도 되나요?","Windows 기준으로 만들고 검증했습니다. 파이썬 기반이라 Mac에서 도는 도구도 있지만 공식 지원은 Windows입니다."),
     ("GPU(그래픽카드)가 꼭 필요한가요?","영상 자동 생성기는 필요합니다. 쇼츠 자동 빌더는 '그림 수동 투입' 방식이면 GPU 없이 사용 가능합니다. 나머지 도구는 GPU가 필요 없습니다."),
     ("인터넷이 필요한가요?","음성 생성(edge-tts)에는 필요합니다. 블로그 레이더·밈 카툰 변환기는 오프라인으로 동작합니다."),
     ("설치가 어려우면 어떻게 하나요?","막힌 화면 캡처와 함께 이메일 주시면 순서대로 같이 해결합니다. 가이드는 처음 쓰는 분 기준으로 썼습니다."),
     ("파일은 어떻게 받나요?","입금 확인 후 주문하신 이메일로 zip 파일을 보내드립니다(영업일 24시간 내)."),
     ("사용 범위는 어디까지인가요?","구매자 개인 사용입니다. 프로그램으로 만든 결과물(영상·이미지·글)은 자유롭게 업로드·수익화할 수 있습니다. 프로그램 파일 자체의 재배포·재판매는 안 됩니다.")]
    faqh="".join(f'<details class="pp-faq"><summary>{q}</summary><p>{a}</p></details>' for q,a in faq)
    body=f"""<main><div class="pp-wrap">
<aside class="frsb pp-side"><div class="pp-sticky">
<div class="pp-sidetitle">💾 유료 프로그램<br><small>모두 ₩9,900</small></div>
{nav}
<div class="pp-sidemail">문의<br><a href="mailto:{MAIL}">{MAIL}</a></div>
</div></aside>
<div class="pp-maincol">
<section class="page-hero" style="padding:26px 0 8px"><div class="pill">💾 직접 개발 · 디지털 상품</div>
<h1>유료 프로그램</h1>
<p style="color:var(--navy2);font-weight:600;max-width:640px">아이와 AI교실이 실제 제작에 사용 중인 프로그램을 정리했습니다.
모든 상품은 디지털 파일로 제공되며, 구매 후 설치 가이드와 기본 사용 설명서를 함께 보내드립니다.
처음 쓰는 분도 설치부터 실행까지 따라갈 수 있도록 구성했습니다.</p></section>
{secs}
<section class="pp-item" id="order">
<h3 class="pp-h">🧾 주문·전달 안내</h3>
<ol class="pp-steps">
<li>상품 카드의 <b>이메일 주문하기</b> 버튼을 누르면 주문 메일이 자동으로 작성됩니다</li>
<li>회신으로 입금 계좌를 안내드립니다</li>
<li>입금 확인 후 <b>영업일 24시간 내</b> zip 파일을 이메일로 전달합니다</li>
</ol>
<div class="pp-warn">아직 카드 결제 페이지가 없어 이메일 주문 방식으로 운영합니다. 디지털 상품 특성상 <b>파일 전달 후 환불은 어렵습니다</b> — 구매 전 각 상품의 '필요 환경'을 꼭 확인해 주세요. 문의: <a href="mailto:{MAIL}">{MAIL}</a></div>
</section>
<section class="pp-item" id="faq"><h3 class="pp-h">❓ 자주 묻는 질문</h3>{faqh}</section>
</div></div>
<style>
.pp-wrap{{display:flex;gap:26px;max-width:1180px;margin:0 auto;padding:0 18px;align-items:flex-start}}
.pp-side{{width:230px;flex:none}}
.pp-sticky{{position:sticky;top:78px;max-height:calc(100vh - 95px);overflow:auto;background:#fff;border:1px solid #EADFCE;border-radius:14px;padding:12px 10px}}
.pp-sidetitle{{font-weight:900;color:#2B3A55;font-size:15px;padding:6px 8px 10px;border-bottom:2px solid #E0684A;margin-bottom:6px}}
.pp-sidetitle small{{color:#B44A31;font-weight:800}}
.pp-navh{{font-size:11px;font-weight:900;color:#9b8a6e;padding:10px 8px 4px}}
.pp-nava{{display:flex;align-items:center;gap:5px;padding:7px 8px;border-radius:8px;text-decoration:none;color:#3a3024;font-size:12.8px;font-weight:700}}
.pp-nava:hover{{background:#FBF3E4}}
.pp-nava.on{{background:#FDECE5;color:#B44A31}}
.pp-navpr{{margin-left:auto;font-size:10.5px;color:#c4b59a;font-weight:800}}
.pp-sidemail{{margin-top:12px;border-top:1px dashed #EAD9BE;padding:10px 8px 4px;font-size:11px;color:#9b8a6e}}
.pp-sidemail a{{color:#3A6FB0;font-weight:700;font-size:11.5px}}
.pp-maincol{{flex:1;min-width:0}}
.pp-item{{background:#fff;border:1px solid #EADFCE;border-radius:18px;padding:22px 24px;margin:18px 0;scroll-margin-top:80px}}
.pp-topgrid{{display:grid;grid-template-columns:1.05fr 1fr;gap:22px}}
.pp-gal .pp-main{{width:100%;border-radius:12px;border:1px solid #F0E6D2;aspect-ratio:12/7;object-fit:cover;background:#FBF6EE}}
.pp-ths{{display:flex;gap:8px;margin-top:8px}}
.pp-th{{width:72px;height:48px;object-fit:cover;border-radius:8px;border:2px solid #F0E6D2;cursor:pointer;opacity:.75}}
.pp-th.on{{border-color:#E0684A;opacity:1}}
.pp-cat{{font-size:11.5px;font-weight:800;color:#9b8a6e}}
.pp-core{{background:#E0684A;color:#fff;border-radius:5px;padding:1px 7px;font-size:10px;font-weight:900;margin-left:4px}}
.pp-buy h2{{margin:4px 0 6px;font-size:23px;color:#2B3A55}}
.pp-one{{margin:0 0 10px;font-size:14px;color:#3a3024;line-height:1.55}}
.pp-price-row{{display:flex;align-items:baseline;gap:10px;border-top:1px solid #F0E6D2;border-bottom:1px solid #F0E6D2;padding:10px 0;margin-bottom:10px}}
.pp-pr{{font-size:26px;font-weight:900;color:#B44A31}}
.pp-prnote{{font-size:12px;color:#9b8a6e;font-weight:700}}
.pp-meta{{width:100%;border-collapse:collapse;font-size:13px}}
.pp-meta th{{width:74px;text-align:left;vertical-align:top;color:#8a6f45;font-size:12px;padding:5px 8px 5px 0}}
.pp-meta td{{padding:5px 0;color:#3a3024;line-height:1.5}}
.pp-inc{{margin:0;padding-left:16px}}
.pp-inc li{{margin:1px 0}}
.pp-btns{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.pp-buybtn{{font-size:14.5px;padding:11px 18px}}
.pp-mailnote{{font-size:11.5px;color:#9b8a6e;margin-top:8px}}
.pp-boxes{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:18px}}
.pp-box{{background:#FBF8F1;border:1px solid #EAD9BE;border-radius:12px;padding:12px 14px;font-size:13px}}
.pp-box b{{display:block;margin-bottom:4px;color:#2B3A55}}
.pp-box p{{margin:0;color:#4a3a28;line-height:1.55}}
.pp-detail{{margin-top:16px}}
.pp-detail h4{{margin:14px 0 4px;font-size:14.5px;color:#B44A31}}
.pp-detail p{{margin:0;font-size:13.5px;color:#3a3024;line-height:1.65}}
.pp-h{{font-size:16px;font-weight:900;color:#2B3A55;margin:22px 0 8px}}
.pp-steps{{margin:0;padding-left:20px;font-size:13.5px;line-height:1.7;color:#3a3024}}
.pp-steps li{{margin:3px 0}}
.pp-tip{{font-size:12px;color:#2E7D4E;background:#EAF6EE;border-radius:8px;padding:7px 11px;margin-top:8px}}
.pp-warn{{font-size:12.5px;color:#8a5b1e;background:#FFF7EA;border:1px solid #EAD9BE;border-radius:9px;padding:9px 12px;margin-top:14px;line-height:1.6}}
.pp-faq{{border:1px solid #F0E6D2;border-radius:10px;padding:0 14px;margin:8px 0;background:#FFFDF8}}
.pp-faq summary{{cursor:pointer;font-weight:800;font-size:13.5px;color:#2B3A55;padding:11px 0}}
.pp-faq p{{margin:0 0 12px;font-size:13px;color:#4a3a28;line-height:1.6}}
@media(max-width:900px){{
.pp-wrap{{flex-direction:column}}
.pp-side{{width:100%}}
.pp-sticky{{position:static;max-height:none;display:flex;flex-wrap:wrap;gap:2px;align-items:center}}
.pp-sidetitle{{width:100%}}
.pp-navh{{width:100%}}
.pp-topgrid{{grid-template-columns:1fr}}
.pp-boxes{{grid-template-columns:1fr}}
}}
</style>
<script>
function ppSwap(el,pid){{document.getElementById('ppMain-'+pid).src=el.src;
 el.parentElement.querySelectorAll('.pp-th').forEach(function(t){{t.classList.toggle('on',t===el);}});}}
(function(){{var links=document.querySelectorAll('.pp-nava[data-p]');
 var obs=new IntersectionObserver(function(es){{es.forEach(function(e){{
  if(e.isIntersecting){{links.forEach(function(l){{l.classList.toggle('on',l.dataset.p===e.target.id);}});}}
 }});}},{{rootMargin:'-30% 0px -60% 0px'}});
 document.querySelectorAll('.pp-item[id]').forEach(function(s){{if(s.id&&document.querySelector('.pp-nava[data-p=\"'+s.id+'\"]'))obs.observe(s);}});}})();
</script></main>"""
    return BS.page("paid","","유료 프로그램 · 모두 9,900원 | 아이와 AI교실",
        "아이와 AI교실이 실제 제작에 사용하는 프로그램 — 쇼츠 자동 빌더, 영상 자동 생성기, 캡컷 에이전트 등. 설치 가이드 포함, 전부 9,900원.", body)

def build():
    import build_site as BS
    BS.write("paid-programs.html", page_html(BS))
    print(f"유료 프로그램 상세페이지 생성 · 상품 {len(P)} · 카테고리 {len(CATS)} · 이미지 {len(os.listdir(IMGD))}")
