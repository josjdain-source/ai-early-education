#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI 경진대회 문제풀이 교실 데이터 authoring — data/competitions.json + data/competition_problems.json.
원칙: 공개 대회만, 원문 무단복붙 금지(요약은 자체 서술), 모든 문제에 source_url/level/skills/practice_problem.
연습문제(practice)는 대회 유형에서 영감받은 '자체 원작' — source_url=영감 준 공개 대회."""
import os, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT,"data"),exist_ok=True)

CONTESTS=[
 {"id":"ai_top_100","name":"AI TOP 100 (Campus)","org":"과학기술정보통신부 주최","levels":["high","university_general"],
  "url":"https://aitop100.org/","availability":"public",
  "desc":"AI 도구를 자유롭게 활용해 주어진 문제를 푸는 개인전. '무엇을 아느냐'보다 'AI와 협업해 얼마나 잘 해결하느냐'를 본다."},
 {"id":"it_gyeongsi","name":"청소년 IT경시대회 · 인공지능/알고리즘 부문","org":"한국정보기술진흥원(KITPA)","levels":["elementary","middle","high"],
  "url":"https://kitpa.org","availability":"public",
  "desc":"전국 초·중·고 대상. 알고리즘(코딩 문제 해결)과 인공지능(numpy·pandas 등 데이터·AI 코드 이해) 부문."},
 {"id":"ai_youth_challenge","name":"전국 청소년 AI 창의 경진대회 (AI Youth Challenge)","org":"포스코DX·한국인공지능산업협회","levels":["middle","high"],
  "url":"https://aichallenge.poscodx.com","availability":"public",
  "desc":"만 12~18세 팀전. AI를 적용해 산업·사회 문제를 개선하는 아이디어를 제안하고 구현한다."},
 {"id":"dacon","name":"DACON 데이터·AI 경진대회","org":"데이콘","levels":["high","university_general"],
  "url":"https://dacon.io/competitions","availability":"public",
  "desc":"데이터 분석·AI 모델링 경진대회 플랫폼. 공개 대회와 교육용 대회가 상시 열린다."},
 {"id":"youth_ai_content","name":"청소년 AI 콘텐츠 경진대회","org":"주최기관(공개 공모)","levels":["elementary","middle","high"],
  "url":"https://www.contestkorea.com","availability":"public",
  "desc":"AI로 만든 콘텐츠(이미지·영상·이야기 등)를 겨루는 공모."},
 {"id":"ai_for_all","name":"전국민 AI 경진대회","org":"주최기관","levels":["university_general"],
  "url":"https://aichallenge4all.or.kr/","availability":"public",
  "desc":"일반인 대상. AI 활용 능력으로 실생활·실무 문제를 해결한다."},
]

# 난이도 라벨(스펙)
DIFF={"elem_a":"초등 A · 자세히 말하기·결과 비교","elem_b":"초등 B · 이상한 부분 찾기·다시 묻기",
 "mid_a":"중등 A · 요약·표 만들기·근거 찾기","mid_b":"중등 B · 답안 비교·오류 검증·발표자료",
 "high_a":"고등 A · 데이터 해석·문제 정의·해결안 설계","high_b":"고등 B · 결과물 평가·윤리/편향 분석·보고서",
 "univ":"대학·일반 · 복합 문제해결·리서치·도구 조합·프롬프트 전략"}

def P(**k): return k
# ---- 공개 대회 문제 '분석'(원문 아님, 유형 요약) ----
ANALYSIS=[
 P(id="an_elem_1",kind="analysis",contest="youth_ai_content",level="elementary",tier="elem_a",type="이미지 생성",difficulty=1,
   title="내가 상상한 장면을 AI로 그리기",skills=["자세히 말하기","결과 비교"],
   problem_summary="AI 그림 도구로 '내가 상상한 한 장면'을 만들어 내는 유형. 얼마나 구체적으로 요청했는지가 결과를 가른다.",
   how_to_solve=["무엇을·어떻게·어디에 를 정한다","AI에게 자세히 부탁한다","나온 그림을 내 상상과 비교한다","다른 점을 찾아 다시 부탁한다"],
   first_question="파란 하늘을 나는, 웃고 있는 노란 병아리를 그려줘.",
   reask="병아리를 더 크게, 구름도 몇 개 넣어서 다시 그려줄래?",
   verify="내가 상상한 것과 그림에서 다른 점 3가지를 말해 본다.",
   parent_tip="정답을 대신 고쳐주지 말고, 아이가 '무엇이 다른지'를 먼저 찾게 한다.",
   practice_problem="우리 가족을 동물로 바꾼 그림을 AI로 만들어 보자(누구는 무슨 동물? 왜?)."),
 P(id="an_elem_2",kind="analysis",contest="it_gyeongsi",level="elementary",tier="elem_b",type="프롬프트 활용",difficulty=2,
   title="AI 답에서 이상한 곳 찾기",skills=["오류 찾기","다시 묻기"],
   problem_summary="AI가 준 답에 일부러(또는 실수로) 이상한 부분이 섞여 있을 때, 그것을 찾아 바로잡는 유형.",
   how_to_solve=["AI 답을 천천히 읽는다","이상하거나 안 맞는 부분을 표시한다","왜 이상한지 이유를 말한다","고쳐 달라고 다시 부탁한다"],
   first_question="공룡에 대해 3가지 사실을 알려줘.",
   reask="방금 answer 중에서 확실하지 않은 게 있으면 표시하고, 다시 정확히 알려줘.",
   verify="사실 하나를 골라 책이나 어른에게 진짜인지 확인한다.",
   parent_tip="'맞았어 넘어가자' 대신 '이거 진짜일까?'를 한 번 더 묻게 한다.",
   practice_problem="AI에게 우리 동네 소개를 시키고, 틀린 부분이 있으면 찾아 고쳐 보자."),
 P(id="an_mid_1",kind="analysis",contest="it_gyeongsi",level="middle",tier="mid_a",type="데이터 분석",difficulty=3,
   title="표로 정리하고 근거 찾기",skills=["자료 요약","표 만들기","근거 확인"],
   problem_summary="흩어진 정보를 표로 정리하고, 각 항목의 근거를 밝히는 유형(자료 요약·구조화).",
   how_to_solve=["무엇을 비교할지 '기준'을 정한다","AI에게 표로 정리해 달라고 한다","각 칸의 근거(출처)를 물어본다","빠진 항목을 채워 다시 요청한다"],
   first_question="재활용 쓰레기 5종류를 '종류/버리는 법/주의점' 표로 정리해줘.",
   reask="각 줄의 정보가 어디서 온 건지 근거도 표에 한 칸 더 추가해줘.",
   verify="표의 한 줄을 골라 실제 분리배출 안내와 맞는지 확인한다.",
   parent_tip="표가 '그럴듯한지'가 아니라 '근거가 있는지'를 함께 본다.",
   practice_problem="우리 반 친구들이 좋아하는 간식을 조사해 표와 그래프로 정리해 보자."),
 P(id="an_mid_2",kind="analysis",contest="ai_youth_challenge",level="middle",tier="mid_b",type="사회문제 해결",difficulty=3,
   title="AI로 우리 학교 문제 해결안 만들기",skills=["문제 정의","여러 답 비교","발표자료"],
   problem_summary="생활 속 문제를 정하고 AI와 함께 해결 아이디어를 여러 개 만든 뒤, 비교해 하나를 고르는 유형.",
   how_to_solve=["문제를 한 문장으로 정의한다","AI에게 해결 아이디어 3개를 요청한다","각 아이디어의 장단점을 비교한다","가장 나은 것을 골라 발표자료로 정리한다"],
   first_question="우리 학교 급식 잔반을 줄이는 방법 3가지를 제안하고, 각각 장단점을 알려줘.",
   reask="3개 중 초등학생이 직접 할 수 있는 걸로 다시 골라, 실천 단계로 나눠줘.",
   verify="고른 방법을 실제로 하루 해보고 되는지 확인한다.",
   parent_tip="'정답'을 고르게 하기보다 '왜 그걸 골랐는지' 이유를 말하게 한다.",
   practice_problem="우리 집 물·전기 낭비를 줄이는 방법을 AI와 찾아 '우리 집 규칙 3가지'로 만들자."),
 P(id="an_high_1",kind="analysis",contest="dacon",level="high",tier="high_a",type="데이터 분석",difficulty=4,
   title="데이터에서 문제를 '정의'하기",skills=["데이터 해석","문제 정의","해결안 설계"],
   problem_summary="주어진 데이터를 해석해 '무엇이 진짜 문제인지'를 스스로 정의하고 해결안을 설계하는 유형.",
   how_to_solve=["데이터에서 눈에 띄는 패턴을 찾는다","'진짜 문제'를 한 문장으로 정의한다","AI에게 가설과 접근법을 물어 비교한다","해결안을 단계로 설계하고 한계도 적는다"],
   first_question="이 데이터에서 이상하거나 눈에 띄는 패턴 3가지를 먼저 짚어줘.",
   reask="그 패턴이 '진짜 문제'인지, 아니면 우연인지 구분할 방법을 알려줘.",
   verify="AI가 말한 패턴을 데이터 원본에서 직접 다시 확인한다.",
   parent_tip="AI의 결론을 받아쓰지 말고, '데이터로 진짜 그런지' 확인하게 한다.",
   practice_problem="우리 반 한 달 지각 기록을 보고 '진짜 원인'이 뭘지 가설을 세우고 확인해 보자."),
 P(id="an_high_2",kind="analysis",contest="ai_top_100",level="high",tier="high_b",type="AI 결과 평가",difficulty=4,
   title="AI 결과물의 편향·오류 평가하기",skills=["결과물 평가","윤리·편향 분석","보고서 작성"],
   problem_summary="AI가 만든 결과물을 그대로 쓰지 않고, 편향·오류·빠진 관점을 평가해 보고서로 정리하는 유형.",
   how_to_solve=["AI 결과물을 받는다","누구에게 불리하거나 빠진 관점이 있는지 본다","근거를 들어 문제점을 적는다","개선 요청 후 전/후를 비교해 보고서로 정리한다"],
   first_question="이 주제로 요약문을 써줘. 단, 어떤 자료를 근거로 썼는지도 알려줘.",
   reask="이 요약이 한쪽 입장에 치우치지 않았는지 점검하고, 빠진 관점을 보완해줘.",
   verify="반대 입장의 자료를 따로 찾아 AI 요약과 대조한다.",
   parent_tip="'잘 썼다'가 아니라 '누가 빠졌나'를 함께 묻는다.",
   practice_problem="AI에게 '좋은 게임'을 추천받고, 그 추천이 어떤 아이에게는 안 맞을 수 있는 이유를 찾아보자."),
 P(id="an_univ_1",kind="analysis",contest="ai_top_100",level="university_general",tier="univ",type="복합 문제해결",difficulty=5,
   title="AI 도구를 '조합'해 실무 문제 풀기",skills=["문제정의","프롬프트 전략","도구 조합","검증","결과정리"],
   problem_summary="하나의 도구가 아니라 여러 AI 도구를 조합해, 현실 상황을 분석하고 실행 가능한 해결안을 만드는 유형.",
   how_to_solve=["문제를 한 문장으로 다시 정의한다","AI에게 역할을 부여한다(예: '너는 데이터 분석가')","첫 답을 믿지 않고 근거·빠진 점을 다시 묻는다","도구를 나눠 쓴다(리서치/정리/시각화)","최종안을 표·발표문으로 정리하고 한계를 밝힌다"],
   first_question="이 상황을 한 문장 문제 정의로 바꿔주고, 접근 방법 3가지를 제시해줘.",
   reask="첫 방법의 근거가 약해 보여. 반대 근거와 놓친 변수도 함께 알려줘.",
   verify="핵심 수치·주장은 1차 출처에서 직접 재확인한다.",
   parent_tip="(성인 학습자) 'AI가 했다'가 아니라 '내가 무엇을 판단했나'를 남긴다.",
   practice_problem="관심 주제로 2쪽짜리 리서치 노트를 만들되, 모든 핵심 주장에 출처를 붙여 보자."),
 P(id="an_univ_2",kind="analysis",contest="ai_for_all",level="university_general",tier="univ",type="발표·보고서",difficulty=4,
   title="AI와 함께 설득력 있는 보고서 쓰기",skills=["구조화","검증","프롬프트 전략","결과정리"],
   problem_summary="AI로 초안을 빠르게 만들되, 논리·근거·표현을 스스로 다듬어 설득력 있는 결과물로 완성하는 유형.",
   how_to_solve=["핵심 메시지 한 줄을 정한다","AI로 구조(목차) 초안을 만든다","각 절의 근거를 확인·보강한다","AI에게 반론을 요청해 약점을 메운다","사람이 최종 표현을 다듬는다"],
   first_question="이 주제로 보고서 목차를 짜고, 각 절에서 답할 핵심 질문도 적어줘.",
   reask="이 주장에 대한 가장 강한 반론과, 그 반론에 답할 근거를 알려줘.",
   verify="반론에 실제로 답이 되는지 사람이 판단한다.",
   parent_tip="(성인) 초안은 AI, 판단·책임은 사람 — 경계를 분명히.",
   practice_problem="관심 주제로 '3분 발표문'을 만들되, 예상 질문 3개와 답을 미리 준비해 보자."),
]

# ---- 우리집 연습문제(자체 원작, 대회 유형에서 영감) ----
def practice(level,tier,n,title,skills,task,fq,rq,vf,tip,contest):
    return P(id=f"pr_{level}_{n}",kind="practice",contest=contest,level=level,tier=tier,type="연습문제",difficulty={"elementary":1,"middle":3,"high":4}.get(level,3),
     title=title,skills=skills,problem_summary=f"[우리집 연습] {task}",how_to_solve=["첫 질문을 한다","답을 보고 이상한 곳을 찾는다","자세히 다시 묻는다","좋아진 점을 확인한다"],
     first_question=fq,reask=rq,verify=vf,parent_tip=tip,practice_problem=task)

PRAC=[]
# 초등 10
el=[("우리 반 마스코트 그리기",["자세히 말하기"],"우리 반을 대표하는 동물 마스코트를 AI로 그려 보자.","우리 반 마스코트로 귀여운 노란 강아지를 그려줘.","모자를 씌우고 배경을 교실로 바꿔줄래?","내 상상과 다른 점 3가지 말하기","무엇을·어떻게·어디에 를 아이가 정하게","it_gyeongsi"),
 ("이상한 답 탐정",["오류 찾기"],"AI에게 간단한 질문을 하고 틀린 곳을 탐정처럼 찾아 보자.","무지개 색깔을 순서대로 알려줘.","혹시 빠지거나 틀린 색이 있으면 고쳐서 다시 알려줘.","진짜 무지개 색과 비교","'틀리면 다시 물어보면 돼'를 알려주기","it_gyeongsi"),
 ("내 이야기 만들기",["자세히 말하기","다시 묻기"],"주인공과 장소를 정해 짧은 동화를 AI와 만들어 보자.","용감한 생쥐가 숲에서 모험하는 짧은 이야기를 써줘.","생쥐에게 친구를 한 명 넣어서 다시 써줄래?","이야기에서 제일 좋은 부분 고르기","결과보다 '함께 고치는 과정'을 칭찬","youth_ai_content"),
 ("숫자 놀이 도우미",["자세히 말하기"],"AI에게 재미있는 덧셈 문제를 만들어 달라고 해보자.","7살이 풀 수 있는 재미있는 덧셈 문제 3개 만들어줘.","동물이 나오는 이야기 문제로 다시 만들어줘.","직접 풀어보고 답 맞추기","정답보다 '어떻게 풀었는지' 말하게","it_gyeongsi"),
 ("우리 집 소개 카드",["자세히 말하기","결과 비교"],"우리 집을 소개하는 짧은 글을 AI와 만들어 보자.","우리 집을 소개하는 3문장 글을 써줘.","우리 강아지 이야기를 한 문장 더 넣어줘.","내가 쓴 것과 비교하기","아이 정보(주소 등)는 넣지 않기","youth_ai_content"),
 ("동물 소리 퀴즈",["다시 묻기"],"AI와 동물 퀴즈를 만들어 가족에게 내보자.","동물 소리 맞추기 퀴즈 3개 만들어줘.","조금 더 쉬운 걸로 다시 만들어줘.","가족이 풀게 하고 반응 보기","아이가 난이도를 조절하게","it_gyeongsi"),
 ("색깔 기분 그림",["자세히 말하기"],"오늘 기분을 색과 그림으로 AI에게 표현해 보자.","오늘 즐거운 기분을 노란색 그림으로 표현해줘.","별과 하트도 조금 넣어서 다시 그려줘.","내 기분과 어울리는지 보기","'왜 그 색이야?'를 물어보기","youth_ai_content"),
 ("우리 동네 길찾기",["자세히 말하기","오류 찾기"],"집에서 학교까지 가는 길을 AI에게 설명하게 하고 확인해 보자.","공원을 지나 학교 가는 길을 순서대로 알려줘.","순서가 이상하면 바르게 다시 알려줘.","실제 길과 비교","순서대로 말하는 힘 기르기","it_gyeongsi"),
 ("칭찬 로봇 만들기",["다시 묻기"],"친구를 칭찬하는 말을 AI와 여러 개 만들어 보자.","친구를 칭찬하는 따뜻한 말 3개 알려줘.","내 친구는 그림을 잘 그려. 그 친구용으로 다시 만들어줘.","진짜 하고 싶은 칭찬 고르기","'네 마음의 말'로 바꾸게","youth_ai_content"),
 ("미래의 나 그리기",["자세히 말하기"],"어른이 된 내 모습을 상상해 AI로 그려 보자.","우주비행사가 된 나를 멋지게 그려줘.","지구를 배경으로 넣어서 다시 그려줘.","내 상상과 비교","꿈을 말로 표현하게","youth_ai_content")]
for i,x in enumerate(el,1): PRAC.append(practice("elementary","elem_a" if i%2 else "elem_b",i,*x))
# 중등 10
mi=[("가짜뉴스 판별 연습",["오류 검증","근거 확인"],"AI에게 어떤 주장을 물어보고 근거가 있는지 확인해 보자.","'물을 많이 마시면 키가 큰다'가 사실인지 알려줘.","근거가 되는 자료 출처도 함께 알려줘.","다른 자료와 대조","'근거 없으면 믿지 않기'","it_gyeongsi"),
 ("우리 반 설문 표 만들기",["자료 요약","표 만들기"],"관심 주제로 설문을 만들고 결과를 표·그래프로 정리해 보자.","좋아하는 과목 설문 문항 5개 만들어줘.","결과를 표로 정리하는 양식도 만들어줘.","실제 조사해 채우기","'기준'을 먼저 정하게","it_gyeongsi"),
 ("두 답 비교하기",["답안 비교"],"같은 질문을 두 번 다르게 물어 답을 비교해 보자.","환경보호 방법을 간단히 알려줘.","이번엔 중학생이 실천할 수 있는 걸로 구체적으로 알려줘.","두 답의 차이 3가지 적기","'질문이 답을 바꾼다'를 체감","ai_youth_challenge"),
 ("발표 슬라이드 초안",["발표자료","구조화"],"주제를 정해 발표 목차를 AI와 만들고 다듬어 보자.","'분리수거' 발표 목차 5장을 짜줘.","각 장에서 말할 핵심 한 줄도 적어줘.","내가 말할 수 있는지 점검","슬라이드보다 '메시지' 먼저","ai_youth_challenge"),
 ("데이터 그래프 읽기",["데이터 해석"],"간단한 표를 주고 AI에게 해석을 시킨 뒤 검증해 보자.","이 월별 기온 표에서 특징 3가지를 알려줘.","그 특징이 표의 어느 숫자 때문인지 짚어줘.","숫자로 직접 확인","AI 해석을 데이터로 검증","dacon"),
 ("문제 정의 훈련",["문제 정의"],"막연한 고민을 '한 문장 문제'로 바꾸는 연습.","'공부가 안 돼요'를 해결 가능한 문제로 바꿔줘.","그중 오늘 당장 할 수 있는 걸로 좁혀줘.","실제로 하루 실천","'진짜 문제'를 좁히게","ai_youth_challenge"),
 ("요약의 기술",["자료 요약"],"긴 글을 AI로 요약하고 빠진 게 없는지 확인해 보자.","이 글을 3문장으로 요약해줘.","중요한데 빠진 내용이 있으면 채워서 다시 요약해줘.","원문과 대조","'짧게'보다 '안 빠지게'","dacon"),
 ("아이디어 3안 비교",["여러 답 비교"],"한 문제에 아이디어 3개를 받아 장단점으로 비교해 보자.","교실 소음을 줄이는 아이디어 3개와 장단점.","가장 돈 안 드는 걸로 다시 정리해줘.","한 개 골라 이유 말하기","'왜 골랐나'를 남기게","ai_youth_challenge"),
 ("오류 심는 검증",["오류 검증"],"AI 답에 일부러 의심을 걸어 스스로 검증하는 연습.","조선시대 왕 순서를 알려줘.","이 중 헷갈리기 쉬운 부분을 표시하고 확인해줘.","한 명 골라 사실 확인","의심하는 태도 칭찬","it_gyeongsi"),
 ("공익 콘텐츠 기획",["구조화","발표자료"],"AI와 함께 공익 메시지 콘텐츠를 기획해 보자.","'교통안전' 짧은 카드뉴스 4컷 구성을 짜줘.","초등 동생도 이해하게 쉬운 말로 다시.","친구에게 보여주고 반응 보기","메시지가 분명한지 함께 점검","youth_ai_content")]
for i,x in enumerate(mi,1): PRAC.append(practice("middle","mid_a" if i%2 else "mid_b",i,*x))
# 고등 10
hi=[("문제 재정의 리서치",["문제정의","리서치"],"관심 사회문제를 정의하고 AI로 자료를 모아 정리해 보자.","'청소년 수면 부족' 문제를 한 문장으로 정의해줘.","원인 가설 3개와 각각의 근거 방향을 알려줘.","1차 자료로 근거 확인","AI 결론 받아쓰기 금지","dacon"),
 ("편향 점검 리포트",["윤리·편향 분석","보고서"],"AI 결과물의 편향을 점검하는 짧은 리포트를 써보자.","이 주제 요약문을 써주고 근거도 밝혀줘.","치우친 관점이 없는지 점검하고 보완해줘.","반대 입장 자료와 대조","'누가 빠졌나'를 묻게","ai_top_100"),
 ("데이터 해석 검증",["데이터 해석","검증"],"표/그래프 해석을 AI에게 맡기고 반드시 재확인하자.","이 데이터에서 결론 하나를 뽑아줘.","그 결론이 우연일 가능성도 알려줘.","원자료에서 직접 확인","상관≠인과를 짚기","dacon"),
 ("해결안 설계",["해결안 설계"],"정의한 문제에 실행 가능한 해결안을 단계로 설계하자.","이 문제의 해결안을 3단계로 설계해줘.","각 단계의 예상 장애물과 대비책도 넣어줘.","한 단계 시범 실행","'실행 가능성'을 따지게","ai_youth_challenge"),
 ("반론 요청 훈련",["결과물 평가"],"내 주장에 AI로 반론을 받아 약점을 메우자.","내 주장은 이렇다. 가장 강한 반론을 해줘.","그 반론에 답할 근거를 찾아줘.","반론에 실제로 답 되는지 판단","반론을 두려워 않게","ai_top_100"),
 ("도구 조합 워크플로",["도구 조합","프롬프트 전략"],"리서치→정리→시각화로 도구를 나눠 쓰는 흐름을 짜자.","이 작업을 단계별로 어떤 순서로 하면 좋을지 알려줘.","각 단계에서 AI에게 줄 역할도 정해줘.","흐름대로 소규모 실행","단계마다 사람이 점검","dacon"),
 ("출처 붙이기",["검증","결과정리"],"모든 핵심 주장에 출처를 붙이는 습관을 연습하자.","이 주제 핵심 사실 5개를 알려줘.","각 사실의 1차 출처도 함께 알려줘.","출처 링크 직접 확인","출처 없는 문장은 빼기","dacon"),
 ("발표문 완성",["발표·보고서"],"AI 초안을 사람이 다듬어 3분 발표문을 완성하자.","이 주제 3분 발표문 초안을 써줘.","예상 질문 3개와 답도 준비해줘.","직접 소리내어 리허설","표현·판단은 사람 몫","ai_for_all"),
 ("AI 윤리 토론",["윤리·편향 분석"],"AI 사용의 옳고 그름을 사례로 토론해 보자.","AI로 숙제를 다 하는 것이 왜 문제인지 정리해줘.","반대로 도움이 되는 경우도 알려줘.","내 기준을 한 문장으로","정답 아닌 '기준'을 세우게","ai_top_100"),
 ("실무형 미니 프로젝트",["복합 문제해결"],"작은 실무 문제를 정해 AI와 끝까지 해결해 보자.","동아리 홍보 계획을 문제 정의부터 도와줘.","첫 안의 약점과 놓친 변수를 알려줘.","핵심 수치 재확인","'내가 판단한 것' 기록","ai_youth_challenge")]
for i,x in enumerate(hi,1): PRAC.append(practice("high","high_a" if i%2 else "high_b",i,*x))
# 부모와 함께
FAMILY=[
 P(id="fam_1",kind="practice",contest="ai_youth_challenge",level="family",tier="mid_a",type="부모와 함께",difficulty=2,
   title="우리 집 문제 함께 풀기",skills=["문제정의","여러 답 비교"],problem_summary="[부모와 함께] 생활 문제를 AI와 같이 해결",
   how_to_solve=["문제 한 문장 정의","아이디어 3개 요청","가족이 비교","하나 실행"],
   first_question="우리 집 아침이 늘 바빠. 여유를 만드는 방법 3개 알려줘.",
   reask="그중 우리 아이가 스스로 할 수 있는 걸로 다시 골라줘.",verify="일주일 해보고 되는지 확인",
   parent_tip="부모가 답을 정하지 말고 아이가 고르게 한다.",practice_problem="우리 집 아침 루틴을 AI와 함께 3단계로 만들어 붙여 보자."),
 P(id="fam_2",kind="practice",contest="it_gyeongsi",level="family",tier="elem_b",type="부모와 함께",difficulty=1,
   title="이상한 답 같이 찾기",skills=["오류 찾기"],problem_summary="[부모와 함께] AI 답의 이상한 곳을 같이 찾기",
   how_to_solve=["질문한다","같이 읽는다","이상한 곳 표시","다시 묻는다"],
   first_question="우리 동네에 대해 알려줘.",reask="틀리거나 확실치 않은 부분을 표시해서 다시 알려줘.",
   verify="아는 사실과 대조",parent_tip="부모도 '나도 모르겠네, 같이 확인하자'라고 말해준다.",
   practice_problem="가족 여행지를 AI에게 물어보고, 틀린 정보가 있는지 같이 찾아보자."),
 P(id="fam_3",kind="practice",contest="youth_ai_content",level="family",tier="elem_a",type="부모와 함께",difficulty=1,
   title="가족 이야기 만들기",skills=["자세히 말하기"],problem_summary="[부모와 함께] 우리 가족 이야기를 AI로",
   how_to_solve=["주인공 정하기","자세히 부탁","함께 고치기","읽어주기"],
   first_question="우리 가족이 주인공인 따뜻한 짧은 이야기를 써줘.",reask="막내가 활약하는 장면을 하나 더 넣어줘.",
   verify="가족이 함께 읽고 좋은 부분 고르기",parent_tip="완성도보다 '함께 만든 시간'을 즐긴다.",
   practice_problem="올해 우리 가족의 좋았던 일을 넣어 '우리 가족 동화'를 만들어 보자."),
 P(id="fam_4",kind="practice",contest="ai_for_all",level="family",tier="mid_b",type="부모와 함께",difficulty=2,
   title="용돈 계획 세우기",skills=["데이터 해석","문제정의"],problem_summary="[부모와 함께] 용돈/지출을 AI와 계획",
   how_to_solve=["목표 정하기","AI에 계획 요청","현실적인지 점검","실행"],
   first_question="한 달 용돈으로 저축과 소비를 나누는 계획을 세워줘.",reask="우리 아이 용돈 금액에 맞게 다시 구체적으로.",
   verify="한 달 실제로 해보기",parent_tip="AI 계획을 그대로 따르지 말고 우리 상황에 맞게 고치게 한다.",
   practice_problem="용돈 기입장을 만들고, 이번 달 목표 하나를 AI와 정해 보자."),
]

ALL=ANALYSIS+PRAC+FAMILY
json.dump({"contests":CONTESTS,"difficulty_labels":DIFF},open(os.path.join(ROOT,"data","competitions.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump({"problems":ALL},open(os.path.join(ROOT,"data","competition_problems.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(f"contests={len(CONTESTS)}  problems={len(ALL)} (analysis={len(ANALYSIS)}, practice={len(PRAC)}, family={len(FAMILY)})")
for lv in ["elementary","middle","high","university_general","family"]:
    print(f"  {lv}: {sum(1 for p in ALL if p['level']==lv)}")
