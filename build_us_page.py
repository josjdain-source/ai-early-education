#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""미국 AI교육 심층 페이지 — /world-cases/usa.html + /videos/us-ai-education.html.
build_site 헬퍼 재사용. facts/metadata/upload_queue 참조. 임베드 ID는 큐에서(업로드 후 자동반영)."""
import os, json, build_site as BS, country_reality as CR
ROOT=os.path.dirname(os.path.abspath(__file__))
def J(p): return json.load(open(os.path.join(ROOT,p),encoding="utf-8"))
FACTS=J("facts/us_ai_education_facts.json"); SRC=J("sources/us_ai_education_sources.json")
META=J("production/us_ai_education_metadata.json")
try: QUEUE=J("youtube/upload_queue.json")
except Exception: QUEUE={"queue":[]}
def yt_id(vid):
    for it in QUEUE["queue"]:
        if it.get("video_id")==vid:
            if it.get("public") and it.get("youtube_id"): return it["youtube_id"]
            u=it.get("youtube_url") or ""; return (u.rstrip("/").split("/")[-1] if u else "") if it.get("public") else ""
    return ""
def embed(vid,title):
    i=yt_id(vid)
    if i: return f'<div class="player"><iframe src="https://www.youtube.com/embed/{i}" title="{title}" loading="lazy" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
    return f'<div class="player" style="display:grid;place-items:center;background:#2B3A55;color:#fff;text-align:center"><div style="padding:20px"><div style="font-size:34px">▶</div><b>{title}</b><br><small style="opacity:.8">업로드 후 여기서 재생됩니다</small></div></div>'

TIMELINE=[
 ("2025.4","AI교육 진흥 행정명령","대통령이 AI 리터러시·교육자 훈련·조기 노출을 국가 정책으로 선언.","US1"),
 ("2025","백악관 AI교육 태스크포스","과학기술정책실(OSTP) 주재, NSF·노동부·교육부 등 범부처.","US1"),
 ("2025","대통령 AI 챌린지","90일 내 전국 대회로 학생·교사 성취 장려·발굴.","US2"),
 ("2025","미 교육부 AI 사용 가이드","학교 AI 사용 가이드 + 재량 보조금 우선순위에 AI.","US4"),
 ("2024~","주별 실행 (캘리포니아 AB2876 등)","연방은 방향, 주가 실행. 주마다 다른 커리큘럼.","US6"),
 ("2025.6","60개+ 기업 서약","4년간 자금·커리큘럼·교사 전문성 개발·도구 지원.","US3"),
 ("진행 중","교사 훈련 확대","대다수 교사가 아직 훈련 전 — 격차 해소가 과제.","US7"),
]
LAYERS=[
 ("① 연방 (방향층)","백악관·행정명령","전국 시간표를 강제하지 않는다. 행정명령·태스크포스·대통령 챌린지로 방향과 동기부여를 준다."),
 ("② 주·지역 (실행층)","캘리포니아·미주리 등","실제 실행은 주와 지역 교육청이 채운다. 캘리포니아는 AB2876으로 리터러시를 넣고, 주마다 접근이 다르다."),
 ("③ 학교·민간 (현장층)","60개+ 기업·비영리","기업·비영리가 자금·자료·교사 훈련·도구를 지원한다. AI를 대체가 아니라 학습 파트너로 가르친다."),
]
KOREA5=[
 ("국가를 기다리지 않는다","미국도 강제 대신 동기부여로 움직인다. 가정도 정책을 기다리지 말고 스스로 시작한다."),
 ("AI를 파트너로","대체가 아니라 함께 하는 도구로. 아이가 AI를 파트너처럼 부리게 한다."),
 ("판단은 아이가","답을 받아도 최종 판단은 아이 몫. '네 생각은?'을 자주 묻는다."),
 ("비판적으로 검증","받은 답을 그대로 믿지 않고, 의심하고 함께 다듬는다."),
 ("만들게 한다","소비만 하는 아이가 아니라, AI로 무언가 만들어보는 창작자로."),
]
EFFECTS=[
 ("🎮","AI를 부리는 아이","AI에 끌려가지 않고, AI를 파트너·도구로 부립니다. 소비자가 아니라 사용자로."),
 ("⚖️","스스로 판단하는 아이","AI 답을 검증하고 자기 생각으로 결정합니다. AI는 파트너, 판단은 나."),
 ("🛠️","만드는 아이","쓰기만 하는 아이에서, AI로 무언가 만들고 고치는 창작자로 자랍니다."),
]
Q10=["AI가 준 답, 네 생각은 어때?","이 답이 맞는지 어떻게 확인할까?","AI 없이 너라면 어떻게 했을까?",
 "이 답에서 이상한 부분 하나 찾아볼까?","AI랑 같이 뭐 하나 만들어볼까?","방금 건 네가 한 거야, AI가 한 거야?",
 "이걸 더 낫게 하려면 뭘 바꿔볼까?","AI도 틀릴 수 있을까? 언제?","이 정보는 어디서 온 걸까?","오늘 AI랑 뭘 만들고, 뭘 고쳤어?"]

def usa_page():
    tl="".join(f"""<div class="tl-item"><div class="tl-year">{y}</div><div class="tl-body"><h4>{t}</h4><p>{d} <span class="src">[{s}]</span></p></div></div>""" for y,t,d,s in TIMELINE)
    layers="".join(f"""<div class="card"><div class="lyr-h">{h}<span>{who}</span></div><p>{d}</p></div>""" for h,who,d in LAYERS)
    k5="".join(f"""<div class="card phil"><div class="pic">🏠</div><div><h4>{t}</h4><p>{d}</p></div></div>""" for t,d in KOREA5)
    eff="".join(f"""<div class="card phil"><div class="pic">{ic}</div><div><h4>{t}</h4><p>{d}</p></div></div>""" for ic,t,d in EFFECTS)
    qs="".join(f"<li>{q}</li>" for q in Q10)
    scards="".join(f"""<a class="card country" href="/videos/us-ai-education.html">
<div class="thumb" style="aspect-ratio:9/16;max-height:280px">{embed(s['video_id'],s['title'])}</div>
<div class="body"><div class="flag">📱 {s['thumbnail_copy']}</div><p>{s['title'].replace(' #Shorts','')}</p></div></a>""" for s in META["shorts"])
    srcs="".join(f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{s["publisher"]} — {s["title"]}</a> <span class="src">[{s["id"]}]</span></li>' for s in SRC["sources"])
    lf=META["longform"]
    body=f"""<main>
{CR.side_rail("usa","/world-cases/usa.html")}
<section class="page-hero"><div class="wrap">
{CR.breadcrumb("usa","1편 · 정책과 방침")}
<div class="pill">🇺🇸 세계 사례 · 미국 심층</div>
<h1 style="font-size:34px">미국은 왜 국가가 시간표를 안 짜고도 AI교육에 나섰나</h1>
<p class="sub">{lf['subtitle']}</p>
<p style="max-width:780px;color:var(--navy2);font-weight:600">중국이 '국가가 관리하는 문해력'이라면, 미국은 <span class="coral">연방이 방향만 주고 주·기업이 채우는 분권형</span>입니다.</p>
{CR.episode_nav("usa","1")}
</div></section>

<section class="block" style="padding-top:12px"><div class="wrap">
{embed(lf['video_id'],lf['title'])}
<p class="center" style="margin-top:12px;color:var(--muted)">미국 편 롱폼 다큐 · 2025 행정명령과 분권형 AI교육</p>
</div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">타임라인 · 2025, 국가가 나선 해</h2>
<p class="sec-desc">미국은 강제 시간표 대신, 방향·챌린지·민관협력으로 움직였습니다.</p>
<div class="timeline">{tl}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">운영 구조 · 연방·주·민간 세 층</h2>
<div class="grid g3">{layers}</div></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">한국 가정에서 배울 점</h2>
<p class="sec-desc">미국이 아이를 'AI를 파트너로 쓰되 스스로 판단하는' 사람으로 키운다면, 우리는 집에서 그 습관을 만듭니다.</p>
<div class="grid g3">{k5}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">그럼, 아이에게 무엇이 생기나</h2>
<p class="sec-desc">미국이 민관 총동원으로 기르려는 힘을, 우리는 집에서 이렇게 기릅니다.</p>
<div class="grid g3">{eff}</div></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">부모가 아이와 해볼 질문 10</h2>
<ol class="qlist">{qs}</ol></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">쇼츠로 빠르게</h2>
<div class="grid g3">{scards}</div></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title" style="font-size:22px">출처</h2>
<p class="sec-desc">모든 수치·정책은 아래 출처에 근거합니다. 특정 정파·정치인을 지지하거나 비하하지 않고, 정책과 교육 방식의 관점으로 정리했습니다.</p>
<ul class="srclist">{srcs}</ul></div></section>


</main>"""
    return BS.page("cases","../","미국은 왜 국가가 시간표를 안 짜고도 AI교육에 나섰나 | AI 조기교육",
        "2025 행정명령과 분권형 AI교육 — 미국을 역사·운영·미래세대 3층으로 본 심층 다큐와 한국 가정의 답.",body)

def us_video_detail():
    lf=META["longform"]
    scards="".join(f"""<a class="card" href="#" style="pointer-events:none"><div class="thumb" style="aspect-ratio:9/16;max-height:320px;overflow:hidden;border-radius:12px">{embed(s['video_id'],s['title'])}</div>
<p style="margin-top:8px;font-size:14px;font-weight:600">{s['title'].replace(' #Shorts','')}</p></a>""" for s in META["shorts"])
    body=f"""<main>
<section class="block" style="padding-top:22px"><div class="wrap">
<p style="color:var(--muted);font-size:14px"><a href="/videos.html">영상관</a> › 미국 AI교육</p>
{embed(lf['video_id'],lf['title'])}
<h1 style="margin-top:18px">{lf['title']}</h1>
<p style="color:var(--navy2);font-weight:600">{lf['subtitle']}</p>
<p style="white-space:pre-line;color:var(--ink)">{lf['description']}</p>
<a class="btn btn-primary" href="/world-cases/usa.html">미국 편 심층 페이지 보기 →</a>
</div></section>
<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">이 주제의 쇼츠 3편</h2>
<div class="grid g3">{scards}</div></div></section>
</main>"""
    return BS.page("cases","../","{} | 영상".format(lf['title']),lf['subtitle'],body)

if __name__=="__main__":
    BS.write("world-cases/usa.html",usa_page())
    BS.write("videos/us-ai-education.html",us_video_detail())
    print("미국 심층 페이지 생성 완료")
