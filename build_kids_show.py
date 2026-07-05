#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""'AI랑 놀자' 시리즈 사이트 빌더 — 대본 JSON(production/kids_ai_show/*.json)으로
시리즈 허브 + 에피소드 페이지 + 부모 활동지(따라 말하기 카드 포함) 생성.
영상은 업로드 후 유튜브 임베드로 채움(현재는 '영상 준비 중' 자리표시). build_site 헬퍼 재사용."""
import os, json, build_site as BS
ROOT=os.path.dirname(os.path.abspath(__file__))
KD=os.path.join(ROOT,"production","kids_ai_show")
def J(f): return json.load(open(os.path.join(KD,f),encoding="utf-8"))
SERIES=J("kids_ai_show_series_plan.json")
EP1=J("episode_001_script.json")
DET=J("episode_001_prompt_detail.json")

# 유튜브 ID(업로드 후 채움). 없으면 밝은 자리표시.
YT={}  # {"kids-ep1-long":"<id>", "kids-ep1-short":"<id>"}
def player(vid,title,vertical=False):
    i=YT.get(vid)
    ar="9/16;max-width:340px;margin:0 auto" if vertical else "16/9"
    if i:
        return f'<div class="player" style="aspect-ratio:{ar}"><iframe src="https://www.youtube.com/embed/{i}" title="{title}" loading="lazy" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width:100%;height:100%;border:0;border-radius:14px"></iframe></div>'
    return f'<div class="player" style="aspect-ratio:{ar};display:grid;place-items:center;background:linear-gradient(150deg,#FFE7B8,#FFC98B);border-radius:16px;text-align:center"><div style="padding:18px"><div style="font-size:40px">🎬🎈</div><b style="color:#8a4b1e">{title}</b><br><small style="color:#a9702f">영상 준비 중 — 곧 여기서 함께 봐요!</small></div></div>'

KIDS_CSS="""<style>
.ks-hero{background:linear-gradient(150deg,#FFF3C4,#FFD9A0);border:2px solid #F6C77a;border-radius:22px;padding:26px 24px;text-align:center}
.ks-hero h1{margin:0 0 6px;font-size:32px;color:#7a3e12}
.ks-hero p{margin:0;color:#9a5b23;font-weight:700}
.ks-ch{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:16px 0}
.ks-ch .c{background:#fff;border:2px solid #F0DDB8;border-radius:16px;padding:16px;text-align:center}
.ks-ch .em{font-size:40px}.ks-ch b{display:block;margin:6px 0 3px;color:#7a3e12}.ks-ch small{color:var(--muted)}
.ks-ep{display:flex;gap:14px;align-items:center;background:#fff;border:1px solid #EADFCE;border-radius:14px;padding:14px 16px;margin-bottom:10px;text-decoration:none;color:inherit}
.ks-ep .no{width:44px;height:44px;flex:none;background:#E0684A;color:#fff;border-radius:12px;display:grid;place-items:center;font-weight:900}
.ks-ep b{color:#2B3A55}.ks-ep .sk{color:var(--muted);font-size:13px}
.ks-ep .go{margin-left:auto;color:#E0684A;font-weight:800;white-space:nowrap}
.ks-ep.soon{opacity:.6}.ks-ep.soon .no{background:#c4b59a}
.ks-scene{display:flex;gap:12px;padding:9px 0;border-bottom:1px dashed #F0E6D2}
.ks-scene .n{width:26px;height:26px;flex:none;background:#FFF0D0;color:#8a5b1e;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:12px}
.ks-scene b{color:#2B3A55;font-size:14px}.ks-scene p{margin:2px 0 0;color:#4a3a28;font-size:13.5px}
.ks-ba{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:8px 0}
.ks-ba .box{border-radius:14px;padding:14px 16px}
.ks-ba .bad{background:#FDECEC;border:1px solid #f3c9c9}.ks-ba .good{background:#EAF7EE;border:1px solid #bfe6cd}
.ks-ba h4{margin:0 0 6px}.ks-ba .p{font-weight:800;font-size:15px}
.ks-promise{background:linear-gradient(150deg,#FFF3C4,#FFE0A6);border-radius:16px;padding:18px 20px;text-align:center;margin:14px 0}
.ks-promise .t{font-size:12px;font-weight:800;color:#b06a1e}.ks-promise b{font-size:19px;color:#7a3e12}
@media(max-width:560px){.ks-ba{grid-template-columns:1fr}}
</style>"""

def hub():
    ch="".join(f'<div class="c"><div class="em">{e}</div><b>{c["name"]}</b><small>{d}</small></div>'
        for (c,e,d) in zip(SERIES["characters"],["🧒","🤖","👩‍🏫","🧚"],
            ["호기심 대장! 실수해도 씩씩하게 다시!","삐빅! 귀엽지만 가끔 엉뚱해요.","정답 대신 '왜 그럴까?'를 물어요.","좋은 부탁 말을 반짝! 보여줘요."]))
    eps=""
    for ep in SERIES["episode_plan"]:
        done=ep["ep"]==1
        cls="ks-ep" if done else "ks-ep soon"
        href=f'/videos/kids-ai-show/episode-{ep["ep"]:03d}.html' if done else "#"
        go="보러가기 →" if done else "곧 나와요"
        eps+=f'<a class="{cls}" href="{href}"><span class="no">{ep["ep"]}화</span><div><b>{ep["theme"]}</b><div class="sk">🎯 {ep["skill"]}</div></div><span class="go">{go}</span></a>'
    body=f"""<main><div class="wrap">
<div class="ks-hero"><h1>🎈 AI랑 놀자</h1><p>{SERIES['tagline']}</p></div>
<div class="ks-ch">{ch}</div>
<h2 style="font-size:20px;color:#2B3A55;margin:24px 0 4px">화 목록</h2>
<p class="sec-desc" style="text-align:left;margin:0 0 14px">반복해서 보면서, 아이가 자연스럽게 'AI와 대화하는 법'을 익혀요. (만 6~10세 · 부모와 함께)</p>
{eps}
</div>{KIDS_CSS}</main>"""
    return BS.page("videos","","AI랑 놀자 · 아이 AI 대화 놀이 시리즈 | AI 조기교육",
        "만 6~10세가 반복해서 보며 AI와 대화하는 법을 배우는 놀이 영상 시리즈 'AI랑 놀자'.",body)

def episode1():
    sc="".join(f'<div class="ks-scene"><span class="n">{s["n"]}</span><div><b>{s["part"]}</b><p>{s["setting"]}</p></div></div>' for s in EP1["scenes"])
    ba=DET["before_after_prompt"]
    body=f"""<main><div class="wrap">
<p style="font-size:13px;color:var(--muted)"><a href="/videos/kids-ai-show.html" style="color:var(--coral);font-weight:700;text-decoration:none">🎈 AI랑 놀자</a> › 1화</p>
<div class="ks-hero" style="text-align:left"><div style="font-size:12px;font-weight:800;color:#b06a1e">1화 · 오늘의 놀이</div>
<h1 style="font-size:26px">{EP1['title']}</h1><p>🎯 오늘 배우는 것 — {DET['skill_taught']}</p></div>

<div style="margin:16px 0">{player("kids-ep1-long", EP1['title']+" (롱폼)")}</div>
<div style="display:grid;grid-template-columns:1fr;gap:8px;max-width:360px;margin:0 auto 8px">{player("kids-ep1-short","1화 쇼츠 (60초)",vertical=True)}</div>

<h2 style="font-size:19px;color:#2B3A55;margin:22px 0 8px">짧게 말하면? 자세히 말하면?</h2>
<div class="ks-ba">
<div class="box bad"><h4>😵 짧게 말하면</h4><div class="p">"{ba['before']}"</div><small>{ba['why_bad']}</small></div>
<div class="box good"><h4>😻 자세히 말하면</h4><div class="p">"{ba['after']}"</div><small>{ba['why_good']}</small></div></div>
<p style="text-align:center;color:#8a5b1e;font-weight:700">{' + '.join(ba['kid_rule_words'])}</p>

<div class="ks-promise"><div class="t">오늘의 AI 약속</div><b>{EP1['today_promise']}</b><br><span style="color:#9a5b23">"{EP1['repeat_line']}"</span></div>

<h2 style="font-size:19px;color:#2B3A55;margin:22px 0 6px">이야기 순서 (9장면)</h2>
<div>{sc}</div>

<div class="cta-band" style="margin-top:22px;background:linear-gradient(135deg,#FFF3E0,#FDE9CE)">
<div><h3>🖍 집에서 따라 해봐요</h3><p>부모 활동지 + 아이 '따라 말하기' 카드 3장(인쇄용).</p></div>
<a class="btn btn-lg btn-primary" href="/free/kids-ai-show-001.html">1화 활동지 열기 →</a></div>
</div>{KIDS_CSS}</main>"""
    return BS.page("videos","../","AI랑 놀자 1화 · AI에게 그냥 말하면 이상하게 나와요 | AI 조기교육",
        "AI랑 놀자 1화 — 자세히 말하면 AI가 더 잘 도와줘요. 롱폼·쇼츠·활동지.",body)

def activity1():
    q=DET["before_after_prompt"]
    steps=[("1","AI에게 처음 말하기","아이가 AI에게 짧게 부탁해봐요. 예: '고양이 그려줘'","여기에 우리 아이의 첫 부탁 말을 적어요:"),
           ("2","이상한 결과 찾기","나온 결과에서 이상한 곳을 찾아 동그라미 쳐요. 무엇이 이상한가요?","어디가 이상했나요? 적거나 그려요:"),
           ("3","자세히 다시 말하기","무엇을 · 어떻게 · 어디에 를 넣어 다시 말해요. 예: '노란 방석 위 귀여운 하얀 고양이'","자세한 부탁 말로 바꿔 적어요:"),
           ("4","좋아진 점 체크하기","다시 하니 무엇이 좋아졌나요? 스티커나 별점으로 표시!","좋아진 점: ☆ ☆ ☆ ☆ ☆")]
    st="".join(f"""<div class="wa"><div class="wn">{n}</div><div><b>{t}</b><p>{d}</p><div class="wline">{ph}</div></div></div>""" for n,t,d,ph in steps)
    cards=[("🐱","고양이야, 나와라!","노란 방석 위에 앉은, 귀여운 하얀 고양이를 그려줘!","무엇을+어떻게+어디에 를 다 말했어요!"),
           ("🤖","아이봇, 다시!","방금 건 조금 이상해. 이번엔 더 자세히 그려줄래?","이상하면 다시 말하면 돼요!"),
           ("⭐","내가 정하는 거야","파란 하늘에 웃고 있는 노란 병아리를 그려줘!","색깔·기분·장소를 넣어봐요!")]
    cd="".join(f"""<div class="wc"><div class="we">{e}</div><b>{t}</b><div class="ws">"{s}"</div><small>{h}</small></div>""" for e,t,s,h in cards)
    body=f"""<div class="wa-doc">
<div class="wa-top">🎈 AI랑 놀자 · <b>1화 활동지</b> — 자세히 말하기</div>
<p class="wa-int">1화를 보고, 아이와 함께 해보세요. 정답을 알려주지 말고, 아이가 스스로 '다시 말하게' 도와주세요. 🖨 인쇄해서 쓰면 좋아요.</p>
<h3 class="wa-h">👨‍👩‍👧 부모와 함께 4단계</h3>
{st}
<h3 class="wa-h">🃏 아이 '따라 말하기' 카드 3장 (오려서 써요)</h3>
<div class="wa-cards">{cd}</div>
<p class="wa-foot">오늘의 약속 — <b>AI는 자세히 말할수록 더 잘 도와줘요!</b> · © 2026 AI조기교육</p>
</div>
<style>
.wa-doc{{max-width:820px}}
.wa-top{{font-size:15px;color:#8a5b1e;background:#FFF3C4;border:1px solid #F0DDA0;border-radius:12px;padding:10px 14px;margin-bottom:10px}}
.wa-int{{color:var(--navy2);font-size:14px}}
.wa-h{{color:#2B3A55;margin:20px 0 10px;border-bottom:2px solid #F0E6D2;padding-bottom:6px}}
.wa{{display:flex;gap:13px;background:#fff;border:1px solid #EADFCE;border-radius:13px;padding:14px 16px;margin-bottom:10px}}
.wn{{width:30px;height:30px;flex:none;background:#E0684A;color:#fff;border-radius:50%;display:grid;place-items:center;font-weight:900}}
.wa b{{color:#2B3A55}}.wa p{{margin:3px 0 8px;font-size:14px;color:#4a3a28}}
.wline{{min-height:44px;background-image:repeating-linear-gradient(#fff,#fff 20px,#D8C9AE 21px,#fff 22px);border:1px solid #E4D8C4;border-radius:8px;padding:6px 10px;color:#9b8a6e;font-size:12.5px}}
.wa-cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.wc{{border:2px dashed #E0684A;border-radius:14px;padding:14px;text-align:center;background:#FFFdf7}}
.we{{font-size:34px}}.wc b{{display:block;margin:4px 0 8px;color:#7a3e12}}
.ws{{background:#EAF7EE;border:1px solid #bfe6cd;border-radius:9px;padding:9px;font-weight:700;font-size:13.5px;color:#186a3b;min-height:64px;display:flex;align-items:center;justify-content:center}}
.wc small{{display:block;margin-top:8px;color:var(--muted);font-size:11.5px}}
.wa-foot{{margin-top:16px;text-align:center;color:#8a5b1e;font-size:13px}}
@media(max-width:640px){{.wa-cards{{grid-template-columns:1fr}}}}
</style>"""
    return BS.free_resource_layout("/free/kids-ai-show-001.html","AI랑 놀자 1화 활동지","",body)

def build_all():
    BS.write("videos/kids-ai-show.html",hub())
    BS.write("videos/kids-ai-show/episode-001.html",episode1())
    BS.write("free/kids-ai-show-001.html",activity1())
    print("AI랑 놀자 · 허브+1화+활동지 생성 완료")

if __name__=="__main__":
    build_all()
