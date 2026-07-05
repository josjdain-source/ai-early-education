#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""나라별 '실제 교실 운영' 데이터 + 섹션 HTML — 정책(방침)을 넘어 실제로 매주·학년별 어떻게 가르치는지.
build_country_page / build_china_page / build_us_page 가 공유해서 딥페이지에 삽입.
모든 내용은 조사한 실제 커리큘럼·운영에 근거(출처는 각 페이지 하단 출처 섹션과 연결)."""

REALITY={
"china": dict(
 intro="정책이 실제 교실로 내려오면 이렇게 됩니다. 중국은 연 최소 8시간 이상의 AI 수업을 독립 과목이나 정보기술 수업에 넣고, 학년이 오를수록 '체험'에서 '제작'으로 나선형으로 깊어집니다.",
 grades=[
  ("1~2학년","일상 속 AI 앱을 직접 써 보고 스마트 기기와 상호작용하며, 'AI가 무엇인지'를 감각으로 체험합니다."),
  ("3학년","정보기술 수업에서 음성·이미지 인식처럼 AI가 어떻게 알아보는지를 체험하기 시작합니다."),
  ("4학년","데이터와 코딩으로 넘어가, AI가 데이터로 배운다는 것을 직접 다뤄봅니다."),
  ("5학년","지능형 에이전트(intelligent agent)와 알고리즘 개념을 배웁니다."),
  ("5~6학년","스마트 하드웨어 응용을 직접 만들어보는 '제작' 단계로 올라갑니다."),
 ],
 how=[("🧩","블록 코딩 플랫폼","프로그래밍을 블록으로 입문"),("🤖","이미지 인식 로봇","iFlytek 등 실물 로봇으로 실습"),("💬","코드 생성 LLM","중국어 지시를 실행 코드로 바꿔주는 AI 활용")],
 cadence="연간 최소 8시간 · 독립 과목 또는 정보기술 통합 · 저학년 체험 → 고학년 제작(체험→이해→응용→혁신)"),
"usa": dict(
 intro="미국은 국가가 강제하는 단일 커리큘럼이 없습니다. 대신 AI4K12의 'AI 5대 빅 아이디어'를 학년대별로 다시·더 깊게 배우는 나선형 틀을 학교·주가 가져다 씁니다. 실제 수업은 이렇게 돌아갑니다.",
 grades=[
  ("K-2","AI의 5대 개념(인식·표현/추론·학습·자연스러운 상호작용·사회적 영향)을 놀이로 처음 만납니다."),
  ("3-5","같은 개념을 더 깊게 — 'AI for Oceans' 같은 게임형 활동으로 AI가 '학습'하는 원리를 체험합니다."),
  ("6-8","AI+윤리 모듈로 편향과 사회적 영향까지, 직접 데이터로 판단해봅니다."),
  ("9-12","표현·추론·모델을 실제 프로젝트로 만들어보며 심화합니다."),
 ],
 how=[("🐬","무료 활동 자료","AI for Oceans·Stanford CRAFT 등(CC 라이선스)"),("🔁","나선형 심화","5대 아이디어를 매 학년대 다시, 더 깊이"),("⚖️","5대 빅 아이디어","인식·표현/추론·학습·상호작용·사회영향")],
 cadence="국가 강제 아님 · 학교·주 단위로 컴퓨터과학·교과에 통합 · 나선형으로 매 학년대 심화"),
"uk": dict(
 intro="영국은 강제 시수 대신, 국가 컴퓨팅 커리큘럼(Teach Computing)과 Oak National Academy 무료 자료로 실제 수업을 돌립니다. 키스테이지(학년군)별로 이렇게 배웁니다.",
 grades=[
  ("KS1-2 (초등)","게임으로 AI를 체험하고 '컴퓨터가 패턴을 배운다'는 개념을 놀이로 이해합니다."),
  ("KS3 (중등 전반)","작은 AI 모델을 직접 만들어보고, 일상 속에서 AI를 찾아 분석합니다."),
  ("KS4 (중등 후반)","더 복잡한 AI 주제로, AI 튜터를 활용한 수학 보충 같은 실전 사례까지 다룹니다."),
 ],
 how=[("📚","교과 통합","영어=AI 생성 텍스트 평가, 시민교육/PSHE=AI 사회영향·윤리"),("🍓","무료 수업자료","Oak National Academy(라즈베리파이 재단 협력)"),("🧑‍🏫","교사 도구","AI 수업 도우미 'Aila'로 수업계획 생성")],
 cadence="컴퓨팅 교과 안에서 학교 재량으로 편성 · 강제보다 자율 · 여러 과목에 걸쳐 통합"),
"singapore": dict(
 intro="싱가포르는 'Code for Fun' 프로그램으로 모든 학생이 실제로 코딩과 AI를 손으로 만집니다. 정책이 아니라, 교실에서 실제로 이렇게 돌아갑니다.",
 grades=[
  ("초등 · Code for Fun 10시간","변수·반복·함수를 블록코딩으로 배우고 AI 기초를 익힙니다. 초5는 Sphero 로봇을 코딩해 가위바위보 게임·로봇 군무를 만듭니다."),
  ("중등 · Code for Fun 10시간","디자인씽킹으로 실제 문제를 풀고, 마이크로컨트롤러로 시제품을 만듭니다(블록/텍스트 코딩 선택)."),
  ("2025~ · AI for Fun (선택 5~10시간)","AI를 넣은 시제품을 직접 만들어보며 '만지작거리며(tinkering)' 배웁니다."),
 ],
 how=[("🤖","실물 로봇 코딩","Sphero BOLT+ 로봇을 손으로 코딩"),("🎓","전교 대상","IMDA+MOE 공동, 2014년부터 모든 학교"),("⚖️","윤리 함께","교과 수업 중 AI의 위험·한계·윤리를 같이 다룸")],
 cadence="Code for Fun 10시간 + AI for Fun 5~10시간 · 전 학생 대상 · 교사 안내 아래 실습"),
"korea": dict(
 intro="한국은 AI 디지털교과서로 실제 수업을 돌리려 했습니다. 교실에서 실제로 이렇게 작동했고, 그리고 왜 흔들렸는지까지 봐야 진짜입니다.",
 grades=[
  ("대상 (2025.3~)","초등 3·4학년, 중1, 고1이 수학·영어·정보(그리고 특수교육 국어) 과목에서 사용했습니다."),
  ("작동 방식","학생마다 문제 속도와 난이도를 AI가 조정하는 개인화 학습입니다."),
  ("교실 경험","하트(보상) 획득·아바타 꾸미기·게임형 문제풀이로 아이의 몰입을 끌어냈습니다."),
  ("교사 역할","실시간 학습 데이터 대시보드를 보며 부족한 부분을 맞춤 지도했습니다."),
 ],
 how=[("🎮","게임형 동기부여","하트·아바타로 재미있게"),("📊","실시간 데이터","성취 데이터로 교사가 바로 개입"),("⚠️","현장의 한계","교사의 진도 모니터링 어려움·급조된 품질 → 넉 달 만에 보조교재로")],
 cadence="정규 교과 수업 중 태블릿으로 사용 · 다만 채택률 37%→19% 하락, '핵심'에서 '보조' 교재로 재분류"),
}

NAMES={"china":("중국","🇨🇳"),"usa":("미국","🇺🇸"),"uk":("영국","🇬🇧"),"singapore":("싱가포르","🇸🇬"),"korea":("한국","🇰🇷")}
def episode_nav(slug,current):
    eps=[("1","정책·방침",f"/world-cases/{slug}.html"),("2","실제 교실 운영",f"/world-cases/{slug}-2.html"),("3","우리 집 주간 적용",None)]
    out=[]
    for n,t,href in eps:
        on=(n==current); base="display:inline-block;border-radius:20px;padding:7px 15px;font-size:13px;font-weight:700;text-decoration:none;border:1.5px solid"
        if href and not on: out.append(f'<a href="{href}" style="{base} #E4D8C4;color:#8a6f45;background:#fff">{n}편 · {t}</a>')
        elif on: out.append(f'<span style="{base} #E0684A;color:#fff;background:#E0684A">{n}편 · {t}</span>')
        else: out.append(f'<span style="{base} #eadfca;color:#b9a98c;background:#faf5ea">{n}편 · {t} · 준비중</span>')
    return '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">'+''.join(out)+'</div>'
def reality_html(key):
    r=REALITY.get(key)
    if not r: return ""
    grades="".join(f"""<div class="tl-item"><div class="tl-year">{g}</div><div class="tl-body"><p>{d}</p></div></div>""" for g,d in r["grades"])
    how="".join(f"""<div class="card"><div class="lyr-h">{ic} {t}</div><p>{d}</p></div>""" for ic,t,d in r["how"])
    return f"""<section class="block"><div class="wrap">
<h2 class="sec-title">🏫 실제 교실은 이렇게 돌아간다</h2>
<p class="sec-desc">{r['intro']}</p>
<div class="timeline">{grades}</div>
<h3 style="margin:22px 0 10px;font-size:17px">수업은 이렇게 · 도구와 방식</h3>
<div class="grid g3">{how}</div>
<p class="sec-desc" style="margin-top:14px">⏱ <b>운영 주기</b> — {r['cadence']}</p>
</div></section>"""
