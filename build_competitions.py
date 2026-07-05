#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 경진대회 문제풀이 교실 — data/competitions.json + competition_problems.json으로 7페이지 생성.
공개 대회 요약+출처링크+풀이전략+연습문제 구조(원문 복붙 없음). build_site 헬퍼 재사용."""
import os, json, build_site as BS
ROOT=os.path.dirname(os.path.abspath(__file__))
C=json.load(open(os.path.join(ROOT,"data","competitions.json"),encoding="utf-8"))
PROB=json.load(open(os.path.join(ROOT,"data","competition_problems.json"),encoding="utf-8"))["problems"]
CMAP={x["id"]:x for x in C["contests"]}
DIFF=C["difficulty_labels"]
LV={"elementary":("초등부","🟢"),"middle":("중등부","🔵"),"high":("고등부","🟣"),"university_general":("대학·일반","🟠"),"family":("부모와 함께","👨‍👩‍👧")}
NAV=[("교실 홈","/competitions.html"),("🟢 초등부","/competitions/elementary.html"),("🔵 중등부","/competitions/middle.html"),
     ("🟣 고등부","/competitions/high.html"),("🟠 대학·일반","/competitions/university-general.html"),
     ("🏆 AI TOP 100","/competitions/ai-top-100.html"),("🏠 우리집 연습문제","/competitions/practice.html")]

CSS="""<style>
.cp-wrap{display:flex;gap:24px;align-items:flex-start;max-width:1180px;margin:0 auto;padding:16px 18px 40px}
.cp-side{width:210px;flex:none;background:#F4F7FB;border:1px solid #D9E2EF;border-radius:14px;padding:12px 8px;position:sticky;top:74px}
.cp-side .t{font-weight:800;font-size:13.5px;color:#2B3A55;padding:4px 11px 9px;border-bottom:2px solid #DCE6F2;margin-bottom:6px}
.cp-side a{display:block;padding:8px 11px;margin:1px 0;border-radius:8px;text-decoration:none;color:#3a4a63;font-size:13.3px;font-weight:600}
.cp-side a:hover{background:#E6EEF9}.cp-side a.on{background:#3A6FB0;color:#fff}
.cp-main{flex:1;min-width:0}
.cp-hero{background:linear-gradient(160deg,#EAF2FB,#DCEAF8);border:1px solid #CADCF0;border-radius:20px;padding:26px 24px}
.cp-hero .k{display:inline-block;background:#3A6FB0;color:#fff;font-weight:800;font-size:12px;border-radius:20px;padding:4px 13px;margin-bottom:8px}
.cp-hero h1{margin:0 0 6px;font-size:27px;color:#22406b}.cp-hero p{margin:0;color:#4a5f7d;font-weight:600}
.cp-sec{font-size:19px;font-weight:900;color:#22406b;margin:30px 0 4px}
.cp-secd{color:var(--muted);margin:0 0 14px;font-size:13.5px}
.cp-lv{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.cp-lv a{background:#fff;border:1px solid #D9E2EF;border-radius:14px;padding:16px;text-decoration:none;color:#22406b;font-weight:800;text-align:center}
.cp-lv a:hover{border-color:#3A6FB0;background:#F4F9FF}.cp-lv .e{font-size:30px;display:block}
.cp-types{display:flex;gap:7px;flex-wrap:wrap}
.cp-types .chip{background:#EAF2FB;border:1px solid #CADCF0;color:#2B3A55;border-radius:20px;padding:6px 13px;font-size:13px;font-weight:700}
.cp-filter{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0}
.cp-filter button{border:1px solid #CADCF0;background:#fff;color:#2B3A55;border-radius:20px;padding:7px 14px;font-weight:700;cursor:pointer;font-size:13px}
.cp-filter button.on{background:#3A6FB0;color:#fff;border-color:#3A6FB0}
.cp-card{background:#fff;border:1px solid #D9E2EF;border-radius:15px;padding:16px 18px;margin-bottom:12px}
.cp-ctop{display:flex;gap:8px;align-items:center;margin-bottom:6px;flex-wrap:wrap}
.cp-badge{font-size:11px;font-weight:800;border-radius:7px;padding:2px 9px;background:#EAF2FB;color:#2B4a72}
.cp-diff{margin-left:auto;color:#E0684A;font-weight:800;font-size:13px}
.cp-card h3{margin:2px 0 7px;font-size:17px;color:#22406b}
.cp-skills{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px}
.cp-skills span{font-size:11px;font-weight:700;background:#F0E6D2;color:#7a5b2e;border-radius:6px;padding:2px 8px}
.cp-sum{font-size:14px;color:#3a3024;margin:0 0 8px}
.cp-card details{background:#F8FAFD;border:1px solid #E4ECF6;border-radius:10px;padding:0 14px}
.cp-card summary{cursor:pointer;font-weight:800;color:#3A6FB0;padding:10px 0;font-size:13.5px}
.cp-card ol{margin:4px 0 10px;padding-left:20px}.cp-card ol li{margin:3px 0;font-size:13.5px}
.cp-q{background:#FFF7EA;border:1px solid #EAD9BE;border-radius:8px;padding:8px 12px;margin:6px 0;font-size:13.5px;font-weight:600}
.cp-q.re{background:#EEF7EF;border-color:#cfe6d6}
.cp-v,.cp-p,.cp-pr{font-size:13px;margin:6px 0;color:#3a4a63}
.cp-pr{background:#EAF2FB;border-radius:8px;padding:8px 12px;font-weight:600}
.cp-src{display:inline-block;margin-top:10px;font-size:12px;color:#3A6FB0;font-weight:700;text-decoration:none}
.cp-src:hover{text-decoration:underline}
.cp-contest{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1px solid #D9E2EF;border-radius:13px;padding:14px 16px;margin-bottom:9px}
.cp-contest b{color:#22406b}.cp-contest p{margin:3px 0 4px;font-size:13px;color:var(--muted)}
@media(max-width:860px){.cp-wrap{flex-direction:column}.cp-side{position:static;width:100%}}
</style>"""

def stars(n): return "★"*int(n)+"☆"*(5-int(n))
def contest_of(p): return CMAP.get(p["contest"],{"name":p["contest"],"url":"#"})
def card(p):
    ct=contest_of(p); lvn=LV.get(p["level"],(p["level"],""))[0]
    tier=DIFF.get(p.get("tier",""),lvn)
    sk="".join(f"<span>{s}</span>" for s in p["skills"])
    steps="".join(f"<li>{s}</li>" for s in p["how_to_solve"])
    return f"""<div class="cp-card" data-level="{p['level']}" data-type="{p['type']}">
<div class="cp-ctop"><span class="cp-badge">{lvn}</span><span class="cp-badge" style="background:#F0E6D2;color:#7a5b2e">{tier}</span><span class="cp-diff">난이도 {stars(p['difficulty'])}</span></div>
<h3>{p['title']}</h3>
<div class="cp-skills">🧠 {sk}</div>
<p class="cp-sum">{p['problem_summary']}</p>
<details><summary>▶ 풀이 순서 · AI에게 물어볼 말 · 검증 · 부모 지도</summary>
<b style="font-size:12.5px;color:#2B3A55">풀이 순서</b><ol>{steps}</ol>
<div class="cp-q">💬 첫 질문 — "{p['first_question']}"</div>
<div class="cp-q re">🔁 다시 묻기 — "{p['reask']}"</div>
<div class="cp-v">✅ 검증 방법 — {p['verify']}</div>
<div class="cp-p">👨‍👩‍👧 부모 지도 — {p['parent_tip']}</div>
<div class="cp-pr">🏠 우리집 연습 — {p['practice_problem']}</div>
</details>
<a class="cp-src" href="{ct['url']}" target="_blank" rel="noopener">📎 출처: {ct['name']} ↗</a>
</div>"""

def layout(active,base,title,desc,inner):
    side="".join(f'<a href="{h}" class="{"on" if h==active else ""}">{t}</a>' for t,h in NAV)
    body=f"""<main><div class="cp-wrap">
<aside class="cp-side"><div class="t">🏆 경진대회 교실</div>{side}</aside>
<div class="cp-main">{inner}</div></div>{CSS}</main>"""
    return BS.page("comp",base,title,desc,body)

def hub():
    lv="".join(f'<a href="{h}"><span class="e">{LV[k][1]}</span>{LV[k][0]}</a>'
        for k,h in [("elementary","/competitions/elementary.html"),("middle","/competitions/middle.html"),("high","/competitions/high.html"),("university_general","/competitions/university-general.html")])
    types=["프롬프트 활용","데이터 분석","이미지·영상 생성","사회문제 해결","코딩·알고리즘","발표·보고서"]
    tc="".join(f'<span class="chip">{t}</span>' for t in types)
    contests="".join(f'<div class="cp-contest"><span style="font-size:22px">🏆</span><div><b>{c["name"]}</b><p>{c["desc"]}</p><a class="cp-src" href="{c["url"]}" target="_blank" rel="noopener">📎 공식 페이지 ↗</a></div></div>' for c in C["contests"])
    an=[p for p in PROB if p["kind"]=="analysis"]
    filt='<div class="cp-filter" id="cpf"><button class="on" data-l="all">전체</button><button data-l="elementary">초등</button><button data-l="middle">중등</button><button data-l="high">고등</button><button data-l="university_general">대학·일반</button></div>'
    cards="".join(card(p) for p in an)
    inner=f"""<div class="cp-hero"><span class="k">🏆 AI 경진대회 문제풀이 교실</span>
<h1>AI를 잘 쓴다는 건 무엇일까?</h1><p>실제 경진대회 문제를 아이 눈높이로 풀어봅니다. 정답이 아니라, '다시 묻는 힘'으로.</p></div>

<h2 class="cp-sec">① 학년별 보기</h2><p class="cp-secd">우리 아이 수준부터 시작하세요.</p>
<div class="cp-lv">{lv}</div>

<h2 class="cp-sec">② 문제 유형별 보기</h2><p class="cp-secd">AI 경진대회에 자주 나오는 문제 종류.</p>
<div class="cp-types">{tc}</div>

<h2 class="cp-sec">③ 공개 대회 문제 분석</h2><p class="cp-secd">공개된 대회의 '문제 유형'을 요약하고, 집에서 풀 수 있게 바꿨어요. (원문은 각 대회 공식 페이지에서)</p>
{contests}
{filt}
<div id="cpgrid">{cards}</div>

<h2 class="cp-sec">④ 우리집 연습문제</h2><p class="cp-secd">대회 유형에서 뽑은 자체 연습문제 — 초등·중등·고등·부모와 함께.</p>
<div class="cp-lv"><a href="/competitions/practice.html"><span class="e">🏠</span>우리집 연습문제 30+ 풀러 가기</a></div>

<p style="margin-top:22px;font-size:12.5px;color:#9b8a6e">※ 공개된 대회만 다루며 문제 원문을 그대로 싣지 않습니다. 각 카드의 '출처' 링크에서 공식 안내를 확인하세요.</p>
<script>
(function(){{var b=document.querySelectorAll('#cpf button'),cs=document.querySelectorAll('#cpgrid .cp-card');
b.forEach(function(x){{x.onclick=function(){{b.forEach(function(y){{y.classList.remove('on')}});x.classList.add('on');var l=x.dataset.l;
cs.forEach(function(c){{c.style.display=(l==='all'||c.dataset.level===l)?'':'none'}});}};}});}})();
</script>"""
    return layout("/competitions.html","","AI 경진대회 문제풀이 교실 | AI 조기교육",
        "국내외 AI 경진대회 공개 문제를 학년별로 아이 눈높이에서 풀어보는 교실. 요약·풀이전략·연습문제·출처.",inner)

def level_page(level,path,base="../"):
    name,emo=LV[level]
    ps=[p for p in PROB if p["level"]==level]
    cards="".join(card(p) for p in ps)
    inner=f"""<div class="cp-hero"><span class="k">{emo} {name}</span>
<h1>{name} · AI 문제 풀이</h1><p>이 수준에서 자주 나오는 문제와, 집에서 하는 풀이법.</p></div>
<p class="cp-secd" style="margin-top:16px">{len(ps)}개 문제 · 각 문제의 '▶ 풀이 순서'를 펼쳐 AI에게 물어볼 말과 검증법을 보세요.</p>
{cards}
<div class="cp-hero" style="margin-top:20px;background:linear-gradient(160deg,#FFF3E9,#FCE7D6);border-color:#F0DDC8">
<b style="color:#7a3e12">집에서 더 연습하기</b><p style="color:#9a5b23;margin-top:4px">우리집 연습문제로 반복하면 실력이 됩니다.</p>
<a class="btn btn-primary" style="margin-top:8px" href="/competitions/practice.html">🏠 우리집 연습문제 →</a></div>"""
    return layout(path,base,f"{name} AI 경진대회 문제 | AI 조기교육",f"{name} 수준 AI 경진대회 공개 문제를 요약·풀이전략·연습문제로. 출처 링크 포함.",inner)

def ai_top_100():
    ct=CMAP["ai_top_100"]; ps=[p for p in PROB if p["contest"]=="ai_top_100"]
    cards="".join(card(p) for p in ps)
    inner=f"""<div class="cp-hero"><span class="k">🏆 대회 분석</span>
<h1>AI TOP 100 (Campus)</h1><p>{ct['desc']}</p></div>
<div class="cp-contest" style="margin-top:16px"><span style="font-size:22px">📌</span><div>
<b>어떤 대회?</b><p>{ct['org']} · 대상 {', '.join(LV[l][0] for l in ct['levels'])}. AI 도구 사용에 제한이 없고, '문제를 얼마나 잘 푸느냐'를 봅니다.</p>
<a class="cp-src" href="{ct['url']}" target="_blank" rel="noopener">📎 공식 페이지 ↗</a></div></div>
<h2 class="cp-sec">이 대회형 문제, 집에서는 이렇게</h2>
<p class="cp-secd">핵심은 'AI와 협업해 스스로 판단하기'. 아래를 펼쳐 첫 질문·다시 묻기·검증을 보세요.</p>
{cards}
<p style="margin-top:18px;font-size:12.5px;color:#9b8a6e">※ 문제 원문은 싣지 않습니다. 공식 페이지에서 확인하세요.</p>"""
    return layout("/competitions/ai-top-100.html","../","AI TOP 100 분석 · 집에서 풀기 | AI 조기교육","AI TOP 100(Campus) 대회 유형을 아이·학생 눈높이 풀이로. AI 협업·검증 중심. 출처 링크.",inner)

def practice_page():
    groups=[("elementary","🟢 초등용"),("middle","🔵 중등용"),("high","🟣 고등용"),("family","👨‍👩‍👧 부모와 함께")]
    sec=""
    for lv,label in groups:
        ps=[p for p in PROB if p["kind"]=="practice" and p["level"]==lv]
        sec+=f'<h2 class="cp-sec">{label} <span style="font-size:13px;color:var(--muted)">({len(ps)}문제)</span></h2>'+"".join(card(p) for p in ps)
    inner=f"""<div class="cp-hero" style="background:linear-gradient(160deg,#FFF3E9,#FCE7D6);border-color:#F0DDC8">
<span class="k" style="background:#E0684A">🏠 우리집 연습문제</span>
<h1 style="color:#7a3e12">대회 문제를, 오늘 집에서</h1><p style="color:#9a5b23">정답을 대신 주지 마세요. 아이가 AI 답의 이상한 곳을 찾아 다시 묻게 도와주세요.</p></div>
<div style="margin-top:14px">{sec}</div>"""
    return layout("/competitions/practice.html","../","우리집 AI 연습문제 · 초·중·고·부모 | AI 조기교육","AI 경진대회 유형에서 뽑은 자체 연습문제. 초등·중등·고등·부모와 함께. 첫 질문·다시 묻기·검증 포함.",inner)

def build_all():
    BS.write("competitions.html",hub())
    BS.write("competitions/elementary.html",level_page("elementary","/competitions/elementary.html"))
    BS.write("competitions/middle.html",level_page("middle","/competitions/middle.html"))
    BS.write("competitions/high.html",level_page("high","/competitions/high.html"))
    BS.write("competitions/university-general.html",level_page("university_general","/competitions/university-general.html"))
    BS.write("competitions/ai-top-100.html",ai_top_100())
    BS.write("competitions/practice.html",practice_page())
    print("AI 경진대회 교실 · 7페이지 생성 완료")

if __name__=="__main__":
    build_all()
