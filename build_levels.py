#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""연령별 AI교실 — 유치원~고등, 같은 철학 다른 깊이. 성장 사다리: 말하기→고치기→의심하기→검증하기→해결하기.
금지: 연령 간 복붙, 코딩학원 표현, 결과물 자랑, 입시/성적 보장, 유치원에 어려운 용어, 고등에 놀이만."""
import build_site as BS

LADDER = [("유치원","말하기"),("초등 저학년","고치기 전 부탁하기"),("초등 고학년","고치기"),("중등","검증하기"),("고등","해결하기")]

LEVELS = [
 dict(slug="kindergarten", name="유치원", age="만 5~7세", color="#E8963E", emoji="🧸",
   goal="AI를 '정답 기계'가 아니라 말을 걸면 반응하는 도구로 경험합니다. 글쓰기보다 말놀이가 중심.",
   heart="AI야, 내가 말한 걸 잘 들었니?",
   powers=["말하기","고르기","다른 점 찾기","안전한 말"],
   activity=["부모가 대신 입력하고, 아이는 말로 설명해요","AI 결과를 함께 보고 마음에 드는 걸 골라요","내가 말한 것과 다른 점을 찾아요","다시 말해보며 바꿔요"],
   ex=dict(mission="AI에게 토끼 그림을 부탁해볼까?", first="(아이 말) 분홍색! 큰 귀! 웃고 있어!",
     parent_input="(부모 입력) 분홍색이고 귀가 큰, 웃고 있는 토끼를 그려줘.",
     checks=["네가 말한 토끼랑 같아?","무엇이 달라?","다시 말한다면 뭐라고 할까?"], reask="(아이 말) 귀를 더 크게, 당근도 들고 있게!"),
   avoid=["'프롬프트' 같은 어려운 말 쓰지 않기(그냥 'AI에게 말하기')","글로 쓰게 강요하지 않기","정답 맞히기 시키지 않기"],
   year=["1분기: AI에게 말 걸기","2분기: 그림 보고 다른 점 찾기","3분기: 이야기 이어 말하기","4분기: 안전한 말 배우기"],
   free=[("🃏 부모용 질문 카드","/free/question-cards.html"),("🎁 7일 질문카드","/free/ai-first-7days.html")],
   daily="1분기(1~3월) · AI와 말하기", youtube_kid="AI야, 내 말을 잘 들었니?"),
 dict(slug="elementary-lower", name="초등 저학년", age="만 8~9세", color="#2E9E63", emoji="✏️",
   goal="내가 원하는 것을 AI에게 분명히 말하는 힘을 기릅니다.",
   heart="내가 원하는 걸 AI에게 잘 말할 수 있을까?",
   powers=["부탁하기","조건 붙이기","빠진 것 찾기","다시 말하기"],
   activity=["오늘의 미션을 아이가 직접 AI에게 말해요","결과에서 마음에 드는 곳·이상한 곳을 찾아요","무엇이 빠졌는지 짚어요","조건을 붙여 다시 말해요"],
   ex=dict(mission="AI에게 '내가 좋아하는 동물 캐릭터'를 만들어달라고 해보자.", first="귀여운 강아지 캐릭터를 만들어줘.",
     parent_input="", checks=["색깔이 마음에 드나요?","표정이 이상한가요?","내가 말 안 했는데 AI가 마음대로 넣은 게 있나요?"],
     reask="하늘색 옷을 입고, 웃고 있고, 초등학생 친구처럼 보이는 강아지 캐릭터로 다시 만들어줘."),
   avoid=["결과물 자랑 중심으로 흐르지 않기","정답을 대신 고쳐주지 않기(아이가 다시 말하게)","한 번에 완벽 요구하지 않기"],
   year=["1분기: AI에게 부탁하기","2분기: 이상한 점 찾기","3분기: 다시 말하기","4분기: 작은 작품 만들기"],
   free=[("🎁 7일 질문카드","/free/ai-first-7days.html"),("💡 첫 프롬프트 20개","/free/first-prompts.html"),("📝 AI 대화 연습지","/free/worksheet.html")],
   daily="1분기(1~3월) · AI와 말하기", youtube_kid="AI에게 다시 말하면 뭐가 달라질까?"),
 dict(slug="elementary-upper", name="초등 고학년", age="만 10~12세", color="#3A6FB0", emoji="🔧",
   goal="AI 답을 그대로 받아들이지 않고, 조건을 바꿔 더 좋은 결과를 만듭니다.",
   heart="AI 답을 보고 내가 고칠 수 있을까?",
   powers=["조건 설계","답 비교","이유 묻기","내 생각과 AI 답 구분","작은 프로젝트"],
   activity=["미션을 정하고 첫 질문을 던져요","나온 답을 '검사 질문'으로 점검해요","조건을 바꿔 더 좋게 고쳐요","내 생각이 어디에 들어갔는지 확인해요"],
   ex=dict(mission="AI에게 환경 보호 포스터 문구를 만들어달라고 해보자.", first="환경 보호 포스터 문구를 만들어줘.",
     parent_input="", checks=["이 문구는 너무 흔하지 않을까?","초등학생이 이해하기 쉬울까?","내 생각이 들어가 있을까?"],
     reask="초등학교 복도에 붙일 문구로, 짧고 기억하기 쉽고, 친구들이 바로 행동하고 싶게 만들어줘."),
   avoid=["'AI가 다 해줌'으로 끝내지 않기","비교·이유 없이 첫 답 채택하지 않기","코딩 기술 자랑으로 흐르지 않기"],
   year=["1분기: 좋은 질문 만들기","2분기: AI 답 검사하기","3분기: AI와 창작하기","4분기: 안전하고 책임 있게 쓰기"],
   free=[("🖨 12주 워크북","/free/uk-12weeks-workbook.html"),("🃏 질문 카드","/free/question-cards.html"),("🏠 경진대회 초등","/competitions/elementary.html")],
   daily="2분기(4~6월) · AI 답 의심하기", youtube_kid="AI 답에서 이상한 점을 찾아라"),
 dict(slug="middle", name="중등", age="만 13~15세", color="#7A5BB0", emoji="🔬",
   goal="AI 답의 근거·출처·편향·한계를 판단합니다. AI 리터러시가 본격 시작됩니다.",
   heart="이 답은 믿을 만한가?",
   powers=["근거 묻기","출처 확인","서로 다른 답 비교","편향 찾기","요약과 왜곡 구분","발표 자료 만들기"],
   activity=["주제에 첫 질문을 던져요","'검사 질문'으로 근거·출처·반대의견을 확인해요","다른 자료와 비교해요","근거를 표시해 다시 요청해요"],
   ex=dict(mission="AI에게 '청소년 스마트폰 사용 시간'에 대해 물어보자.", first="청소년 스마트폰 사용 시간이 많으면 어떤 문제가 있어?",
     parent_input="", checks=["근거가 있나?","언제 자료인가?","모든 청소년에게 해당되나?","반대 의견은 없나?"],
     reask="이 주장에 대한 근거와 반대 의견을 함께 알려줘. 출처가 필요한 부분은 표시해줘."),
   avoid=["'AI가 틀릴 수 있다'에서 멈추지 않기 — 'AI가 그럴듯하게 틀릴 수 있다'까지","출처 없이 요약만 믿지 않기","암기·정답 중심으로 흐르지 않기"],
   year=["1분기: AI 답의 구조 이해","2분기: 근거와 출처 확인","3분기: 자료 비교와 토론","4분기: 문제 해결 프로젝트"],
   free=[("🔵 경진대회 중등","/competitions/middle.html"),("🏠 우리집 연습문제","/competitions/practice.html")],
   daily="2분기(4~6월) · AI 답 의심하기", youtube_kid="AI가 그럴듯하게 틀렸어요"),
 dict(slug="high", name="고등", age="만 16~18세", color="#E0684A", emoji="🎓",
   goal="AI를 학습·탐구·진로·프로젝트 도구로 쓰되, 최종 판단과 책임은 사람이 가집니다.",
   heart="AI를 도구로 써서 내가 어떤 문제를 해결할 수 있을까?",
   powers=["탐구 질문 설계","자료 분석","보고서 구조화","발표 자료 제작","코드·데이터 기초 활용","윤리와 저작권","진로 포트폴리오"],
   activity=["탐구 질문(1차 질문)을 설계해요","AI 제안을 '검사 질문'으로 검증해요(실현성·개인정보·데이터)","실행 가능한 조사 계획으로 좁혀요","자료·방법·예상결과·한계로 구조화해요"],
   ex=dict(mission="학교 주변 교통 문제를 AI와 함께 조사해보자.", first="우리 학교 주변 교통 문제를 조사하려면 어떤 자료가 필요할까?",
     parent_input="", checks=["AI가 제안한 자료는 실제로 구할 수 있나?","개인정보 문제는 없나?","주장이 아니라 데이터로 확인할 수 있나?"],
     reask="고등학생이 2주 안에 할 수 있는 조사 계획으로 바꿔줘. 필요한 자료·조사 방법·예상 결과·한계를 나눠줘."),
   avoid=["단순 'AI 사용법'으로 끝내지 않기 — AI 협업형 탐구로","입시·성적·수상 효과를 말하지 않기(교육적 표현: '탐구 질문 설계와 자료 검증 훈련')","AI에게 판단·책임을 넘기지 않기"],
   year=["1분기: 탐구 질문 만들기","2분기: 자료 수집과 검증","3분기: AI 협업 프로젝트","4분기: 발표·포트폴리오·윤리"],
   free=[("🟣 경진대회 고등","/competitions/high.html"),("🏆 AI TOP 100 분석","/competitions/ai-top-100.html")],
   daily="3·4분기 · AI와 만들기 / 책임 있게 쓰기", youtube_kid="AI와 함께 문제를 해결해보자"),
]

CSS = """<style>
.lv-hero{background:linear-gradient(160deg,#FFF3E9,#FCE7D6);border:1px solid #F0DDC8;border-radius:20px;padding:26px 24px}
.lv-hero .k{display:inline-block;color:#fff;font-weight:800;font-size:12px;border-radius:20px;padding:4px 13px;margin-bottom:8px}
.lv-hero h1{margin:0 0 6px;font-size:27px}.lv-hero .heart{margin:8px 0 0;font-size:16px;font-weight:800;color:#7a3e12}
.lv-ladder{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin:14px 0}
.lv-ladder .s{background:#fff;border:1px solid #EADFCE;border-radius:10px;padding:8px 12px;font-weight:700;font-size:12.5px}
.lv-ladder .a{color:#c4b59a}
.lv-sec{font-size:18px;font-weight:900;color:#2B3A55;margin:26px 0 4px}
.lv-secd{color:var(--muted);margin:0 0 12px;font-size:13.5px}
.lv-chips{display:flex;gap:6px;flex-wrap:wrap}
.lv-chips span{background:#FFF7EA;border:1px solid #EAD9BE;border-radius:20px;padding:5px 13px;font-size:13px;font-weight:700;color:#7a5b2e}
.lv-step{display:flex;gap:12px;background:#fff;border:1px solid #EADFCE;border-radius:11px;padding:12px 15px;margin-bottom:8px}
.lv-step .n{width:26px;height:26px;flex:none;background:var(--lc,#E0684A);color:#fff;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:12px}
.lv-ex{background:#fff;border:1px solid #EADFCE;border-left:5px solid var(--lc,#E0684A);border-radius:12px;padding:15px 17px}
.lv-ex .m{font-weight:800;color:#2B3A55;margin-bottom:8px}
.lv-q{background:#FFF7EA;border:1px solid #EAD9BE;border-radius:8px;padding:8px 12px;margin:6px 0;font-size:13.5px;font-weight:600}
.lv-q.re{background:#EEF7EF;border-color:#cfe6d6}
.lv-check{font-size:13.5px;margin:3px 0;color:#3a4a63}
.lv-avoid{background:#FDECEC;border:1px solid #f3c9c9;border-radius:12px;padding:13px 17px}
.lv-avoid li{margin:5px 0;font-size:13.5px;color:#7a3b34}
.lv-card{background:#fff;border:1px solid #EADFCE;border-radius:14px;padding:16px;text-decoration:none;color:inherit;display:block}
.lv-card:hover{border-color:var(--lc,#E0684A)}
.lv-links a{display:inline-block;margin:3px 6px 3px 0;padding:7px 13px;border:1px solid #EADFCE;border-radius:9px;text-decoration:none;color:#5a4a35;font-weight:700;font-size:13px}
.lv-links a:hover{background:#FBF3E4}
</style>"""

def hub():
    ladder = ""
    for i,(n,f) in enumerate(LADDER):
        ladder += f'<span class="s">{n}<br><b style="color:#E0684A">{f}</b></span>' + ('<span class="a">→</span>' if i<len(LADDER)-1 else '')
    cards = "".join(f"""<a class="lv-card" href="/levels/{L['slug']}.html" style="--lc:{L['color']};border-top:4px solid {L['color']}">
<div style="font-size:30px">{L['emoji']}</div><b style="font-size:16px;color:{L['color']}">{L['name']}</b> <span style="font-size:12px;color:var(--muted)">{L['age']}</span>
<p style="margin:6px 0 8px;font-weight:700;color:#2B3A55;font-size:13.5px">"{L['heart']}"</p>
<div class="lv-chips">{''.join(f'<span style="font-size:11.5px;padding:3px 9px">{p}</span>' for p in L['powers'][:3])}</div></a>""" for L in LEVELS)
    inner = f"""<div class="lv-hero"><span class="k" style="background:#E0684A">🎯 연령별 AI교실</span>
<h1>우리 아이 나이엔, AI를 이렇게</h1>
<p style="color:#7c6a4d;font-weight:600">같은 철학, 다른 깊이. 나이에 따라 <b>질문의 깊이와 결과물의 복잡도</b>를 바꿉니다.</p>
<div class="lv-ladder">{ladder}</div></div>
<div class="grid g3" style="margin-top:16px">{cards}</div>
<div style="margin-top:16px;font-size:12.5px;color:#9b8a6e">세계 AI교육(근거) → 매일 AI교실(운영) → 연령별 AI교실(맞춤 처방). 한 솥에 다 넣지 않습니다.</div>"""
    return BS.page("levels","","연령별 AI교실 · 유치원~고등 AI교육 로드맵 | AI 조기교육",
        "우리 아이 나이에 맞는 AI교육 — 유치원 말놀이부터 고등 탐구 프로젝트까지. 말하기→고치기→의심→검증→해결.",
        f'<main><div class="wrap" style="max-width:980px">{inner}</div>{CSS}</main>')

def level_page(L):
    c = L['color']
    powers = "".join(f'<span>{p}</span>' for p in L['powers'])
    act = "".join(f'<div class="lv-step" style="--lc:{c}"><span class="n">{i+1}</span><div>{a}</div></div>' for i,a in enumerate(L['activity']))
    ex = L['ex']
    pin = f'<div class="lv-q">{ex["parent_input"]}</div>' if ex.get("parent_input") else ''
    checks = "".join(f'<div class="lv-check">· {q}</div>' for q in ex['checks'])
    avoid = "".join(f'<li>❌ {a}</li>' for a in L['avoid'])
    year = "".join(f'<div class="lv-step" style="--lc:{c}"><span class="n">{i+1}</span><div>{y}</div></div>' for i,y in enumerate(L['year']))
    free = "".join(f'<a href="{h}">{t}</a>' for t,h in L['free'])
    idx = [i for i,x in enumerate(LEVELS) if x['slug']==L['slug']][0]
    prevn = f'<a href="/levels/{LEVELS[idx-1]["slug"]}.html">← {LEVELS[idx-1]["name"]}</a>' if idx>0 else ''
    nextn = f'<a href="/levels/{LEVELS[idx+1]["slug"]}.html">{LEVELS[idx+1]["name"]} →</a>' if idx<len(LEVELS)-1 else ''
    inner = f"""<div class="lv-hero" style="border-color:{c}"><span class="k" style="background:{c}">{L['emoji']} {L['name']} · {L['age']}</span>
<h1>{L['name']} — 이 나이엔 AI를 이렇게</h1><div class="heart">"{L['heart']}"</div></div>

<h2 class="lv-sec">① 이 나이에는 AI교육을 이렇게</h2><p class="lv-secd">{L['goal']}</p>

<h2 class="lv-sec">② 이 단계에서 중요한 힘</h2><div class="lv-chips">{powers}</div>

<h2 class="lv-sec">③ 부모가 집에서 하는 10분 활동</h2>{act}

<h2 class="lv-sec">④ 오늘의 예시 수업</h2>
<div class="lv-ex" style="--lc:{c}"><div class="m">🎯 {ex['mission']}</div>
<div class="lv-q">💬 {ex['first']}</div>{pin}
<div style="font-weight:700;color:#2B3A55;margin:8px 0 4px;font-size:13.5px">👀 검사·찾기 질문</div>{checks}
<div class="lv-q re">🔁 다시 묻기 — "{ex['reask']}"</div></div>

<h2 class="lv-sec">⑤ 하면 안 되는 방식</h2><div class="lv-avoid"><ul style="margin:0;padding-left:18px">{avoid}</ul></div>

<h2 class="lv-sec">⑥ 이 나이 1년 목표</h2>{year}

<h2 class="lv-sec">⑦ 관련 무료 자료</h2><div class="lv-links">{free}</div>

<h2 class="lv-sec">⑧ 매일 AI교실 · 영상 연결</h2>
<div class="lv-links"><a href="/daily-class/today.html">🏫 오늘의 10분 수업</a><a href="/daily-class/year.html">🗺 {L['daily']}</a><a href="/videos.html">🎬 관련 영상 (아이용: "{L['youtube_kid']}")</a></div>

<div class="lv-secd" style="margin-top:20px">{prevn} &nbsp; {nextn} &nbsp; · &nbsp; <a href="/levels.html">전체 로드맵</a></div>"""
    return BS.page("levels","../",f"{L['name']} AI교실 · {L['heart']} | AI 조기교육",
        f"{L['name']}({L['age']}) AI교육 — {L['goal'][:50]} 중요한 힘·10분 활동·예시 수업·1년 목표.",
        f'<main><div class="wrap" style="max-width:900px">{inner}</div>{CSS}</main>')

def build_all():
    BS.write("levels.html", hub())
    for L in LEVELS:
        BS.write(f"levels/{L['slug']}.html", level_page(L))
    print("연령별 AI교실 · 대문+5개 연령 페이지 생성 완료")

if __name__ == "__main__":
    build_all()
