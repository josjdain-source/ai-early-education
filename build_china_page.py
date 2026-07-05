#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""중국 AI교육 심층 페이지 빌더 — /world-cases/china.html(심층) + /videos/china-ai-education.html.
build_site 헬퍼(head/header/footer/page/write) 재사용. facts/metadata/upload_queue 참조.
임베드 유튜브 ID는 upload_queue.json에서 읽어 업로드 후 자동 반영(없으면 '곧 공개' 플레이스홀더)."""
import os, json, build_site as BS, country_reality as CR
ROOT=os.path.dirname(os.path.abspath(__file__))
def J(p): return json.load(open(os.path.join(ROOT,p),encoding="utf-8"))
FACTS=J("facts/china_ai_education_facts.json"); SRC=J("sources/china_ai_education_sources.json")
META=J("production/china_ai_education_metadata.json")
try: QUEUE=J("youtube/upload_queue.json")
except Exception: QUEUE={"queue":[]}
def yt_id(vid):
    for it in QUEUE["queue"]:
        if it.get("video_id")==vid:
            if it.get("youtube_id"): return it["youtube_id"]
            u=it.get("youtube_url") or ""; return u.rstrip("/").split("/")[-1] if u else ""
    return ""
def embed(vid,title):
    i=yt_id(vid)
    if i: return f'<div class="player"><iframe src="https://www.youtube.com/embed/{i}" title="{title}" loading="lazy" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
    return f'<div class="player" style="display:grid;place-items:center;background:#2B3A55;color:#fff;text-align:center"><div style="padding:20px"><div style="font-size:34px">▶</div><b>{title}</b><br><small style="opacity:.8">업로드 후 여기서 재생됩니다</small></div></div>'

TIMELINE=[
 ("2017","차세대 AI 발전 계획","국무원이 2030년 세계 주요 AI 혁신 중심을 목표로. AI를 국가 전략으로 격상.","S9"),
 ("2018","대학 AI 혁신 행동계획","교육부가 대학 AI 인재·커리큘럼 강화. 먼저 대학·연구 고급 인재부터.","S10"),
 ("2019~","교육 현대화 2035","AI를 교육 개혁의 핵심 엔진으로. 교육 시스템 전체의 디지털 전환.","S13"),
 ("2024","초·중등 AI교육 강화 지침","AI교육이 대학에서 기초교육으로 내려옴.","S6"),
 ("2025","베이징·광둥 등 지역 실행","연간 최소 8시간·독립/통합·학년별 운영으로 구체화.","S1"),
 ("2025","생성형 AI 사용 가이드","안전·윤리·표절·교사 역할 경계 설정.","S7"),
 ("2030 목표","초·중등 AI교육 보급","모든 학교에서 AI 리터러시 체계화.","S12"),
 ("2035 목표","AI 기반 교육강국","AI가 교재·평가·수업에 깊게 통합.","S13"),
]
LAYERS=[
 ("① 국가 지침층","교육부(MOE)","AI교육의 방향, 금지선, 학년별 원칙, 생성형 AI 사용 기준을 정한다. 2025년 지침은 단계적·나선형 체계를 말하고, 초등생의 독립적 개방형 생성 AI 사용을 제한하며, 교사의 역할을 AI가 대체하지 못하게 못박았다."),
 ("② 지방 실행층","베이징·광둥","베이징은 2025년 가을학기부터 모든 초·중등학교에서 연간 최소 8시간 이상의 AI 수업을 제공하고, 독립 과목 또는 정보기술 등 기존 과목에 통합할 수 있게 했다."),
 ("③ 학교 수업층","현장 교실","초등은 음성·이미지 인식처럼 'AI가 어떻게 작동하는지 감각으로 이해하는' 체험 단계. 나이가 올라갈수록 데이터·알고리즘·프로젝트·윤리 판단으로 넘어간다(체험→이해→응용→혁신)."),
]
KOREA5=[
 ("학교는 국가가, 습관은 가정이","중국은 국가 단위로 교과와 시간을 설계한다. 우리는 가정 단위로 아이의 습관을 설계하면 된다."),
 ("생활 시간표에 '다시 묻기'를","중국이 학교 시간표에 AI를 넣는다면, 한국 가정은 아이의 생활 시간표에 '다시 묻기'를 넣는다."),
 ("답을 받으면 검증부터","'이상한 부분 찾아볼까?' 한마디로 아이가 결과를 검증하는 습관을 만든다."),
 ("쓰는 법보다 경계를 먼저","중국도 초등 독립 사용을 제한했다. 집에서도 쓰는 법보다 안전한 경계·윤리를 먼저."),
 ("'AI 없이라면?'을 자주","AI가 아이 생각을 대신하지 않도록, 'AI 없이 너라면?'을 자주 묻는다."),
]
EFFECTS=[
 ("🔎","스스로 확인하는 아이","AI가 준 답을 그대로 믿지 않고, 이상한 부분을 스스로 찾아냅니다. 정답을 받는 아이에서, 정답을 검증하는 아이로."),
 ("⚖️","스스로 판단하는 아이","AI에 휘둘리지 않고, 여러 답을 비교해 자기 생각으로 결정합니다. AI는 도구, 판단은 내가."),
 ("🛡️","속지 않는 아이","정보를 의심하고 근거를 확인하는 습관이 몸에 뱁니다. AI 시대에 가짜와 오류에 속지 않는 힘."),
]
Q10=["AI가 준 답에서 이상한 부분 하나만 찾아볼까?","이 답이 진짜인지 어떻게 확인할 수 있을까?","AI 없이 너라면 어떻게 했을까?",
 "방금 그건 네가 한 거야, AI가 한 거야?","왜 그렇게 답했는지 AI에게 다시 물어볼까?","이 답을 더 좋게 하려면 뭘 더 물어봐야 할까?",
 "AI도 틀릴 수 있을까? 언제 틀릴까?","이 정보는 어디서 온 걸까?","친구한테 설명한다면 어떻게 말할래?","오늘 AI랑 뭐 했고, 뭘 다시 물어봤어?"]

def china_page():
    tl="".join(f"""<div class="tl-item"><div class="tl-year">{y}</div><div class="tl-body"><h4>{t}</h4><p>{d} <span class="src">[{s}]</span></p></div></div>""" for y,t,d,s in TIMELINE)
    layers="".join(f"""<div class="card"><div class="lyr-h">{h}<span>{who}</span></div><p>{d}</p></div>""" for h,who,d in LAYERS)
    k5="".join(f"""<div class="card phil"><div class="pic">🏠</div><div><h4>{t}</h4><p>{d}</p></div></div>""" for t,d in KOREA5)
    eff="".join(f"""<div class="card phil"><div class="pic">{ic}</div><div><h4>{t}</h4><p>{d}</p></div></div>""" for ic,t,d in EFFECTS)
    qs="".join(f"<li>{q}</li>" for q in Q10)
    scards="".join(f"""<a class="card country" href="/videos/china-ai-education.html">
<div class="thumb" style="aspect-ratio:9/16;max-height:280px">{embed(s['video_id'],s['title'])}</div>
<div class="body"><div class="flag">📱 {s['thumbnail_copy']}</div><p>{s['title'].replace(' #Shorts','')}</p></div></a>""" for s in META["shorts"])
    srcs="".join(f'<li><a href="{s["url"]}" target="_blank" rel="noopener">{s["publisher"]} — {s["title"]}</a> <span class="src">[{s["id"]}]</span></li>' for s in SRC["sources"])
    lf=META["longform"]
    body=f"""<main>
<section class="page-hero"><div class="wrap">
<div class="pill">🇨🇳 세계 사례 · 중국 심층</div>
<h1 style="font-size:34px">중국은 왜 초등학생에게 AI를 가르치기 시작했나</h1>
<p class="sub">{lf['subtitle']}</p>
<p style="max-width:760px;color:var(--navy2);font-weight:600">중국은 AI를 '미래 직업 과목'이 아니라, <span class="coral">국가가 관리하는 기본 문해력</span>으로 만들고 있습니다.</p>
{CR.episode_nav("china","1")}
</div></section>

<section class="block" style="padding-top:12px"><div class="wrap">
{embed(lf['video_id'],lf['title'])}
<p class="center" style="margin-top:12px;color:var(--muted)">중국 편 롱폼 다큐 · 2017 국가 전략에서 2035 교육강국까지</p>
</div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">타임라인 · 8년의 흐름</h2>
<p class="sec-desc">중국 AI교육은 갑자기 시작된 게 아닙니다. 국가 전략에서 초등 시간표까지 내려온 긴 설계입니다.</p>
<div class="timeline">{tl}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">운영 구조 · 세 층으로 본다</h2>
<div class="grid g3">{layers}</div></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">한국 가정에서 배울 점</h2>
<p class="sec-desc">중국이 학교 시간표에 AI를 넣는다면, 한국 가정은 아이의 생활 시간표에 '다시 묻기'를 넣습니다.</p>
<div class="grid g3">{k5}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">그럼, 아이에게 무엇이 생기나</h2>
<p class="sec-desc">'다시 묻기' 습관 하나가 아이를 바꿉니다. 중국이 국가로 기른 힘을, 우리는 집에서 이렇게 기릅니다.</p>
<div class="grid g3">{eff}</div></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">부모가 아이와 해볼 질문 10</h2>
<ol class="qlist">{qs}</ol></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">쇼츠로 빠르게</h2>
<div class="grid g5">{scards}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title" style="font-size:22px">출처</h2>
<p class="sec-desc">이 페이지의 모든 수치·정책은 아래 출처에 근거합니다. 중국을 감시국가로 자극화하지 않고, 국가 주도형 AI 리터러시·교육과정 편입·윤리적 사용 규칙의 관점으로 정리했습니다.</p>
<ul class="srclist">{srcs}</ul></div></section>

<section class="block"><div class="wrap"><div class="cta-band" style="background:linear-gradient(135deg,#FFF3E0,#FDE9CE)">
<div><h3>▶ 2편 · 🇨🇳 실제 교실은 이렇게 돌아간다</h3><p>정책은 봤으니, 이제 학년별로 매주 실제로 무엇을 가르치는지 — 실무편으로 이어집니다.</p></div>
<a class="btn btn-lg" href="/world-cases/china-2.html">2편 보러가기 →</a></div></div></section>

<section class="block"><div class="wrap"><div class="cta-band">
<div><h3>다음 편도 같은 구조로</h3><p>미국·영국·싱가포르·한국 편도 국가별 콘텐츠 패키지로 이어집니다.</p></div>
<a class="btn" href="/world-cases.html">세계 사례 전체 보기</a></div></div></section>
</main>"""
    return BS.page("cases","../","중국은 왜 초등학생에게 AI를 가르치기 시작했나 | AI 조기교육",
        "2017 국가 AI 전략에서 2035 교육강국까지 — 중국 AI교육을 역사·운영·미래세대 3층으로 본 심층 다큐와 한국 가정의 답.",body)

def china_video_detail():
    lf=META["longform"]
    scards="".join(f"""<a class="card" href="#" style="pointer-events:none"><div class="thumb" style="aspect-ratio:9/16;max-height:320px;overflow:hidden;border-radius:12px">{embed(s['video_id'],s['title'])}</div>
<p style="margin-top:8px;font-size:14px;font-weight:600">{s['title'].replace(' #Shorts','')}</p></a>""" for s in META["shorts"])
    body=f"""<main>
<section class="block" style="padding-top:22px"><div class="wrap">
<p style="color:var(--muted);font-size:14px"><a href="/videos.html">영상관</a> › 중국 AI교육</p>
{embed(lf['video_id'],lf['title'])}
<h1 style="margin-top:18px">{lf['title']}</h1>
<p style="color:var(--navy2);font-weight:600">{lf['subtitle']}</p>
<p style="white-space:pre-line;color:var(--ink)">{lf['description']}</p>
<a class="btn btn-primary" href="/world-cases/china.html">중국 편 심층 페이지 보기 →</a>
</div></section>
<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">이 주제의 쇼츠 5편</h2>
<div class="grid g5">{scards}</div></div></section>
</main>"""
    return BS.page("cases","../","{} | 영상".format(lf['title']),lf['subtitle'],body)

if __name__=="__main__":
    BS.write("world-cases/china.html",china_page())
    BS.write("videos/china-ai-education.html",china_video_detail())
    print("중국 심층 페이지 생성 완료")
