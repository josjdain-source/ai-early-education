#!/usr/bin/env python3
"""증거 스샷 최종화: 무관 영역 화이트 마스킹 + 하단 출처 바 합성 → final/.
원본 1280x720(16:9) 유지. 렌더/업로드 없음."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE="assets/world-ai-education-5min/evidence-screenshots"
RAW=f"{BASE}/raw"; MAN=f"{BASE}/manual-needed"; FIN=f"{BASE}/final"
KB=r"C:\Windows\Fonts\malgunbd.ttf"; KF=r"C:\Windows\Fonts\malgun.ttf"
W,H=1280,720; BAR=94  # 하단 출처 바 13%

def F(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()

# (src_dir, raw_file, final_file, [화이트 마스크 박스들], 출처1줄)
ITEMS=[
 (RAW,"US-01-ai-education-order-raw.png","US-01-ai-education-order-evidence.png",[],
   "출처: [미국 정부] White House · Advancing AI Education for American Youth · 2025-04-23"),
 (RAW,"US-02-ai-toolkit-safe-ethical-raw.png","US-02-ai-toolkit-safe-ethical-evidence.png",[],
   "출처: [미국 교육부] Dept of Education(OET) · Toolkit for Safe, Ethical, Equitable AI Integration · 2024"),
 (RAW,"UK-01-dfe-genai-guidance-raw.png","UK-01-dfe-genai-guidance-evidence.png",[],
   "출처: [영국 정부] GOV.UK/DfE · Generative AI in education · 2025"),
 (RAW,"UK-02-education-hub-ai-schools-raw.png","UK-02-education-hub-ai-schools-evidence.png",[],
   "출처: [영국 교육부 블로그] The Education Hub · AI in schools and colleges · 2025-06"),
 (RAW,"KR-01-ai-digital-textbook-policy-raw.png","KR-01-ai-digital-textbook-policy-evidence.png",
   [(925,0,W,H-BAR)],  # 우측 인기뉴스 사이드바
   "출처: [대한민국 정부] 정책브리핑(korea.kr) · AI 디지털교과서 우선 도입 · 2025"),
 (RAW,"KR-02-ai-digital-textbook-intro-raw.png","KR-02-ai-digital-textbook-intro-evidence.png",
   [(925,0,W,H-BAR)],
   "출처: [대한민국 정부] 정책브리핑(korea.kr) · AI 디지털교과서 도입 · 2025"),
 (MAN,"CN-01-classroom-ai-policy-raw.png","CN-01-classroom-ai-policy-evidence.png",
   [(930,0,W,H-BAR),(0,578,W,H-BAR)],  # 우측 정치 사이드바 + 하단 쿠키배너
   "출처: [중국 관영매체] CGTN · China's classrooms get an AI makeover · 2025-09-08"),
 (MAN,"CN-02-genai-guide-guardrail-raw.png","CN-02-genai-guide-guardrail-evidence.png",[],
   "출처: [해외 연구기관] CSET Georgetown · China Gen-AI Use Guide · 2025"),
 (MAN,"SG-01-moe-ai-sls-raw.png","SG-01-moe-ai-sls-evidence.png",[],
   "출처: [싱가포르 교육부] MOE/SLS · About AI in SLS"),
 (MAN,"SG-02-govtech-ai-classroom-raw.png","SG-02-govtech-ai-classroom-evidence.png",[],
   "출처: [싱가포르 정부기관] GovTech · Inside Singapore's digital classroom · 2025"),
]
LINE2="용도: 해외 AI교육 사례 설명을 위한 짧은 화면 인용"

def fit(d,text,maxw,start=21,mn=15):
    s=start
    while s>=mn:
        f=F(KB,s)
        if d.textlength(text,font=f)<=maxw: return f
        s-=1
    return F(KB,mn)

os.makedirs(FIN,exist_ok=True)
for src,raw,fin,masks,src1 in ITEMS:
    im=Image.open(os.path.join(src,raw)).convert("RGB")
    if im.size!=(W,H): im=im.resize((W,H))
    d=ImageDraw.Draw(im)
    for box in masks:
        d.rectangle(box,fill=(255,255,255))
    # 하단 출처 바(완전 불투명 — 쿠키/위젯 잔재 완전 차단)
    d.rectangle((0,H-BAR,W,H),fill=(18,20,34))
    d.line([(0,H-BAR),(W,H-BAR)],fill=(124,108,255),width=3)
    f1=fit(d,src1,W-48,21,15)
    d.text((24,H-BAR+16),src1,font=f1,fill=(255,255,255))
    d.text((24,H-BAR+54),LINE2,font=F(KF,17),fill=(200,198,220))
    im.save(os.path.join(FIN,fin))
    print("saved",fin,"masks:",len(masks))
print("done ·",len(ITEMS),"evidence images")
