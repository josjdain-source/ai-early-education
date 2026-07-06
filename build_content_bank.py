#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""콘텐츠 금고(Content Bank) — 토큰 많은 날 대량 제작 → 냉동 보관 → 토큰 적은 날 꺼내 발행.
데이터: content_bank/*.json (진실원본). 화면은 읽기+복사 전용, 상태 변경은 JSON 수정→재빌드(자동 발행 없음).
Source Vault(조종판)=원본 기억 / Content Bank=제작·발행 상태 관리로 역할 분리."""
import os, json, html, build_site as BS
ROOT = os.path.dirname(os.path.abspath(__file__))
CB = os.path.join(ROOT, "content_bank")
def J(f): return json.load(open(os.path.join(CB, f), encoding="utf-8"))
SER = J("series_bank.json"); ITEMS = J("content_items.json")["items"]; SRC = J("source_items.json")["sources"]
try: PL = J("pattern_lab.json")
except Exception: PL = None
PKG_DIR = os.path.join(CB, "approved", "shorts")
PKGS = {}
if os.path.isdir(PKG_DIR):
    for fn in os.listdir(PKG_DIR):
        if fn.endswith(".json"):
            p = json.load(open(os.path.join(PKG_DIR, fn), encoding="utf-8"))
            PKGS[p["id"]] = p
SMAP = {s["series_id"]: s for s in SER["series"]}
STATUS_KO = {"idea":"💡 아이디어","source_ready":"📚 자료됨","draft_ready":"📝 초안됨","asset_ready":"🎨 소재됨",
             "approved":"✅ 승인","scheduled":"📌 예약","published":"🚀 발행","measured":"📈 성과기록"}
ORDER = ["idea","source_ready","draft_ready","asset_ready","approved","scheduled","published","measured"]

def esc(x): return html.escape(str(x or ""))
def full_desc(it):
    d = it.get("description","")
    tags = " ".join("#"+t for t in it.get("hashtags",[]))
    return (d + ("\n\n"+tags if tags else "")).strip()

def item_card(it, show_copy=True):
    s = SMAP.get(it["series"],{}).get("title", it["series"])
    st = STATUS_KO.get(it["status"], it["status"])
    pr = ' <span class="cb-pr">HIGH</span>' if it.get("priority")=="high" else ''
    btns = ""
    if show_copy:
        btns = f"""<div class="cb-btns">
<button onclick='cbCopy({json.dumps(it["title"],ensure_ascii=False)},this)'>제목 복사</button>
<button onclick='cbCopy({json.dumps(full_desc(it),ensure_ascii=False)},this)'>설명+태그 복사</button>
<button onclick='cbCopy({json.dumps(it.get("script",""),ensure_ascii=False)},this)'>대본 복사</button></div>"""
    yt = f'<a href="{esc(it["youtube_url"])}" target="_blank" rel="noopener" style="color:#3A6FB0;font-weight:700;font-size:12px">▶ 발행 링크</a>' if it.get("youtube_url") else ""
    pkg_html = package_block(PKGS[it["id"]]) if show_copy and it["id"] in PKGS else ""
    return f"""<div class="cb-item">
<div class="cb-meta"><span class="cb-tag">{esc(s)}</span><span class="cb-st">{st}</span>{pr}{'<span class="cb-pkg">🎬 제작 패키지</span>' if it["id"] in PKGS else ''}<span class="cb-ord">#{it.get('publish_order','-')}</span></div>
<b>{esc(it['title'])}</b>
{f'<p class="cb-hook">🪝 {esc(it["hook"])}</p>' if it.get('hook') else ''}
{btns}{yt}{pkg_html}
</div>"""

def package_block(p):
    cuts_rows = "".join(f"""<tr><td style="white-space:nowrap"><b>컷{c['n']}</b><br><span style="color:#9b8a6e">{c['t']}s</span></td>
<td>{esc(c['scene'])}</td><td style="font-weight:700">{esc(c['subtitle'])}</td></tr>""" for c in p["cuts"])
    st = p["image_style"]
    NL = chr(10)
    prompts_all = (NL+NL).join(
        f"[컷{c['n']} {c['t']}s] {c['image_prompt']}, {st['style_token']}{NL}NEG: {st['negative']}"
        for c in p["cuts"])
    return f"""<details class="cb-pkgbox"><summary>🎬 제작 패키지 열기 — 대본 {p['duration_target_sec']}초 · 컷 6 · 자막 · 프롬프트 · 고정댓글</summary>
<div class="cb-pkgin">
<div style="font-size:12px;color:#8a6f45;margin:8px 0 4px">📜 대본 ({p['duration_target_sec']}초 목표)</div>
<div class="cb-script">{esc(p['script'])}</div>
<div style="font-size:12px;color:#8a6f45;margin:10px 0 4px">🎞 화면 컷 6개 + 자막</div>
<table class="cb-t" style="font-size:12px"><thead><tr><th>컷</th><th>화면</th><th>자막</th></tr></thead><tbody>{cuts_rows}</tbody></table>
<div style="font-size:11.5px;color:#9b8a6e;margin-top:6px">🎨 {esc(st['engine'])} · {esc(st['aspect'])} · 스타일 토큰은 프롬프트 복사에 포함</div>
<div style="font-size:12px;color:#8a6f45;margin:10px 0 4px">📌 고정댓글</div>
<div class="cb-script" style="background:#EEF7EF;border-color:#cfe6d6">{esc(p['pinned_comment'])}</div>
<div class="cb-btns" style="margin-top:10px">
<button onclick='cbCopy({json.dumps(p["script"],ensure_ascii=False)},this)'>📜 대본 복사</button>
<button onclick='cbCopy({json.dumps(p["subtitles_all"],ensure_ascii=False)},this)'>💬 자막 전체 복사</button>
<button onclick='cbCopy({json.dumps(prompts_all,ensure_ascii=False)},this)'>🎨 이미지 프롬프트 6컷 복사</button>
<button onclick='cbCopy({json.dumps(p["pinned_comment"],ensure_ascii=False)},this)'>📌 고정댓글 복사</button>
</div>
<div style="margin-top:10px;font-size:11.5px;color:#8a6f45">🎬 렌더(로컬, Ollama 언로드+ComfyUI 필요):</div>
<div class="cb-script" style="font-family:monospace;font-size:12px;padding:8px 11px">python production/build_ai_edu_shorts.py {esc(p['id'])}</div>
<div class="cb-btns" style="margin-top:6px"><button onclick='cbCopy({json.dumps("cd C:/Users/admin/Desktop/ai-craft-kids && python production/build_ai_edu_shorts.py "+p["id"],ensure_ascii=False)},this)'>▶ 렌더 명령 복사</button></div>
</div></details>"""

def pattern_lab_section():
    if not PL: return ""
    S = PL["viral_test_score_formula"]
    plus = "".join(f'<span class="pl-lever pl-plus">+ {k}</span>' for k in S["plus"])
    minus = "".join(f'<span class="pl-lever pl-minus">− {k}</span>' for k in S["minus"])
    # 영상 역추적 카드(Viral Test Score 순)
    def tier(t): return ("S","#2E9E63") if t>=9 else (("B","#C98A2E") if t>=6 else ("D","#C0473A"))
    vids=""
    for v in PL["videos"]:
        sc=v["viral_test_score"]; tl,col=tier(sc["total"])
        bars=(f'<b>Stop</b> {sc["stop_power"]} · <b>Pain</b> {sc["personal_pain"]} · '
              f'<b>Curio</b> {sc["curiosity_gap"]} · <b>Watch</b> {sc["watch_completion"]} · <b>Take</b> {sc["clear_takeaway"]}')
        mods=[]
        if sc["boring_policy"]: mods.append(f'−Policy {sc["boring_policy"]}')
        if sc["abstract_talk"]: mods.append(f'−Abstract {sc["abstract_talk"]}')
        if sc["clickbait_mismatch"]: mods.append(f'−Mismatch {sc["clickbait_mismatch"]}')
        mtxt=(" · <span style='color:#C0473A'>"+" · ".join(mods)+"</span>") if mods else ""
        vids+=f"""<div class="pl-vid" style="border-left:5px solid {col}">
<div class="pl-vhead"><span class="pl-tier" style="background:{col}">{tl} · {sc['total']}</span> <b>{esc(v['title'])}</b> <span class="pl-type">{esc(v['pattern_type'])}</span></div>
<div class="pl-bars">{bars}{mtxt}</div>
<div class="pl-guess">🔎 {esc(v['algorithm_guess']['likely_reason'])}</div></div>"""
    priors="".join(f'<span class="pl-prior pl-t{p["tier"]}"><b>{p["tier"]}</b> {esc(p["pattern"])} — {esc(p["verdict"])}</span>' for p in PL["priors"])
    levers="".join(f'<span class="pl-lever pl-key">{esc(x)}</span>' for x in PL["next_title_levers"])
    q="".join(f"<li>{esc(x)}</li>" for x in PL["core_questions"])
    return f"""<h2 class="cb-sec">🔬 YouTube Pattern Lab <span class="cb-hint">우리 채널 데이터 역추적 · 공식 알고리즘 주장 아님</span></h2>
<div class="pl-manifesto">{esc(PL['_manifesto'])}</div>
<div class="pl-stance">공식 원칙 <b>= 참고자료</b> &nbsp;·&nbsp; 우리 데이터 <b>= 판단 기준</b> &nbsp;·&nbsp; 반복 실험 <b>= 알고리즘 추정</b></div>
<div class="pl-note">⚠ {esc(PL['data_status'])}</div>
<h3 class="pl-h3">Viral Test Score <span class="cb-hint">{esc(PL['viral_test_score_formula']['formula'])}</span></h3>
<div class="pl-levers">{plus}{minus}</div>
<div style="margin:10px 0">{vids}</div>
<h3 class="pl-h3">초기 결론 (Priors) <span class="cb-hint">데이터로 검증·갱신</span></h3>
<div class="pl-priors">{priors}</div>
<h3 class="pl-h3">다음 제목 3레버 <span class="cb-hint">Stop Power · Personal Pain · Clear Takeaway</span></h3>
<div class="pl-levers">{levers}</div>
<details style="margin-top:10px"><summary style="cursor:pointer;font-weight:700;color:#5a4a35">🧭 Pattern Lab 6대 질문 펼치기</summary>
<ol class="pl-q">{q}</ol></details>
"""

def page():
    # 집계
    agg = {}
    for it in ITEMS:
        a = agg.setdefault(it["series"], {k:0 for k in ORDER})
        a[it["status"]] = a.get(it["status"],0)+1
    # ① 오늘 꺼낼 것: approved/scheduled 중 publish_order 최소
    ready = sorted([i for i in ITEMS if i["status"] in ("approved","scheduled")], key=lambda x: x.get("publish_order",999))
    today = item_card(ready[0]) if ready else '<p class="cb-empty">승인된 콘텐츠가 없습니다 — 제작일에 채우세요.</p>'
    # ② 시리즈 재고판
    rows = ""
    for s in SER["series"]:
        a = agg.get(s["series_id"], {k:0 for k in ORDER})
        created = sum(a[k] for k in ORDER if k not in ("idea",))
        low = ' style="background:#FDECEC"' if a["approved"]+a["scheduled"]==0 else ''
        hi = ' <span class="cb-pr">HIGH</span>' if s.get("priority")=="high" else ''
        rows += f"""<tr{low}><td><b>{esc(s['title'])}</b>{hi}</td><td>{s['items_planned']}</td><td>{created}</td>
<td>{a['approved']+a['scheduled']}</td><td>{a['published']+a['measured']}</td>
<td style="font-size:12px;color:#5a4a35">{esc(s['next_batch'])}</td></tr>"""
    # ③ 토큰 여유날 만들 것 (priority high 우선)
    make = "".join(f'<li><b>{esc(s["title"])}</b> — {esc(s["next_batch"])}</li>'
        for s in sorted(SER["series"], key=lambda x: 0 if x.get("priority")=="high" else 1)[:4])
    # ④ 발행 대기실
    waiting = "".join(item_card(i) for i in ready) or '<p class="cb-empty">비어 있음</p>'
    # 준비중(초안~소재)
    making = "".join(item_card(i, show_copy=False) for i in sorted(
        [i for i in ITEMS if i["status"] in ("draft_ready","asset_ready")], key=lambda x: x.get("publish_order",999)))
    ideas_n = sum(1 for i in ITEMS if i["status"]=="idea")
    # ⑤ 발행 기록
    pub = "".join(f"""<div class="cb-item"><div class="cb-meta"><span class="cb-tag">{esc(SMAP.get(i['series'],{}).get('title',''))}</span>
<span class="cb-st">🚀 {esc(i.get('published_at',''))}</span></div><b>{esc(i['title'])}</b>
{f'<a href="{esc(i["youtube_url"])}" target="_blank" rel="noopener" style="color:#3A6FB0;font-weight:700;font-size:12px">▶ {esc(i["youtube_url"])}</a>' if i.get('youtube_url') else '<span style="font-size:12px;color:var(--muted)">사이트 자료</span>'}
<span style="font-size:12px;color:var(--muted)"> · 조회 {i['performance'].get('views') if i['performance'].get('views') is not None else '미기록'}</span></div>"""
        for i in ITEMS if i["status"] in ("published","measured")) or '<p class="cb-empty">아직 없음</p>'
    # ⑥ 자료 창고
    srcs = "".join(f"""<div class="cb-item"><div class="cb-meta"><span class="cb-tag">{esc(SMAP.get(x['series'],{}).get('title',x['series']))}</span>
<span class="cb-st">{'📦 보관' if x['status']=='stored' else '✅ 사용됨'}</span></div>
<b>{esc(x['title'])}</b><p style="font-size:13px;margin:4px 0">{esc(x['summary'])}</p>
<div style="font-size:11.5px;color:#8a6f45">쓸 곳: {' · '.join(x['usable_for'])}</div>
{f'<a href="{esc(x["source_url"])}" target="_blank" rel="noopener" style="font-size:11.5px;color:#3A6FB0">📎 출처</a>' if x.get('source_url') else ''}</div>""" for x in SRC)
    # 발행 캘린더
    cal = "".join(f'<span class="cb-cal"><b>{d}</b> {esc(SMAP.get(sid,{}).get("title",sid))}</span>' for d,sid in SER["publish_calendar"].items())

    body = f"""<main><div class="wrap" style="max-width:1000px">
<section class="page-hero" style="padding:30px 0 14px"><div class="pill">🧊 운영자 전용</div>
<h1 style="font-size:28px">콘텐츠 금고</h1>
<p>토큰 많은 날 만들어 얼리고, 적은 날 꺼내 올립니다. <b>기억은 금고가, 사람은 방향만.</b></p>
<p style="font-size:12px;color:#9b8a6e">상태 변경·성과 입력 = content_bank/*.json 수정 → 재빌드. 자동 발행 없음.</p></section>

<h2 class="cb-sec">① 오늘 꺼낼 것 <span class="cb-hint">approved 중 순서 1번</span></h2>
{today}

<h2 class="cb-sec">② 시리즈별 재고판 <span class="cb-hint">빨간 줄 = 승인 재고 0(보충 필요)</span></h2>
<table class="cb-t"><thead><tr><th>시리즈</th><th>계획</th><th>제작</th><th>승인대기</th><th>발행</th><th>다음 배치</th></tr></thead>
<tbody>{rows}</tbody></table>

<h2 class="cb-sec">③ 토큰 여유날 만들 것 <span class="cb-hint">HIGH 우선</span></h2>
<ol class="cb-make">{make}</ol>

<h2 class="cb-sec">④ 발행 대기실 <span class="cb-hint">approved만 · 복사해서 업로드</span></h2>
{waiting}
<details style="margin-top:10px"><summary style="cursor:pointer;font-weight:700;color:#5a4a35">🧊 냉동 중(초안·소재 {len([i for i in ITEMS if i['status'] in ('draft_ready','asset_ready')])}개 · 아이디어 {ideas_n}개) 펼치기</summary>
<div style="margin-top:8px">{making}</div></details>

<h2 class="cb-sec">⑤ 발행 기록</h2>
{pub}

{pattern_lab_section()}

<h2 class="cb-sec">⑥ 자료 창고 <span class="cb-hint">출처·요약·사용처만(본문 복제 금지)</span></h2>
{srcs}

<h2 class="cb-sec">📅 발행 캘린더</h2>
<div style="display:flex;gap:7px;flex-wrap:wrap">{cal}</div>
</div>
<style>
.cb-sec{{font-size:18px;font-weight:900;color:#2B3A55;margin:26px 0 10px}}
.cb-hint{{font-size:12px;color:#9b8a6e;font-weight:600}}
.cb-item{{background:#fff;border:1px solid #EADFCE;border-radius:12px;padding:13px 16px;margin-bottom:9px}}
.cb-meta{{display:flex;gap:7px;align-items:center;margin-bottom:5px;flex-wrap:wrap}}
.cb-tag{{font-size:11px;font-weight:800;background:#EAF2FB;color:#2B4a72;border-radius:6px;padding:2px 8px}}
.cb-st{{font-size:11px;font-weight:800;background:#F0E6D2;color:#7a5b2e;border-radius:6px;padding:2px 8px}}
.cb-pr{{font-size:10px;font-weight:900;background:#E0684A;color:#fff;border-radius:5px;padding:1px 6px}}
.cb-ord{{margin-left:auto;font-size:11px;color:#c4b59a;font-weight:800}}
.cb-hook{{margin:4px 0 0;font-size:13px;color:#5a4a35}}
.cb-btns{{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}}
.cb-btns button{{border:1px solid #EADFCE;background:#FBF3E4;border-radius:8px;padding:6px 12px;font-weight:700;font-size:12px;cursor:pointer}}
.cb-btns button:hover{{background:#FDECE5}}
.cb-t{{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border-radius:10px;overflow:hidden}}
.cb-t th,.cb-t td{{padding:8px 10px;border-bottom:1px solid #F0E6D2;text-align:left}}
.cb-t th{{background:#FFF7EA;font-size:12px}}
.cb-make li{{margin:5px 0;font-size:14px}}
.cb-empty{{color:#9b8a6e;font-size:13px}}
.cb-cal{{background:#fff;border:1px solid #EADFCE;border-radius:9px;padding:7px 12px;font-size:12.5px}}
.cb-cal b{{color:#E0684A;margin-right:4px}}
.cb-pkg{{font-size:10px;font-weight:900;background:#2E9E63;color:#fff;border-radius:5px;padding:1px 7px}}
.cb-pkgbox{{margin-top:9px;background:#FBF8F1;border:1px dashed #EAD9BE;border-radius:10px;padding:0 12px}}
.cb-pkgbox summary{{cursor:pointer;font-weight:800;font-size:12.5px;color:#2E9E63;padding:9px 0}}
.cb-pkgin{{padding:0 0 12px}}
.cb-script{{background:#fff;border:1px solid #EADFCE;border-radius:9px;padding:10px 13px;font-size:13px;line-height:1.65;white-space:pre-wrap}}
.pl-manifesto{{background:#20304A;color:#F4ECDD;border-radius:11px;padding:14px 18px;font-weight:700;font-size:14px;line-height:1.6}}
.pl-stance{{margin:8px 0;font-size:13px;color:#2B3A55}}.pl-stance b{{color:#E0684A}}
.pl-note{{font-size:12px;color:#8a5b1e;background:#FFF7EA;border:1px solid #EAD9BE;border-radius:8px;padding:8px 12px;margin:8px 0}}
.pl-h3{{font-size:15px;font-weight:900;color:#2B3A55;margin:20px 0 8px}}
.pl-levers{{display:flex;gap:6px;flex-wrap:wrap}}
.pl-lever{{font-size:11.5px;font-weight:800;border-radius:7px;padding:3px 9px}}
.pl-plus{{background:#EAF6EE;color:#2E7D4E}}.pl-minus{{background:#FBECEA;color:#C0473A}}.pl-key{{background:#FDECE5;color:#B44A31;border:1px solid #F0C9BB}}
.pl-vid{{background:#fff;border:1px solid #EADFCE;border-radius:10px;padding:11px 14px;margin-bottom:8px}}
.pl-vhead{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:14px}}
.pl-tier{{color:#fff;font-weight:900;font-size:11px;border-radius:6px;padding:2px 9px;flex:none}}
.pl-type{{font-size:11px;font-weight:800;background:#EAF2FB;color:#2B4a72;border-radius:6px;padding:1px 8px}}
.pl-bars{{font-size:12.5px;color:#4a3a28;margin-top:5px}}.pl-bars b{{color:#8a6f45}}
.pl-guess{{font-size:12px;color:#5a4a35;margin-top:5px;background:#FBF8F1;border-radius:7px;padding:6px 10px}}
.pl-priors{{display:flex;gap:6px;flex-wrap:wrap}}
.pl-prior{{font-size:12px;border-radius:8px;padding:4px 10px;border:1px solid #EADFCE;background:#fff}}
.pl-prior b{{margin-right:4px}}
.pl-tS b{{color:#2E9E63}}.pl-tA b{{color:#3A6FB0}}.pl-tB b{{color:#C98A2E}}.pl-tD b{{color:#C0473A}}
.pl-q li{{font-size:13px;margin:4px 0;color:#3a3024}}
</style>
<script>
function cbCopy(t,btn){{
  (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){{
    var o=btn.textContent;btn.textContent='복사됨 ✓';setTimeout(function(){{btn.textContent=o;}},1200);
  }}).catch(function(){{
    var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();
    document.execCommand('copy');document.body.removeChild(ta);
    var o=btn.textContent;btn.textContent='복사됨 ✓';setTimeout(function(){{btn.textContent=o;}},1200);
  }});
}}
</script></main>"""
    return BS.page("bank","","콘텐츠 금고 · 발행 대기실 | 아이와 AI교실(운영)",
        "운영자 전용 — 시리즈별 콘텐츠 재고·발행 대기·성과 기록.", body)

def build_all():
    for d in ("sources","series","drafts/shorts","drafts/youtube_descriptions","drafts/worksheets",
              "approved/shorts","approved/descriptions","published"):
        os.makedirs(os.path.join(CB,d), exist_ok=True)
    BS.write("content-bank.html", page())
    n_appr = sum(1 for i in ITEMS if i["status"] in ("approved","scheduled"))
    print(f"콘텐츠 금고 생성 · 아이템 {len(ITEMS)} (승인대기 {n_appr}) · 시리즈 {len(SER['series'])} · 자료 {len(SRC)}")

if __name__ == "__main__":
    build_all()
