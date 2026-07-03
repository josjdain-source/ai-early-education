#!/usr/bin/env python3
"""EP02 싱가포르 편 편집용 텍스트 카드 생성기(1920x1080). 우리 자체 콘텐츠 카드(공식 자료 아님)."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "assets/ai-early-education/video-episode-02-singapore/cards"
KFONT = r"C:\Windows\Fonts\malgun.ttf"
KBOLD = r"C:\Windows\Fonts\malgunbd.ttf"
W, H = 1920, 1080
LAV = (243, 240, 255); BLUE = (47, 107, 216); PUR = (124, 108, 255)
GREEN = (10, 138, 74); ORANGE = (192, 81, 43); INK = (31, 31, 40); GRAY = (120, 120, 140)

def F(path, size):
    try: return ImageFont.truetype(path, size)
    except Exception: return ImageFont.load_default()

def center(d, text, font, y, fill, w=W):
    bb = d.textbbox((0, 0), text, font=font); tw = bb[2] - bb[0]
    d.text(((w - tw) / 2, y), text, font=font, fill=fill); return bb[3] - bb[1]

def base(bg=LAV):
    img = Image.new("RGB", (W, H), bg); return img, ImageDraw.Draw(img)

def rrect(d, xy, r, fill, outline=None, width=2):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def save(img, name):
    img.save(os.path.join(OUT, name)); print("saved", name)

def c08_age():
    img, d = base()
    center(d, "나이에 맞게, 어떻게 쓰냐", F(KBOLD, 78), 80, INK)
    cols = [("유아", "상상하고 말하기", BLUE), ("초등 저학년", "함께 보고 다시 말하기", PUR),
            ("초등 고학년", "비교·틀린 답 찾기", ORANGE), ("중학생", "출처·윤리까지", GREEN)]
    cw, gap = 400, 40; total = cw * 4 + gap * 3; x0 = (W - total) // 2
    for i, (a, b, c) in enumerate(cols):
        x = x0 + i * (cw + gap)
        rrect(d, [x, 320, x + cw, 820], 28, (255, 255, 255), c, 8)
        center(d, a, F(KBOLD, 52), 380, c, w=W) if False else None
        bb = d.textbbox((0,0), a, font=F(KBOLD,52)); d.text((x+(cw-(bb[2]-bb[0]))/2,380), a, font=F(KBOLD,52), fill=c)
        # wrap b
        words = b.split("·") if "·" in b else [b]
        yy = 500
        for line in ([b] if len(b) < 12 else b.split("·")):
            bb2 = d.textbbox((0,0), line, font=F(KFONT,40)); d.text((x+(cw-(bb2[2]-bb2[0]))/2, yy), line, font=F(KFONT,40), fill=INK); yy += 60
    center(d, "어릴수록 직접 사용보다 안내·보호 먼저", F(KFONT, 44), 900, GRAY)
    save(img, "c08_age_4_steps_card.png")

def c09_questions():
    img, d = base((238, 246, 255))
    center(d, "집에서는 이 네 마디만", F(KBOLD, 78), 90, INK)
    qs = ["이 답이 맞을까?", "개인정보는 안 넣었지?", "다른 답이랑 비교해볼까?", "한 번 더 물어볼까?"]
    cols = [PUR, ORANGE, BLUE, GREEN]
    for i, q in enumerate(qs):
        x = 260 + (i % 2) * 720; y = 300 + (i // 2) * 300
        rrect(d, [x, y, x + 640, y + 220], 40, (255, 255, 255), cols[i], 8)
        bb = d.textbbox((0,0), q, font=F(KBOLD, 50)); d.text((x + (640-(bb[2]-bb[0]))/2, y + 80), q, font=F(KBOLD, 50), fill=INK)
    save(img, "c09_parent_questions_4_card.png")

def c10_school_home():
    img, d = base()
    center(d, "역할이 다른 거지, 빠져도 되는 게 아니다", F(KBOLD, 66), 90, INK)
    rrect(d, [180, 320, 900, 820], 32, (255, 255, 255), BLUE, 8)
    rrect(d, [1020, 320, 1740, 820], 32, (255, 255, 255), GREEN, 8)
    d.text((240, 380), "학교", font=F(KBOLD, 70), fill=BLUE)
    for i, t in enumerate(["제도", "평가·공정성", "감독"]):
        d.text((240, 520 + i*90), "· " + t, font=F(KFONT, 52), fill=INK)
    d.text((1080, 380), "가정", font=F(KBOLD, 70), fill=GREEN)
    for i, t in enumerate(["짧은 실험", "함께 정한 약속", "시작 전 체크리스트"]):
        d.text((1080, 520 + i*90), "· " + t, font=F(KFONT, 52), fill=INK)
    center(d, "가정 = 아이가 AI와 안전하게 대화하는 첫 경험", F(KFONT, 44), 900, GRAY)
    save(img, "c10_school_vs_home_card.png")

def c11_actions():
    img, d = base((243, 240, 255))
    center(d, "한국 부모가 오늘 가져갈 세 가지", F(KBOLD, 74), 90, INK)
    acts = [("①", "앱보다 나이별 시작 방식을 먼저", PUR),
            ("②", "혼자가 아니라 함께 쓰는 구조", BLUE),
            ("③", "AI 답을 그대로 믿지 않고 다시 확인하는 습관", GREEN)]
    for i, (n, t, c) in enumerate(acts):
        y = 300 + i * 220
        rrect(d, [220, y, 1700, y + 180], 28, (255, 255, 255), c, 8)
        d.text((270, y + 45), n, font=F(KBOLD, 90), fill=c)
        d.text((420, y + 60), t, font=F(KBOLD, 52), fill=INK)
    save(img, "c11_three_actions_card.png")

def c12_homepage():
    img, d = base((238, 246, 255))
    center(d, "우리 아이 나이엔 어떻게 시작할까", F(KBOLD, 70), 110, INK)
    links = ["연령별 가이드 (age-guide)", "인쇄용 시작 카드 (age-cards)",
             "부모 7가지 약속 (parent-rules)", "시작 전 체크리스트 (printable-checklist)"]
    for i, t in enumerate(links):
        y = 320 + i * 130
        rrect(d, [360, y, 1560, y + 100], 24, (255, 255, 255), PUR, 6)
        d.text((410, y + 24), "🔗 " + t, font=F(KBOLD, 46), fill=INK)
    center(d, "프로필 링크 · 오늘 딱 10분만 함께", F(KBOLD, 50), 900, PUR)
    save(img, "c12_homepage_link_card.png")

def source_label():
    # 편집용 하단 출처 라벨 바 템플릿(투명 대신 짙은 바)
    img = Image.new("RGB", (W, 120), (24, 26, 42)); d = ImageDraw.Draw(img)
    d.text((40, 20), "Source: Singapore MOE / SLS", font=F(KBOLD, 40), fill=(255, 255, 255))
    d.text((40, 72), "확인일 2026-07-04 · 정책은 바뀔 수 있음 · URL은 캡처 이미지 참조", font=F(KFONT, 30), fill=(180, 180, 190))
    img.save(os.path.join(OUT, "source_label_card.png")); print("saved source_label_card.png")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    c08_age(); c09_questions(); c10_school_home(); c11_actions(); c12_homepage(); source_label()
    print("done")
