#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""아이와 AI교실 — 무료 유입(7일 질문카드) + 4주 질문력 교실 안내.
정체성: '많이 쓰는 아이'가 아니라 'AI 답을 의심·수정·다시 묻는 아이'.
안전: 온라인 AI교육 클래스로 표기(정식 학원 아님). 성적/입시/수상 보장 표현 금지. 결제·등록은 사람이 처리(자동 결제 없음)."""
import build_site as BS

SLOGAN = "AI를 많이 쓰는 아이보다, AI 답을 고칠 줄 아는 아이로."

DAYS = [
 ("1일차", "AI에게 부탁해보기", "아이가 원하는 걸 AI에게 직접 말해봐요.",
  "고양이 그려줘.", "노란 방석 위에 앉은 귀여운 하얀 고양이를 그려줘.",
  "무엇을·어떻게·어디에 를 아이가 정하게 두세요."),
 ("2일차", "이상한 부분 찾기", "AI 답에서 이상하거나 확실하지 않은 곳을 하나 찾아요.",
  "공룡에 대해 3가지 알려줘.", "방금 답에서 확실하지 않은 게 있으면 표시하고 다시 알려줘.",
  "'맞았어, 넘어가자' 대신 '이거 진짜일까?'를 한 번 더."),
 ("3일차", "다시 말하기", "원하는 결과가 안 나오면, 조건을 바꿔 다시 말해요.",
  "이야기 하나 써줘.", "주인공을 용감한 생쥐로 바꾸고, 친구도 한 명 넣어서 다시 써줘.",
  "다시 묻기 한 번이 실력을 만듭니다. 실패해도 괜찮아요."),
 ("4일차", "이유 물어보기", "AI에게 '왜 그렇게 답했어?'라고 근거를 물어요.",
  "이 답이 왜 맞아? 어디서 나온 거야?", "그 근거가 믿을 만한지 어떻게 확인할 수 있어?",
  "근거를 확인하는 습관이 의심하는 힘이 됩니다."),
 ("5일차", "다른 답 비교하기", "같은 걸 다르게 물어, 두 답을 비교해요.",
  "환경보호 방법 알려줘.", "이번엔 초등학생이 오늘 할 수 있는 걸로 구체적으로 알려줘.",
  "'질문이 답을 바꾼다'를 아이가 직접 느끼게 하세요."),
 ("6일차", "내 생각 먼저 쓰기", "AI에게 묻기 전에, 내 생각을 먼저 말하거나 적어요.",
  "(먼저 내 생각) 나는 이렇게 생각해 → 그다음 AI에게: 내 생각 어때?", "내 생각에서 빠진 점이 있으면 알려줘.",
  "아이 생각이 AI 뒤로 숨지 않게, 먼저 말하게 하세요."),
 ("7일차", "AI와 작은 작품 만들기", "그림·이야기·문제 중 하나를 AI와 만들고, 한 번 고쳐요.",
  "우리 가족 이야기를 짧게 만들어줘.", "막내가 활약하는 장면을 하나 더 넣어서 다시 만들어줘.",
  "결과물보다 '함께 만들고 고친 과정'을 칭찬하세요."),
]

WEEKS = [
 ("1주차", "AI에게 잘 말하기", "내 생각 말하기 카드"),
 ("2주차", "이상한 답 찾기", "AI 답 검사표"),
 ("3주차", "다시 묻기", "고쳐 말하기 질문카드"),
 ("4주차", "작은 프로젝트 만들기", "AI와 만든 이야기·포스터·문제풀이"),
]

TIERS = [
 ("녹화 강의 + 자료", "19,000원", "영상으로 4주 과정을 스스로 · 인쇄 자료 포함"),
 ("부모 동행 과제반", "49,000원", "매주 과제 제출 → 부모용 피드백 가이드 · 아이 말 고치기 중심"),
 ("소규모 피드백반", "99,000원~", "소수 정예 · 아이 결과물에 직접 피드백"),
]

def seven_days():
    style = """
.sd-card{background:#fff;border:1px solid #EADFCE;border-left:5px solid #E0684A;border-radius:13px;padding:15px 17px;margin-bottom:11px}
.sd-h{display:flex;align-items:center;gap:11px;margin-bottom:8px}
.sd-day{background:#E0684A;color:#fff;font-weight:900;border-radius:10px;padding:5px 11px;font-size:13px;flex:none}
.sd-h b{font-size:16px;color:#2B3A55}
.sd-act{font-size:14px;color:#3a3024;margin:0 0 8px}
.sd-q{background:#FFF7EA;border:1px solid #EAD9BE;border-radius:9px;padding:8px 12px;margin:5px 0;font-size:13.5px;font-weight:600}
.sd-q.re{background:#EEF7EF;border-color:#cfe6d6}
.sd-tip{font-size:12.5px;color:#8a6f45;border-top:1px solid #f2ecdf;padding-top:7px;margin-top:8px}
@media print{.no-print{display:none!important}}
"""
    cards = "".join(f"""<div class="sd-card">
<div class="sd-h"><span class="sd-day">{d}</span><b>{t}</b></div>
<p class="sd-act">🎯 {act}</p>
<div class="sd-q">💬 첫 질문 — "{fq}"</div>
<div class="sd-q re">🔁 다시 묻기 — "{rq}"</div>
<div class="sd-tip">👨‍👩‍👧 부모 — {tip}</div></div>""" for d, t, act, fq, rq, tip in DAYS)
    body = f"""<div style="max-width:820px">
<div style="background:linear-gradient(160deg,#FFF3E9,#FCE7D6);border:1px solid #F0DDC8;border-radius:18px;padding:22px 24px;margin-bottom:14px">
<div style="display:inline-block;background:#E0684A;color:#fff;font-weight:800;font-size:12px;border-radius:20px;padding:4px 13px">🎁 무료 · 7일 미니 코스</div>
<h1 style="margin:10px 0 4px;font-size:25px">아이에게 AI를 처음 보여주는 7일 질문카드</h1>
<p style="margin:0;color:#7c6a4d;font-weight:600">하루 한 장, 5~10분. '많이 쓰기'가 아니라 <b>의심하고 다시 묻는 힘</b>부터.</p></div>
<p style="color:var(--muted);font-size:13.5px">🖨 인쇄해서 냉장고에 붙여두고, 하루에 한 장씩 아이와 해보세요. 정답을 대신 알려주지 말고, 아이가 스스로 '다시 말하게' 도와주세요.</p>
{cards}
<div class="cta-band no-print" style="margin-top:16px"><div><h3>7일이 끝났다면?</h3><p>4주 '질문력 교실'에서 과제·피드백으로 습관을 굳혀요.</p></div>
<a class="btn btn-lg" href="/class.html">4주 교실 안내 →</a></div>
</div>
<style>{style}</style>"""
    return BS.free_resource_layout("/free/ai-first-7days.html", "7일 질문카드 (무료)", "", body)

def class_page():
    wk = "".join(f'<tr><td style="font-weight:800;color:#E0684A;white-space:nowrap">{w}</td><td>{t}</td><td style="color:var(--muted)">{r}</td></tr>' for w, t, r in WEEKS)
    tiers = "".join(f"""<div class="card" style="text-align:center"><h4 style="margin:0 0 4px">{n}</h4>
<div style="font-size:22px;font-weight:900;color:#2B3A55">{p}</div>
<p style="color:var(--muted);font-size:13px;margin:6px 0 0">{d}</p></div>""" for n, p, d in TIERS)
    body = f"""<main><div class="wrap" style="max-width:860px">
<section class="page-hero" style="padding:34px 0 20px"><div class="pill">🎓 온라인 AI교육 클래스</div>
<h1 style="font-size:30px">아이와 AI <span class="coral">질문력</span> 4주 교실</h1>
<p style="font-size:16px;color:var(--navy2);font-weight:700;margin-top:8px">"{SLOGAN}"</p></section>

<section class="block" style="padding:6px 0"><div class="callout" style="background:#EEF7EF;border-color:#cfe6d6">
🛡️ <b>우리 교실의 칼</b> — 요즘 유튜브엔 아이를 붙잡아 두려는 저품질 AI 영상(AI slop)이 넘칩니다. 우리는 반대예요.
<b>AI로 아이를 붙잡는 교실이 아니라, 아이가 AI를 의심하고 다룰 줄 알게 하는 교실</b>입니다.</div></div></section>

<section class="block"><h2 class="sec-title" style="font-size:20px">4주 커리큘럼</h2>
<table style="width:100%;border-collapse:collapse;font-size:14px">
<thead><tr style="border-bottom:2px solid #EADFCE"><th style="text-align:left;padding:8px">주차</th><th style="text-align:left;padding:8px">배우는 것</th><th style="text-align:left;padding:8px">결과물</th></tr></thead>
<tbody>{wk}</tbody></table>
<p style="color:var(--muted);font-size:13px;margin-top:10px">※ 핵심 가치는 '영상 시청'이 아니라 <b>과제 제출 → 부모 피드백 → 아이 말 고치기</b>입니다.</p></section>

<section class="block" style="background:var(--cream2)"><h2 class="sec-title" style="font-size:20px">반 구성 <span style="font-size:13px;color:var(--muted)">(초기 테스트 가격)</span></h2>
<div class="grid g3">{tiers}</div></section>

<section class="block"><div class="cta-band"><div><h3>먼저 무료로 맛보기</h3><p>7일 질문카드로 집에서 먼저 해보세요.</p></div>
<a class="btn btn-lg btn-primary" href="/free/ai-first-7days.html">🎁 7일 질문카드 (무료) →</a></div>
<div style="margin-top:14px;padding:16px 18px;border:1px dashed #CADCF0;border-radius:12px;background:#F4F7FB;font-size:13px;color:#4a5f7d">
📩 <b>신청·문의</b> — 정규반은 소수로 운영 예정입니다. 관심 있으시면 <a href="mailto:2011kstudentlife@gmail.com" style="color:#3A6FB0;font-weight:700">2011kstudentlife@gmail.com</a> 으로 연락 주세요.<br>
<span style="color:#9b8a6e;font-size:12px">본 프로그램은 콘텐츠 기반 <b>온라인 AI교육 클래스</b>입니다(정식 학원 아님). 성적·입시·수상 효과를 보장하지 않습니다. 가격·일정은 확정 시 공지됩니다.</span></div></section>
</div></main>"""
    return BS.page("free", "", "아이와 AI 질문력 4주 교실 | 아이와 AI교실",
        "AI를 많이 쓰는 아이보다 AI 답을 고칠 줄 아는 아이로 — 온라인 AI교육 클래스. 4주 커리큘럼·무료 7일 코스.", body)

def build_all():
    BS.write("free/ai-first-7days.html", seven_days())
    BS.write("class.html", class_page())
    print("아이와 AI교실 · 7일 질문카드 + 4주 교실 안내 생성 완료")

if __name__ == "__main__":
    build_all()
