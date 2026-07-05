#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""영국·싱가포르·한국 AI교육 롱폼 — 세계영상(build_illust_video_v2) 정본 방식.
RealVisXL 스토리북 그림체 + 문장매칭 그림 + 타이틀배너 + 차분한 내레이션 + 디졸브. 16:9.
★그나라→한국가정→아이효과 3단 완결. Ollama 언로드 후 실행(VRAM).
산출: assets/{c}-ai-education/render/{c}-ai-longform.mp4 · 사용: python build_country_video.py [uk singapore korea]"""
import json, time, uuid, os, subprocess, urllib.request, urllib.parse, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRV="http://127.0.0.1:8188"
FF="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffmpeg.exe"
FP="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"
EDGE=r"C:/Users/admin/Desktop/tts_lab/edge_tts/venv/Scripts/python.exe"
BASE="C:/Users/admin/Desktop/ai-craft-kids"; HERE=f"{BASE}/production"
TMP="C:/Users/admin/AppData/Local/Temp/claude/cvid"
KB=r"C:\Windows\Fonts\malgunbd.ttf"; VOICE="ko-KR-InJoonNeural"; SPEED=1.0
STYLE=("editorial storybook illustration, warm muted color palette, thick clean black outlines, "
 "semi-realistic cartoon style, flat shading, soft warm lighting, detailed cozy background, hand-drawn look, wide cinematic composition")
NEG=("photo, photorealistic, 3d render, text, letters, words, korean text, watermark, signature, logo, "
 "ugly, deformed, extra fingers, bad hands, blurry, low quality, creepy, scary, surveillance, weapon")
GB="British, diverse ethnicities, "; SG="Singaporean, multicultural Asian, "; KR="Korean, black hair, "
def F(s):
    try: return ImageFont.truetype(KB,s)
    except Exception: return ImageFont.load_default()
def run(c): subprocess.run(c,check=True)
def dur(p): return float(subprocess.run([FP,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p],capture_output=True,text=True).stdout.strip())

# 나라별: (key, title, accent, [ (sec_title, narration, [(subfile,seed,scene,caption)]) ])
COUNTRIES={
"uk": ("영국은 왜 커리큘럼보다 안전과 책임을 먼저 말했나",[
  ("영국 · 강제보다 안전과 책임","영국은 다른 나라처럼 AI를 강제 과목으로 밀어붙이지 않았습니다. 그렇다고 막지도 않았죠. 영국이 가장 먼저 세운 것은, 아이가 AI를 안전하게 쓰는 규칙과, 최종 판단과 책임은 언제나 사람에게 남긴다는 원칙이었습니다. 화려한 커리큘럼보다 안전과 책임이 먼저였던 겁니다. 왜 이렇게 신중했는지, 그 흐름을 차근차근 따라가 봅니다.",
   [("uk_s1a",6101,"a "+GB+"teacher gently guiding a young child using a friendly AI tablet in a warm bright classroom, safe and calm, storybook","영국은 안전한 규칙을 먼저"),
    ("uk_s1b",6102,"a warm glowing rulebook and a gentle shield beside a small friendly AI robot, safety first, storybook","판단과 책임은 사람에게"),
    ("uk_s1c",6112,"a wide calm view of a British school building at soft morning light, thoughtful and steady, storybook","서두르지 않은 나라, 영국")]),
  ("왜 신중했나 · 이미 교실에","이유는 분명합니다. 아이들은 이미 챗봇과 이미지 생성 AI를 일상에서 만나고 있었습니다. 문제는 쓰느냐 마느냐가 아니라, 어떻게 쓰느냐였죠. 그래서 영국은 도구를 먼저 쥐여주기보다, 안전하게 다루는 힘부터 세우기로 했습니다. 빠른 도입보다, 흔들리지 않는 기초를 먼저 놓은 셈입니다.",
   [("uk_s2z",6113,"children already surrounded by friendly glowing AI apps and chatbots in daily life, a gentle question mark, storybook","아이들은 이미 AI를 만나고 있었다"),
    ("uk_s2y",6114,"a "+GB+"teacher thoughtfully choosing to build a strong foundation before speed, a steady base stone, storybook","도구보다, 다루는 힘부터")]),
  ("2023 · 첫 공식 입장","출발은 2023년입니다. 영국 교육부는 학교의 생성형 AI 사용에 대한 첫 공식 입장을 냈습니다. 막지도, 무작정 권하지도 않고, 투명하고 안전하게 쓰라는 방향이었죠. 무엇보다 학교가 AI 사용을 숨기지 말고 열어 두라는 원칙을 강조했습니다. 첫 단추부터 '투명함'이었던 겁니다.",
   [("uk_s2a",6103,"a "+GB+"education official placing a first friendly guidance document on a desk, a new beginning, warm office, storybook","2023 · 첫 생성형 AI 입장문"),
    ("uk_s2b",6104,"a "+GB+"teacher calmly reading a gentle guidance booklet in a staff room, thoughtful, storybook","막지도 권하지도 않고, 투명하게")]),
  ("2025 · 데이터를 지키다","2025년 초, 가이드는 훨씬 촘촘해졌습니다. 가장 먼저 챙긴 것은 학생의 데이터였습니다. 영국의 데이터 보호 규칙과 아동 보호 규약에 맞춰, AI가 아이의 개인정보를 함부로 쓰지 못하게 못박았죠. 학교에는 어떤 AI를 쓰는지 투명하게 알리라고 안내했습니다. 편리함보다 아이의 정보가 먼저였습니다.",
   [("uk_s3a",6105,"a warm protective bubble around a child's personal data and notebook, data protection, gentle storybook","학생 데이터를 먼저 지킨다"),
    ("uk_s3z",6115,"a friendly lock and shield over a school's AI tools, transparent and safe, storybook","어떤 AI를 쓰는지 투명하게")]),
  ("2025 · 시험의 진실성","다음은 평가였습니다. 시험 기관은 과제와 시험에서 AI를 어떻게 다룰지 지침을 냈습니다. AI를 무조건 금지한 게 아니라, 무엇이 아이가 한 것이고 무엇이 AI가 한 것인지 구분하게 한 겁니다. 학문적 진실성, 즉 정직하게 배우는 것이 핵심이었습니다.",
   [("uk_s3b",6106,"a fair balanced scale beside an exam paper and a small AI helper, honesty in tests, storybook","시험에서 AI를 어떻게 다룰지"),
    ("uk_s5a",6108,"a "+GB+"child's drawing hand and a glowing AI hand clearly separated by a soft line, whose work is whose, storybook","무엇이 내 것, 무엇이 AI 것")]),
  ("2025 · 아이 안전을 먼저","같은 해, 아동 안전 지침에도 AI가 들어갔습니다. AI가 만든 유해한 콘텐츠나, AI를 이용한 괴롭힘으로부터 아이를 지키는 것이 먼저라는 뜻입니다. 영국은 AI를 가르치기 전에, AI 시대에도 아이가 안전한지부터 물었습니다. 기술보다 아이가 먼저였죠.",
   [("uk_s4a",6107,"a big warm umbrella sheltering a "+GB+"child who is safely using a tablet, protection from harm, storybook","아이 안전이 먼저"),
    ("uk_s4z",6116,"a caring adult watching over a child online, gentle guardianship, warm storybook","AI 시대에도 아이가 안전하게")]),
  ("영국의 철학 · 비판적 사고","영국이 아이에게 정말 기르려는 힘은 무엇일까요. 바로 비판적으로 읽는 힘입니다. AI가 준 답을 그대로 삼키지 않고, 근거가 무엇인지 묻고, 데이터가 믿을 만한지 따지는 능력이죠. 도구를 잘 다루는 아이가 아니라, 도구를 의심할 줄 아는 아이를 키우려는 겁니다.",
   [("uk_s9a",6117,"a "+GB+"child looking closely at an AI answer with a magnifying glass, questioning the evidence, curious, storybook","근거를 묻는 비판적 사고"),
    ("uk_s9b",6118,"a child weighing two sources on a small scale, thinking for themselves, warm storybook","데이터가 믿을 만한지 따진다")]),
  ("현장의 과제 · 준비","물론 쉽지만은 않습니다. 조사에 따르면 아직 많은 교사가 AI 사용을 아이에게 조언하는 데 자신이 없다고 답했습니다. AI가 어떻게 작동하는지 가르치는 학교도 다섯 곳 중 한 곳 정도에 그쳤죠. 그래서 영국은 화려한 속도 대신, 교사부터 천천히 준비시키는 길을 택했습니다.",
   [("uk_s6a",6109,"a "+GB+"teacher patiently learning how AI works, step by step, determined and warm, storybook","교사부터 천천히 준비"),
    ("uk_s6z",6119,"a steady staircase rising slowly and safely instead of a risky leap, storybook","속도보다 준비를 택한 이유")]),
  ("강제하지 않은 이유 · 자율","흥미로운 건, 영국이 끝까지 AI를 전국 공통 필수 과목으로 강제하지 않았다는 점입니다. 대신 학교와 교사에게 재량을 줬죠. 위에서 획일적으로 밀어붙이기보다, 현장이 준비된 만큼 스스로 도입하게 한 겁니다. 느려 보여도 뿌리가 튼튼한 방식이라, 정책이 바뀌어도 뒤로 물러설 일이 적습니다.",
   [("uk_a1",6131,"a "+GB+"school choosing its own pace to adopt AI, autonomy and calm, storybook","강제하지 않고, 학교 재량으로"),
    ("uk_a2",6132,"strong deep roots under a slowly growing tree, slow but sturdy, warm storybook","느려도 뿌리가 튼튼한 방식")]),
  ("영국이 준 교훈","영국의 이야기를 한 문장으로 줄이면 이렇습니다. AI를 빨리 쓰는 것보다, 안전하게 그리고 책임 있게 쓰는 것이 먼저다. 도구를 능숙하게 다루는 기술보다, 도구를 의심하고 스스로 판단하는 힘이 먼저다. 이 순서를 지킨 나라가 결국 멀리 갑니다.",
   [("uk_a3",6133,"a clear warm signpost pointing to safety and responsibility first, a long road ahead, storybook","안전과 책임이, 기술보다 먼저")]),
  ("그럼, 한국 가정은 (1)","이 이야기가 한국 가정과 무슨 상관일까요. 아주 큽니다. 영국이 나라 차원에서 '책임은 사람에게'라고 못박았다면, 한국 가정은 저녁 식탁에서 그걸 실천할 수 있습니다. AI가 답을 줘도, 마지막 결정은 아이가 하게 하는 겁니다. '그래서 넌 어떻게 할래?' 이 한마디가 시작입니다.",
   [("uk_s7a",6110,"a "+KR+"parent and child looking at an AI answer together, the child pointing and deciding, warm home, storybook","결정은 아이가, '넌 어떻게 할래?'")]),
  ("그럼, 한국 가정은 (2)","영국이 비판적 사고를 강조했다면, 집에서는 '이 답의 근거가 뭘까?'를 함께 물어보면 됩니다. 영국이 '무엇이 네 것인지 구분'하게 했다면, 집에서도 '방금 그건 네가 한 거야, AI가 한 거야?'를 물어보는 거죠. 거창한 교육과정이 아니라, 짧은 질문 하나면 충분합니다.",
   [("uk_s10a",6120,"a "+KR+"parent and child asking 'where is the evidence' about an AI answer at home, warm storybook","'이 답의 근거가 뭘까?'"),
    ("uk_s10b",6121,"a child proudly showing what part they did themselves versus AI, warm home, storybook","'네가 한 거야, AI가 한 거야?'")]),
  ("그럼 아이는","그러면 아이는 어떻게 자랄까요. AI 말을 그대로 따르지 않고 스스로 판단하는 아이, 무엇이 자기 생각인지 아는 아이, 그리고 근거를 물어 속지 않는 아이로 자랍니다. 영국이 제도와 규칙으로 지키려 한 것을, 우리는 집에서 매일의 대화로 기를 수 있습니다. 시작은 오늘 저녁, 질문 하나입니다.",
   [("uk_s8a",6111,"a confident "+KR+"child keeping their own idea while gently using AI, self-judging and calm, hopeful storybook","스스로 판단하는 아이로"),
    ("uk_s11a",6122,"a warm hopeful scene of a "+KR+"parent and child talking happily in the evening, a small AI device dimmed aside, storybook","오늘 저녁, 질문 하나부터")]),
]),
"singapore": ("싱가포르는 왜 아이에게 AI 가드레일을 먼저 채웠나",[
  ("싱가포르 · 균형을 먼저","싱가포르는 작지만 강한 나라입니다. AI를 빨리 쓰게 하는 것은 어렵지 않았죠. 하지만 싱가포르가 먼저 고민한 것은 속도가 아니라 균형이었습니다. 아이 생각이 AI 뒤로 숨지 않도록, 안전한 틀, 즉 가드레일을 먼저 설계한 겁니다. 그리고 그 균형을 나라 전체가 하나의 전략으로 묶었습니다.",
   [("sg_s1a",6201,"a "+SG+"child learning with an AI tablet inside a gentle safe railing, balanced and protected, bright classroom, storybook","아이 생각이 AI 뒤로 숨지 않게"),
    ("sg_s1b",6202,"a bright thought bubble glowing above a "+SG+"child, their own idea staying visible in front of the AI screen, storybook","속도가 아니라, 균형을 먼저"),
    ("sg_s1c",6211,"a wide warm view of the Singapore skyline with gentle AI light, small but strong nation, storybook","작지만 강한 나라의 선택")]),
  ("2019 · 국가 AI 전략","시작은 2019년입니다. 싱가포르는 국가 AI 전략을 세우며 AI를 나라 경쟁력의 축으로 삼았습니다. 중요한 건 이걸 산업만의 문제로 두지 않았다는 점입니다. 교육을 처음부터 그 전략의 한 부분으로 함께 설계했죠. AI 인재는 학교에서 자란다고 본 겁니다.",
   [("sg_s2a",6203,"a friendly national blueprint of a smart city with AI, a hopeful rising plan, warm storybook","2019 · 국가 AI 전략"),
    ("sg_s2z",6212,"a plan connecting a school and industry with a warm bright line, education inside the national strategy, storybook","교육을 전략의 한 부분으로")]),
  ("2023 · 전략 2.0 · 신뢰","2023년에는 국가 AI 전략 2.0으로 확장했습니다. 더 빠른 기술만을 좇지 않았습니다. 사회 전체의 신뢰와 안전을 함께 키우겠다는 방향이었죠. AI를 잘 쓰는 나라이면서, 동시에 AI를 믿을 수 있는 나라가 되겠다는 겁니다. 속도와 신뢰를 같이 가져간 셈입니다.",
   [("sg_s3a",6204,"an upgraded glowing plan with a heart of trust and a shield of safety at its center, storybook","2023 · 신뢰와 안전을 함께"),
    ("sg_s3z",6213,"people trusting a friendly AI in daily life, warm and safe society, storybook","믿을 수 있는 AI 사회")]),
  ("EdTech 2030 · 교실로","전략은 교실로 내려옵니다. 에듀테크 마스터플랜 2030은 학습에 AI를 책임 있게 통합하는 로드맵입니다. 여기서 핵심 단어는 '책임 있게'입니다. 무작정 태블릿을 나눠주는 게 아니라, 교사의 안내 아래 아이에게 맞는 방식으로 쓰겠다는 뜻이죠.",
   [("sg_s4a",6205,"a warm classroom of the future with gentle AI helpers guided by a teacher, storybook","교실로 내려온 로드맵"),
    ("sg_s4z",6214,"a teacher thoughtfully guiding how each child uses AI, responsible integration, storybook","핵심은 '책임 있게'")]),
  ("적응형 학습 · 개인화","학교에서는 적응형 학습 시스템이 쓰입니다. 아이마다 속도와 난이도를 맞춰, 어려워하는 부분은 더 연습하게 돕는 거죠. 하지만 AI에게 아이를 통째로 맡기지 않습니다. 교사가 늘 곁에서 데이터를 보고 지도합니다. 개인화하되, 사람이 중심에 있는 겁니다.",
   [("sg_s5a",6206,"a "+SG+"child following a personalized glowing learning path while a teacher watches warmly beside, storybook","아이마다 맞춤, 교사가 곁에"),
    ("sg_s5z",6215,"a teacher reading gentle learning data to help a child, human at the center, storybook","AI에 통째로 맡기지 않는다")]),
  ("네 원칙 · 가드레일","그 모든 것의 중심에는 네 가지 원칙이 있습니다. 주도성, 포용, 공정, 그리고 안전. 아이가 주인이 되고, 누구도 소외되지 않고, 치우치지 않고, 무엇보다 안전하게. 이 네 기둥이 싱가포르의 가드레일입니다.",
   [("sg_s6a",6207,"four warm guiding pillars around a happy "+SG+"child using AI safely, agency inclusivity fairness safety, storybook","주도성·포용·공정·안전")]),
  ("배우고·쓰고·넘어서기","싱가포르는 아이가 AI를 네 단계로 익히게 합니다. AI가 무엇인지 배우고, 직접 써 보고, AI와 함께 배우고, 그리고 마지막으로 AI를 넘어섭니다. 가장 중요한 건 이 마지막, '넘어서기'입니다. AI 없이도 스스로 생각할 줄 아는 힘을 남기는 거죠.",
   [("sg_s6b",6208,"a "+SG+"child putting down the tablet to think on their own, going beyond AI, storybook","배우고, 쓰고, 함께, 넘어서기"),
    ("sg_s6z",6216,"a child thinking deeply without any device, own imagination glowing, storybook","AI 없이도 스스로 생각하는 힘")]),
  ("AI 편향을 의심하기","싱가포르가 아이에게 특별히 가르치는 게 하나 더 있습니다. AI도 편향될 수 있다는 사실입니다. AI의 답이 한쪽으로 치우칠 수 있고, 틀린 정보를 그럴듯하게 말할 수 있다는 걸 아이 스스로 알아채게 합니다. 의심할 줄 아는 것도 리터러시입니다.",
   [("sg_s7z",6217,"a "+SG+"child noticing an AI answer leaning to one side, spotting bias, thoughtful storybook","AI도 편향될 수 있다")]),
  ("포용 · 누구도 소외되지 않게","싱가포르가 특히 신경 쓴 원칙이 하나 더 있습니다. 바로 포용입니다. 집안 형편이나 사는 곳에 상관없이, 모든 아이가 AI를 배울 기회를 갖게 하는 거죠. AI가 잘사는 집 아이만의 도구가 되면 격차는 더 벌어지니까요. 그래서 학교를 통해, 모두에게 똑같이 문을 열었습니다.",
   [("sg_a1",6231,"children from all backgrounds equally learning with AI in a school, inclusive and warm, storybook","누구도 소외되지 않게, 포용"),
    ("sg_a2",6232,"an open warm door of opportunity for every child regardless of background, storybook","모두에게 똑같이 열린 문")]),
  ("싱가포르가 준 교훈","싱가포르의 이야기를 한 문장으로 줄이면 이렇습니다. 빠르게 쓰는 것보다 균형 있게 쓰는 것이 먼저다. 그리고 AI를 쓰는 힘만큼, AI 없이 스스로 생각하는 힘을 함께 길러야 한다. 가드레일은 아이를 가두는 벽이 아니라, 안전하게 멀리 가게 하는 길입니다.",
   [("sg_a3",6233,"a safe guiding path leading a child far and safely, guardrail as a road not a cage, warm storybook","가드레일은 벽이 아니라 길")]),
  ("그럼, 한국 가정은 (1)","한국 가정도 배울 게 많습니다. 싱가포르의 첫 교훈은 균형이었죠. 집에서도 '많이'보다 '알맞게'입니다. 쓰는 시간을 아이와 함께 정하고, AI를 켜기 전에 '네 생각 먼저 말해볼래?'를 앞에 두는 겁니다. 아이 생각이 먼저, 도구는 그다음입니다.",
   [("sg_s7a",6209,"a "+KR+"parent and child setting a gentle timer and talking before using AI together, balanced, warm home, storybook","'많이'보다 '알맞게', 네 생각 먼저")]),
  ("그럼, 한국 가정은 (2)","싱가포르가 '넘어서기'를 가르쳤듯, 집에서도 'AI 없이 너라면 어떻게 했을까?'를 물어보세요. 싱가포르가 편향을 의심하게 했듯, '이 답이 한쪽으로 치우친 건 아닐까?'를 함께 보는 거죠. 균형과 의심, 이 두 습관이면 충분합니다.",
   [("sg_s10a",6218,"a "+KR+"parent asking 'what would you do without AI', child thinking proudly, warm home, storybook","'AI 없이 너라면?'"),
    ("sg_s10b",6219,"parent and child gently checking if an AI answer is one-sided, storybook","'한쪽으로 치우친 건 아닐까?'")]),
  ("그럼 아이는","그러면 아이는, AI를 쓰되 자기 생각을 잃지 않는 균형 잡힌 아이, AI를 의심할 줄 알아 속지 않는 아이로 자랍니다. 싱가포르가 나라 차원의 가드레일로 지킨 것을, 우리는 집에서 두 가지 질문으로 세울 수 있습니다. 오늘 저녁, 그 한 걸음을 시작해 보세요.",
   [("sg_s8a",6210,"a balanced happy "+KR+"child holding both a book and a small AI device, keeping their own voice, hopeful storybook","균형 잡힌, 속지 않는 아이로"),
    ("sg_s11a",6220,"a warm hopeful evening of a "+KR+"parent and child talking together, storybook","오늘 저녁, 한 걸음부터")]),
]),
"korea": ("한국은 AI교과서를 넣었다 뺐다, 그래서 가정이 답이다",[
  ("한국 · 서울에서 울린 경고음","2016년, 알파고가 이세돌을 이긴 곳은 중국도 미국도 아닌 서울이었습니다. AI 시대의 첫 경고음은 우리 한복판에서 울린 겁니다. 세계가 그 장면을 보며 움직이기 시작했고, 한국도 예외는 아니었습니다. 학교를 바꿔서라도 이 흐름을 따라잡아야 한다고 생각했죠. 그렇게 한국의 시도가 시작됩니다.",
   [("kr_s1a",6301,"a quiet solemn scene of a person facing a soft glowing AI light in Seoul, the alarm of the AI era, storybook","2016 · 서울에서 울린 경고음"),
    ("kr_s1b",6302,"a "+KR+"school preparing to change, hopeful morning light, storybook","한국도 학교를 바꾸려 움직였다"),
    ("kr_s1c",6310,"the world watching the AlphaGo moment, a turning point, storybook","세계가 움직이기 시작했다")]),
  ("2023 · 디지털 교육혁신","2023년, 교육부는 디지털 기반 교육혁신 방안을 발표했습니다. 종이 교과서의 시대를 넘어, 데이터와 AI로 아이마다 맞춤 교육을 하겠다는 큰 그림이었죠. 그 중심에 바로 AI 디지털교과서가 있었습니다. 야심 찬 출발이었습니다.",
   [("kr_s2a",6303,"a friendly national plan poster about digital education reform, hopeful, warm storybook","2023 · 디지털 교육혁신 방안"),
    ("kr_s2z",6311,"a hopeful vision of personalized learning with data and AI beyond paper books, storybook","아이마다 맞춤 교육의 큰 그림")]),
  ("2024 · 도입 확정, 그리고 걱정","2024년 말, 정부는 2025년부터 수학과 영어, 정보 과목에 AI 디지털교과서를 넣기로 확정했습니다. 기대가 컸습니다. 하지만 동시에 걱정도 터져 나왔죠. 아이들이 화면에 과몰입하는 건 아닐까, 준비가 충분한 걸까. 기대와 우려가 함께 출발선에 섰습니다.",
   [("kr_s3a",6304,"glowing AI digital textbooks on tablets ready for a "+KR+"classroom, hopeful but a small worry cloud above, storybook","2024 · 도입 확정"),
    ("kr_s3z",6312,"parents and teachers with mixed feelings, hope and worry side by side, storybook","기대와 과몰입 우려가 함께")]),
  ("2025.3 · 교실에 들어오다","2025년 3월, AI 디지털교과서가 드디어 교실에 들어왔습니다. 초등학교 3, 4학년과 중학교 1학년, 고등학교 1학년이 대상이었죠. 태블릿 속 AI가 아이마다 속도를 맞추고, 틀린 문제를 다시 짚어 주는 맞춤 학습을 내세웠습니다. 미래가 성큼 온 것 같았습니다.",
   [("kr_s4a",6305,"a "+KR+"classroom of children using new glowing AI tablets, personalized learning, bright, storybook","2025.3 · 교실에 들어오다"),
    ("kr_s4z",6313,"an AI tablet adjusting to each child's pace, personalized help, warm storybook","아이마다 속도를 맞추는 맞춤 학습")]),
  ("2025 여름 · 한 걸음 뒤로","그런데 넉 달 만에 흐름이 꺾였습니다. 교사와 학부모의 반발이 이어졌고, 결국 국회는 AI 디지털교과서를 '핵심 교재'에서 '보조 교재'로 되돌렸습니다. 반드시 써야 하는 것에서, 골라 쓰는 것으로 지위가 내려앉은 겁니다. 큰 걸음이 한 걸음 뒤로 물러섰습니다.",
   [("kr_s5a",6306,"a "+KR+"AI tablet being gently set aside back beside a paper book, a step back, thoughtful mood, storybook","넉 달 만에 보조교재로"),
    ("kr_s5z",6314,"a national policy stepping back one careful step, thoughtful muted storybook","핵심에서 보조로 내려앉다")]),
  ("흔들린 도입 · 왜","숫자가 그 흔들림을 보여 줍니다. 채택률은 첫 학기 37퍼센트에서, 다음 학기 19퍼센트로 반토막이 났습니다. 왜였을까요. 준비보다 속도가 앞섰고, 디지털 과몰입에 대한 걱정이 컸으며, 효과가 확실하지 않다는 논란도 있었습니다. 좋은 의도만으로는 부족했던 겁니다.",
   [("kr_s6a",6307,"a wobbly path with numbers falling from 37 to 19, a "+KR+"school unsure, thoughtful muted storybook","채택률 37에서 19로"),
    ("kr_s6z",6315,"speed running ahead of preparation, a lesson learned, storybook","준비보다 속도가 앞섰다")]),
  ("세계와 비교 · 우리는 어디에","여기서 잠깐 세계를 봅시다. 중국은 2017년부터 국가 전략으로 십 년 가까이 차근차근 준비했습니다. 영국은 안전과 책임의 규칙을 먼저 세웠고, 싱가포르는 네 원칙으로 균형을 잡았죠. 그에 비해 한국은 빠르게 넣고 빠르게 뺐습니다. 방향이 틀렸던 게 아니라, 준비와 사회적 합의가 부족했던 겁니다.",
   [("kr_a1",6331,"a world map comparing steady long preparation versus a quick in and out, thoughtful storybook","세계는 길게 준비, 한국은 빠르게"),
    ("kr_a2",6332,"a "+KR+"path missing a step of preparation and agreement, storybook","준비와 합의가 부족했다")]),
  ("과몰입 걱정 · 진짜 문제","반대의 큰 이유였던 디지털 과몰입 걱정도 짚어 봅시다. 사실 이건 교과서만의 문제가 아닙니다. 아이가 화면 앞에서 스스로 멈추고 생각하는 힘이 없다면, 어떤 도구든 위험하죠. 반대로 그 힘이 있다면, AI는 훌륭한 배움의 친구가 됩니다. 문제는 도구가 아니라, 습관이었던 겁니다.",
   [("kr_a3",6333,"a "+KR+"child learning to pause and think in front of a screen, self-control glowing, storybook","멈추고 생각하는 힘이 먼저"),
    ("kr_a4",6334,"a friendly AI becoming a good learning friend when the child has good habits, warm storybook","문제는 도구가 아니라 습관")]),
  ("그럼에도, 방향은 맞았다","오해하지 마세요. AI교육의 방향 자체가 틀린 건 아닙니다. 세계가 다 그쪽으로 가고 있으니까요. 다만 한국은 속도 조절에 실패했을 뿐입니다. 그러니 우리가 할 일은 AI를 포기하는 게 아니라, 집에서 올바른 습관부터 단단히 다지며 이 흐름을 함께 타는 것입니다.",
   [("kr_a5",6335,"a correct direction with better pacing, a hopeful steady path forward, warm storybook","방향은 맞았다, 속도만 조절")]),
  ("교훈 · 도구는 흔들린다","여기서 배울 점이 있습니다. 학교에 어떤 도구가 들어오고 나가는지는, 정책에 따라 계속 바뀔 수 있다는 겁니다. AI교과서일 수도, 다른 무엇일 수도 있죠. 도구는 흔들립니다. 그렇다면 흔들리지 않는 건 무엇일까요.",
   [("kr_s9a",6316,"tools coming and going in a school, changing with policy, but something steady remains, storybook","도구는 정책 따라 흔들린다"),
    ("kr_s9b",6317,"a steady warm light remaining while tools change around it, storybook","흔들리지 않는 것은 무엇일까")]),
  ("그래서, 가정이 답이다","답은 가정입니다. 어떤 교과서 논쟁과도 무관하게, 아이의 '다시 묻는 힘'은 집에서 지킬 수 있습니다. 학교 정책은 해마다 바뀌어도, 저녁 식탁의 대화는 바뀌지 않으니까요. AI가 답을 주면, '이상한 부분 없을까?' 한마디를 건네는 겁니다. 그 습관이 진짜 교육입니다.",
   [("kr_s7a",6308,"a warm "+KR+"home evening, a parent and child talking about an AI answer together, steady and cozy, storybook","'다시 묻는 힘'은 가정이 지킨다"),
    ("kr_s10a",6318,"a "+KR+"parent gently asking 'is there anything strange here' about an AI answer, warm home, storybook","'이상한 부분 없을까?' 한마디")]),
  ("그럼, 한국 가정은","거창할 필요 없습니다. AI가 답을 주면 '진짜인지 어떻게 확인할까?'를 묻고, 'AI 없이 너라면 어떻게 했을까?'를 물어보세요. 방금 그건 네가 한 것인지, AI가 한 것인지도 함께 짚어 주고요. 짧은 질문 몇 개가, 학교가 못다 한 교육을 채웁니다.",
   [("kr_s10b",6319,"a "+KR+"parent and child checking if an AI answer is true together, warm home, storybook","'진짜인지 어떻게 확인할까?'"),
    ("kr_s10c",6320,"a child proudly showing what they did themselves versus AI, storybook","'네가 한 거야, AI가 한 거야?'")]),
  ("그럼 아이는","그러면 아이는, 학교가 흔들려도 스스로 확인하고 다시 묻는 힘을 잃지 않습니다. 정답을 빨리 받는 아이가 아니라, 정답을 검증하는 아이. 나라가 미처 못다 지킨 것을, 우리는 집에서 매일의 대화로 기를 수 있습니다. 시작은 오늘 저녁, 질문 하나입니다.",
   [("kr_s8a",6309,"a "+KR+"child confidently finding a mistake in an AI answer and re-asking with a smile, hopeful storybook","스스로 확인하고 다시 묻는 아이로"),
    ("kr_s11a",6321,"a warm hopeful evening of a "+KR+"parent and child talking happily together, storybook","오늘 저녁, 질문 하나부터")]),
]),
}
def tts(text,out):
    tf=out+".txt"; open(tf,"w",encoding="utf-8").write(text)
    run([EDGE,f"{HERE}/_tts_param.py",tf,out,VOICE,"+0%","+0Hz"])
def sdxl(scene,seed,out):
    g={"4":{"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"RealVisXL_V5.0_fp16.safetensors"}},
       "5":{"class_type":"EmptyLatentImage","inputs":{"width":1344,"height":768,"batch_size":1}},
       "6":{"class_type":"CLIPTextEncode","inputs":{"text":scene+", "+STYLE,"clip":["4",1]}},
       "7":{"class_type":"CLIPTextEncode","inputs":{"text":NEG,"clip":["4",1]}},
       "3":{"class_type":"KSampler","inputs":{"seed":seed,"steps":30,"cfg":6.5,"sampler_name":"dpmpp_2m","scheduler":"karras","denoise":1.0,"model":["4",0],"positive":["6",0],"negative":["7",0],"latent_image":["5",0]}},
       "8":{"class_type":"VAEDecode","inputs":{"samples":["3",0],"vae":["4",2]}},
       "9":{"class_type":"SaveImage","inputs":{"filename_prefix":"cvid","images":["8",0]}}}
    cid=uuid.uuid4().hex
    for attempt in range(3):
        try:
            pid=json.load(urllib.request.urlopen(urllib.request.Request(SRV+"/prompt",data=json.dumps({"prompt":g,"client_id":cid}).encode(),headers={"Content-Type":"application/json"}),timeout=30))["prompt_id"]
            t0=time.time()
            while time.time()-t0<300:
                h=json.load(urllib.request.urlopen(SRV+f"/history/{pid}",timeout=30))
                if pid in h and h[pid].get("outputs"): break
                time.sleep(2)
            im=h[pid]["outputs"]["9"]["images"][0]
            q=urllib.parse.urlencode({"filename":im["filename"],"subfolder":im.get("subfolder",""),"type":im["type"]})
            open(out,"wb").write(urllib.request.urlopen(SRV+"/view?"+q,timeout=30).read()); return
        except Exception as e: print(f"  [재시도 {attempt+1}/3] {out}: {repr(e)[:60]}"); time.sleep(6)
    raise RuntimeError("sdxl 실패: "+out)
def overlay_png(title,caption,out):
    W,H=1280,720; im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); b=16
    for r in [(0,0,W,b),(0,H-b,W,H),(0,0,b,H),(W-b,0,W,H)]: d.rectangle(r,fill=(28,18,12,235))
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rectangle([b,b,W-b,H-b],outline=(0,0,0,120),width=22)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); d=ImageDraw.Draw(im)
    fs=46; f=F(fs)
    while d.textlength(title,font=f)>W-360 and fs>26: fs-=2; f=F(fs)
    tw=d.textlength(title,font=f); cx=W//2; y=34; pad=34; hh=fs+28; x0,x1=cx-tw/2-pad,cx+tw/2+pad
    d.polygon([(x0-24,y+hh/2),(x0,y+6),(x0,y+hh-6)],fill=(150,96,52)); d.polygon([(x1+24,y+hh/2),(x1,y+6),(x1,y+hh-6)],fill=(150,96,52))
    d.rounded_rectangle([x0,y,x1,y+hh],radius=12,fill=(245,232,205),outline=(150,96,52),width=4); d.text((cx-tw/2,y+13),title,font=f,fill=(60,40,20))
    cfs=42; cf=F(cfs)
    while d.textlength(caption,font=cf)>W-80 and cfs>24: cfs-=2; cf=F(cfs)
    cw=d.textlength(caption,font=cf); cxx=(W-cw)/2; cyy=H-cfs-48
    for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,3),(0,-3),(3,0),(-3,0)]: d.text((cxx+dx,cyy+dy),caption,font=cf,fill=(0,0,0))
    d.text((cxx,cyy),caption,font=cf,fill=(255,255,255)); im.save(out)
def build_one(key):
    title,SEC=COUNTRIES[key]
    A=f"{BASE}/assets/{key}-ai-education"; ILL=f"{A}/illust/scenes"; OVL=f"{A}/illust/overlays"; RND=f"{A}/render"
    for p in (ILL,OVL,RND,f"{TMP}/{key}"): os.makedirs(p,exist_ok=True)
    sys.path.insert(0,HERE); import reassemble_dissolve as RD
    beats_all=[]; auds=[]
    for sec_title,narr,beats in SEC:
        raw=f"{TMP}/{key}/{beats[0][0]}_raw.mp3"; tts(narr,raw)
        sa=f"{TMP}/{key}/{beats[0][0]}.mp3"; run([FF,"-hide_banner","-loglevel","error","-y","-i",raw,"-filter:a",f"atempo={SPEED}",sa])
        sd=dur(sa); auds.append(sa); per=sd/len(beats)
        for subfile,seed,scene,cap in beats:
            ip=f"{ILL}/{subfile}.png"
            if not os.path.exists(ip): print("  gen",subfile); sdxl(scene,seed,ip)
            op=f"{OVL}/{subfile}.png"; overlay_png(sec_title,cap,op)
            beats_all.append((ip,op,per))
        print(" sec",sec_title[:16],round(sd,2),"s")
    out=f"{RND}/{key}-ai-longform.mp4"
    RD.assemble(beats_all,auds,out,f"{TMP}/{key}/dtmp")
    print(f"[{key}] {title} · {round(dur(out),1)}s -> {out}")
    return out
if __name__=="__main__":
    for k in (sys.argv[1:] or ["uk","singapore","korea"]):
        build_one(k)
