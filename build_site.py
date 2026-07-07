#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ai-craft-kids 전면 개편 사이트 생성기 — 그림책형 교육 랜딩(시안 반영).
루트 클린패스 페이지 + world-cases/·videos/ 서브폴더. 국가 일러스트·영상 재사용."""
import os
import parent_coach as PC
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
            if it["video_id"]=="wae-illust-v2" and it.get("public"):
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

# ---------- 상단 드롭다운 메뉴 (nav 항목 바로 아래 · 카드 없음 · 5항목) ----------
YT_CH="https://www.youtube.com/channel/UCzCA_HXDHMVGvWpQv4PSZgw"
MEGA=[
 ("why","왜 AI교육인가","/why-ai-education.html",[
   ("왜 지금 AI교육인가","/why-ai-education.html"),
   ("알파고 이후, 놓친 시간","/why-ai-education.html#alphago"),
   ("다시 묻는 힘","/why-ai-education.html#reask"),
   ("막을 것인가, 다룰 것인가","/why-ai-education.html#handle"),
  ],"전체 보기"),
 ("cases","세계 AI교육","/world-cases.html",[
   ("중국 · 시간표에 AI를 넣다","/world-cases/china.html"),
   ("미국 · 만드는 아이를 키우다","/world-cases/usa.html"),
   ("영국 · 비판적으로 판단하다","/world-cases/uk.html"),
   ("싱가포르 · 생활 속에서 실습","/world-cases/singapore.html"),
  ],"전체 국가 보기"),
 ("videos","영상관","/videos.html",[
   ("롱폼 다큐 · 세계 5개국","/videos/world-ai-education.html"),
   ("중국 AI교육 심층","/videos/china-ai-education.html"),
   ("미국 AI교육 심층","/videos/us-ai-education.html"),
   ("한국의 잃어버린 AI 10년","/videos/korea-ai-education.html"),
  ],"전체 영상 보기"),
 ("start","시작 가이드","/start-guide.html",[
   ("집에서 시작하는 6단계","/start-guide.html"),
   ("첫 질문 시키기","/start-guide.html#step2"),
   ("다시 묻기 연습","/start-guide.html#step5"),
   ("하루 10분 루틴","/world-cases/korea-3.html"),
  ],"전체 가이드 보기"),
 ("res","부모 자료실","/parent-resources.html",[
   ("국가별 자료실 한눈에","/parent-resources.html"),
   ("중국 부모 자료","/parents/china.html"),
   ("영국 부모 자료","/parents/uk.html"),
   ("자주 묻는 질문","/parent-resources.html#faq"),
  ],"전체 자료실 보기"),
 ("free","무료 프로그램","/free-programs.html",[
   ("🎤 음성 만들기 (TTS)","/free-programs.html#voice"),
   ("🎬 영상 만들기·조립","/free-programs.html#video"),
   ("💬 자막·오디오 편집","/free-programs.html#subtitle"),
   ("💻 로컬 AI 실행","/free-programs.html#localai"),
  ],"전체 프로그램 보기"),
 ("paid","유료 프로그램","/paid-programs.html",[
   ("🎬 쇼츠 자동 빌더","/paid-programs.html#shorts-builder"),
   ("📽 영상 자동 생성기","/paid-programs.html#video-maker"),
   ("✂️ 캡컷 에이전트","/paid-programs.html#capcut-agent"),
   ("📝 블로그 레이더","/paid-programs.html#blog-radar"),
  ],"전체 보기 (모두 ₩9,900)"),
]
def header(active,base):
    tops="".join(f'<a class="mg-t{" on" if k==active else ""}" data-k="{k}" href="{h}">{t}</a>' for k,t,h,_,_ in MEGA)
    dds=""
    for k,t,h,items,more in MEGA:
        links="".join(f'<a href="{u}">{lb}</a>' for lb,u in items)
        dds+=f'<div class="mg-dd-c" data-k="{k}">{links}<a class="mg-more" href="{h}">{more} →</a></div>'
    sdata=[]
    for k,t,h,items,_ in MEGA:
        sdata.append({"t":t,"u":h,"c":t})
        for lb,u in items: sdata.append({"t":lb,"u":u,"c":t})
    import json as _j; sjson=_j.dumps(sdata,ensure_ascii=False)
    mob=""
    for k,t,h,items,more in MEGA:
        mi="".join(f'<a href="{u}">{lb}</a>' for lb,u in items)+f'<a href="{h}" style="color:var(--coral);font-weight:800">{more} →</a>'
        mob+=f'<details{"" if k!=active else " open"}><summary>{t}</summary>{mi}</details>'
    return f"""<header class="mgh" id="mgh">
<div class="mg-bar">
<a class="mg-brand" href="/"><span class="bot">🤖</span><span><b>AI 조기교육</b><small>결과물이 아니라 과정이 교육이다</small></span></a>
<nav class="mg-nav">{tops}</nav>
<div class="mg-right">
<button class="mg-ic mg-allbtn" onclick="document.body.classList.toggle('mg-open')" title="전체메뉴">☰ <small style="font-size:10px;font-weight:800">전체</small></button>
<button class="mg-ic" onclick="mgSearch()" title="검색">🔍</button>
<a class="mg-ic" href="{YT_CH}" target="_blank" rel="noopener" title="유튜브 채널">▶</a>
<a class="btn btn-primary mg-cta" href="/start-guide.html">무료로 시작하기</a>
<button class="mg-ic mg-hamb" onclick="document.body.classList.toggle('mg-open')">☰</button>
</div></div>
<div class="mg-dd" id="mgDD">{dds}</div>
<div class="mg-srch" id="mgSrch"><div class="mg-sin">
<input id="mgQ" placeholder="찾으실 내용을 입력하세요 — 국가, 영상, 자료, 시작법…" oninput="mgF()">
<div id="mgR" class="mg-res"></div></div></div>
<div class="mg-mob">{mob}<a class="btn btn-primary" style="margin:12px" href="/start-guide.html">무료로 시작하기</a></div>
</header>
<style>
.mgh{{position:sticky;top:0;z-index:80;background:#fff;border-bottom:1px solid #EADFCE;box-shadow:0 1px 6px rgba(0,0,0,.04)}}
.mg-bar{{width:100%;max-width:none;margin:0;display:flex;align-items:center;gap:14px;padding:10px 24px;box-sizing:border-box}}
.mg-brand{{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--ink);flex:0 0 auto}}
.mg-brand .bot{{width:34px;height:34px;background:var(--navy);color:#fff;border-radius:10px;display:grid;place-items:center;font-size:17px}}
.mg-brand b{{font-size:16px;display:block;line-height:1.1;white-space:nowrap}}
.mg-brand small{{font-size:10.5px;color:#9b8a6e;font-weight:600;white-space:nowrap}}
.mg-nav{{display:flex;flex-wrap:nowrap;flex:1 1 auto;min-width:0;gap:2px;overflow-x:auto;overflow-y:hidden;white-space:nowrap;scrollbar-width:none;-ms-overflow-style:none}}
.mg-nav::-webkit-scrollbar{{display:none}}
.mg-t:first-child{{margin-left:auto}}.mg-t:last-child{{margin-right:auto}}
.mg-t{{flex:0 0 auto;white-space:nowrap;line-height:1;padding:12px clamp(7px,0.9vw,15px);text-decoration:none;color:var(--ink);font-weight:700;font-size:clamp(12.5px,0.95vw,14.5px);border-bottom:3px solid transparent}}
.mg-t:hover{{color:var(--coral)}}
.mg-t.on{{color:var(--coral);border-bottom-color:var(--coral)}}
.mg-right{{display:flex;align-items:center;gap:8px;flex:0 0 auto}}
.mg-ic{{height:36px;min-width:36px;border:1px solid #EADFCE;background:#fff;border-radius:10px;display:grid;place-items:center;font-size:15px;cursor:pointer;text-decoration:none;color:var(--ink)}}
.mg-ic:hover{{background:#FBF3E4}}
.mg-allbtn{{width:auto;padding:0 10px;display:flex;align-items:center;gap:4px}}
.mg-cta{{white-space:nowrap}}
.mg-hamb{{display:none}}
.mg-dd{{position:fixed;display:none;width:300px;background:#fffaf0;border:1px solid #EAD9BE;border-radius:14px;box-shadow:0 14px 30px rgba(0,0,0,.12);padding:10px 8px;z-index:95}}
.mg-dd.show{{display:block}}
.mg-dd-c{{display:none}}
.mg-dd-c.sh{{display:block}}
.mg-dd-c a{{display:block;padding:8px 11px;border-radius:8px;text-decoration:none;color:#5a4a35;font-size:13.5px;font-weight:600}}
.mg-dd-c a:hover{{background:#FDECE5;color:#B44A31}}
.mg-dd-c .mg-more{{margin-top:5px;border-top:1px dashed #EAD9BE;color:var(--coral);font-weight:800;font-size:12.5px;border-radius:0 0 8px 8px}}
.mg-srch{{display:none;position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid #EADFCE;box-shadow:0 14px 30px rgba(43,32,22,.12)}}
.mgh.srch .mg-srch{{display:block}}
.mg-sin{{max-width:900px;margin:0 auto;padding:18px 20px 22px}}
#mgQ{{width:100%;border:2px solid var(--coral);border-radius:12px;padding:13px 16px;font:inherit;font-size:15px}}
.mg-res{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:6px;margin-top:12px}}
.mg-res a{{display:block;padding:8px 12px;border:1px solid #F0E6D2;border-radius:9px;text-decoration:none;color:var(--ink);font-size:13px;font-weight:600}}
.mg-res a small{{color:#9b8a6e;display:block;font-size:11px}}
.mg-res a:hover{{background:#FBF3E4}}
.mg-mob{{position:fixed;inset:56px 0 0 0;background:#fff;overflow:auto;padding:8px 6px;transform:translateX(100%);transition:transform .18s;z-index:90}}
body.mg-open .mg-mob{{transform:none}}
.mg-mob details{{border-bottom:1px solid #F0E6D2}}
.mg-mob summary{{padding:13px 16px;font-weight:800;cursor:pointer;list-style:none}}
.mg-mob details a{{display:block;padding:9px 26px;text-decoration:none;color:#5a4a35;font-size:14px}}
@media(max-width:1450px){{.mg-brand small{{display:none}}}}
@media(max-width:960px){{
.mg-nav,.mg-cta,.mg-allbtn{{display:none}}.mg-hamb{{display:grid}}
.mg-brand small{{display:none}}
.mg-dd{{display:none!important}}
}}
</style>
<script>
(function(){{
var H=document.getElementById('mgh'),DD=document.getElementById('mgDD'),tm;
function show(k,el){{
 if(window.innerWidth<=960)return;
 clearTimeout(tm);H.classList.remove('srch');
 DD.querySelectorAll('.mg-dd-c').forEach(function(c){{c.classList.toggle('sh',c.dataset.k===k);}});
 var r=el.getBoundingClientRect(),hb=H.getBoundingClientRect().bottom;
 DD.classList.add('show');
 var w=DD.offsetWidth,left=r.left;
 if(left+w>window.innerWidth-12)left=window.innerWidth-w-12;
 DD.style.left=left+'px';DD.style.top=(hb+4)+'px';
}}
function hide(){{tm=setTimeout(function(){{DD.classList.remove('show');}},150);}}
document.querySelectorAll('.mg-t').forEach(function(a){{
 a.addEventListener('mouseenter',function(){{show(a.dataset.k,a);}});
 a.addEventListener('mouseleave',hide);
}});
DD.addEventListener('mouseenter',function(){{clearTimeout(tm);}});
DD.addEventListener('mouseleave',hide);
document.addEventListener('click',function(e){{
 if(!DD.contains(e.target)&&!e.target.closest('.mg-t'))DD.classList.remove('show');}});
document.addEventListener('keydown',function(e){{
 if(e.key==='Escape'){{DD.classList.remove('show');H.classList.remove('srch');document.body.classList.remove('mg-open');}}}});
window.addEventListener('scroll',function(){{DD.classList.remove('show');}});
window.mgSearch=function(){{DD.classList.remove('show');H.classList.toggle('srch');
 if(H.classList.contains('srch')){{document.getElementById('mgQ').focus();mgF();}}}};
var D={sjson};
window.mgF=function(){{var q=(document.getElementById('mgQ').value||'').trim().toLowerCase();
 var r=D.filter(function(d){{return !q||d.t.toLowerCase().indexOf(q)>=0||d.c.toLowerCase().indexOf(q)>=0;}}).slice(0,18);
 document.getElementById('mgR').innerHTML=r.map(function(d){{return '<a href="'+d.u+'">'+d.t+'<small>'+d.c+'</small></a>';}}).join('')||'<p style="color:#9b8a6e">결과가 없습니다.</p>';}};
}})();
</script>"""

def footer(base):
    b=base or "/"
    return f"""<footer class="site"><div class="wrap"><div class="foot-grid">
<div class="foot-brand"><a class="brand" href="{b}"><span class="bot">🤖</span> AI 조기교육</a>
<p>아이와 부모가 함께 성장하는<br>미래 교육의 시작</p></div>
<div class="foot-col"><h5>서비스</h5><a href="{b}start-guide.html">시작 가이드</a><a href="{b}videos.html">영상</a><a href="{b}parent-resources.html">부모용 자료</a><a href="{b}free-programs.html">무료 프로그램</a></div>
<div class="foot-col"><h5>소개</h5><a href="{b}why-ai-education.html">왜 필요한가</a><a href="{b}world-cases.html">세계 사례</a><a href="{b}why-ai-education.html#philosophy">우리의 철학</a></div>
<div class="foot-col"><h5>고객 지원</h5><a href="{b}parent-resources.html#faq">자주 묻는 질문</a><a href="{b}start-guide.html">이용 가이드</a><a href="{b}privacy/">개인정보처리방침</a></div>
<div class="foot-col"><h5>문의</h5><a href="mailto:2011kstudentlife@gmail.com">2011kstudentlife@gmail.com</a><a href="{b}videos.html">영상관</a></div>
</div><div class="foot-bottom">© 2026 AI조기교육. 아이가 AI와 대화하며 '다시 묻는 힘'을 기르는 교육. <span id="footVisits" style="margin-left:10px;opacity:.75"></span> <a href="/content-bank.html" style="color:inherit;opacity:.35;text-decoration:none">🧊</a></div></div></footer>
<script>(function(){{var K='sb_publishable_oafZabTGRQFOeZLCNZX1Dg_bk5nid4U',U='https://nmzngmmaxcqrtdryubsd.supabase.co/rest/v1/rpc/hit_visit';
var seen=false;try{{seen=!!sessionStorage.getItem('vseen');}}catch(e){{}}
fetch(U,{{method:'POST',headers:{{'apikey':K,'Content-Type':'application/json'}},body:JSON.stringify({{site_in:'ai-edu',peek:seen}})}})
.then(function(r){{return r.json();}}).then(function(d){{
  try{{sessionStorage.setItem('vseen','1');}}catch(e){{}}
  var el=document.getElementById('footVisits');
  if(el&&d&&typeof d.total!=='undefined') el.textContent='👀 오늘 '+d.today+' · 누적 '+d.total;
}}).catch(function(){{}});}})();</script>
<script src="{base}scripts/main.js" defer></script></body></html>"""

def global_sidebar():
    """(비활성) 좌측 고정 사이드바 제거 — 상단 GNB+브레드크럼으로 단순화."""
    return ""
def _global_sidebar_legacy():
    """모든 페이지 좌측 고정 카테고리(사이트 전체 트리). 넓은화면=고정, 좁은화면=☰ 버튼."""
    import country_reality as CRX
    tops=[("🏠","홈","/"),("💡","왜 필요한가","/why-ai-education.html"),("📚","세계 AI교육법 연재","/world-cases.html"),
          ("🚀","시작 가이드","/start-guide.html"),("🎬","영상관","/videos.html"),
          ("👨‍👩‍👧","부모 자료실","/parent-resources.html"),("🖨","무료 인쇄 자료","/free-kit.html")]
    top_html="".join(f'<a class="gs-i" href="{h}">{ic} {t}</a>' for ic,t,h in tops)
    cty=""
    for c in COUNTRIES:
        slug,name,flag=c[0],c[1],c[2]
        subs=f'<a class="gs-s" href="/parent-resources/{slug}.html">📂 {name} 자료실</a>'
        subs+="".join(f'<a class="gs-s" href="{h}"{" target=_blank rel=noopener" if h.startswith("/free/") else ""}>{ic} {t}</a>' for ic,t,h in CRX.subs_list(slug))
        cty+=f'<div class="gs-c" id="gsc-{slug}"><button class="gs-cb" onclick="gsT(\'{slug}\')"><span>{flag} {name}</span><span class="gs-ar">▸</span></button><div class="gs-sub">{subs}</div></div>'
    return f"""<aside class="gside" id="gside">
<a class="gs-brand" href="/">🤖 AI 조기교육</a>
{top_html}
<div class="gs-h">🌍 국가별 자료</div>
{cty}
</aside>
<button class="gs-fab" onclick="document.body.classList.toggle('gs-open')">☰ 메뉴</button>
<style>
.gside{{position:fixed;left:0;top:0;bottom:0;width:236px;background:#fff;border-right:1px solid #EADFCE;padding:14px 10px 34px;overflow:auto;z-index:45}}
.gs-brand{{display:block;font-weight:900;font-size:15px;color:var(--ink);text-decoration:none;padding:6px 12px 14px}}
.gs-h{{font-size:11.5px;font-weight:800;color:#9b8a6e;padding:12px 12px 5px}}
.gs-i{{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:9px;text-decoration:none;color:var(--ink);font-weight:700;font-size:13.5px}}
.gs-i:hover,.gs-cb:hover{{background:#FBF3E4}}
.gs-cb{{display:flex;justify-content:space-between;align-items:center;width:100%;border:0;background:none;padding:8px 12px;border-radius:9px;font:inherit;font-weight:700;font-size:13.5px;cursor:pointer;color:var(--ink)}}
.gs-ar{{color:#c4b59a;transition:transform .15s}}
.gs-c.open .gs-ar{{transform:rotate(90deg)}}
.gs-sub{{display:none;padding:1px 0 4px 10px}}
.gs-c.open .gs-sub{{display:block}}
.gs-s{{display:flex;align-items:center;gap:6px;padding:6px 10px;margin:1px 4px;border-radius:8px;text-decoration:none;color:var(--navy2);font-weight:600;font-size:12.4px;border:1px solid transparent}}
.gs-s:hover{{background:#FBF3E4;border-color:#EADFCE}}
.gs-i.on,.gs-s.on{{background:#FDECE5;border:1px solid #E0684A;color:#B44A31}}
.gs-fab{{display:none;position:fixed;left:14px;bottom:16px;z-index:46;background:#E0684A;color:#fff;border:0;border-radius:24px;padding:11px 18px;font-weight:800;font-size:13.5px;box-shadow:0 4px 14px rgba(0,0,0,.25);cursor:pointer}}
@media(min-width:1200px){{body{{padding-left:236px}}}}
@media(max-width:1199px){{.gside{{transform:translateX(-100%);transition:transform .18s;box-shadow:6px 0 20px rgba(0,0,0,.14)}}
body.gs-open .gside{{transform:none}}.gs-fab{{display:block}}}}
</style>
<script>
function gsT(s){{document.getElementById('gsc-'+s).classList.toggle('open');}}
(function(){{var p=(location.pathname.replace(/\\/$/,'')||'/').replace(/\\.html$/,'');
document.querySelectorAll('.gside a').forEach(function(a){{var h=a.getAttribute('href');if(!h||h.charAt(0)!=='/')return;
var hp=(h.replace(/\\/$/,'')||'/').replace(/\\.html$/,'');
if(hp===p){{a.classList.add('on');var c=a.closest('.gs-c');if(c)c.classList.add('open');}}}});
}})();
</script>"""


# ---------- 섹션별 좌측 사이드바 (2컬럼 레이아웃) ----------
# 항목: (라벨, href|None=준비중). 실존 페이지만 링크(죽은 링크 금지).
SECTIONS={
 "why":("왜 AI교육인가",[
   ("왜 지금 AI교육인가","/why-ai-education.html"),
   ("알파고 이후, 놓친 시간","/why-ai-education.html#alphago"),
   ("결과물이 아니라 과정이 교육","/why-ai-education.html#philosophy"),
   ("다시 묻는 힘","/why-ai-education.html#reask"),
   ("막을 것인가, 다룰 것인가","/why-ai-education.html#handle"),
 ]),
 "world":("세계 AI교육",[
   ("전체 지도 보기","/world-cases.html"),
   ("🇨🇳 중국","/world-cases/china.html"),
   ("🇺🇸 미국","/world-cases/usa.html"),
   ("🇬🇧 영국","/world-cases/uk.html"),
   ("🇸🇬 싱가포르","/world-cases/singapore.html"),
   ("🇰🇷 한국","/world-cases/korea.html"),
   ("🇩🇪 독일","/world-cases/germany.html"),
   ("🇯🇵 일본","/world-cases/japan.html"),
   ("─ 영국 심화 ─",None),
   ("학년별 로드맵 (만5~16세)","/world-cases/uk-roadmap.html"),
   ("1년 커리큘럼 (Year 8)","/world-cases/uk-year.html"),
   ("집 실전판","/world-cases/uk-home.html"),
   ("만 8세 12주 프로그램","/world-cases/uk-8yo-12weeks.html"),
   ("국가별 비교표",None),
 ]),
 "videos":("영상관",[
   ("전체 영상","/videos.html"),
   ("🎈 AI랑 놀자 (아이 전용)","/videos/kids-ai-show.html"),
   ("롱폼 다큐 · 세계 5개국","/videos/world-ai-education.html"),
   ("중국 AI교육 심층","/videos/china-ai-education.html"),
   ("미국 AI교육 심층","/videos/us-ai-education.html"),
   ("영국 AI교육 심층","/videos/uk-ai-education.html"),
   ("싱가포르 AI교육 심층","/videos/singapore-ai-education.html"),
   ("한국의 잃어버린 AI 10년","/videos/korea-ai-education.html"),
 ]),
 "guide":("시작 가이드",[
   ("집에서 시작하는 6단계","/start-guide.html"),
   ("첫 질문 시키기","/start-guide.html#step2"),
   ("결과 관찰하기","/start-guide.html#step3"),
   ("다시 묻기 연습","/start-guide.html#step5"),
   ("하루 10분 루틴","/world-cases/korea-3.html"),
   ("🏆 AI 경진대회 교실","/competitions.html"),
 ]),
 "parents":("부모 자료실",[
   ("자료실 홈","/parent-resources.html"),
   ("🇨🇳 중국 부모 자료","/parents/china.html"),
   ("🇺🇸 미국 부모 자료","/parents/usa.html"),
   ("🇬🇧 영국 부모 자료","/parents/uk.html"),
   ("🇸🇬 싱가포르 부모 자료","/parents/singapore.html"),
   ("🇰🇷 한국 부모 자료","/parents/korea.html"),
   ("🇩🇪 독일 부모 자료","/parents/germany.html"),
   ("🇯🇵 일본 부모 자료","/parents/japan.html"),
   ("자주 묻는 질문","/parent-resources.html#faq"),
 ]),
 "paid":("유료 프로그램 · 모두 ₩9,900",[
   ("전체 안내","/paid-programs.html"),
   ("🎬 쇼츠 자동 빌더","/paid-programs.html#shorts-builder"),
   ("📽 영상 자동 생성기","/paid-programs.html#video-maker"),
   ("✂️ 캡컷 에이전트","/paid-programs.html#capcut-agent"),
   ("📝 네이버 블로그 레이더","/paid-programs.html#blog-radar"),
   ("🎨 밈 카툰 변환기","/paid-programs.html#meme-cartoon"),
   ("🃏 12주 워크북 부모 해설판","/paid-programs.html#workbook-guide"),
 ]),
 "free":("무료 프로그램",[
   ("전체 안내","/free-programs.html"),
   ("🎤 음성 만들기","/free-programs.html#voice"),
   ("🎬 영상 만들기","/free-programs.html#video"),
   ("🖼 이미지 만들기","/free-programs.html#image"),
   ("💬 자막·오디오 편집","/free-programs.html#subtitle"),
   ("💻 로컬 AI 실행","/free-programs.html#localai"),
   ("🛠 개발 도구","/free-programs.html#dev"),
 ]),
}
ACTIVE2SEC={"why":"why","cases":"world","videos":"videos","start":"guide","res":"parents","free":"free"}
def section_sidebar(section):
    title,items=SECTIONS[section]
    links=""
    for lb,u in items:
        if u: links+=f'<a class="sb-a" href="{u}">{lb}</a>'
        elif lb.startswith("─"): links+=f'<div style="font-size:11px;font-weight:800;color:#9b8a6e;padding:8px 11px 2px">{lb.strip("─ ")}</div>'
        else: links+=f'<span class="sb-a sb-x">{lb} <small>준비중</small></span>'
    return f"""<aside class="secbar"><div class="sb-t" onclick="this.parentElement.classList.toggle('fold')">{title} <span class="sb-ar">▾</span></div><nav class="sb-nav">{links}</nav></aside>
<style>
.ly2{{max-width:1240px;margin:0 auto;padding:16px 20px 0;display:flex;gap:26px;align-items:flex-start}}
.ly2-main{{flex:1;min-width:0}}
.secbar{{width:238px;flex:none;background:#FFF9EF;border:1px solid #EAD9BE;border-radius:14px;padding:12px 9px;position:sticky;top:74px}}
.sb-t{{font-weight:800;font-size:14.5px;color:var(--navy);padding:5px 11px 10px;border-bottom:2px solid #F0E6D2;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center}}
.sb-ar{{display:none;color:#c4b59a}}
.sb-a{{display:block;padding:7px 11px;margin:1px 0;border-radius:8px;text-decoration:none;color:#5a4a35;font-size:13.3px;font-weight:600}}
a.sb-a:hover{{background:#FDECE5;color:#B44A31}}
.sb-a.on{{background:var(--coral);color:#fff}}
.sb-x{{color:#c4b59a;cursor:default}}.sb-x small{{font-size:10px;background:#F0E6D2;border-radius:6px;padding:1px 6px;margin-left:4px}}
@media(max-width:960px){{
.ly2{{flex-direction:column;gap:12px}}
.secbar{{position:static;width:100%}}
.sb-ar{{display:inline}}
.secbar.fold .sb-nav{{display:none}}
.sb-t{{cursor:pointer;border-bottom:0;margin-bottom:0}}
.secbar:not(.fold) .sb-t{{border-bottom:2px solid #F0E6D2;margin-bottom:6px}}
}}
</style>
<script>
(function(){{var p=(location.pathname.replace(/[/]$/,'')||'/').replace(/[.]html$/,'');
document.querySelectorAll('.secbar a.sb-a').forEach(function(a){{
 var h=a.getAttribute('href').split('#')[0];var hp=(h.replace(/[/]$/,'')||'/').replace(/[.]html$/,'');
 if(hp===p&&!document.querySelector('.sb-a.on'))a.classList.add('on');}});
if(window.innerWidth<=960)document.querySelector('.secbar').classList.add('fold');
}})();
</script>"""

def page(active,base,title,desc,body):
    sec=ACTIVE2SEC.get(active)
    if sec and "rsLoad(" not in body and 'class="frsb' not in body:
        body=f'<div class="ly2">{section_sidebar(sec)}<div class="ly2-main">{body}</div></div>'
    return head(title,desc,base)+header(active,base)+global_sidebar()+body+footer(base)

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
    cc="".join(f"""<a class="card" href="/world-cases/{c[0]}.html" style="text-decoration:none;display:flex;gap:12px;align-items:center;padding:14px 16px">
<span style="font-size:26px">{c[2]}</span><div><b style="color:var(--ink)">{c[1]}</b><span style="color:var(--muted);font-size:13px"> — {c[5]}</span></div>
<span style="margin-left:auto;color:var(--coral);font-weight:800">→</span></a>""" for c in COUNTRIES)
    body=f"""<main>
<section class="page-hero" style="padding:44px 0 26px"><div class="wrap" style="text-align:center">
<h1 style="font-size:33px;margin:0 0 10px">AI를 <span style="color:#9b8a6e">많이 쓰는</span> 아이보다,<br><span class="coral">AI 답을 고칠 줄 아는</span> 아이로.</h1>
<p style="color:var(--navy2);font-weight:600;margin:0 0 4px">아이 나이에 맞게, 매일 10분씩 — AI에게 묻고 <b>다시 묻는 힘</b>을 기릅니다.</p>
<p style="color:var(--muted);font-size:13.5px;margin:0 0 18px">결과물이 아니라 과정이 교육이다</p>
<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
<a class="btn btn-primary btn-lg" href="/daily-class/today.html">▶ 오늘의 10분 수업</a>
<a class="btn btn-ghost btn-lg" href="/levels.html">🎯 우리 아이 나이별</a></div>
</div></section>

<section class="block" style="padding:8px 0 20px"><div class="wrap" style="max-width:900px">
<h2 class="sec-title" style="font-size:20px;margin-bottom:14px">🏫 우리 집 3층 교실 시스템</h2>
<div class="grid g3">
<a class="card" href="/world-cases.html" style="text-decoration:none;display:block;border-top:4px solid #2E8B96"><div style="font-size:30px">🌍</div><b style="color:#22406b">① 세계 AI교육에서 배운 원칙</b><p style="color:var(--muted);font-size:13px;margin:5px 0 0">7개국이 아이에게 AI를 어떻게 가르치나 — 우리 교실의 근거.</p></a>
<a class="card" href="/daily-class/today.html" style="text-decoration:none;display:block;border-top:4px solid #E0684A"><div style="font-size:30px">🏫</div><b style="color:#7a3e12">② 오늘 집에서 하는 10분 수업</b><p style="color:var(--muted);font-size:13px;margin:5px 0 0">오늘의 질문 → 다시 묻기. 매일 켜지는 작은 교실.</p></a>
<a class="card" href="/levels.html" style="text-decoration:none;display:block;border-top:4px solid #7A5BB0"><div style="font-size:30px">🎯</div><b style="color:#5a3ec8">③ 우리 아이 나이에 맞는 로드맵</b><p style="color:var(--muted);font-size:13px;margin:5px 0 0">유치원~고등. 말하기→고치기→의심→검증→해결.</p></a>
</div></div></section>

<section class="block" style="padding:26px 0 20px"><div class="wrap" style="max-width:760px">
<h2 class="sec-title" style="font-size:20px;margin-bottom:14px">🌍 세계는 아이에게 AI를 어떻게 가르치나</h2>
<div style="display:grid;gap:9px">{cc}</div>
</div></section>
<section class="block" style="padding:8px 0 20px"><div class="wrap" style="max-width:760px">
<h2 class="sec-title" style="font-size:20px;margin-bottom:14px">🎬 우리 채널 공개 영상</h2>
<div class="player"><iframe src="https://www.youtube.com/embed/{YT_MAIN}" title="세계 5개국은 아이에게 AI를 어떻게 가르치나" loading="lazy" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:12px">
<a class="btn btn-ghost" href="/videos/china-ai-education.html">🇨🇳 중국 심층</a>
<a class="btn btn-ghost" href="/videos/us-ai-education.html">🇺🇸 미국 심층</a>
<a class="btn btn-ghost" href="/videos/uk-ai-education.html">🇬🇧 영국</a>
<a class="btn btn-ghost" href="/videos/singapore-ai-education.html">🇸🇬 싱가포르</a>
<a class="btn btn-ghost" href="/videos/korea-ai-education.html">🇰🇷 잃어버린 AI 10년</a>
<a class="btn btn-primary" href="/videos.html">영상관 전체 →</a></div>
</div></section>
<section class="block" style="padding:0 0 44px"><div class="wrap" style="max-width:760px">
<a href="/daily-class.html" style="display:flex;gap:14px;align-items:center;background:linear-gradient(135deg,#FFF3E9,#FCE7D6);border:1px solid #F0DDC8;border-radius:16px;padding:16px 20px;text-decoration:none;color:#7a3e12;margin-bottom:10px">
<span style="font-size:34px">🏫</span><div><b style="font-size:16px">매일 AI교실 · 매일 10분</b><p style="margin:2px 0 0;color:#9a5b23;font-weight:600;font-size:13.5px">오늘의 질문 → AI에게 말하기 → 이상한 점 찾기 → 다시 묻기. 1년 커리큘럼.</p></div>
<span style="margin-left:auto;color:#E0684A;font-weight:900">→</span></a>
<a href="/levels.html" style="display:flex;gap:14px;align-items:center;background:linear-gradient(135deg,#FFF7EA,#FBEBD3);border:1px solid #EAD9BE;border-radius:16px;padding:16px 20px;text-decoration:none;color:#7a3e12;margin-bottom:10px">
<span style="font-size:34px">🎯</span><div><b style="font-size:16px">연령별 AI교실 · 유치원~고등</b><p style="margin:2px 0 0;color:#9a5b23;font-weight:600;font-size:13.5px">우리 아이 나이엔 뭘? 말하기→고치기→의심→검증→해결.</p></div>
<span style="margin-left:auto;color:#E0684A;font-weight:900">→</span></a>
<a href="/competitions.html" style="display:flex;gap:14px;align-items:center;background:linear-gradient(135deg,#EAF2FB,#DCEAF8);border:1px solid #CADCF0;border-radius:16px;padding:16px 20px;text-decoration:none;color:#22406b">
<span style="font-size:34px">🏆</span><div><b style="font-size:16px">AI 경진대회 문제풀이 교실</b><p style="margin:2px 0 0;color:#4a5f7d;font-weight:600;font-size:13.5px">실제 대회 문제를 아이 눈높이로 — 학년별 문제·풀이전략·우리집 연습문제.</p></div>
<span style="margin-left:auto;color:#3A6FB0;font-weight:900">→</span></a>
</div></section>
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
<h2 id="alphago" style="margin-top:40px;scroll-margin-top:90px">알파고 이후, 놓친 시간</h2>
<p>2016년, 알파고가 이세돌을 이긴 곳은 서울이었습니다. AI 시대의 경고음이 우리 한복판에서 울렸지만, 그 후 10년 — 세계가 교실을 바꾸는 동안 우리는 속도 조절에 실패했습니다. 문제는 과거가 아니라, <b>지금 우리 아이의 습관</b>입니다.</p>
<h2 id="reask" style="margin-top:34px;scroll-margin-top:90px">다시 묻는 힘</h2>
<p>AI 시대의 핵심 역량은 정답을 빨리 받는 힘이 아니라 <b>받은 답을 의심하고, 더 낫게 다시 묻는 힘</b>입니다. 이 힘은 학교 커리큘럼이 아니라 저녁 식탁의 대화 습관에서 자랍니다.</p>
<h2 id="handle" style="margin-top:34px;scroll-margin-top:90px">AI를 막을 것인가, 다룰 것인가</h2>
<p>아이들은 이미 AI를 만나고 있습니다. 막으면 몰래 쓰고, 풀어두면 끌려갑니다. 답은 하나 — <b>안전한 경계 안에서, 다루는 법을 함께 배우는 것</b>입니다. 방식은 나라마다 달라도 방향은 같습니다.</p>
<div class="cta-band" style="margin-top:38px"><div><h3>관련 링크</h3><p>세계가 실제로 어떻게 가르치는지 · 오늘 집에서 시작하는 법</p></div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn" href="/world-cases.html">세계 AI교육 →</a><a class="btn btn-lg btn-primary" href="/start-guide.html">시작 가이드 →</a></div></div>
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
<div class="grid g3">{cc}</div></div></section></main>"""
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
<section class="block" style="padding-bottom:0"><div class="wrap">
<a href="/videos/kids-ai-show.html" style="display:flex;gap:16px;align-items:center;background:linear-gradient(150deg,#FFF3C4,#FFD9A0);border:2px solid #F6C77a;border-radius:18px;padding:18px 22px;text-decoration:none;color:#7a3e12">
<span style="font-size:44px">🎈</span><div><div style="font-size:12px;font-weight:800;color:#b06a1e">아이 전용 · 만 6~10세</div>
<h3 style="margin:2px 0;font-size:22px">AI랑 놀자</h3><p style="margin:0;font-weight:700;color:#9a5b23">하루·아이봇과 반복해서 보며 'AI와 대화하는 법'을 배워요.</p></div>
<span style="margin-left:auto;font-weight:900;font-size:18px">→</span></a></div></section>
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
<div class="cta-band" style="margin-top:28px"><div><h3>집에서 바로 시작해볼까요?</h3><p>부모 가이드와 인쇄 자료가 준비돼 있어요.</p></div><a class="btn btn-lg" href="/parent-resources.html">부모 자료실 →</a></div>
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
        return f"""<div class="card" id="step{n}" style="margin-bottom:16px;scroll-margin-top:90px"><div class="phil" style="align-items:center;margin-bottom:12px">
<div class="pic" style="background:var(--coral);color:#fff">{n}</div><h3 style="margin:0">{t}</h3></div>
<p>{d}</p>
<div class="callout" style="margin:10px 0"><b>부모 멘트</b><br>{ment}</div>
<div class="callout good" style="margin:10px 0"><b>아이에게 물어볼 질문</b><br>💬 {ask}</div>{gp}{bp}</div>"""
    body=f"""<main>
<section class="page-hero"><div class="wrap"><div class="pill">시작 가이드</div>
<h1>집에서 따라 하는 6단계</h1><p>오늘 저녁, 아이와 15분이면 충분해요. 순서대로 따라만 하세요.</p></div></section>
<section class="block"><div class="wrap" style="max-width:760px">{"".join(sc(*s) for s in steps)}
<div class="cta-band" style="margin-top:20px"><div><h3>연습지와 질문 카드가 필요하세요?</h3><p>아이와 오늘 쓰는 인쇄 자료는 부모 자료실에서.</p></div><div style="display:flex;gap:8px;flex-wrap:wrap"><a class="btn btn-lg" href="/free/ai-first-7days.html">🎁 7일 질문카드</a><a class="btn btn-lg" href="/parent-resources.html">부모 자료실 →</a></div></div>
<div class="cta-band" style="margin-top:12px;background:linear-gradient(135deg,#FFF3E9,#FCE7D6)"><div><h3>🏫 오늘부터 매일 10분 · 매일 AI교실</h3><p>세계 사례를 한국 가정용 1년 커리큘럼으로. 오늘의 수업·연령별 로드맵.</p></div><a class="btn btn-lg" href="/daily-class.html">매일 AI교실 →</a></div>
<div class="cta-band" style="margin-top:12px;background:linear-gradient(135deg,#EAF2FB,#DCEAF8)"><div><h3>🏆 실력으로 이어질까? · AI 경진대회 문제풀이 교실</h3><p>실제 AI 경진대회 문제를 아이 눈높이로. 학년별 문제·풀이전략·우리집 연습문제.</p></div><a class="btn btn-lg" href="/competitions.html">경진대회 교실 →</a></div>
</div></section></main>"""
    return page("start","","집에서 시작하는 6단계 가이드 | AI 조기교육","아이와 AI를 시작하는 6단계. 부모 멘트·질문·좋은/나쁜 프롬프트 예시까지.",body)

def parent_resources():
    return page("res","","부모 자료실 · 세계 사례를 부모의 오늘 행동으로 | AI 조기교육",
        "국가 정책 분석이 아니라, 세계 사례를 한국 가정의 오늘 행동으로 바꾸는 부모 코칭 자료실.",PC.hub_body())

def free_kit():
    """(이동 안내) 부모용 인쇄 자료는 부모 자료실로 통합. 외부 유입 보호를 위해 URL 유지, 삭제 금지."""
    body = f"""<main><div class="wrap" style="max-width:720px;text-align:center">
<section class="page-hero" style="padding:46px 0 10px">
<div class="pill">안내</div>
<h1 style="font-size:26px">아이와 AI교실 무료 자료는<br><span class="coral">부모 자료실</span>로 이동했습니다</h1>
<p style="margin-top:10px;color:var(--navy2);font-weight:600">질문카드, 7일 카드, 매일 활동지처럼 아이와 함께 쓰는 자료는<br>부모 자료실과 매일 AI교실에서 확인할 수 있습니다.</p></section>
<section class="block" style="padding:10px 0 40px">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:560px;margin:0 auto">
<a class="btn btn-lg btn-primary" href="/parent-resources.html">부모 자료실 보기 →</a>
<a class="btn btn-lg" href="/free/ai-first-7days.html">🎁 7일 질문카드 보기</a>
<a class="btn btn-lg" href="/free/daily-sheet.html">🖨 매일 활동지 보기</a>
<a class="btn btn-lg" href="/daily-class/today.html">▶ 오늘의 10분 수업 보기</a>
</div>
<p style="margin-top:22px;font-size:13px;color:var(--muted)">콘텐츠 제작용 무료·로컬 도구를 찾으셨다면 → <a href="/free-programs.html" style="color:var(--coral);font-weight:700">무료 프로그램</a></p>
</section></div></main>"""
    return page("res","","무료 자료 안내 · 부모 자료실로 이동 | 아이와 AI교실",
        "아이와 함께 쓰는 질문카드·7일 카드·매일 활동지는 부모 자료실과 매일 AI교실에서 제공합니다.",body)

# ---------- 무료 자료 하위 페이지 공통 레이아웃 ----------
FREE_ITEMS=[("부모 자료실 홈","/parent-resources.html"),
 ("🎁 7일 질문카드 (무료 코스)","/free/ai-first-7days.html"),
 ("매일 활동지","/free/daily-sheet.html"),
 ("12주 워크북 PDF","/free/uk-12weeks-workbook.html"),
 ("AI 대화 연습지","/free/worksheet.html"),
 ("부모용 질문 카드 10장","/free/question-cards.html"),
 ("첫 프롬프트 20개","/free/first-prompts.html")]
def free_sidebar(cur):
    links=""
    for lb,u in FREE_ITEMS:
        if u is None: links+=f'<span class="fs-a fs-x">{lb} <small>준비중</small></span>'
        else: links+=f'<a class="fs-a{" on" if u==cur else ""}" href="{u}">{lb}</a>'
    return f"""<aside class="frsb no-print"><div class="fs-t" onclick="this.parentElement.classList.toggle('fold')">🖨 부모 인쇄 자료 <span class="fs-ar">▾</span></div><nav class="fs-nav">{links}</nav></aside>"""
def free_resource_layout(cur,title,doc_style,doc_body):
    """무료 자료 하위 페이지 = 사이트 헤더 + 좌측 무료자료 카테고리 + 보조바(←자료실·제목·인쇄) + 본문."""
    body=f"""<div class="fr2">
{free_sidebar(cur)}
<main class="fr-main">
<div class="fr-aux no-print"><a href="/parent-resources.html">← 부모 자료실</a><b>{title}</b><button class="btn btn-primary" onclick="window.print()">🖨 인쇄 / PDF 저장</button></div>
<div class="fr-doc">{doc_body}</div>
</main></div>
<style>
{doc_style}
.fr2{{max-width:1200px;margin:0 auto;padding:16px 16px 40px;display:flex;gap:22px;align-items:flex-start}}
.fr-main{{flex:1;min-width:0;max-width:900px}}
.frsb{{width:236px;flex:none;background:#FFF9EF;border:1px solid #EAD9BE;border-radius:14px;padding:12px 9px;position:sticky;top:100px}}
.fs-t{{font-weight:800;font-size:14px;color:#2B3A55;padding:4px 11px 9px;border-bottom:2px solid #F0E6D2;margin-bottom:6px;display:flex;justify-content:space-between}}
.fs-ar{{display:none;color:#c4b59a}}
.fs-a{{display:block;padding:7px 11px;margin:1px 0;border-radius:8px;text-decoration:none;color:#5a4a35;font-size:13.2px;font-weight:600}}
a.fs-a:hover{{background:#FDECE5;color:#B44A31}}
.fs-a.on{{background:var(--coral,#E0684A);color:#fff}}
.fs-x{{color:#c4b59a;cursor:default}}.fs-x small{{font-size:10px;background:#F0E6D2;border-radius:6px;padding:1px 6px}}
.fr-aux{{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid #EADFCE;border-radius:12px;padding:10px 14px;margin-bottom:14px}}
.fr-aux a{{color:var(--coral,#E0684A);font-weight:800;text-decoration:none;font-size:13px}}
.fr-aux b{{margin:0 auto;font-size:14px;color:#2B3A55}}
.fr-doc .sheet{{padding:0;max-width:none}}
@media(max-width:900px){{.fr2{{flex-direction:column}}.frsb{{position:static;width:100%}}.fs-ar{{display:inline}}.frsb.fold .fs-nav{{display:none}}.fs-t{{cursor:pointer}}}}
@media print{{header.mgh,footer.site,.frsb,.fr-aux,.no-print{{display:none!important}}.fr2{{padding:0;display:block}}.fr-main{{max-width:none}}}}
</style>
<script>if(window.innerWidth<=900){{var f=document.querySelector('.frsb');if(f)f.classList.add('fold');}}</script>"""
    return page("res","../",f"{title} | AI 조기교육",f"{title} — 부모 인쇄 자료. 이메일 없이 바로 인쇄·저장.",body)


# ---------- 무료 프로그램 (콘텐츠 제작 도구 창고) ----------
FREE_PROGRAMS_SECTIONS = [
 ("voice","🎤","음성 만들기","무료 TTS 도구"),
 ("video","🎬","영상 만들기","쇼츠 영상 제작 도구"),
 ("image","🖼","이미지 만들기","로컬 이미지 생성 도구"),
 ("subtitle","💬","자막·오디오 편집","오디오·자막 편집 도구"),
 ("localai","💻","로컬 AI 실행","로컬 AI 실행 도구"),
 ("dev","🛠","개발 도구","기반 개발 도구"),
]
FREE_PROGRAMS = [
 dict(sec="voice", icon="🎤", name="edge-tts", category="무료 TTS",
   short="글을 자연스러운 음성으로 바꾸는 Python TTS 도구.",
   use="유튜브 쇼츠 대본 음성(내레이션) 만들기 — 우리 쇼츠 빌더의 목소리 담당.",
   who="쇼츠 제작자, 부모 안내 음성 제작", diff="중급", run="Python / 온라인 TTS 서비스 활용",
   official="https://github.com/rany2/edge-tts", download="https://github.com/rany2/edge-tts",
   caution="Microsoft Edge 온라인 TTS 서비스를 활용하므로 완전 오프라인 도구는 아닙니다. 사용 조건을 확인하세요.",
   internal=("쇼츠 제작 흐름 보기","/videos.html")),
 dict(sec="voice", icon="🗣", name="Piper TTS", category="로컬 TTS",
   short="로컬에서 실행 가능한 신경망 TTS 엔진.",
   use="인터넷 의존도를 줄인 음성 제작 실험.",
   who="로컬 실행을 선호하는 제작자", diff="중급", run="로컬 / Python",
   official="https://github.com/OHF-voice/piper1-gpl", download="https://github.com/OHF-voice/piper1-gpl",
   caution="음성 모델과 언어(한국어) 지원 범위를 먼저 확인하세요.",
   internal=("음성이 쓰인 수업 보기","/daily-class/today.html")),
 dict(sec="video", icon="🎞", name="FFmpeg", category="영상/오디오 조립",
   short="영상·음성·자막을 합치고 변환하는 필수 도구.",
   use="쇼츠 mp4 조립, 오디오 합성, 자막 번인 — 우리 영상 조립의 심장.",
   who="영상 자동화를 하려는 모든 제작자", diff="중급", run="로컬 / 명령줄(Windows·Mac·Linux)",
   official="https://www.ffmpeg.org/download.html", download="https://www.gyan.dev/ffmpeg/builds/",
   caution="공식 FFmpeg는 소스 중심입니다. Windows 실행 파일은 별도 빌드 페이지(gyan.dev 등)를 확인하세요.",
   internal=("조립된 쇼츠 예시","/videos.html")),
 dict(sec="video", icon="✂️", name="CapCut", category="영상 편집",
   short="쇼츠/릴스 편집에 널리 쓰이는 영상 편집 도구.",
   use="최종 컷 편집, 자막 보정, 효과 추가.",
   who="마우스로 편집하고 싶은 제작자", diff="초급", run="Windows/Mac/모바일 앱",
   official="https://www.capcut.com/", download="https://www.capcut.com/",
   caution="무료 기능과 유료 기능 구분이 필요합니다. 계정·약관을 확인하세요.",
   internal=("영상관 보기","/videos.html")),
 dict(sec="video", icon="🖥", name="OBS Studio", category="화면 녹화",
   short="무료 오픈소스 화면 녹화·방송 도구.",
   use="AI 사용 과정 녹화, 튜토리얼 제작.",
   who="과정을 영상으로 남기고 싶은 부모·제작자", diff="초급", run="로컬 / Windows·Mac·Linux",
   official="https://obsproject.com/", download="https://obsproject.com/download",
   caution="녹화 해상도와 소리(마이크/시스템) 설정을 먼저 확인하세요.",
   internal=("아이와 실습 아이디어","/free/first-prompts.html")),
 dict(sec="image", icon="🎨", name="ComfyUI", category="로컬 이미지 생성",
   short="로컬에서 이미지 생성 워크플로를 구성하는 도구.",
   use="쇼츠 컷 일러스트, 캐릭터 장면 생성 — 우리 쇼츠 그림 담당.",
   who="GPU가 있는 고급 사용자", diff="고급", run="로컬 / Python + GPU",
   official="https://github.com/comfyanonymous/ComfyUI", download="https://github.com/comfyanonymous/ComfyUI",
   caution="GPU·모델·워크플로 설정이 필요합니다. 초보자에게는 어려울 수 있습니다.",
   internal=("생성 일러스트가 쓰인 연재","/world-cases.html")),
 dict(sec="subtitle", icon="🎚", name="Audacity", category="오디오 편집",
   short="무료 오픈소스 오디오 녹음·편집 프로그램.",
   use="TTS 음성 확인, 잡음 제거, 볼륨 조정.",
   who="음성 품질을 다듬고 싶은 제작자", diff="초급", run="로컬 / Windows·Mac·Linux",
   official="https://www.audacityteam.org/download/", download="https://www.audacityteam.org/download/",
   caution="설치 파일은 공식 사이트에서 받으세요.",
   internal=("음성이 들어간 수업","/daily-class/today.html")),
 dict(sec="subtitle", icon="💬", name="Subtitle Edit", category="자막 편집",
   short="자막 생성·수정·싱크 조정 도구.",
   use="쇼츠 자막 정리, 긴 영상 자막 편집.",
   who="자막을 손보는 제작자", diff="중급", run="로컬 / Windows",
   official="https://www.nikse.dk/subtitleedit", download="https://github.com/SubtitleEdit/subtitleedit/releases",
   caution="자동 생성 자막은 반드시 사람이 검수하세요.",
   internal=("자막이 쓰인 영상","/videos.html")),
 dict(sec="subtitle", icon="🎙", name="Whisper", category="음성→자막(STT)",
   short="음성을 글로 바꾸는 오픈소스 음성 인식 모델.",
   use="영상 속 말소리를 자막 초안으로 변환.",
   who="자막 초안을 자동으로 만들고 싶은 제작자", diff="고급", run="로컬 / Python + (권장) GPU",
   official="https://github.com/openai/whisper", download="https://github.com/openai/whisper",
   caution="자동 변환 결과는 오탈자가 있으므로 반드시 사람이 검수하세요.",
   internal=("자막 정리 후 영상관으로","/videos.html")),
 dict(sec="localai", icon="🦙", name="Ollama", category="로컬 LLM 실행",
   short="로컬 PC에서 대화형 AI 모델을 실행하는 도구.",
   use="대본 초안·아이디어 생성 실험(외부 전송 없이 로컬에서).",
   who="로컬에서 AI를 실험하고 싶은 사용자", diff="중급", run="로컬 / Windows·Mac·Linux",
   official="https://ollama.com/", download="https://ollama.com/download",
   caution="모델 크기에 따라 메모리(RAM/VRAM)가 많이 필요합니다.",
   internal=("AI 답 의심 연습(수업)","/daily-class/today.html")),
 dict(sec="dev", icon="🌿", name="Git", category="버전 관리",
   short="파일 변경 기록을 남기고 되돌릴 수 있는 버전 관리 도구.",
   use="사이트·대본·금고 JSON의 변경 이력 관리, 실수해도 되돌리기 — 우리 사이트 배포의 기반.",
   who="콘텐츠·코드를 안전하게 쌓고 싶은 제작자", diff="중급", run="로컬 / 명령줄(Windows·Mac·Linux)",
   official="https://git-scm.com/", download="https://git-scm.com/downloads",
   caution="처음엔 add·commit·push 세 가지만 익혀도 충분합니다. 비밀키·개인정보 파일은 커밋하지 마세요(.gitignore).",
   internal=("우리 제작 흐름 보기","/videos.html")),
 dict(sec="dev", icon="📝", name="Visual Studio Code", category="코드 편집기",
   short="무료 코드 편집기 — 스크립트 수정·실행·폴더 관리를 한 화면에서.",
   use="TTS·조립 스크립트 열어보고 고치기, JSON(금고·플랜) 편집.",
   who="자동화 스크립트를 직접 만지고 싶은 제작자", diff="초급", run="로컬 / Windows·Mac·Linux",
   official="https://code.visualstudio.com/", download="https://code.visualstudio.com/download",
   caution="확장(Extension)은 필요한 것만 설치하세요. Python 확장을 함께 쓰면 편합니다.",
   internal=("경진대회 문제로 연습","/competitions.html")),
 dict(sec="dev", icon="🐍", name="Python", category="기반 도구",
   short="위 도구들(edge-tts·Whisper 등)을 실행하는 기반 언어.",
   use="TTS·자막·조립 스크립트 실행 환경.",
   who="자동화를 시작하려는 제작자", diff="중급", run="로컬 / Windows·Mac·Linux",
   official="https://www.python.org/downloads/", download="https://www.python.org/downloads/",
   caution="설치 시 'Add to PATH' 옵션을 확인하세요.",
   internal=("경진대회 문제로 연습","/competitions.html")),
]

def free_programs():
    sec_cards = {}
    for p in FREE_PROGRAMS:
        sec_cards.setdefault(p["sec"], []).append(p)
    def card(p):
        return f"""<div class="fp-card">
<div class="fp-ico">{p['icon']}<span>{p['category']}</span></div>
<div class="fp-body">
<h3>{p['name']}</h3>
<p class="fp-short">{p['short']}</p>
<div class="fp-row"><b>우리가 쓰는 용도</b>{p['use']}</div>
<div class="fp-row"><b>추천 대상</b>{p['who']}</div>
<div class="fp-row"><b>난이도</b><span class="fp-diff">{p['diff']}</span> · <b style="margin-left:6px">실행</b>{p['run']}</div>
<div class="fp-caut">⚠ {p['caution']}</div>
<div class="fp-links">
<a class="btn btn-primary" href="{p['official']}" target="_blank" rel="noopener">공식 사이트 ↗</a>
<a class="btn" href="{p['download']}" target="_blank" rel="noopener">다운로드·GitHub ↗</a>
<a class="fp-int" href="{p['internal'][1]}">{p['internal'][0]} →</a>
</div></div></div>"""
    secs = ""
    for sid, emo, name, h2 in FREE_PROGRAMS_SECTIONS:
        cards = "".join(card(p) for p in sec_cards.get(sid, []))
        secs += f"""<h2 id="{sid}" class="fp-sec" style="scroll-margin-top:90px">{emo} {h2}</h2>{cards}"""
    body = f"""<main><div class="wrap" style="max-width:880px">
<section class="page-hero" style="padding:36px 0 14px"><div class="pill">🧰 제작 도구 창고</div>
<h1>무료 AI 프로그램 모음</h1>
<p style="color:var(--navy2);font-weight:600">아이와 AI교실이 실제 제작에 쓰는 무료·로컬 AI 도구 모음</p></section>
<section class="block" style="padding:6px 0"><div class="callout">
이 페이지는 아이와 AI교실 콘텐츠 제작에 쓰는 <b>무료 또는 로컬 실행 도구</b>를 정리한 곳입니다.
단순 링크 모음이 아니라, 각 프로그램을 <b>어디에 쓰는지, 어떤 사람이 쓰면 좋은지, 공식 링크는 어디인지</b> 함께 안내합니다.
설치 전에는 각 프로그램의 공식 안내와 라이선스를 반드시 확인하세요.</div>
<p style="font-size:12.5px;color:var(--muted);margin-top:8px">👨‍👩‍👧 아이와 함께 쓰는 질문카드·활동지는 <a href="/parent-resources.html" style="color:var(--coral);font-weight:700">부모 자료실</a>에 있습니다. 이 방은 '만드는 사람'용 도구방입니다. &nbsp;💾 우리가 직접 개발한 도구는 <a href="/paid-programs.html" style="color:var(--coral);font-weight:700">유료 프로그램(모두 9,900원)</a>에.</p>
{secs}
<div class="callout" style="margin-top:26px;background:#F4F7FB;border-color:#CADCF0;font-size:13px">
이 페이지의 도구들은 아이와 AI교실이 콘텐츠 제작과 교육 실습을 위해 참고하는 무료 또는 로컬 실행 도구입니다.
각 도구의 무료 범위, 라이선스, 설치 방법, 사용 조건은 시간이 지나며 바뀔 수 있습니다.
다운로드 전 반드시 공식 사이트의 최신 안내를 확인하세요.
<b>아이 개인정보, 얼굴, 음성, 학교 정보 등을 외부 서비스에 입력하지 않도록 주의하세요.</b></div>
</section></div>
<style>
.fp-sec{{font-size:19px;font-weight:900;color:#2B3A55;margin:28px 0 12px}}
.fp-card{{display:flex;gap:16px;background:#fff;border:1px solid #EADFCE;border-radius:15px;padding:16px 18px;margin-bottom:12px}}
.fp-ico{{width:86px;flex:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;background:linear-gradient(160deg,#FFF7EA,#FBEBD3);border:1px solid #EAD9BE;border-radius:13px;font-size:34px;padding:12px 6px}}
.fp-ico span{{font-size:10.5px;font-weight:800;color:#8a5b1e;text-align:center;line-height:1.3}}
.fp-body{{flex:1;min-width:0}}
.fp-body h3{{margin:0 0 4px;font-size:17px;color:#2B3A55}}
.fp-short{{margin:0 0 8px;font-size:14px;color:#3a3024}}
.fp-row{{font-size:13px;margin:3px 0;color:#4a3a28}}
.fp-row b{{color:#8a6f45;font-size:12px;margin-right:7px}}
.fp-diff{{background:#EAF2FB;color:#2B4a72;border-radius:6px;padding:1px 8px;font-weight:700;font-size:12px}}
.fp-caut{{font-size:12.5px;color:#8a5b1e;background:#FFF7EA;border:1px solid #EAD9BE;border-radius:8px;padding:7px 11px;margin:8px 0}}
.fp-links{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px}}
.fp-links .btn{{padding:7px 14px;font-size:12.5px}}
.fp-int{{font-size:12.5px;font-weight:700;color:#5a4a35;text-decoration:none}}
.fp-int:hover{{color:var(--coral)}}
@media(max-width:560px){{.fp-card{{flex-direction:column}}.fp-ico{{width:100%;flex-direction:row;justify-content:flex-start;padding:8px 12px;font-size:26px}}}}
</style></main>"""
    return page("free","","무료 AI 프로그램 모음 | 아이와 AI교실",
        "아이와 AI교실이 실제 콘텐츠 제작에 활용하는 무료·로컬 AI 도구를 소개합니다. TTS, 영상 편집, 자막, 오디오 편집, 로컬 이미지 생성 도구를 용도별로 정리했습니다.", body)



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
    for c in COUNTRIES:
        write(f"parents/{c[0]}.html",page("res","../",
            f"{c[1]} 부모 코칭 · 우리 집에서 | AI 조기교육",
            f"{c[1]} AI교육 사례로 우리 집에서 오늘 할 부모 행동·연령별 팁·FAQ. 정책 분석 아님.",
            PC.country_body(c[0])))
    write("free-kit.html",free_kit())
    write("free-programs.html",free_programs())
    import build_paid; build_paid.build()
    import build_kids_show as KIDS
    KIDS.build_all()
    import build_competitions as COMP
    COMP.build_all()
    import build_academy as ACAD
    ACAD.build_all()
    import build_daily_class as DAILY
    DAILY.build_all()
    import build_levels as LVL
    LVL.build_all()
    import build_content_bank as BANK
    BANK.build_all()
    import free_docs as FD
    for _slug,_d in FD.DOCS.items():
        write(f"free/{_slug}.html",free_resource_layout(f"/free/{_slug}.html",_d["title"],_d["style"],_d["body"]))
    print("완료.")
