#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-craft-kids 전면 개편 사이트 생성기 — 그림책형 교육 랜딩(시안 반영).
루트 클린패스 페이지 + world-cases/·videos/ 서브폴더. 국가 일러스트·영상 재사용."""
import os
ROOT=os.path.dirname(os.path.abspath(__file__))
SCENE="assets/world-ai-education-5min/illust/scenes"
RENDER="assets/world-ai-education-5min/render"
POSTER="assets/world-ai-education-5min/poster"
VIDEO_MAIN=f"{RENDER}/world-ai-education-illust-v2.mp4"
def _yt_main():
    """메인 영상 유튜브 ID를 upload_queue.json(wae-illust-v2)에서 읽음. 없으면 폴백."""
    import json as _j
    try:
        q=_j.load(open(os.path.join(ROOT,"youtube","upload_queue.json"),encoding="utf-8"))
        for it in q["queue"]:
            if it["video_id"]=="wae-illust-v2":
                ref=it.get("youtube_id") or (it.get("youtube_url") or "").rstrip("/").split("/")[-1]
                if ref: return ref
    except Exception: pass
    return "lY9B2t1k1Io"   # 임시 폴백(데이터 없을 때만)
YT_MAIN=_yt_main()
NAV=[("홈","/","home"),("왜 필요한가","/why-ai-education.html","why"),("세계 사례","/world-cases.html","cases"),
     ("시작 가이드","/start-guide.html","start"),("영상","/videos.html","videos"),("부모용 자료","/parent-resources.html","res")]

def head(title,desc,base):
    return f"""<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:type" content="website"><meta name="theme-color" content="#FBF6EE">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">
<link rel="stylesheet" href="{base}styles/main.css">
</head><body>"""

def header(active,base):
    links="".join(f'<a href="{base.rstrip("/") or ""}{u}" class="{"active" if k==active else ""}">{n}</a>' for n,u,k in NAV)
    return f"""<header class="site"><div class="wrap nav">
<a class="brand" href="{base or "/"}"><span class="bot">🤖</span> AI 조기교육</a>
<button class="hamb" aria-label="메뉴" onclick="document.getElementById('nav').classList.toggle('open')">☰</button>
<nav class="nav-links" id="nav">{links}
<a class="btn btn-primary nav-cta" href="{base or "/"}start-guide.html">무료로 시작하기</a></nav>
</div></header>"""

def footer(base):
    b=base or "/"
    return f"""<footer class="site"><div class="wrap"><div class="foot-grid">
<div class="foot-brand"><a class="brand" href="{b}"><span class="bot">🤖</span> AI 조기교육</a>
<p>아이와 부모가 함께 성장하는<br>미래 교육의 시작</p></div>
<div class="foot-col"><h5>서비스</h5><a href="{b}start-guide.html">시작 가이드</a><a href="{b}videos.html">영상</a><a href="{b}parent-resources.html">부모용 자료</a><a href="{b}free-kit.html">무료 자료</a></div>
<div class="foot-col"><h5>소개</h5><a href="{b}why-ai-education.html">왜 필요한가</a><a href="{b}world-cases.html">세계 사례</a><a href="{b}why-ai-education.html#philosophy">우리의 철학</a></div>
<div class="foot-col"><h5>고객 지원</h5><a href="{b}parent-resources.html#faq">자주 묻는 질문</a><a href="{b}start-guide.html">이용 가이드</a><a href="{b}privacy/">개인정보처리방침</a></div>
<div class="foot-col"><h5>문의</h5><a href="mailto:2011kstudentlife@gmail.com">2011kstudentlife@gmail.com</a><a href="{b}videos.html">영상관</a></div>
</div><div class="foot-bottom">© 2026 AI조기교육. 아이가 AI와 대화하며 '다시 묻는 힘'을 기르는 교육.</div></div></footer>
<script src="{base}scripts/main.js" defer></script></body></html>"""

def page(active,base,title,desc,body):
    return head(title,desc,base)+header(active,base)+body+footer(base)

# ---------- 국가 데이터 ----------
COUNTRIES=[
 ("china","중국","🇨🇳",f"{SCENE}/china.png","AI 리터러시를 의무 교육으로 확대.",
  "학교 안으로 AI, 그래도 다 맡기진 않는다",
  ["초·중등에서 AI·코딩·로봇을 정규 교육으로 편성","AI 도구를 직접 다루는 실습 중심","빠른 확산 속에서도 '과의존 경계'가 과제"],
  "학교 밖에서도 AI 접점을 자연스럽게 만들되, 아이가 '직접 한 부분'을 스스로 말하게 하기.",
  "AI가 도와준 것 중에, 네가 직접 한 건 뭐야?"),
 ("usa","미국","🇺🇸",f"{SCENE}/usa.png","프로젝트 기반으로 창의적 문제 해결 교육.",
  "많이 쓰기가 아니라, 이해하고 의심하고 고쳐 쓰기",
  ["AI 리터러시 = 이해하고 의심하고 수정하는 힘","프로젝트로 실제 문제를 풀며 사고력 훈련","'많이 쓰는' 능력보다 '검증하는' 능력 강조"],
  "AI 답을 그대로 받지 말고, 아이가 이상한 부분을 찾아 고쳐 쓰게 하기.",
  "이 답에서 이상한 부분 하나만 찾아볼까?"),
 ("uk","영국","🇬🇧",f"{SCENE}/uk.png","비판적 사고와 데이터 이해를 핵심 역량으로.",
  "AI는 도구, 판단과 책임은 사람에게",
  ["정책적으로 'AI는 교사를 대체하지 않는다' 명시","최종 판단·책임은 사람에게 남긴다","데이터·근거를 비판적으로 읽는 힘 강조"],
  "AI에 결정을 맡기지 않고, 최종 선택은 아이가 하도록 습관 들이기.",
  "AI 말이 맞는지, 네 생각은 어때?"),
 ("singapore","싱가포르","🇸🇬",f"{SCENE}/sg.png","AI를 일상 속 도구로, 실습 중심 수업.",
  "쓰게 하되, 안전한 틀 안에서",
  ["가드레일(안전한 틀) 안에서 AI를 사용","아이 생각이 AI 뒤로 숨지 않게 설계","디지털 학습 도구를 교사가 감독·안내"],
  "사용 규칙과 시간을 아이와 함께 정하고, 'AI 없이라면?'을 자주 묻기.",
  "AI 없이 너라면 어떻게 했을까?"),
 ("korea","한국","🇰🇷",f"{SCENE}/kr.png","맞춤형 AI 교육 가이드로 학교·가정 연계 강화.",
  "학교 도입과 아이 습관은 다르다",
  ["AI 디지털교과서로 학교가 AI를 들여오기 시작","맞춤형 학습·데이터 기반 지도","'학교 도입'과 '집에서의 습관'은 별개의 과제"],
  "학교가 AI를 들여와도, '다시 묻는 힘'은 집에서 대화로 길러야 한다.",
  "오늘 AI랑 뭐 했어? 뭘 다시 물어봤어?"),
 ("germany","독일","🇩🇪",f"{SCENE}/germany.png","AI보다 신뢰와 기반을 먼저 — 프라이버시 우선 분권형.",
  "신뢰와 기반을 먼저",
  ["디지털팍트로 인프라·교사부터","GDPR·EU AI법으로 아이 데이터 보호","전국 필수화보다 기반·신뢰 우선"],
  "기술보다 안전과 신뢰를 먼저 세우고, 결정은 아이에게 남긴다.",
  "이 답에 개인정보는 안 들어갔지? 안전하게 썼어?"),
 ("japan","일본","🇯🇵",f"{SCENE}/japan.png","기기·프로그래밍 먼저, 생성형 AI는 비판적으로.",
  "기기·논리 먼저, AI는 비판적으로",
  ["GIGA로 1인 1기기 먼저","프로그래밍으로 논리적 사고","생성형 AI는 검증하며 비판적으로"],
  "순서대로 생각하는 힘을 먼저, AI 답은 검증하는 습관을 집에서.",
  "그거 어떤 순서로 한 거야? AI 답은 진짜인지 확인해봤어?"),
]

# ---------- 홈 ----------
def home():
    val=f"""<div class="value-row">
<div class="value"><div class="vicon vteal">💬</div><div><h4>말로 요청하기</h4><p>생각을 말로 정리하고 AI에게 정확히 전달해요.</p></div></div>
<div class="value"><div class="vicon vblue">👁️</div><div><h4>결과 관찰하기</h4><p>AI의 결과를 비교하고 무엇이 좋은지 살펴봐요.</p></div></div>
<div class="value"><div class="vicon vcoral">🔁</div><div><h4>다시 묻기</h4><p>더 나은 결과를 위해 다시 질문하고 발전시켜요.</p></div></div></div>"""
    cc="".join(f"""<a class="card country" href="/world-cases/{c[0]}.html">
<div class="thumb"><img src="/{c[3]}" alt="{c[1]} AI교육" loading="lazy"></div>
<div class="body"><div class="flag"><span class="fl">{c[2]}</span>{c[1]}</div><p>{c[4]}</p></div></a>""" for c in COUNTRIES)
    phil="".join(f"""<div class="card phil"><div class="pic">{ic}</div><div><h4>{t}</h4><p>{d}</p></div></div>"""
        for ic,t,d in [("🖼️","출력물은 결과","멋진 결과물은 과정의 일부일 뿐이에요."),
        ("🌱","교육은 과정","생각을 말하고, 관찰하고, 다시 묻는 과정이 핵심이에요."),
        ("👨‍👦","부모는 감독이 아니라 동반자","함께 탐색하고 격려하며, 질문을 던지는 동반자가 돼요."),
        ("💬","중요한 것은 다시 묻는 힘","포기하지 않고 더 나은 답을 찾아가는 힘을 길러요.")])
    small=[("AI 결과가 마음에 안 들 때 대처법","6:15",f"{SCENE}/usa_b3.png"),
           ("좋은 프롬프트의 3가지 비밀","7:02",f"{SCENE}/common_b2.png"),
           ("아이와 함께하는 AI 프로젝트 예시","9:10",f"{SCENE}/parent.png")]
    sm="".join(f"""<a class="vcard" href="/videos.html"><div class="vthumb"><img src="/{img}" alt="{t}" loading="lazy"><div class="play"><span>▶</span></div><span class="len">{ln}</span></div><div class="vmeta"><h4>{t}</h4></div></a>""" for t,ln,img in small)
    steps="".join(f"""<div class="step {cl}"><div class="num">{n}</div><h4>{t}</h4><p>{d}</p></div>"""
        for n,cl,t,d in [(1,"","원하는 결과 떠올리기","아이와 함께 상상하고 무엇을 만들지 정해요."),
        (2,"b","AI에게 요청하기","생각을 말로 정리해 AI에 요청해요."),
        (3,"g","마음에 안 들면 다시 말하기","더 나은 결과를 위해 다시 설명해요.")])
    quotes="".join(f"""<div class="quote"><p class="q">"{q}"</p><div class="who"><div class="av">{av}</div><div><div class="stars">★★★★★</div><div class="name">{n}</div></div></div></div>"""
        for q,av,n in [("결과물보다 아이가 질문을 계속하고 스스로 수정하는 모습이 더 좋았어요. AI와 대화하는 경험이 사고력을 키워줘요.","🧑","김o준 님 · 초3 학부모"),
        ("아이가 스스로 프롬프트를 쓰고 결과를 분석해요. 이제는 숙제보다 AI 프로젝트를 더 즐거워해요!","🧑‍🦱","이o우 님 · 초5 학부모"),
        ("부모인 저도 함께 배우니 아이와 대화가 늘고, 새로운 놀이가 생겼어요.","👩","박o연 님 · 초2 학부모")])
    body=f"""<main>
<section class="hero"><div class="wrap"><div class="hero-grid">
<div><h1>아이와 함께 배우는<br><span class="coral">생성형 AI</span></h1>
<p class="sub">정답을 찾는 교육이 아니라, 다시 묻고 더 나은 결과를 만드는 힘을 기르는 과정형 AI 교육.</p>
<div class="hero-btns"><a class="btn btn-primary btn-lg" href="/start-guide.html">시작 가이드 보기 →</a>
<a class="btn btn-ghost btn-lg" href="/world-cases.html">🌍 세계 AI교육법 연재</a></div></div>
<div class="hero-art"><img src="/{SCENE}/parent.png" alt="아이와 부모가 함께 AI로 배우는 모습"></div>
</div><div class="hero-banner">결과물이 아니라 <span style="color:#FFD98A">과정이</span> 교육이다.</div></div></section>

<section class="block"><div class="wrap">{val}</div></section>

<section class="block"><div class="wrap"><h2 class="sec-title">세계는 아이에게 AI를 어떻게 가르치나</h2>
<div class="grid g5">{cc}</div></div></section>

<section class="block" id="philosophy"><div class="wrap"><h2 class="sec-title">우리의 핵심 철학</h2>
<div class="grid g4">{phil}</div></div></section>

<section class="block"><div class="wrap"><h2 class="sec-title">설명형 AI 영상으로 쉽게 배워요</h2>
<div class="video-feature">
<a class="vcard" href="/videos/world-ai-education.html"><div class="vthumb"><img src="/{POSTER}/world-ai-education-v2.jpg" alt="세계 AI교육 본편"><div class="play"><span>▶</span></div><span class="len">2:41</span></div>
<div class="vmeta"><h4>세계 5개국은 아이에게 AI를 어떻게 가르치나</h4><p>부모 눈높이로 정리한 대표 영상</p></div></a>
<div class="vsmall-list">{sm}</div></div>
<div class="center" style="margin-top:16px"><a href="/videos.html" style="color:var(--coral);font-weight:700">모든 영상 보러가기 →</a></div>
</div></section>

<section class="block"><div class="wrap"><h2 class="sec-title">집에서 이렇게 시작하세요</h2>
<div class="steps3">{steps}</div>
<div class="center" style="margin-top:18px"><a class="btn btn-ghost" href="/start-guide.html">전체 6단계 가이드 보기 →</a></div></div></section>

<section class="block"><div class="wrap"><h2 class="sec-title">부모님들의 이야기</h2>
<div class="grid g3">{quotes}</div></div></section>

<section class="block"><div class="wrap"><div class="cta-band">
<div><h3>오늘부터 아이와 함께 AI를 연습해보세요</h3><p>무료 자료와 가이드로 쉽고 안전하게 시작할 수 있어요.</p></div>
<a class="btn btn-lg" href="/free-kit.html">무료 자료 받기 ⬇</a></div></div></section>
</main>"""
    return page("home","",
      "아이와 함께 배우는 생성형 AI | AI 조기교육",
      "정답이 아니라 다시 묻는 힘. 아이가 AI와 대화하며 사고력을 기르는 과정형 AI 교육. 세계 5개국 사례·부모 시작 가이드·설명 영상.",body)

# ---------- 서브 페이지들 ----------
def why():
    body=f"""<main>
<section class="page-hero"><div class="wrap"><div class="pill">우리의 철학</div>
<h1>결과물이 아니라, 과정이 교육이다</h1>
<p>멋진 그림 한 장이 목표가 아닙니다. 아이가 AI와 대화하며 <b>질문하고, 관찰하고, 다시 묻는 힘</b>을 기르는 것이 진짜 교육입니다.</p></div></section>
<section class="block"><div class="wrap" style="max-width:820px">
<h2>왜 지금, AI 조기교육일까요?</h2>
<p>아이들은 이미 챗봇·이미지 생성 AI를 만나고 있습니다. 문제는 '쓰느냐'가 아니라 <b>'어떻게 쓰느냐'</b>입니다. AI가 준 답을 그대로 받아들이는 아이와, 이상한 곳을 찾아 다시 묻는 아이는 완전히 다르게 자랍니다.</p>
<div class="callout" style="margin:22px 0">핵심 질문은 하나입니다 — <b>"AI에게 정답을 맡길 것인가, 아이에게 다시 묻는 힘을 길러줄 것인가?"</b></div>
<h2 id="philosophy" style="margin-top:34px">우리의 4가지 원칙</h2>
<div class="grid g4" style="margin-top:16px">
<div class="card phil"><div class="pic">🖼️</div><div><h4>출력물은 결과</h4><p>멋진 결과물은 과정의 일부일 뿐이에요.</p></div></div>
<div class="card phil"><div class="pic">🌱</div><div><h4>교육은 과정</h4><p>말하고, 관찰하고, 다시 묻는 과정이 핵심.</p></div></div>
<div class="card phil"><div class="pic">👨‍👦</div><div><h4>부모는 동반자</h4><p>감독이 아니라 함께 탐색하는 동반자.</p></div></div>
<div class="card phil"><div class="pic">💬</div><div><h4>다시 묻는 힘</h4><p>포기하지 않고 더 나은 답을 찾는 힘.</p></div></div></div>
<div class="cta-band" style="margin-top:34px"><div><h3>세계는 이미 이렇게 가르치고 있어요</h3><p>중국·미국·영국·싱가포르·한국의 사례를 확인해보세요.</p></div><a class="btn btn-lg" href="/world-cases.html">세계 사례 보기 →</a></div>
</div></section></main>"""
    return page("why","","왜 AI 조기교육인가 | AI 조기교육","AI를 쓰느냐가 아니라 어떻게 쓰느냐. 아이에게 다시 묻는 힘을 길러주는 과정형 교육 철학.",body)

def world_cases():
    chip="display:inline-block;font-size:12px;font-weight:700;text-decoration:none;border-radius:8px;padding:4px 9px;border:1px solid"
    def eps(slug):
        e=[("1편·정책",f"/world-cases/{slug}.html","#f0d8cc","#E0684A","#fff"),
           ("2편·실제운영",f"/world-cases/{slug}-2.html","#E4D8C4","#8a6f45","#fff"),
           ("3편·우리집",f"/world-cases/{slug}-3.html","#cfe6d6","#188038","#f2fbf5")]
        return "".join(f'<a href="{h}" style="{chip} {bd};color:{co};background:{bg}">{t}</a>' for t,h,bd,co,bg in e)
    cc="".join(f"""<div class="card country">
<a href="/world-cases/{c[0]}.html"><div class="thumb"><img src="/{c[3]}" alt="{c[1]}" loading="lazy"></div></a>
<div class="body"><div class="flag"><span class="fl">{c[2]}</span>{c[1]}</div><p>{c[4]}</p>
<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:10px">{eps(c[0])}</div></div></div>""" for c in COUNTRIES)
    steps="".join(f"""<div class="step {cl}"><div class="num">{n}</div><h4>{t}</h4><p>{d}</p></div>"""
        for n,cl,t,d in [(1,"","세계가 이렇게 (정책)","각 나라가 왜 그렇게 가르치는지 — 타임라인과 근거."),
        (2,"b","실제로 이렇게 (교실)","학년별로 매주 실제로 무엇을, 어떤 도구로 가르치는지."),
        (3,"g","우리 집은 이렇게 (적용)","그 방식을 우리 아이의 한 주 습관으로. 무료 자료까지.")])
    body=f"""<main>
<section class="page-hero"><div class="wrap"><div class="pill">📚 무료 연재</div>
<h1>세계 AI교육법</h1>
<p>중국·미국·영국·싱가포르·한국은 아이에게 AI를 <b>실제로</b> 어떻게 가르칠까요? 정책부터 교실, 그리고 우리 집 적용까지 — <b>매주 한 편씩 무료로</b> 풀어갑니다.</p></div></section>
<section class="block"><div class="wrap"><h2 class="sec-title">각 나라를 3편으로 읽으세요</h2>
<div class="steps3">{steps}</div></div></section>
<section class="block" style="background:var(--cream2)"><div class="wrap"><h2 class="sec-title">나라별 연재</h2>
<p class="sec-desc">각 카드에서 1편(정책) · 2편(실제 교실) · 3편(우리 집)을 바로 열 수 있어요.</p>
<div class="grid g3">{cc}</div></div></section>
<section class="block"><div class="wrap"><div class="cta-band">
<div><h3>지금 바로 시작</h3><p>어느 나라든 3편 '우리 집 적용'에는 바로 쓰는 무료 자료가 붙어 있어요.</p></div><a class="btn btn-lg" href="/free-kit.html">무료 자료 받기 ⬇</a></div>
<div class="cta-band" style="margin-top:14px"><div><h3>영상으로 5개국을 한 번에</h3><p>대표 영상에서 5개국 흐름을 정리했어요.</p></div><a class="btn btn-lg" href="/videos/world-ai-education.html">영상 보기 →</a></div>
</div></section></main>"""
    return page("cases","","세계 AI교육법 · 무료 연재 | AI 조기교육","중국·미국·영국·싱가포르·한국이 아이에게 AI를 실제로 가르치는 법. 정책·실제 교실·우리 집 적용을 3편 무료 연재로.",body)

def country_page(c):
    key,name,flag,img,short,msg,points,learn,q=c
    pts="".join(f"<li>{p}</li>" for p in points)
    idx=[x[0] for x in COUNTRIES].index(key)
    anchor={"china":"china","usa":"usa","uk":"uk","singapore":"singapore","korea":"korea"}[key]
    body=f"""<main>
<section class="block" style="padding:20px 0 0"><div class="wrap" style="max-width:900px">
<div class="crumb" style="margin-bottom:4px"><a href="/world-cases.html">← 세계 사례</a></div>
<h1 style="font-size:25px;line-height:1.3;margin:0 0 16px">{flag} {name} · {msg}</h1>
<div class="cta-band" style="margin-bottom:28px"><div><h3>이 내용을 영상으로 보기</h3><p>{name} 편을 영상에서 바로 확인하세요.</p></div><a class="btn btn-lg" href="/videos/world-ai-education.html#{anchor}">▶ 영상에서 보기</a></div>
<div class="card pad0" style="margin-bottom:26px"><img src="/{img}" alt="{name} AI교육" style="width:100%"></div>
<h2>{name}의 AI교육 방향</h2><ul class="checklist" style="padding:0">{pts}</ul>
<h2 style="margin-top:28px">아이에게 가르치는 핵심 능력</h2>
<div class="callout">{msg}</div>
<h2 style="margin-top:28px">한국 가정에서 배울 점</h2><p>{learn}</p>
<h2 style="margin-top:28px">부모가 아이와 해볼 질문</h2>
<div class="callout good">💬 "{q}"</div>
<div class="center" style="margin-top:24px"><a href="/world-cases.html" style="color:var(--coral);font-weight:700">← 다른 나라 사례 보기</a></div>
</div></section></main>"""
    return page("cases","../",f"{name} AI교육 사례 | AI 조기교육",f"{name}이 아이에게 AI를 가르치는 법과 한국 가정에서 배울 점. {short}",body)

def videos():
    cats=["전체","세계 사례"]
    fil="".join(f'<button class="{"on" if i==0 else ""}" data-f="{c}">{c}</button>' for i,c in enumerate(cats))
    vids=[("중국 · 학교 안으로 AI, 그래도 다 맡기진 않는다","세계 사례","롱폼 다큐",f"{SCENE}/china.png","/videos/china-ai-education.html"),
          ("미국 · 많이보다, 이해하고 의심하고 고쳐 쓰기","세계 사례","롱폼 다큐",f"{SCENE}/usa.png","/videos/us-ai-education.html"),
          ("영국 · AI는 도구, 판단과 책임은 사람에게","세계 사례","심층 페이지",f"{SCENE}/uk.png","/videos/uk-ai-education.html"),
          ("싱가포르 · 안전한 틀(가드레일) 안에서","세계 사례","심층 페이지",f"{SCENE}/sg.png","/videos/singapore-ai-education.html"),
          ("한국 · AI교과서는 흔들려도, 가정 습관은 남는다","세계 사례","심층 페이지",f"{SCENE}/kr.png","/videos/korea-ai-education.html")]
    def vc(t,cat,badge,img,href):
        return f"""<a class="vcard" href="{href}" data-cat="{cat}"><div class="vthumb"><img src="/{img}" alt="{t}" loading="lazy"><div class="play"><span>▶</span></div><span class="len">{badge}</span></div>
<div class="vmeta"><h4>{t}</h4><p><span class="tag">{cat}</span></p></div></a>"""
    cards="".join(vc(*v) for v in vids)
    body=f"""<main>
<section class="page-hero"><div class="wrap"><div class="pill">📺 아이와 AI교실 영상관</div>
<h1>설명형 AI 영상으로 쉽게 배워요</h1>
<p>세계 사례, 부모 가이드, 아이와 함께하는 실습을 짧은 영상으로 정리했습니다.</p></div></section>
<section class="block" style="padding-bottom:0"><div class="wrap">
<div class="cta-band"><div><h3>📺 아이와 AI교실</h3><p>결과물이 아니라 과정이 교육이다 — 아이와 함께 말하고, 보고, 다시 묻는 생성형 AI 교육 채널.</p></div>
<a class="btn btn-lg" href="/videos/world-ai-education.html">대표 영상 보기 ▶</a></div></div></section>
<section class="block" style="padding-top:24px"><div class="wrap">
<div class="player"><iframe src="https://www.youtube.com/embed/{YT_MAIN}" title="세계 5개국 AI교육" loading="lazy" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
<p class="center" style="margin-top:12px;color:var(--muted)">대표 영상 · 세계 5개국은 아이에게 AI를 어떻게 가르치나</p></div></section>
<section class="block"><div class="wrap">
<div class="filters" id="filters">{fil}</div>
<div class="grid g3" id="vgrid">{cards}</div>
<p class="center" style="color:var(--muted);margin-top:20px;font-size:14px">※ 중국·미국 편은 영상이, 영국·싱가포르·한국 편은 심층 페이지가 준비돼 있어요. 영상은 순차 확장됩니다. 자동재생 없이, 누르셔야 재생됩니다.</p>
</div></section></main>"""
    return page("videos","","AI교육 영상관 | AI 조기교육","세계 사례·부모 가이드·아이 실습을 짧은 설명 영상으로. 자동재생 없는 내부 영상관.",body)

def video_detail():
    tl=[("#opening","0:00","오프닝 — 세계는 아이에게 AI를 어떻게?"),("#china","0:23","중국 · 학교 안으로 AI"),
        ("#usa","0:41","미국 · 의심하는 힘"),("#uk","0:58","영국 · 판단은 사람"),
        ("#singapore","1:15","싱가포르 · 가드레일"),("#korea","1:33","한국 · AI 디지털교과서"),("#summary","2:10","공통점과 오늘 할 일")]
    tls="".join(f'<a href="{a}" id="{a[1:]}"><span>{t}</span><span class="t">{tm}</span></a>' for a,tm,t in tl)
    rel="".join(f"""<a class="card country" href="/world-cases/{c[0]}.html"><div class="thumb"><img src="/{c[3]}" loading="lazy" alt="{c[1]}"></div><div class="body"><div class="flag"><span class="fl">{c[2]}</span>{c[1]}</div></div></a>""" for c in COUNTRIES[:3])
    body=f"""<main>
<section class="block" style="padding-top:28px"><div class="wrap">
<div class="crumb"><a href="/videos.html">영상관</a> › 세계 AI교육</div>
<div class="player"><iframe src="https://www.youtube.com/embed/{YT_MAIN}" title="세계 5개국 AI교육" loading="lazy" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
<h1 style="margin-top:22px">세계 5개국은 아이에게 AI를 어떻게 가르치나</h1>
<p style="max-width:760px;color:var(--navy2)">중국·미국·영국·싱가포르·한국의 AI교육 흐름을 부모 눈높이로 2분 41초에 정리했습니다. 방식은 달라도 공통점은 하나 — 정답이 아니라 다시 묻는 힘.</p>
<div class="grid g3" style="margin:22px 0">
<div class="card"><h4>① 학교 안으로 AI</h4><p style="color:var(--muted);margin:0">세계가 AI를 교실에 들이는 중.</p></div>
<div class="card"><h4>② 판단은 사람</h4><p style="color:var(--muted);margin:0">AI는 도구, 결정은 아이가.</p></div>
<div class="card"><h4>③ 다시 묻는 힘</h4><p style="color:var(--muted);margin:0">막는 게 아니라 다루는 힘.</p></div></div>
<h2 style="margin-top:10px">영상 속 섹션</h2>
<div class="timeline" style="max-width:560px">{tls}</div>
<h2 style="margin-top:24px">아이와 해볼 질문</h2>
<div class="callout good">💬 "오늘 AI가 준 답에서, 이상한 부분 하나만 같이 찾아볼까?"</div>
<h2 style="margin-top:24px">관련 사례</h2><div class="grid g3">{rel}</div>
<div class="cta-band" style="margin-top:28px"><div><h3>집에서 바로 시작해볼까요?</h3><p>부모 가이드와 무료 자료가 준비돼 있어요.</p></div><a class="btn btn-lg" href="/free-kit.html">무료 자료 받기 ⬇</a></div>
</div></section></main>"""
    return page("videos","../","세계 5개국 AI교육 영상 | AI 조기교육","세계 5개국이 아이에게 AI를 가르치는 법을 2분 41초에. 섹션 타임라인·부모 질문 포함.",body)

def start_guide():
    steps=[("1","원하는 결과를 말하게 하기","아이가 무엇을 만들고 싶은지 스스로 말로 정리하게 해요.",
            "\"오늘은 뭘 만들어보고 싶어? 어떤 그림/이야기가 좋을까?\"","네가 상상한 걸 나한테 설명해줄래?",
            "우주에서 피아노를 치는 고양이를 그려줘. 밤하늘 배경으로.","고양이 그려줘"),
        ("2","AI에게 첫 요청하기","생각을 문장으로 만들어 AI에 요청해요. 짧고 구체적으로.",
            "\"방금 말한 걸 AI가 알아듣게 문장으로 만들어볼까?\"","어떤 단어를 넣으면 더 정확할까?",
            "파란 배경에, 웃고 있는 강아지를 만화 스타일로 그려줘","강아지"),
        ("3","결과를 같이 관찰하기","나온 결과를 함께 보고 무엇이 좋고 아쉬운지 이야기해요.",
            "\"어디가 마음에 들어? 어디가 생각과 달라?\"","이 결과에서 좋은 점 하나, 아쉬운 점 하나는?","",""),
        ("4","마음에 안 드는 부분 찾기","AI가 완벽하지 않다는 걸 배우는 순간. 이상한 곳을 찾아요.",
            "\"AI가 실수한 곳이나 이상한 부분이 있을까?\"","여기서 뭘 바꾸면 더 좋아질까?","",""),
        ("5","다시 말하기","고칠 점을 담아 다시 요청해요. '다시 묻는 힘'의 핵심 단계.",
            "\"그럼 그 부분을 이렇게 바꿔달라고 다시 말해볼까?\"","이번엔 어떻게 다르게 말해볼까?",
            "배경을 밤하늘에서 바닷속으로 바꿔줘. 강아지는 그대로.","다시"),
        ("6","결과 비교하기","처음과 바뀐 결과를 나란히 비교하며 성장 과정을 확인해요.",
            "\"처음이랑 지금, 뭐가 더 좋아졌어?\"","네가 다시 물어봐서 뭐가 달라졌어?","","")]
    def sc(n,t,d,ment,ask,good,bad):
        gp=f'<div class="prompt-ex g">👍 좋은 프롬프트: "{good}"</div>' if good else ''
        bp=f'<div class="prompt-ex b">👎 아쉬운 프롬프트: "{bad}"</div>' if bad else ''
        return f"""<div class="card" style="margin-bottom:16px"><div class="phil" style="align-items:center;margin-bottom:12px">
<div class="pic" style="background:var(--coral);color:#fff">{n}</div><h3 style="margin:0">{t}</h3></div>
<p>{d}</p>
<div class="callout" style="margin:10px 0"><b>부모 멘트</b><br>{ment}</div>
<div class="callout good" style="margin:10px 0"><b>아이에게 물어볼 질문</b><br>💬 {ask}</div>{gp}{bp}</div>"""
    body=f"""<main>
<section class="page-hero"><div class="wrap"><div class="pill">시작 가이드</div>
<h1>집에서 따라 하는 6단계</h1><p>오늘 저녁, 아이와 15분이면 충분해요. 순서대로 따라만 하세요.</p></div></section>
<section class="block"><div class="wrap" style="max-width:760px">{"".join(sc(*s) for s in steps)}
<div class="cta-band" style="margin-top:20px"><div><h3>연습지와 질문 카드가 필요하세요?</h3><p>집에서 바로 쓰는 무료 자료를 받아보세요.</p></div><a class="btn btn-lg" href="/free-kit.html">무료 자료 받기 ⬇</a></div>
</div></section></main>"""
    return page("start","","집에서 시작하는 6단계 가이드 | AI 조기교육","아이와 AI를 시작하는 6단계. 부모 멘트·질문·좋은/나쁜 프롬프트 예시까지.",body)

def parent_resources():
    faqs=[("AI가 아이에게 위험하지 않나요?","부모와 함께, 정해진 시간·규칙 안에서 쓰면 안전해요. 핵심은 '혼자 두지 않기'입니다. 아이가 AI 답을 그대로 믿지 않고 다시 묻게 돕는 것이 안전 교육이에요."),
        ("몇 살부터 시작할 수 있나요?","말로 원하는 걸 표현할 수 있으면 시작할 수 있어요(대략 6~7세+). 어릴수록 '결과'보다 '함께 대화하는 과정'에 집중하세요."),
        ("어떤 AI 도구를 쓰면 되나요?","이미지 생성·챗봇 등 부모가 관리 가능한 도구면 됩니다. 도구보다 '어떻게 대화하는가'가 중요해요."),
        ("숙제를 AI로 시키면 안 되지 않나요?","'대신 시키기'는 위험하지만, '함께 검증하고 고쳐 쓰기'는 훌륭한 학습이에요. AI 답의 이상한 곳을 찾는 연습이 진짜 공부입니다.")]
    fq="".join(f"""<div class="card" style="margin-bottom:12px"><h4>Q. {q}</h4><p style="margin:0;color:var(--navy2)">{a}</p></div>""" for q,a in faqs)
    res="".join(f"""<div class="card"><div style="font-size:34px;margin-bottom:8px">{ic}</div><h4>{t}</h4><p style="color:var(--muted);font-size:14px">{d}</p><a class="btn btn-ghost" href="{href}" target="_blank" rel="noopener" style="margin-top:6px">열기 · 인쇄 →</a></div>"""
        for ic,t,d,href in [("📝","AI 대화 연습지","집에서 하는 첫 AI 대화 워크시트.","/free/worksheet.html"),("🃏","부모용 질문 카드","상황별로 바로 쓰는 질문 10장.","/free/question-cards.html"),("💡","첫 프롬프트 20개","아이와 시작하기 좋은 프롬프트 예시.","/free/first-prompts.html")])
    # 국가별 세부 카테고리 (좌측 아코디언 → 우측 인라인 뷰어)
    def subs(slug):
        s=[("1️⃣","1편 · 정책과 방침",f"/world-cases/{slug}.html"),
           ("2️⃣","2편 · 실제 교실 운영",f"/world-cases/{slug}-2.html"),
           ("3️⃣","3편 · 우리 집 주간 적용",f"/world-cases/{slug}-3.html")]
        if slug=="uk":
            s+=[("🗺","학년별 로드맵 (만 5~16세)",f"/world-cases/{slug}-roadmap.html"),
                ("🔬","1년 커리큘럼 (Year 8)",f"/world-cases/{slug}-year.html"),
                ("🏠","집 실전판 (단원별)",f"/world-cases/{slug}-home.html"),
                ("📅","만 8세 12주 프로그램",f"/world-cases/{slug}-8yo-12weeks.html"),
                ("🖨","12주 워크북 (인쇄·PDF)",f"/free/{slug}-12weeks-workbook.html")]
        return s
    countries=[(c[0],c[1],c[2]) for c in COUNTRIES]
    def nav_country(slug,name,flag):
        items="".join(
            (f'<a class="rs-sub" href="{h}" target="_blank" rel="noopener">{ic} {t} <span class="dl">다운로드</span></a>'
             if h.startswith("/free/") else
             f'<a class="rs-sub" href="{h}" onclick="return rsLoad(this)" data-href="{h}">{ic} {t}</a>')
            for ic,t,h in subs(slug))
        return f"""<div class="rs-cat"><button class="rs-cbtn" onclick="rsToggle('{slug}')"><span>{flag} {name}</span><span class="ar" id="ar-{slug}">▸</span></button>
<div class="rs-subs" id="sub-{slug}">{items}</div></div>"""
    nav_c="".join(nav_country(s,n,f) for s,n,f in countries)
    body=f"""<main>
<section class="page-hero"><div class="wrap"><div class="pill">부모용 자료</div>
<h1>부모 자료실</h1><p>왼쪽에서 나라를 고르면 세부 자료가 펼쳐지고, 내용은 이 페이지 안에서 바로 읽습니다.</p></div></section>
<section class="block"><div class="wrap">
<div class="rs-wrap">
<aside class="rs-side">
<div class="rs-h">📥 인쇄 자료</div>
<a class="rs-top" href="#" onclick="return rsHome()">🖨 바로 인쇄·다운로드</a>
<div class="rs-h">🌍 국가별 자료</div>
{nav_c}
<div class="rs-h">❓ 도움말</div>
<a class="rs-top" href="#" onclick="return rsFaq()">자주 묻는 질문</a>
</aside>
<div class="rs-main" id="rsMain">
<div id="rsHome">
<h3 style="margin:0 0 10px;font-size:18px">🖨 바로 인쇄·다운로드</h3>
<div class="grid g3">{res}</div>
<div style="margin-top:10px"><a class="rs-sub" style="max-width:460px" href="/free/uk-12weeks-workbook.html" target="_blank" rel="noopener">📘 만 8세 12주 홈 워크북 (표지·삽화·수료장) <span class="dl">다운로드</span></a></div>
<div class="callout" style="margin-top:22px">🌍 왼쪽에서 나라를 누르면 세부 자료(1·2·3편, 심화)가 펼쳐집니다. 내용은 페이지 이동 없이 여기서 바로 읽어요.</div>
<h3 id="faq" style="margin:26px 0 10px;font-size:18px">❓ 자주 묻는 질문</h3>{fq}
</div>
<div id="rsDoc" style="display:none">
<div class="rs-bar"><button class="btn btn-ghost" onclick="rsHome()">← 자료실 홈</button><a class="btn btn-ghost" id="rsOrig" href="#" target="_blank" rel="noopener">새 창에서 크게 ↗</a></div>
<div id="rsBody"></div>
</div>
</div></div>
</div></section>
<style>
.rs-wrap{{display:flex;gap:24px;align-items:flex-start}}
.rs-side{{width:230px;flex:none;position:sticky;top:84px;background:#fff;border:1px solid #EADFCE;border-radius:14px;padding:10px 8px;max-height:calc(100vh - 110px);overflow:auto}}
.rs-h{{font-size:11.5px;font-weight:800;color:#9b8a6e;padding:10px 12px 5px}}
.rs-top{{display:block;padding:8px 12px;border-radius:9px;text-decoration:none;color:var(--ink);font-weight:700;font-size:13.5px}}
.rs-top:hover,.rs-cbtn:hover{{background:#FBF3E4}}
.rs-cbtn{{display:flex;justify-content:space-between;align-items:center;width:100%;border:0;background:none;padding:9px 12px;border-radius:9px;font:inherit;font-weight:700;font-size:14px;cursor:pointer;color:var(--ink)}}
.rs-cbtn .ar{{color:#c4b59a;transition:transform .15s}}
.rs-cat.open .ar{{transform:rotate(90deg)}}
.rs-subs{{display:none;padding:2px 0 6px 10px}}
.rs-cat.open .rs-subs{{display:block}}
.rs-sub{{display:flex;align-items:center;gap:7px;padding:7px 10px;margin:2px 4px;border-radius:8px;text-decoration:none;color:var(--navy2);font-weight:600;font-size:12.8px;border:1px solid transparent}}
.rs-sub:hover{{background:#FBF3E4;border-color:#EADFCE}}
.rs-sub.on{{background:#FDECE5;border-color:#E0684A;color:#B44A31}}
.rs-sub .dl{{font-size:10.5px;font-weight:800;color:#188038;background:#e6f4ea;border-radius:6px;padding:1px 7px;margin-left:auto}}
.rs-main{{flex:1;min-width:0}}
.rs-bar{{display:flex;justify-content:space-between;gap:10px;margin-bottom:14px}}
#rsBody .page-hero{{padding:18px 0}}#rsBody .block{{padding:22px 0}}
@media(max-width:880px){{.rs-wrap{{flex-direction:column}}.rs-side{{position:static;width:100%;max-height:none}}}}
</style>
<script>
function rsToggle(s){{const c=document.getElementById('sub-'+s).parentElement;c.classList.toggle('open');return false;}}
function rsHome(){{document.getElementById('rsDoc').style.display='none';document.getElementById('rsHome').style.display='block';document.querySelectorAll('.rs-sub.on').forEach(e=>e.classList.remove('on'));window.scrollTo({{top:0,behavior:'smooth'}});return false;}}
function rsFaq(){{rsHome();setTimeout(()=>document.getElementById('faq').scrollIntoView({{behavior:'smooth'}}),80);return false;}}
async function rsLoad(el){{
  const href=el.dataset.href;
  try{{
    const r=await fetch(href);const t=await r.text();
    const doc=new DOMParser().parseFromString(t,'text/html');
    const m=doc.querySelector('main');if(!m)return true;
    m.querySelectorAll('header.site,footer.site,script').forEach(x=>x.remove());
    m.querySelectorAll('a[href^="/world-cases/"]').forEach(a=>{{const h=a.getAttribute('href');if(h.endsWith('.html')&&!h.includes('workbook')){{a.setAttribute('data-href',h);a.setAttribute('onclick','return rsLoad(this)');}}}});
    document.getElementById('rsBody').innerHTML=m.innerHTML;
    document.getElementById('rsOrig').href=href;
    document.getElementById('rsHome').style.display='none';
    document.getElementById('rsDoc').style.display='block';
    document.querySelectorAll('.rs-sub.on').forEach(e=>e.classList.remove('on'));
    if(el.classList)el.classList.add('on');
    document.getElementById('rsMain').scrollIntoView({{behavior:'smooth',block:'start'}});
    return false;
  }}catch(e){{return true;}}
}}
</script>
</main>"""
    return page("res","","부모 자료실 · 국가별 자료 & 다운로드 | AI 조기교육","왼쪽 나라 카테고리에서 세부 자료를 펼쳐 페이지 안에서 바로 읽는 부모 자료실. 인쇄 워크북 다운로드 포함.",body)

def free_kit():
    kits=[("📝","집에서 하는 AI 대화 연습지","아이와 함께 AI에게 요청하고, 관찰하고, 다시 묻는 과정을 적는 워크시트.","/free/worksheet.html"),
        ("🃏","부모용 질문 카드","'이상한 부분 찾아볼까?' 같은 상황별 질문 카드 10장.","/free/question-cards.html"),
        ("💡","아이와 함께하는 첫 프롬프트 20개","처음 시작하기 좋은 프롬프트 20가지 + 각 '다시 묻기'까지.","/free/first-prompts.html")]
    kc="".join(f"""<div class="card center"><div style="font-size:44px;margin-bottom:10px">{ic}</div><h4>{t}</h4><p style="color:var(--muted);font-size:14px">{d}</p>
<a class="btn btn-primary" href="{href}" target="_blank" rel="noopener">열기 · 인쇄 🖨</a>
<div style="margin-top:8px"><span class="tag" style="background:#e6f4ea;color:#188038;border-color:#b7dfc2">바로 사용</span></div></div>""" for ic,t,d,href in kits)
    body=f"""<main>
<section class="page-hero"><div class="wrap"><div class="pill">무료 자료</div>
<h1>집에서 바로 쓰는 무료 자료</h1><p>이메일·회원가입 없이, 지금 바로 열어 인쇄하거나 PDF로 저장하세요.</p></div></section>
<section class="block"><div class="wrap" style="max-width:900px"><div class="grid g3">{kc}</div>
<p class="center" style="color:var(--muted);margin-top:20px;font-size:14px">※ 세 자료 모두 <b>바로 열람·인쇄</b> 가능합니다. 브라우저의 인쇄에서 'PDF로 저장'을 고르면 파일로도 보관돼요.</p>
<div class="cta-band" style="margin-top:24px"><div><h3>어떻게 쓰는지 먼저 볼까요?</h3><p>6단계 시작 가이드와 함께 쓰면 더 좋아요.</p></div><a class="btn btn-lg" href="/start-guide.html">시작 가이드 보기 →</a></div>
</div></section></main>"""
    return page("res","","무료 자료 | AI 조기교육","집에서 바로 쓰는 무료 AI교육 자료 — 연습지·질문 카드·첫 프롬프트 20개. 이메일 없이 바로 인쇄.",body)

# ---------- 쓰기 ----------
def write(path,html):
    full=os.path.join(ROOT,path); os.makedirs(os.path.dirname(full) or ".",exist_ok=True)
    open(full,"w",encoding="utf-8").write(html); print(" ",path)

if __name__=="__main__":
    print("생성:")
    write("index.html",home())
    write("why-ai-education.html",why())
    write("world-cases.html",world_cases())
    for c in COUNTRIES:
        if c[0] in ("china","usa","uk","singapore","korea","germany","japan"): continue   # 전부 심층 페이지로 대체
        write(f"world-cases/{c[0]}.html",country_page(c))
    import build_china_page as CN
    write("world-cases/china.html",CN.china_page())
    write("videos/china-ai-education.html",CN.china_video_detail())
    import build_us_page as US
    write("world-cases/usa.html",US.usa_page())
    write("videos/us-ai-education.html",US.us_video_detail())
    import build_country_page as CP
    for k in ("uk","singapore","korea","germany","japan"):
        cfg=CP.C[k]
        write(f"world-cases/{cfg['slug']}.html",CP.render(cfg))
        write(f"videos/{cfg['vslug']}.html",CP.video_detail(cfg))
    CP.write_all_practice()   # 2·3편(실제 운영·우리집) 7개국
    write("videos.html",videos())
    write("videos/world-ai-education.html",video_detail())
    write("start-guide.html",start_guide())
    write("parent-resources.html",parent_resources())
    write("free-kit.html",free_kit())
    print("완료.")
