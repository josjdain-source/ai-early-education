#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""부모 자료실 = '부모 행동 변환' 전용 콘텐츠(/parents/*). world-cases(정책 분석)와 완전 분리.
같은 나라라도: world-cases=정책·제도 보고서 / parents=우리 집에서 오늘 할 행동 코칭 / free=인쇄물.
world-cases 데이터·문장·카드클래스를 재사용하지 않는다(전용 PARENT/SITUATIONS/CHILD_POWERS + pc-* 클래스)."""
from country_reality import NAMES

ORDER=["china","usa","uk","singapore","korea","germany","japan"]

# 섹션1(허브) — 상황별(보편): (문제 상황, 부모가 할 행동)
SITUATIONS=[
 ("AI 답을 그대로 믿는 아이","정답을 확인해주지 말고 '이 답이 진짜인지 어떻게 확인할까?'로 되물으세요. 검증은 아이 몫으로."),
 ("질문을 한 번만 하고 끝내는 아이","'더 좋게 하려면 뭘 더 물어볼까?'로 한 번 더 묻게 하세요. 다시 묻기 한 번이 학습을 만듭니다."),
 ("결과만 보고 과정은 안 보는 아이","'어떤 순서로 나온 거야? 네가 직접 한 건 뭐야?'로 과정을 짚으세요."),
 ("부모가 대신 고쳐주고 싶은 집","고쳐주지 말고 '어디를 바꾸면 더 좋을까?'로 아이가 스스로 고치게 하세요."),
 ("AI를 숙제 기계로 쓰는 경우","'대신 시키기'가 아니라 '함께 검증하고 고쳐 쓰기'로 방향을 바꾸세요."),
]
# 섹션3(허브) — 아이에게 생기는 힘(보편): (이모지, 제목, 설명)
CHILD_POWERS=[
 ("🔁","다시 묻는 힘","포기하지 않고 더 나은 답을 찾아가는 힘."),
 ("🔎","근거 찾는 힘","'이건 어디서 왔을까'를 확인하는 힘."),
 ("⚖️","결과 비교하는 힘","여러 답을 견주어 스스로 고르는 힘."),
 ("💬","생각을 말로 바꾸는 힘","원하는 것을 정확히 표현하는 힘."),
 ("🛠️","AI로 자기 일을 만드는 힘","소비자가 아니라 창작자가 되는 힘."),
]

# 국가별 부모 코칭 — lesson(핵심1줄) / actions(집에서 3가지: 제목·방법·부모대사) / ages / faq
PARENT={
 "china": dict(lesson="시간표보다 중요한 건 '반복 습관'입니다.",
   actions=[("매일 10분 AI 대화 습관","매일(또는 주 2~3회) 저녁 10분, 오늘 만난 AI를 함께 이야기해요.","오늘 AI랑 뭐 했어? 뭘 다시 물어봤어?"),
            ("믿지 말고 다시 확인하기","AI 답을 그대로 믿지 않고 이상한 곳을 하나 찾게 해요.","이 답이 진짜인지 어떻게 확인할까?"),
            ("'내가 한 부분' 짚기","결과에서 아이가 직접 한 부분을 말하게 해요.","AI가 도와준 것 중에, 네가 직접 한 건 뭐야?")],
   ages=[("초등 저학년","화면 앞에서 '이거 진짜일까?'만 같이 물어봐도 충분해요. 짧고 자주."),
         ("초등 고학년","이상한 곳 하나 찾기 + '네가 직접 한 건 뭐야?'를 매일 저녁 10분."),
         ("중학생 이상","반복 루틴을 스스로 정하게 하고, 부모는 '오늘 뭘 다시 물었어?'만 확인.")],
   faq=[("매일 10분도 부담돼요","매일 아니어도 됩니다. 주 2~3회 저녁 대화만으로도 반복의 효과가 쌓여요."),
        ("아이가 AI를 너무 좋아해요","좋아하는 건 기회예요. '얼마나'의 경계만 함께 정하고 그 안에서 반복 습관으로 연결하세요."),
        ("제가 AI를 잘 몰라요","몰라도 됩니다. 부모는 답을 아는 사람이 아니라 '다시 묻게 하는 사람'이면 충분해요.")]),
 "usa": dict(lesson="쓰는 아이가 아니라 '만드는 아이'로 키웁니다.",
   actions=[("AI로 직접 만들기","AI로 그림·짧은 이야기·계획 하나를 아이가 직접 만들게 해요.","AI랑 같이 뭐 하나 만들어볼까?"),
            ("실패한 결과 고쳐 만들기","완성물을 한 번 더 고쳐 더 낫게 만들어요.","이걸 더 낫게 하려면 뭘 바꿀까?"),
            ("'내 것' 확인해주기","만든 게 아이 자신의 것임을 확인해줘요.","방금 그건 네가 한 거야, AI가 한 거야?")],
   ages=[("초등 저학년","AI로 그림 하나 만들고 '여기 뭐 바꿀까?' 정도면 훌륭한 창작이에요."),
         ("초등 고학년","짧은 이야기·포스터·계획을 AI로 만들고 한 번 고쳐보게 하세요."),
         ("중학생 이상","발표자료·글 같은 작은 프로젝트를 AI와 만들고 실패한 부분을 고치는 습관.")],
   faq=[("만들다 실패하면 실망해요","실패를 고치는 게 핵심이에요. '어디를 바꾸면 좋아질까?'로 다시 만들면 됩니다."),
        ("결과물이 조잡해요","완성도보다 '아이가 만든 과정'이 목표예요. 조잡해도 아이 것이면 성공입니다."),
        ("그냥 베끼는 것 같아요","'네가 바꾼 부분은 뭐야?'를 물으면 베끼기가 창작으로 바뀝니다.")]),
 "uk": dict(lesson="비판적 사고와 '근거 확인' — 판단과 책임은 사람에게.",
   actions=[("이상한 곳·빠진 곳 찾기","AI 답에서 이상하거나 빠진 부분을 하나 찾아요.","이 답에서 이상한 부분 하나만 찾아볼까?"),
            ("근거·출처 확인하기","그 답의 출처와 근거를 함께 따져요.","이 정보는 어디서 온 걸까?"),
            ("'왜 그렇게?' 질문 훈련","아이 생각의 이유를 묻는 습관을 들여요.","왜 그렇게 생각해?")],
   ages=[("초등 저학년","'왜 그렇게 생각해?'만 자주 물어도 비판적 사고가 자라요."),
         ("초등 고학년","AI 답의 '빠진 부분·이상한 부분'을 함께 찾는 놀이."),
         ("중학생 이상","출처를 스스로 확인하고 '이 근거 믿을 만해?'를 판단하게.")],
   faq=[("아이가 다 맞다고 해요","'그럼 틀린 부분을 하나만 찾아볼까?'로 뒤집어 물어보세요. 찾는 순간 비판이 시작돼요."),
        ("근거 확인이 어렵대요","'이거 누가 말한 거야?' 한 줄이면 충분한 출발이에요."),
        ("제가 답을 몰라 판단을 못 도와줘요","판단은 아이 몫으로 남기세요. 부모는 '왜 그렇게 생각해?'만 물으면 됩니다.")]),
 "singapore": dict(lesson="생활 속 '작은 실습'으로, 안전한 틀 안에서.",
   actions=[("생활 문제 함께 풀기","오늘의 생활 문제 하나(메뉴·정리·용돈)를 AI와 같이 해결해요.","이걸 우리 생활에 어떻게 써먹을까?"),
            ("생각 먼저 말하기","AI 답보다 아이 생각을 먼저 말하게 해요.","네 생각을 먼저 말해볼래?"),
            ("편향 점검하기","답이 한쪽으로 치우쳤는지 함께 살펴요.","이 답, 한쪽으로 치우친 건 없을까?")],
   ages=[("초등 저학년","간식 고르기·정리 순서 같은 생활 문제를 AI와 같이 정해봐요."),
         ("초등 고학년","여행 계획·용돈 계획을 AI와 세우고 실제로 해보기."),
         ("중학생 이상","발표 준비·일정 관리에 AI를 도구로, 편향은 스스로 점검.")],
   faq=[("생활에 AI 쓰는 게 의존 아닐까요?","먼저 아이 생각을 말한 뒤 AI와 비교하면 의존이 아니라 실습이 됩니다."),
        ("무슨 문제부터 시작하죠?","오늘 저녁 메뉴 정하기처럼 작고 실제적인 것부터."),
        ("편향을 어떻게 가르치죠?","'이 답 한쪽에 치우친 건 없을까?' 한 마디면 충분해요.")]),
 "korea": dict(lesson="놓친 시간을 '집에서 회복'합니다 — AI는 숙제 기계가 아니라.",
   actions=[("하루 10분 대화 루틴","저녁마다 오늘의 AI 사용을 되짚어요.","오늘 AI랑 뭐 했어? 뭘 다시 물어봤어?"),
            ("숙제 기계 탈출","'대신'이 아니라 '함께 검증하고 고쳐 쓰기'로 바꿔요.","이 답에서 이상한 곳을 같이 찾아볼까?"),
            ("자기 일 만들기","AI로 관심사(영상·글·계획)를 만들어 자기 일로.","네가 만들고 싶은 거, AI로 하나 만들어볼까?")],
   ages=[("초등 저학년","'오늘 AI랑 뭐 했어?' 대화만으로도 회복의 시작이에요."),
         ("초등 고학년","숙제를 '대신'이 아니라 '함께 검증'하는 방식으로 바꿔요."),
         ("중학생 이상","AI로 자기 관심사(영상·글·계획)를 만들어 자기 일로 연결.")],
   faq=[("학교에서 AI교육 하잖아요","학교는 도입, 습관은 가정이에요. 겹치는 게 아니라 서로 다른 역할입니다."),
        ("숙제에 AI 쓰면 실력이 안 늘까요?","'대신 시키기'는 그래요. '검증하고 고쳐 쓰기'로 바꾸면 실력이 늡니다."),
        ("너무 늦은 건 아닐까요?","늦지 않았어요. 놓친 시간은 매일 10분 대화로 회복됩니다.")]),
 "germany": dict(lesson="신뢰와 안전 먼저 — 데이터 책임을 아는 아이로.",
   actions=[("개인정보 안 넣기","이름·주소·얼굴 사진은 넣지 않기로 약속해요.","이 답에 우리 개인정보는 안 들어갔지?"),
            ("우리 집 AI 규칙 카드","무엇을·얼마나·무엇은 안 됨을 함께 정해 붙여요.","우리가 정한 규칙에 맞아?"),
            ("정보 신뢰성 판단","정보를 믿어도 될지 함께 판단해요.","이 정보, 믿어도 될까?")],
   ages=[("초등 저학년","'개인정보는 안 넣기' 약속 하나면 충분한 출발이에요."),
         ("초등 고학년","우리 집 AI 규칙 카드를 함께 만들고 지켜요."),
         ("중학생 이상","정보의 신뢰성과 데이터 책임을 스스로 판단하게.")],
   faq=[("개인정보 뭘 조심하죠?","이름·주소·학교·얼굴 사진. 이 넷만 안 넣어도 크게 안전해집니다."),
        ("규칙을 아이가 안 지켜요","부모가 먼저 지키고, 어길 때 혼내기보다 규칙 카드를 함께 다시 봐요."),
        ("너무 조심시키면 위축되지 않을까요?","금지가 아니라 '안전한 틀 안에서 자유롭게'가 목표예요.")]),
 "japan": dict(lesson="기기보다 논리와 절차 먼저 — 결과보다 과정을 기록.",
   actions=[("순서로 말하기","한 일을 '어떤 순서로 했는지' 말로 정리해요.","그거 어떤 순서로 한 거야?"),
            ("천천히 묻고 비교·검증","AI 답을 하나 골라 진짜인지 확인해요.","이 답, 진짜인지 확인해봤어?"),
            ("과정 기록하기","결과보다 '무엇을 어떻게 물었는지'를 적게 해요.","오늘 뭘 어떻게 물었어?")],
   ages=[("초등 저학년","'어떤 순서로 했어?'를 말로 정리하게 하는 것부터."),
         ("초등 고학년","AI 답을 '천천히 묻고 비교하고 정리'하는 3단계로."),
         ("중학생 이상","결과보다 과정을 기록하게(무엇을 어떻게 물었는지).")],
   faq=[("논리부터라니 어렵게 들려요","'순서대로 말하기'가 논리예요. 요리·정리 순서를 말하게 하는 것으로 충분해요."),
        ("과정 기록을 어떻게 시키죠?","'오늘 뭘 어떻게 물었어?' 한 줄만 적게 해도 기록이 됩니다."),
        ("AI를 늦게 시작해도 되나요?","네. 기기·논리를 먼저 익힌 뒤 AI로 가면 오히려 탄탄합니다.")]),
}

PC_STYLE="""<style>
.pc-hero{background:linear-gradient(160deg,#FFF3E9,#FCE7D6);border:1px solid #F0DDC8;border-radius:20px;padding:28px 26px;margin-bottom:6px}
.pc-hero .k{display:inline-block;background:#E0684A;color:#fff;font-weight:800;font-size:12px;border-radius:20px;padding:4px 13px;margin-bottom:8px}
.pc-hero h1{margin:0 0 6px;font-size:28px}
.pc-hero p{margin:0;color:#7c6a4d;font-weight:600}
.pc-sec-t{font-size:19px;font-weight:900;color:#2B3A55;margin:32px 0 3px}
.pc-sec-d{color:var(--muted);margin:0 0 14px;font-size:13.5px}
.pc-sit .row{display:flex;align-items:stretch;background:#fff;border:1px solid #EADFCE;border-radius:14px;margin-bottom:9px;overflow:hidden}
.pc-sit .p{flex:none;width:250px;background:#FDECEC;color:#B44A31;font-weight:800;padding:13px 16px;font-size:14px;display:flex;align-items:center}
.pc-sit .a{padding:13px 16px;font-size:14px;color:#2B2016;display:flex;align-items:center}
.pc-nat{display:flex;align-items:center;gap:14px;background:#fff;border:1px solid #EADFCE;border-radius:13px;padding:13px 16px;margin-bottom:8px;text-decoration:none;color:inherit}
.pc-nat .fl{font-size:26px;flex:none}
.pc-nat b{color:#2B3A55}.pc-nat .ls{color:#5a4a35;font-weight:600}
.pc-nat .go{margin-left:auto;color:#E0684A;font-weight:800;white-space:nowrap}
.pc-nat:hover{border-color:#E0684A;background:#FFFaf2}
.pc-power{display:flex;gap:14px;align-items:flex-start;background:#fff;border:1px solid #EADFCE;border-radius:13px;padding:14px 16px;margin-bottom:9px}
.pc-power .em{font-size:26px;flex:none}
.pc-power b{color:#2B3A55}.pc-power p{margin:2px 0 0;color:var(--muted);font-size:13.5px}
.pc-act{display:flex;gap:14px;background:#fff;border:1px solid #EADFCE;border-left:5px solid #E0684A;border-radius:12px;padding:15px 17px;margin-bottom:10px}
.pc-act .n{width:30px;height:30px;flex:none;background:#E0684A;color:#fff;border-radius:50%;display:grid;place-items:center;font-weight:900}
.pc-act b{color:#2B3A55;display:block;margin-bottom:3px}
.pc-act .how{margin:0 0 7px;font-size:14px;color:#3a3024}
.pc-act .say{margin:0;font-size:13.5px;background:#EEF7EF;border:1px solid #cfe6d6;border-radius:8px;padding:7px 11px;color:#186a3b}
.pc-age{display:flex;gap:0;background:#fff;border:1px solid #EADFCE;border-radius:12px;margin-bottom:8px;overflow:hidden}
.pc-age .lv{flex:none;width:120px;background:#FFF7EA;color:#8a6f45;font-weight:800;padding:12px 14px;font-size:13px;display:flex;align-items:center}
.pc-age .tip{padding:12px 15px;font-size:14px;display:flex;align-items:center}
.pc-faq{background:#fff;border:1px solid #EADFCE;border-radius:12px;padding:13px 16px;margin-bottom:9px}
.pc-faq b{color:#2B3A55}.pc-faq p{margin:5px 0 0;color:var(--navy2);font-size:14px}
.pc-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
.pc-related{margin-top:26px;border-top:1px dashed #EAD9BE;padding-top:14px;font-size:13px;color:#9b8a6e}
.pc-related a{color:#5a4a35;font-weight:700;text-decoration:none;margin-right:14px}
.pc-related a:hover{color:#E0684A}
@media(max-width:640px){.pc-sit .p{width:150px}.pc-age .lv{width:92px}}
</style>"""

def hub_body():
    sit="".join(f'<div class="row"><div class="p">⚠️ {p}</div><div class="a">→ {a}</div></div>' for p,a in SITUATIONS)
    nat="".join(f'<a class="pc-nat" href="/parents/{s}.html"><span class="fl">{NAMES[s][1]}</span><span><b>{NAMES[s][0]}에서 배울 점</b> — <span class="ls">{PARENT[s]["lesson"]}</span></span><span class="go">부모 코칭 →</span></a>' for s in ORDER)
    pw="".join(f'<div class="pc-power"><span class="em">{e}</span><div><b>{t}</b><p>{d}</p></div></div>' for e,t,d in CHILD_POWERS)
    faqs=[("AI가 아이에게 위험하지 않나요?","부모와 함께, 정해진 시간·규칙 안에서 쓰면 안전해요. 핵심은 '혼자 두지 않기'. 아이가 답을 그대로 믿지 않고 다시 묻게 돕는 것이 안전 교육입니다."),
     ("몇 살부터 시작할 수 있나요?","말로 원하는 걸 표현할 수 있으면 시작할 수 있어요(대략 6~7세+). 어릴수록 결과보다 '함께 대화하는 과정'에 집중하세요."),
     ("숙제를 AI로 시키면 안 되지 않나요?","'대신 시키기'는 위험하지만 '함께 검증하고 고쳐 쓰기'는 훌륭한 학습이에요. 이상한 곳을 찾는 연습이 진짜 공부입니다.")]
    fq="".join(f'<div class="pc-faq"><b>Q. {q}</b><p>{a}</p></div>' for q,a in faqs)
    return f"""<main><div class="wrap">
<div class="pc-hero"><span class="k">👨‍👩‍👧 부모 코칭 자료실</span>
<h1>세계 사례를, 부모의 <span class="coral">오늘 행동</span>으로</h1>
<p>정책 분석이 아닙니다. "그래서 오늘 우리 집에서 뭘 할까?"에 답하는 부모 코칭 자료실입니다.</p></div>
<h2 class="pc-sec-t">① 상황별로 보기</h2>
<p class="pc-sec-d">우리 집에서 자주 벌어지는 장면 → 부모가 바로 할 행동.</p>
<div class="pc-sit">{sit}</div>
<h2 class="pc-sec-t">② 국가 사례에서 배울 '부모 행동'</h2>
<p class="pc-sec-d">같은 나라라도 여기선 정책이 아니라 '오늘 우리가 할 행동'으로 바꿔 봅니다.</p>
{nat}
<h2 class="pc-sec-t">③ 그래서 아이에게 생기는 힘</h2>
<p class="pc-sec-d">이 행동들이 쌓이면 아이에게 남는 것.</p>
{pw}
<h2 id="faq" class="pc-sec-t" style="scroll-margin-top:90px">④ 자주 묻는 질문</h2>
<div style="margin-top:6px">{fq}</div>
<div class="pc-cta" style="margin-top:20px">
<a class="btn btn-lg btn-primary" href="/free/question-cards.html" target="_blank" rel="noopener">🃏 아이와 해볼 질문 카드 열기</a>
<a class="btn btn-lg" href="/start-guide.html">오늘 집에서 시작하기 →</a></div>
<p class="pc-related">국가 정책·제도를 자세히 읽고 싶다면 · <a href="/world-cases.html">세계 AI교육 분석 →</a></p>
</div>{PC_STYLE}</main>"""

def country_body(slug):
    d=PARENT[slug]; name,flag=NAMES[slug]
    acts="".join(f'<div class="pc-act"><span class="n">{i+1}</span><div><b>{t}</b><p class="how">{how}</p><p class="say">💬 이렇게 말해요 — "{say}"</p></div></div>' for i,(t,how,say) in enumerate(d["actions"]))
    ages="".join(f'<div class="pc-age"><div class="lv">{lv}</div><div class="tip">{tip}</div></div>' for lv,tip in d["ages"])
    faq="".join(f'<div class="pc-faq"><b>Q. {q}</b><p>{a}</p></div>' for q,a in d["faq"])
    return f"""<main><div class="wrap">
<div class="pc-hero"><span class="k">{flag} 부모 코칭 · {name} 사례로</span>
<h1>{name} 사례로, <span class="coral">우리 집</span>에서</h1>
<p>{d['lesson']}</p></div>
<h2 class="pc-sec-t">① 집에서 따라할 수 있는 3가지</h2>
<p class="pc-sec-d">{name}의 방식을 '오늘 우리가 할 행동' 3가지로 바꿨습니다.</p>
{acts}
<h2 class="pc-sec-t">② 연령별 적용 팁</h2>
<p class="pc-sec-d">아이 나이에 맞춰, 부모가 어떻게 말하고 도와줄지.</p>
{ages}
<h2 class="pc-sec-t">③ {name} 관련 부모 FAQ</h2>
<div style="margin-top:6px">{faq}</div>
<div class="pc-cta" style="margin-top:20px">
<a class="btn btn-lg btn-primary" href="/free/question-cards.html" target="_blank" rel="noopener">🃏 질문 카드 열기</a>
<a class="btn btn-lg" href="/free/worksheet.html" target="_blank" rel="noopener">📝 대화 연습지로 오늘 해보기</a></div>
<p class="pc-related">이 나라의 정책·커리큘럼 자세히 보기 · <a href="/world-cases/{slug}.html">{name} 세계 AI교육 분석 →</a></p>
</div>{PC_STYLE}</main>"""
