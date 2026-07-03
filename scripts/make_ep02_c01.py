#!/usr/bin/env python3
"""c01 거실 장면(1920x1080) 플랫 일러스트 생성. 로고/앱UI/실존아동 없음, 무섭지 않게."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "assets/ai-early-education/video-episode-02-singapore/cards/c01_parent_livingroom_scene.png"
KB = r"C:\Windows\Fonts\malgunbd.ttf"; KF = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1920, 1080
CREAM = (247, 244, 236); LAV = (243, 240, 255); WALL = (238, 240, 250)
SOFA = (124, 108, 255); SOFA_D = (98, 84, 214); FLOOR = (224, 214, 196)
SKIN = (247, 214, 189); SKIN2 = (240, 200, 172); HAIR_P = (74, 60, 48); HAIR_C = (60, 48, 40)
TEE_P = (47, 107, 216); TEE_C = (192, 81, 43); INK = (40, 40, 52); GRAY = (120, 120, 140)

def F(p, s):
    try: return ImageFont.truetype(p, s)
    except Exception: return ImageFont.load_default()

img = Image.new("RGB", (W, H), WALL)
d = ImageDraw.Draw(img)

# 바닥
d.rectangle([0, 760, W, H], fill=FLOOR)
# 벽 장식(창문)
d.rounded_rectangle([120, 150, 520, 470], 18, fill=(255, 255, 255), outline=(210, 214, 230), width=6)
d.line([320, 150, 320, 470], fill=(210, 214, 230), width=5)
d.line([120, 310, 520, 310], fill=(210, 214, 230), width=5)
# 액자
d.rounded_rectangle([1500, 180, 1740, 380], 12, fill=(255, 255, 255), outline=(210, 214, 230), width=6)
d.ellipse([1560, 240, 1620, 300], fill=(255, 214, 120))
d.polygon([(1560, 340), (1640, 250), (1720, 340)], fill=(150, 210, 170))

# 소파
d.rounded_rectangle([430, 560, 1330, 900], 60, fill=SOFA)
d.rounded_rectangle([430, 560, 1330, 700], 60, fill=SOFA_D)   # 등받이
d.rounded_rectangle([470, 690, 860, 900], 40, fill=(150, 136, 255))  # 쿠션1
d.rounded_rectangle([900, 690, 1290, 900], 40, fill=(150, 136, 255)) # 쿠션2

# 부모(왼쪽, 앉아서 폰 든 채 망설이는 표정)
# 몸
d.rounded_rectangle([560, 560, 760, 860], 70, fill=TEE_P)
# 머리
d.ellipse([590, 430, 730, 570], fill=SKIN)
d.pieslice([585, 420, 735, 540], 180, 360, fill=HAIR_P)  # 머리카락
# 눈(망설임: 살짝 위 곡선), 입(작게)
d.ellipse([632, 490, 648, 506], fill=INK)
d.ellipse([678, 490, 694, 506], fill=INK)
d.arc([645, 515, 685, 540], 200, 340, fill=INK, width=4)  # 애매한 입
# 물음표(부모 머리 위)
d.text((520, 400), "?", font=F(KB, 90), fill=SOFA_D)
# 폰(손에)
d.rounded_rectangle([740, 700, 820, 800], 14, fill=(60, 62, 80), outline=(40,42,56), width=4)
d.rounded_rectangle([750, 712, 810, 788], 6, fill=(210, 220, 240))  # 빈 화면(브랜드 없음)

# 아이(오른쪽, 부모 쪽 보며 질문)
d.rounded_rectangle([980, 620, 1160, 870], 60, fill=TEE_C)
d.ellipse([1010, 500, 1130, 620], fill=SKIN2)
d.pieslice([1005, 492, 1135, 600], 180, 360, fill=HAIR_C)
d.ellipse([1042, 548, 1058, 564], fill=INK)
d.ellipse([1088, 548, 1104, 564], fill=INK)
d.arc([1050, 566, 1096, 592], 20, 160, fill=INK, width=4)  # 웃는 입(질문, 무섭지 않게)
# 아이 책상/노트(숙제 느낌)
d.rounded_rectangle([1180, 820, 1420, 900], 12, fill=(255, 255, 255), outline=(210,214,230), width=5)
d.line([1210, 850, 1390, 850], fill=(200, 204, 220), width=4)
d.line([1210, 875, 1360, 875], fill=(200, 204, 220), width=4)

# 말풍선 (아이 대사)
d.rounded_rectangle([1150, 360, 1780, 500], 40, fill=(255, 255, 255), outline=SOFA, width=6)
d.polygon([(1180, 500), (1180, 560), (1240, 500)], fill=(255, 255, 255))
d.polygon([(1180, 500), (1180, 560), (1240, 500)], outline=SOFA, width=6)
bb = d.textbbox((0,0), "엄마, 숙제할 때 AI 써도 돼?", font=F(KB, 52))
d.text((1465 - (bb[2]-bb[0])/2, 410), "엄마, 숙제할 때 AI 써도 돼?", font=F(KB, 52), fill=INK)

# 하단 자막(부모 내면)
sub = "막을까, 허락할까 — 이 애매한 지점"
bb2 = d.textbbox((0,0), sub, font=F(KF, 44))
d.rounded_rectangle([(W-(bb2[2]-bb2[0]))/2 - 30, 960, (W+(bb2[2]-bb2[0]))/2 + 30, 1035], 16, fill=(24,26,42))
d.text(((W-(bb2[2]-bb2[0]))/2, 972), sub, font=F(KF, 44), fill=(255,255,255))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT)
print("saved", OUT, img.size)
