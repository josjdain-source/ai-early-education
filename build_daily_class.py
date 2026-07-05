#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""매일 AI교실 — 세계 AI교육 원칙을 한국 가정용 1년 커리큘럼으로 운영.
철학: 결과물이 아니라 과정. 매일 10~15분, 같은 힘(말하기→의심→다시묻기)을 반복.
world-cases/부모자료실 문장 복사 금지. 코딩학원·결과자랑·ChatGPT사용법 나열 금지."""
import build_site as BS

# 요일별 코너
DOW = [("월","AI에게 말해요","프롬프트 연습","🗣"),("화","이상한 답 찾기","비판적 사고","🔎"),
       ("수","다시 물어보기","수정 질문","🔁"),("목","AI와 만들기","창작","🎨"),
       ("금","부모 질문 시간","대화","👨‍👩‍👧"),("토","작은 프로젝트","응용","🧩"),("일","복습·쉬는 날","정리","🌿")]

# 4분기
QUARTERS = [
 ("1분기","AI와 말하기","부탁하기·설명하기·조건 말하기","#2E8B96","🗣",
  ["무엇을 원해?","어떤 모습이면 좋겠어?","빠진 게 있어?","다시 말하면 어떻게 말할까?"]),
 ("2분기","AI 답 의심하기","틀린 점 찾기·근거 묻기·비교하기","#E0684A","🔎",
  ["이 답이 정말 맞을까?","왜 그렇게 생각해?","근거가 있어?","다른 답도 있을까?","내가 아는 것과 다른 점은?"]),
 ("3분기","AI와 만들기","이야기·그림·문제·발표·생활 프로젝트","#2E9E63","🎨",
  ["내가 먼저 정한 주제는?","AI가 도와준 부분은?","내가 바꾼 부분은?","처음보다 좋아진 점은?"]),
 ("4분기","AI를 책임 있게 쓰기","출처·저작권·개인정보·공정성","#7A5BB0","🛡",
  ["이건 AI에게 말해도 될까?","누가 만든 자료일까?","그대로 써도 될까?","내 생각은 어디에 들어갔을까?"]),
]
# 12개월: (월, 테마, 분기idx, [4주 주제], 세계연결)
MONTHS = [
 (1,"AI에게 부탁하기",0,["AI에게 인사하고 부탁하기","원하는 결과 설명하기","조건을 붙여 말하기","마음에 안 들 때 다시 말하기"],"중국식 '빨리 경험'을 우리 집 첫걸음으로"),
 (2,"원하는 결과 설명하기",0,["무엇을 원하는지 말하기","어떤 모습인지 자세히","예시 들어 설명하기","빠진 것 채워 다시"],"자세히 말할수록 잘 도와준다"),
 (3,"조건을 붙여 다시 말하기",0,["색·크기·위치 붙이기","분위기·기분 붙이기","여러 조건 한 번에","조건 바꿔 비교하기"],"말이 결과를 바꾼다"),
 (4,"이상한 답 찾기",1,["틀린 곳 하나 찾기","빠진 곳 찾기","어색한 곳 찾기","찾아서 고쳐 말하기"],"영국식 '비판적 사고'를 우리식으로"),
 (5,"이유와 근거 묻기",1,["'왜 그렇게 답했어?'","'근거가 뭐야?'","'어디서 나온 거야?'","근거 직접 확인하기"],"영국식 '근거 확인'"),
 (6,"다른 답과 비교하기",1,["같은 질문 다르게 묻기","두 답 비교하기","내가 아는 것과 비교","더 나은 답 고르기"],"의심하고 판단하는 힘"),
 (7,"이야기 만들기",2,["주제 먼저 정하기","주인공 만들기","사건 넣기","내가 고쳐 완성"],"미국식 '만드는 아이'"),
 (8,"그림과 캐릭터 만들기",2,["캐릭터 정하기","자세히 그리기","배경·장면 넣기","고쳐 완성"],"창작의 주인은 아이"),
 (9,"생활 문제 해결하기",2,["문제 정하기","아이디어 받기","비교해 고르기","실제 해보기"],"싱가포르식 '생활 속 실습'"),
 (10,"개인정보와 안전",3,["안 넣을 정보 정하기","우리 집 규칙 만들기","안전하게 묻기","규칙 지키기"],"독일식 '데이터 책임'"),
 (11,"출처와 저작권",3,["'누가 만든 거야?'","그대로 써도 될까","출처 밝히기","내 것과 남의 것 구분"],"영국·독일식 '책임'"),
 (12,"나만의 AI 프로젝트 발표",3,["주제 정하기","AI와 만들기","내 생각 넣기","발표·돌아보기"],"1년의 힘을 내 작품으로"),
]

# 1월 4주 × 요일별 수업 (첫 4주만 상세). (요일idx, 활동, 첫질문예)
WEEKS = {
 1:("AI에게 인사하고 부탁하기",[
   ("AI에게 자기소개 부탁하기","안녕! 너를 소개해줄래?"),
   ("좋아하는 동물 설명하기","내가 좋아하는 강아지를 설명해줄게, 그림으로 그려줘"),
   ("그림 부탁하고 이상한 점 찾기","노란 모자를 쓴 고양이를 그려줘"),
   ("조건을 바꿔 다시 부탁하기","고양이 머리 위에 노란 모자를 꼭 넣고, 웃는 표정으로 다시"),
   ("내가 더 잘 말한 문장 고르기","(두 부탁 말 중) 어떤 게 더 자세했을까?"),
   ("부모와 이번 주 복습","이번 주에 가장 잘 부탁한 말은?"),
   ("쉬는 날 · 자유 놀이","오늘은 쉬어요")]),
 2:("원하는 결과 설명하기",[
   ("무엇을 원하는지 한 문장으로","내가 원하는 건 ○○야, 만들어줘"),
   ("어떤 모습인지 자세히","색깔·크기·표정까지 넣어 다시 말해요"),
   ("나온 답에서 빠진 것 찾기","내가 말한 것 중 빠진 게 있어?"),
   ("예시를 들어 설명하기","이런 느낌으로(예시) 다시 만들어줘"),
   ("부모 질문: 무엇을 원했어?","네가 정말 원한 건 뭐였어?"),
   ("작은 프로젝트: 내 물건 소개","내가 좋아하는 물건을 AI로 소개글 만들기"),
   ("복습 · 쉬는 날","이번 주 배운 말 한 줄 적기")]),
 3:("조건을 붙여 다시 말하기",[
   ("색·크기·위치를 붙여 말하기","크고 파란 공을 왼쪽에 그려줘"),
   ("이상한 답에서 틀린 조건 찾기","내가 말한 조건이 다 들어갔어?"),
   ("조건을 바꿔 다시 묻기","이번엔 작고 빨간 공으로 바꿔줘"),
   ("여러 조건 한 번에 말하기","노란 방석 위 하얀 고양이가 웃고 있게"),
   ("부모 질문: 어디가 달라?","네 생각이랑 어디가 달라?"),
   ("작은 프로젝트: 우리 반 마스코트","조건을 붙여 우리 반 마스코트 만들기"),
   ("복습 · 쉬는 날","가장 잘 통한 조건은?")]),
 4:("마음에 안 들 때 다시 말하기",[
   ("마음에 안 든 부분 말로 표현","어디가 마음에 안 드는지 말해볼까?"),
   ("이상한 부분을 콕 집어 다시","여기만 이렇게 바꿔줘"),
   ("두 번 고쳐 더 좋게 만들기","한 번 더, 이 부분을 이렇게"),
   ("AI와 작은 작품 완성하기","우리가 고친 걸로 완성해줘"),
   ("부모 질문: 처음보다 뭐가 좋아졌어?","처음보다 좋아진 점은?"),
   ("작은 프로젝트: 한 달 돌아보기","1월에 만든 것 중 제일 마음에 드는 것"),
   ("복습 · 쉬는 날","다음 달엔 뭘 해보고 싶어?")]),
}

# 오늘의 수업(요일별 7개, 7단계 완결) — today.html이 JS로 오늘 요일 선택
TODAY = [
 # (요일idx, 오늘의질문, 아이먼저생각, AI에게말해보기, 이상한점찾기, 다시묻기, 부모코칭)
 (0,"AI에게 고양이를 그려달라고 하면 어떤 말이 필요할까?","나는 어떤 고양이를 보고 싶지? (색·모습·장소)",
  "노란 모자를 쓴 귀여운 고양이를 그려줘.","모자가 없나요? 색이 다른가요? 표정이 이상한가요?",
  "고양이 머리 위에 노란 모자를 꼭 넣어줘. 웃는 표정이면 좋겠어.","정답을 알려주지 말고 물어보세요 — \"어떤 부분이 네 생각이랑 달라?\""),
 (1,"AI 답에 이상한 곳이 하나 있다면 어떻게 찾을까?","내가 아는 것과 다른 부분은 없을까?",
  "공룡에 대해 3가지 알려줘.","셋 중 확실하지 않은 게 있나요? 내가 아는 것과 다른가요?",
  "방금 답에서 확실하지 않은 게 있으면 표시하고 다시 알려줘.","\"이거 진짜일까? 어떻게 확인할 수 있을까?\"라고 물어보세요."),
 (2,"원하는 결과가 아니면 어떻게 다시 말할까?","무엇을 바꾸면 더 좋아질까?",
  "이야기 하나 써줘.","내가 원한 주인공·장소가 들어갔나요? 빠진 건?",
  "주인공을 용감한 생쥐로 바꾸고, 숲에서 모험하게 다시 써줘.","\"어디를 바꾸면 네 마음에 들까?\"로 아이가 고치게 하세요."),
 (3,"AI와 무엇을 함께 만들어볼까?","내가 먼저 정한 주제는 뭐지?",
  "우리 가족 이야기를 짧게 만들어줘.","내 생각이 들어갔나요? 더 넣고 싶은 장면은?",
  "막내가 활약하는 장면을 하나 더 넣어서 다시 만들어줘.","결과물보다 \"네가 바꾼 부분은 뭐야?\"를 물어 창작으로 만드세요."),
 (4,"오늘 AI랑 한 일을 어떻게 이야기할까?","오늘 뭘 묻고, 뭘 다시 물었지?",
  "(부모와 대화) 오늘 AI에게 물어본 것 중 제일 재밌던 것","다시 물었을 때 무엇이 좋아졌나요?",
  "내일은 무엇을 더 물어볼까?","\"오늘 뭘 다시 물어봤어?\" 한마디로 과정을 되짚어 주세요."),
 (5,"작은 프로젝트 하나를 AI와 해볼까?","내가 만들고 싶은 건 뭐지?",
  "내가 좋아하는 것으로 짧은 포스터 문구를 만들어줘.","내 생각이 주인인가요? AI가 도운 부분은?",
  "이 문구를 더 신나게, 한 줄 더 넣어서 다시.","\"이건 네가 만든 거야\"라고 소유감을 확인해 주세요."),
 (6,"이번 주 배운 질문을 정리해볼까?","이번 주 가장 좋았던 질문은?",
  "(복습) 이번 주 다시 물어서 좋아진 예를 하나 말해보기","반복하니 무엇이 늘었나요?",
  "다음 주엔 어떤 힘을 길러볼까?","오늘은 쉬어도 좋아요. 대화만으로 충분합니다."),
]

CSS = """<style>
.dc-wrap{max-width:1150px;margin:0 auto;padding:16px 18px 44px;display:flex;gap:24px;align-items:flex-start}
.dc-side{width:210px;flex:none;background:#FFF9EF;border:1px solid #EAD9BE;border-radius:14px;padding:12px 8px;position:sticky;top:74px}
.dc-side .t{font-weight:800;font-size:13.5px;color:#2B3A55;padding:4px 11px 9px;border-bottom:2px solid #F0E6D2;margin-bottom:6px}
.dc-side a{display:block;padding:7px 11px;margin:1px 0;border-radius:8px;text-decoration:none;color:#5a4a35;font-size:13px;font-weight:600}
.dc-side a:hover{background:#FDECE5}.dc-side a.on{background:#E0684A;color:#fff}
.dc-main{flex:1;min-width:0}
.dc-hero{background:linear-gradient(160deg,#FFF3E9,#FCE7D6);border:1px solid #F0DDC8;border-radius:20px;padding:26px 24px}
.dc-hero .k{display:inline-block;background:#E0684A;color:#fff;font-weight:800;font-size:12px;border-radius:20px;padding:4px 13px;margin-bottom:8px}
.dc-hero h1{margin:0 0 6px;font-size:27px}.dc-hero p{margin:0;color:#7c6a4d;font-weight:600}
.dc-sec{font-size:19px;font-weight:900;color:#2B3A55;margin:28px 0 4px}
.dc-secd{color:var(--muted);margin:0 0 14px;font-size:13.5px}
.dc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:11px}
.dc-card{background:#fff;border:1px solid #EADFCE;border-radius:14px;padding:15px 16px;text-decoration:none;color:inherit;display:block}
.dc-card:hover{border-color:#E0684A}
.dc-q{border-left:5px solid var(--qc,#E0684A);padding:12px 16px;background:#fff;border:1px solid #EADFCE;border-radius:12px;margin-bottom:10px}
.dc-q b{color:#2B3A55}
.dc-step{display:flex;gap:13px;background:#fff;border:1px solid #EADFCE;border-radius:12px;padding:13px 16px;margin-bottom:9px}
.dc-step .n{width:28px;height:28px;flex:none;background:#E0684A;color:#fff;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:13px}
.dc-step b{color:#2B3A55;display:block;font-size:13px}.dc-step p{margin:3px 0 0;font-size:14px}
.dc-step .say{background:#FFF7EA;border:1px solid #EAD9BE;border-radius:8px;padding:6px 11px;margin-top:5px;font-size:13.5px;font-weight:600}
.dc-dow{display:flex;gap:8px;align-items:center;background:#fff;border:1px solid #EADFCE;border-radius:11px;padding:11px 14px;margin-bottom:7px}
.dc-dow .d{width:30px;height:30px;flex:none;background:#F0E6D2;color:#7a5b2e;border-radius:8px;display:grid;place-items:center;font-weight:900}
.dc-chip{display:inline-block;font-size:11px;font-weight:800;border-radius:7px;padding:2px 9px;background:#EAF2FB;color:#2B4a72;margin-left:auto}
table.dc-t{width:100%;border-collapse:collapse;font-size:14px}
table.dc-t td,table.dc-t th{padding:8px 10px;border-bottom:1px solid #F0E6D2;text-align:left}
@media(max-width:860px){.dc-wrap{flex-direction:column}.dc-side{position:static;width:100%}}
</style>"""

NAV = [("🏫 매일 AI교실 대문","/daily-class.html"),("▶ 오늘의 10분 수업","/daily-class/today.html"),
       ("🗺 1년 커리큘럼","/daily-class/year.html")]

def layout(active, base, title, desc, inner):
    side = "".join(f'<a href="{h}" class="{"on" if h==active else ""}">{t}</a>' for t,h in NAV)
    mons = "".join(f'<a href="/daily-class/month-{m:02d}.html" style="display:block;padding:5px 11px;border-radius:7px;text-decoration:none;color:#8a6f45;font-size:12px">{m}월 · {name}</a>' for m,name,_,_,_ in MONTHS)
    body = f"""<main><div class="dc-wrap">
<aside class="dc-side"><div class="t">🏫 매일 AI교실</div>{side}<div class="t" style="margin-top:12px">📅 월별</div>{mons}</aside>
<div class="dc-main">{inner}</div></div>{CSS}</main>"""
    return BS.page("daily", base, title, desc, body)

def home():
    inner = f"""<div class="dc-hero"><span class="k">🏫 매일 AI교실</span>
<h1>매일 10분, 아이와 AI를 대화하는 힘을 기릅니다</h1>
<p>이 교실의 목표는 AI 결과물을 만드는 것이 아닙니다. 아이가 AI에게 말하고, 결과를 보고, 이상한 부분을 찾고, <b>다시 묻는 힘</b>을 기르는 것입니다.</p></div>
<div class="dc-grid" style="margin-top:16px">
<a class="dc-card" href="/daily-class/today.html"><div style="font-size:30px">▶</div><b>오늘의 수업</b><p style="color:var(--muted);font-size:13px;margin:4px 0 0">지금 바로 10분, 오늘 요일에 맞춰</p></a>
<a class="dc-card" href="/daily-class/week-01.html"><div style="font-size:30px">📆</div><b>이번 주 주제</b><p style="color:var(--muted);font-size:13px;margin:4px 0 0">요일별 수업 한눈에</p></a>
<a class="dc-card" href="/daily-class/month-01.html"><div style="font-size:30px">🎯</div><b>이번 달 능력</b><p style="color:var(--muted);font-size:13px;margin:4px 0 0">한 달에 한 가지 힘</p></a>
<a class="dc-card" href="/daily-class/year.html"><div style="font-size:30px">🗺</div><b>1년 지도</b><p style="color:var(--muted);font-size:13px;margin:4px 0 0">4분기 · 12개월 전체</p></a>
</div>
<h2 class="dc-sec">매일 수업은 이렇게 (10~15분)</h2>
<p class="dc-secd">매일 같은 형식을 반복합니다. 반복이 힘을 만듭니다.</p>
{''.join(f'<div class="dc-step"><span class="n">{i+1}</span><div><b>{t}</b></div></div>' for i,t in enumerate(["오늘의 질문 (아이가 먼저 생각)","AI에게 말하기 (직접 프롬프트)","결과 보기 (관찰)","이상한 점 찾기 (틀림·부족함)","다시 묻기 (조건을 바꿔)","한 줄 기록 (오늘 배운 질문 저장)"]))}
<div class="callout" style="margin-top:14px">🖨 매일 한 장 <a href="/free/daily-sheet.html">매일 활동지</a>에 기록하고, <a href="/free/question-cards.html">질문 카드</a>를 함께 쓰세요.</div>
<div class="callout" style="margin-top:12px;background:#FFF7EA;border-color:#EAD9BE">🎯 우리 아이 나이에 맞게 — <a href="/levels.html">연령별 AI교실(유치원~고등)</a>에서 단계별로 보세요.</div>
<div style="margin-top:12px;font-size:12.5px;color:#9b8a6e">이 커리큘럼은 세계 AI교육 원칙(중국 경험·영국 의심·미국 만들기·싱가포르 생활·독일/일본 책임)을 한국 가정용으로 녹인 것입니다.</div>"""
    return layout("/daily-class.html","","매일 AI교실 · 매일 10분 아이와 AI 질문력 | AI 조기교육",
        "매일 10분, 아이가 AI에게 말하고 의심하고 다시 묻는 힘을 기르는 1년 커리큘럼. 오늘의 수업·월별·주간.", inner)

def year():
    qs = ""
    for qi,(qn,qt,qd,qc,qe,cards) in enumerate(QUARTERS):
        mine = [m for m in MONTHS if m[2]==qi]
        ml = "".join(f'<a href="/daily-class/month-{m:02d}.html" style="text-decoration:none;color:inherit"><div class="dc-card" style="border-left:5px solid {qc}"><b>{m}월 · {name}</b><p style="color:var(--muted);font-size:12.5px;margin:3px 0 0">{link}</p></div></a>' for m,name,_,wk,link in mine)
        cc = " ".join(f'<span style="display:inline-block;background:#FFF7EA;border:1px solid #EAD9BE;border-radius:8px;padding:3px 10px;font-size:12.5px;margin:2px 0">"{c}"</span>' for c in cards)
        qs += f"""<h2 class="dc-sec" style="color:{qc}">{qe} {qn} · {qt}</h2><p class="dc-secd">{qd}</p>
<div class="dc-grid">{ml}</div>
<div style="margin:8px 0 6px">🗝 핵심 질문 카드 — {cc}</div>"""
    inner = f"""<div class="dc-hero"><span class="k">🗺 1년 커리큘럼</span>
<h1>1년, 매일 같은 힘을 조금씩</h1><p>새 지식을 매일 넣는 게 아니라, 말하기 → 의심하기 → 만들기 → 책임의 힘을 1년 내내 반복합니다.</p></div>
<div style="margin-top:16px">{qs}</div>"""
    return layout("/daily-class/year.html","../","1년 AI 질문력 커리큘럼 지도 | 매일 AI교실","4분기·12개월 — AI와 말하기/의심하기/만들기/책임 있게 쓰기. 세계 사례를 한국 가정용으로.",inner)

def today():
    import json as _j
    data = [{"dow":DOW[t[0]][0],"corner":DOW[t[0]][1],"q":t[1],"think":t[2],"say":t[3],"weird":t[4],"reask":t[5],"coach":t[6]} for t in TODAY]
    inner = f"""<div class="dc-hero"><span class="k">▶ 오늘의 10분 AI수업</span>
<h1 id="dcTitle">오늘의 AI수업</h1><p id="dcCorner"></p></div>
<div id="dcBody" style="margin-top:16px"></div>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">
<a class="btn btn-primary" href="/free/daily-sheet.html" target="_blank" rel="noopener">🖨 오늘 활동지 인쇄하기</a>
<a class="btn btn-ghost" href="/levels.html">🎯 우리 아이 나이별 수업 보기</a>
<a class="btn btn-ghost" href="/free/ai-first-7days.html" target="_blank" rel="noopener">🎁 7일 질문카드 받기</a></div>
<div class="callout" style="margin-top:14px">정답을 대신 주지 말고, 아이가 '다시 말하게' 도와주세요. 결과물이 아니라 <b>다시 묻는 과정</b>이 교육입니다.</div>
<script>
var L={_j.dumps(data,ensure_ascii=False)};
var d=new Date().getDay(); var idx=(d===0)?6:d-1; var x=L[idx];
document.getElementById('dcCorner').textContent=x.dow+'요일 · '+x.corner+' 코너';
var steps=[['🧠 오늘의 질문 (아이가 먼저 생각)',x.q],['💭 아이 먼저 생각하기',x.think],
 ['💬 AI에게 말해보기','"'+x.say+'"'],['👀 결과 보기 · 이상한 점 찾기',x.weird],
 ['🔁 다시 묻기','"'+x.reask+'"'],['👨‍👩‍👧 부모 코칭',x.coach]];
document.getElementById('dcBody').innerHTML=steps.map(function(s,i){{
 return '<div class="dc-step"><span class="n">'+(i+1)+'</span><div><b>'+s[0]+'</b><p>'+s[1]+'</p></div></div>';
}}).join('');
</script>"""
    return layout("/daily-class/today.html","../","오늘의 10분 AI수업 | 매일 AI교실","오늘 요일에 맞춘 10분 AI 질문력 수업 — 오늘의 질문·다시 묻기·부모 코칭.",inner)

def month_page(m, name, qi, weeks, link):
    qn,qt,qd,qc,qe,cards = QUARTERS[qi]
    wk = ""
    for i,w in enumerate(weeks,1):
        href = f'/daily-class/week-{i:02d}.html' if m==1 else "#"
        wk += f'<tr><td style="font-weight:800;color:{qc};white-space:nowrap">{i}주</td><td>{w}</td><td>{("<a href=\"%s\">수업 열기 →</a>"%href) if m==1 else "<span style=\"color:#c4b59a\">곧</span>"}</td></tr>'
    cc = " ".join(f'<span style="display:inline-block;background:#FFF7EA;border:1px solid #EAD9BE;border-radius:8px;padding:3px 10px;font-size:12.5px;margin:2px 0">"{c}"</span>' for c in cards)
    nav = f'{("<a href=\"/daily-class/month-%02d.html\">← %d월</a>"%(m-1,m-1)) if m>1 else ""} &nbsp; {("<a href=\"/daily-class/month-%02d.html\">%d월 →</a>"%(m+1,m+1)) if m<12 else ""}'
    inner = f"""<div class="dc-hero" style="border-color:{qc}"><span class="k" style="background:{qc}">{qe} {m}월 · {qn}</span>
<h1>{m}월 — {name}</h1><p>{qd} · 세계 연결: {link}</p></div>
<h2 class="dc-sec">이번 달 4주</h2>
<table class="dc-t"><thead><tr><th>주차</th><th>주제</th><th>수업</th></tr></thead><tbody>{wk}</tbody></table>
<div style="margin:14px 0 6px">🗝 {qn} 핵심 질문 카드 — {cc}</div>
<div class="dc-secd" style="margin-top:16px">{nav}</div>"""
    return layout(f"/daily-class/month-{m:02d}.html","../",f"{m}월 {name} | 매일 AI교실",f"매일 AI교실 {m}월 — {name}. 주차별 수업과 핵심 질문 카드.",inner)

def week_page(w, topic, days):
    rows = ""
    for di, (act, q) in enumerate(days):
        dow, corner, purpose, emo = DOW[di]
        rows += f"""<div class="dc-dow"><span class="d">{dow}</span><div><b>{act}</b><div style="font-size:12.5px;color:var(--muted)">{emo} {corner} · {purpose}</div>{f'<div style="font-size:13px;background:#FFF7EA;border:1px solid #EAD9BE;border-radius:7px;padding:5px 10px;margin-top:4px">💬 예: "{q}"</div>' if q else ''}</div><span class="dc-chip">{dow}</span></div>"""
    nav = f'{("<a href=\"/daily-class/week-%02d.html\">← %d주차</a>"%(w-1,w-1)) if w>1 else ""} &nbsp; {("<a href=\"/daily-class/week-%02d.html\">%d주차 →</a>"%(w+1,w+1)) if w<4 else "<a href=\"/daily-class/month-02.html\">2월 →</a>"}'
    inner = f"""<div class="dc-hero"><span class="k">📆 1월 {w}주차</span>
<h1>{w}주차 — {topic}</h1><p>요일마다 코너가 다릅니다. 하루 10분, 한 가지씩.</p></div>
<div style="margin-top:16px">{rows}</div>
<div class="callout" style="margin-top:12px">🖨 <a href="/free/daily-sheet.html">매일 활동지</a>에 기록 · <a href="/daily-class/today.html">오늘의 수업 바로가기</a></div>
<div class="dc-secd" style="margin-top:14px">{nav}</div>"""
    return layout(f"/daily-class/week-{w:02d}.html","../",f"1월 {w}주차 {topic} | 매일 AI교실",f"매일 AI교실 1월 {w}주차 — {topic}. 요일별 10분 수업.",inner)

def daily_sheet():
    fields = ["오늘 내가 AI에게 부탁한 것","AI가 준 답","이상했던 부분","다시 물어본 말","처음보다 좋아진 점","오늘의 질문왕 문장"]
    rows = "".join(f'<div style="margin-bottom:12px"><div style="font-weight:800;color:#2B3A55;font-size:13.5px;margin-bottom:5px">{i+1}. {f}</div><div style="min-height:46px;background-image:repeating-linear-gradient(#fff,#fff 21px,#D8C9AE 22px,#fff 23px);border:1px solid #E4D8C4;border-radius:8px"></div></div>' for i,f in enumerate(fields))
    body = f"""<div style="max-width:760px">
<div style="background:linear-gradient(160deg,#FFF3E9,#FCE7D6);border:1px solid #F0DDC8;border-radius:16px;padding:18px 22px;margin-bottom:12px">
<div style="display:inline-block;background:#E0684A;color:#fff;font-weight:800;font-size:12px;border-radius:20px;padding:4px 13px">🖨 매일 한 장</div>
<h1 style="margin:8px 0 3px;font-size:22px">오늘의 AI수업 활동지</h1>
<p style="margin:0;color:#7c6a4d;font-weight:600">부모가 "오늘 뭐 하지?" 하기 전에, 이 종이 한 장이 답합니다.</p></div>
<p style="color:var(--muted);font-size:13px">날짜: __________ · 오늘의 코너: __________ (매일 AI교실 <a href="/daily-class/today.html">오늘의 수업</a> 참고)</p>
{rows}
<p style="text-align:center;color:#8a6f45;font-size:12.5px;margin-top:14px">© 2026 아이와 AI교실 · 결과물이 아니라 다시 묻는 과정이 교육입니다</p></div>"""
    return BS.free_resource_layout("/free/daily-sheet.html","매일 활동지 (오늘의 AI수업)","",body)

def build_all():
    BS.write("daily-class.html", home())
    BS.write("daily-class/year.html", year())
    BS.write("daily-class/today.html", today())
    for m,name,qi,weeks,link in MONTHS:
        BS.write(f"daily-class/month-{m:02d}.html", month_page(m,name,qi,weeks,link))
    for w,(topic,days) in WEEKS.items():
        BS.write(f"daily-class/week-{w:02d}.html", week_page(w,topic,days))
    BS.write("free/daily-sheet.html", daily_sheet())
    print("매일 AI교실 · 대문+1년지도+오늘수업+12개월+4주+매일활동지 생성 완료")

if __name__ == "__main__":
    build_all()
