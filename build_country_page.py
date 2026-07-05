#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""영국·싱가포르·한국 AI교육 심층 페이지 빌더 — 중국/미국(build_china_page)과 동일 구조·스타일.
world-cases/{c}.html + videos/{c}-ai-education.html 생성. build_site 헬퍼 재사용.
영상 미업로드면 embed가 '업로드 후 재생' 플레이스홀더로 자동 대체(유튜브 24h 차단 대응).
출처=조사한 실제 URL만. 자극화 금지, 관점=국가별 AI 리터러시·거버넌스."""
import os, json, build_site as BS, country_reality as CR
ROOT=os.path.dirname(os.path.abspath(__file__))
try: QUEUE=json.load(open(os.path.join(ROOT,"youtube/upload_queue.json"),encoding="utf-8"))
except Exception: QUEUE={"queue":[]}
def yt_id(vid):
    for it in QUEUE["queue"]:
        if it.get("video_id")==vid:
            if it.get("public") and it.get("youtube_id"): return it["youtube_id"]
            u=it.get("youtube_url") or ""; return (u.rstrip("/").split("/")[-1] if u else "") if it.get("public") else ""
    return ""
def embed(vid,title):
    i=yt_id(vid)
    if i: return f'<div class="player"><iframe src="https://www.youtube.com/embed/{i}" title="{title}" loading="lazy" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
    return f'<div class="player" style="display:grid;place-items:center;background:#2B3A55;color:#fff;text-align:center"><div style="padding:20px"><div style="font-size:34px">▶</div><b>{title}</b><br><small style="opacity:.8">영상 준비 중 · 업로드 후 여기서 재생됩니다</small></div></div>'

Q10=["AI가 준 답에서 이상한 부분 하나만 찾아볼까?","이 답이 진짜인지 어떻게 확인할 수 있을까?","AI 없이 너라면 어떻게 했을까?",
 "방금 그건 네가 한 거야, AI가 한 거야?","왜 그렇게 답했는지 AI에게 다시 물어볼까?","이 답을 더 좋게 하려면 뭘 더 물어봐야 할까?",
 "AI도 틀릴 수 있을까? 언제 틀릴까?","이 정보는 어디서 온 걸까?","친구한테 설명한다면 어떻게 말할래?","오늘 AI랑 뭐 했고, 뭘 다시 물어봤어?"]
EFFECTS=[
 ("🔎","스스로 확인하는 아이","AI가 준 답을 그대로 믿지 않고, 이상한 부분을 스스로 찾아냅니다. 정답을 받는 아이에서, 정답을 검증하는 아이로."),
 ("⚖️","스스로 판단하는 아이","AI에 휘둘리지 않고, 여러 답을 비교해 자기 생각으로 결정합니다. AI는 도구, 판단은 내가."),
 ("🛡️","속지 않는 아이","정보를 의심하고 근거를 확인하는 습관이 몸에 뱁니다. AI 시대에 가짜와 오류에 속지 않는 힘."),
]

C={}
C["uk"]=dict(slug="uk", vslug="uk-ai-education", flag="🇬🇧", pill="영국 심층",
 h1="영국은 왜 커리큘럼보다 '안전과 책임'을 먼저 말했나",
 subtitle="강제 시간표 대신, 안전·데이터·비판적 사고의 가이드라인",
 angle="중국이 '국가가 관리하는 문해력'이라면, 영국은 <span class=\"coral\">AI는 도구, 최종 판단과 책임은 사람에게</span> 남기는 가이드 중심입니다.",
 lf_caption="영국 편 · 강제 커리큘럼보다 안전·책임·비판적 사고",
 tl_desc="영국은 과목을 강제하기보다, 안전하게 쓰는 규칙과 판단력을 먼저 세웠습니다.",
 timeline=[
  ("2023","생성형 AI 입장문 발표","교육부(DfE)가 학교의 생성형 AI 활용에 대한 첫 공식 입장을 발표. 투명하고 안전한 사용을 원칙으로.","S1"),
  ("2025.01","생성형 AI 가이드 업데이트","데이터 보호(UK GDPR·아동 규약), 평가 부정 방지, 교사 업무 경감 관점으로 가이드 보강.","S2"),
  ("2025","아동 안전 지침에 AI 포함","'Keeping Children Safe in Education'에 AI 생성 유해물·괴롭힘 등 안전 항목 반영.","S3"),
  ("2025","시험·평가 AI 사용 지침","시험기관(JCQ)이 과제·평가에서의 AI 사용 경계와 학문적 진실성 규칙 제시.","S4"),
  ("2026 목표","모든 학교 AI 사용 정책","학교가 DfE·Ofsted 가이드에 맞춰 자체 AI 사용 정책을 갖추도록 권고.","S5"),
 ],
 layers=[
  ("① 정부 지침층","교육부(DfE)","AI를 강제 과목으로 밀어붙이기보다, 안전·데이터 보호·투명성의 원칙을 먼저 세운다. '교사를 대체하지 않는다', '최종 판단·책임은 사람에게'가 방향의 축이다."),
  ("② 안전·평가층","Ofsted·JCQ","아동 안전(유해물·괴롭힘)과 시험 부정을 막는 경계를 만든다. AI를 쓰되, 무엇이 아이의 것이고 무엇이 AI의 것인지 구분하게 한다."),
  ("③ 학교 현장층","교사 재량","교사가 상황에 맞게 활용하되, 준비 격차가 과제다. 조사에 따르면 다수 교사가 AI 조언에 자신 없고, AI 작동 원리를 가르치는 학교는 일부에 그친다.","S6"),
 ],
 korea5=[
  ("책임은 사람에게","영국은 '최종 책임은 사람'이라고 못박았다. 집에서도 결정은 AI가 아니라 아이가 하게 한다."),
  ("판단을 아이에게 남기기","AI 답을 받은 뒤 '네 생각은 어때?'로 아이의 판단을 한 번 더 거치게 한다."),
  ("근거를 비판적으로 읽기","영국이 강조한 비판적 사고를, 집에서는 '이 정보 어디서 왔을까?'로 연습한다."),
  ("무엇이 네 것인지 구분","영국이 시험에서 경계를 두듯, 집에서도 'AI가 한 것, 네가 한 것'을 구분해 준다."),
  ("쓰는 법보다 안전을 먼저","영국도 안전·데이터 보호를 앞세웠다. 집에서도 쓰는 법보다 안전한 경계를 먼저."),
 ],
 sources=[
  ("S1","Generative artificial intelligence (AI) in education","GOV.UK (DfE)","https://www.gov.uk/government/publications/generative-artificial-intelligence-in-education"),
  ("S2","Generative AI in education — Updated January 2025","AI in Education","https://www.ai-in-education.co.uk/news-events/generative-artificial-intelligence-ai-in-education---updated-january-2025"),
  ("S3","Artificial intelligence in schools: everything you need to know","GOV.UK Education Hub","https://educationhub.blog.gov.uk/2025/06/artificial-intelligence-in-schools-everything-you-need-to-know/"),
  ("S4","Guidance on the use of Generative AI in MATs and Schools","SchoolPro TLC","https://schoolpro.uk/2025/07/guidance-on-the-use-of-generative-ai-in-mats-and-schools/"),
  ("S5","Generation Ready: Scaling Safe, High-Quality AI in England's Schools","Tony Blair Institute","https://institute.global/insights/public-services/generation-ready-scaling-safe-high-quality-ai-englands-schools"),
  ("S6","Using AI and technology in education (roadmap)","GOV.UK","https://roadmap-for-modern-digital-government.campaign.gov.uk/ai/ai-in-education/"),
 ],
 srcnote="영국을 '규제만 하는 나라'로 단순화하지 않고, 안전·데이터 보호·비판적 사고·책임 소재를 먼저 세운 가이드 중심 접근으로 정리했습니다.",
 lf=dict(video_id="uk-ai-longform", title="영국은 왜 커리큘럼보다 안전과 책임을 먼저 말했나", subtitle="강제 시간표 대신, 안전·데이터·비판적 사고의 가이드라인",
   description="영국은 AI를 강제 과목으로 밀지 않았습니다. 대신 안전하게 쓰는 규칙, 데이터 보호, 그리고 '최종 판단과 책임은 사람에게'라는 원칙을 먼저 세웠죠.\n한국 가정도 같습니다. 쓰는 법보다, 결정을 아이가 하게 하는 습관이 먼저입니다."),
 shorts=[
  dict(video_id="uk-ai-short-1", copy="영국은 책임을 사람에게", title="영국은 왜 아이에게 AI를 '믿지 말라'고 할까?"),
  dict(video_id="uk-ai-short-2", copy="네 생각은 어때?", title="아이에게 AI를 시키기 전, 꼭 해야 할 질문"),
  dict(video_id="uk-ai-short-3", copy="쓰는 법보다 안전 먼저", title="한국 부모가 놓치는 AI교육의 한 가지"),
 ],
)
C["singapore"]=dict(slug="singapore", vslug="singapore-ai-education", flag="🇸🇬", pill="싱가포르 심층",
 h1="싱가포르는 왜 아이에게 'AI 가드레일'을 먼저 채웠나",
 subtitle="네 원칙(주도성·포용·공정·안전)과 균형의 설계",
 angle="싱가포르는 AI를 빨리 쓰게 하기보다, <span class=\"coral\">아이 생각이 AI 뒤로 숨지 않도록 균형(가드레일)</span>을 먼저 설계합니다.",
 lf_caption="싱가포르 편 · 국가 전략과 네 원칙의 균형",
 tl_desc="싱가포르는 국가 AI 전략과 교육을 하나로 묶어, 개인화와 안전을 함께 설계했습니다.",
 timeline=[
  ("2019","국가 AI 전략","싱가포르가 국가 차원의 AI 전략을 수립. AI를 국가 경쟁력의 축으로.","S1"),
  ("2023","국가 AI 전략 2.0","AI 전략을 2.0으로 확장. 사회 전반의 신뢰·안전 강조.","S2"),
  ("2023~","EdTech 마스터플랜 2030","교육의 기술 전환 로드맵. 학습에 AI를 책임 있게 통합.","S3"),
  ("2024","적응형 학습 시스템(ALS) 확대","MOE·GovTech의 SLS에 ALS 탑재. 수학·지리 등 개인화 학습 경로 제공.","S3"),
  ("2025","전 학생·교사 생성형 AI 리터러시","MOE가 모든 학생·교사에게 기초 생성형 AI 리터러시를 목표로 제시.","S4"),
 ],
 layers=[
  ("① 국가 전략층","Smart Nation·NAIS 2.0","AI를 국가 경쟁력이자 사회 신뢰의 문제로 본다. 교육을 국가 AI 전략과 하나로 묶는다."),
  ("② 교육부 프레임워크층","MOE AIEd 4원칙","주도성(Agency)·포용(Inclusivity)·공정(Fairness)·안전(Safety)의 네 원칙. 아이는 AI를 '배우고(about)·쓰고(use)·함께 배우고(with)·넘어서(beyond)' 익힌다."),
  ("③ 학교 현장층","SLS·Code for Fun","적응형 학습(ALS)으로 개인화하되, 사이버 웰니스·코딩 수업에서 AI 편향을 의심하고 거짓 정보를 가려내는 리터러시를 함께 기른다.","S5"),
 ],
 korea5=[
  ("균형(가드레일)을 먼저","싱가포르는 4원칙으로 균형을 잡는다. 집에서도 '많이'보다 '알맞게' 쓰게 한다."),
  ("아이 생각이 숨지 않게","AI 뒤로 아이 생각이 사라지지 않도록, '네 생각 먼저 말해볼래?'를 앞에 둔다."),
  ("AI 편향을 의심하기","싱가포르가 가르치는 'AI도 편향될 수 있다'를, 집에서 '이 답 한쪽으로 치우쳤을까?'로."),
  ("안전·윤리를 함께","개인화 도구를 쓰되, 안전·윤리를 늘 같이 이야기한다."),
  ("넘어서는 힘까지","'AI로'만이 아니라 'AI 없이도' 스스로 생각하는 힘(beyond)을 남긴다."),
 ],
 sources=[
  ("S1","National AI Strategy","Smart Nation Singapore","https://www.smartnation.gov.sg/nais/"),
  ("S2","AI in Education — EdTech Masterplan","Ministry of Education Singapore","https://www.moe.gov.sg/education-in-sg/educational-technology-journey/edtech-masterplan/artificial-intelligence-in-education"),
  ("S3","AI in Education: Transforming Singapore's education with Student Learning Space","GovTech Singapore","https://www.tech.gov.sg/technews/ai-in-education-transforming-singapore-education-system-with-student-learning-space/"),
  ("S4","Foundational Gen AI Literacy and Skills for All Students, Teachers and Educators","MOE Singapore","https://www.moe.gov.sg/news/parliamentary-replies/20250925-foundational-gen-ai-literacy-and-skills-for-all-students-teachers-and-educators"),
  ("S5","AI in Education Ethics Framework","MOE — Student Learning Space","https://www.learning.moe.edu.sg/ai-in-sls/responsible-ai/ai-in-education-ethics-framework/"),
 ],
 srcnote="싱가포르를 '통제'가 아니라, 국가 전략과 교육을 잇고 네 원칙(주도성·포용·공정·안전)으로 균형을 잡는 관점으로 정리했습니다.",
 lf=dict(video_id="sg-ai-longform", title="싱가포르는 왜 아이에게 AI 가드레일을 먼저 채웠나", subtitle="네 원칙(주도성·포용·공정·안전)과 균형의 설계",
   description="싱가포르는 AI를 빨리 쓰게 하기보다, 아이 생각이 AI 뒤로 숨지 않도록 균형을 먼저 설계했습니다. 주도성·포용·공정·안전, 네 원칙이 그 가드레일이죠.\n한국 가정도 '많이'보다 '알맞게', 그리고 '네 생각 먼저'를 앞에 둘 수 있습니다."),
 shorts=[
  dict(video_id="sg-ai-short-1", copy="많이보다 알맞게", title="싱가포르는 왜 아이에게 AI를 '마음껏' 쓰게 하지 않을까?"),
  dict(video_id="sg-ai-short-2", copy="네 생각 먼저", title="AI 잘 쓰는 아이는 답보다 '이것'을 먼저 한다"),
  dict(video_id="sg-ai-short-3", copy="AI도 편향된다", title="AI교육에서 진짜 중요한 건 '속도'가 아니었다"),
 ],
)
C["korea"]=dict(slug="korea", vslug="korea-ai-education", flag="🇰🇷", pill="한국 심층",
 h1="한국은 AI교과서를 넣었다 뺐다 — 그래서 가정이 답이다",
 subtitle="AI 디지털교과서의 도입과 후퇴, 그리고 흔들리지 않는 가정 습관",
 angle="한국은 학교에 AI를 넣었다가 물러섰습니다. 정책은 요동쳐도, <span class=\"coral\">가정의 '다시 묻기' 습관은 흔들리지 않습니다.</span>",
 lf_caption="한국 편 · AI 디지털교과서의 도입과 후퇴, 가정의 답",
 tl_desc="한국의 학교 AI는 빠르게 들어왔다가 빠르게 흔들렸습니다. 그래서 가정의 역할이 더 커집니다.",
 timeline=[
  ("2023","디지털 기반 교육혁신 방안","교육부가 AI 디지털교과서 등 디지털 전환 로드맵을 발표.","S1"),
  ("2024.11","AI 디지털교과서 도입 확정","2025년 수학·영어·정보 과목에 AI 디지털교과서 도입 결정. 과몰입 우려도 함께 제기.","S2"),
  ("2025.03","AI 디지털교과서 시행","초3·4, 중1, 고1 대상 수학·영어·정보 등에서 도입. 개인화 학습 표방.","S3"),
  ("2025 여름","보조교재로 재분류","교사·학부모 반발 속에 국회가 AI 디지털교과서를 '핵심'에서 '보조' 교재로 재분류.","S4"),
  ("2025 하반기","채택률 하락","도입 학기 37%에서 다음 학기 19%로 채택률이 떨어짐.","S5"),
  ("2028 (원안)","확대 예정(불투명)","국어·사회·과학 등으로 확대가 계획됐으나, 정책 후퇴로 불투명해짐.","S3"),
 ],
 layers=[
  ("① 국가 정책층","교육부","AI 디지털교과서를 국가 주도로 빠르게 추진했으나, 준비·검증보다 속도가 앞서며 후퇴로 이어졌다."),
  ("② 입법·현장 반발층","국회·교사·학부모","디지털 과몰입·효과 논란 속에 국회가 보조교재로 재분류. 학교 현장의 도입이 학기마다 흔들렸다."),
  ("③ 가정층","우리 집","학교 정책이 요동쳐도, 아이의 생활 습관은 가정이 지킨다. '다시 묻기'는 어떤 교과서 논쟁과도 무관하게 남는다."),
 ],
 korea5=[
  ("학교는 흔들려도, 습관은 가정이","교과서 정책은 바뀐다. 하지만 아이의 '다시 묻는 습관'은 가정이 지킬 수 있다."),
  ("도구 논쟁보다 '다시 묻기'","AI교과서를 쓰든 안 쓰든, 집에서는 결과를 다시 묻는 힘을 기른다."),
  ("과몰입 대신 경계를","디지털 과몰입이 걱정이라면, 쓰는 시간과 경계를 가정이 먼저 정한다."),
  ("답을 받으면 검증부터","'이상한 부분 찾아볼까?'로 아이가 스스로 검증하게 한다."),
  ("'AI 없이 너라면?'을 자주","AI가 아이 생각을 대신하지 않도록, 'AI 없이 너라면?'을 자주 묻는다."),
 ],
 sources=[
  ("S1","Digital-driven Education Reform Plan Announced in South Korea","AACRAO","https://www.aacrao.org/edge/emergent-news/digital-driven-education-reform-plan-announced-in-south-korea"),
  ("S2","Korea to introduce AI textbooks in 2025 amid digital overuse concerns","The Korea Times","https://www.koreatimes.co.kr/southkorea/society/20241129/korea-to-introduce-ai-textbooks-in-2025-despite-concerns-over-effectiveness-digital-overuse"),
  ("S3","Briefing on the Plan for AI Digital Textbooks","Ministry of Education (Korea)","https://english.moe.go.kr/boardCnts/viewRenewal.do?boardID=254&boardSeq=95291&lev=0&m=0202"),
  ("S4","South Korea slows down on AI education","Friedrich Naumann Foundation","https://www.freiheit.org/north-and-south-korea/south-korea-slows-down-ai-education"),
  ("S5","South Korea's AI textbooks fail after rushed rollout","Rest of World","https://restofworld.org/2025/south-korea-ai-textbook/"),
 ],
 srcnote="한국을 비하하지 않고, AI 디지털교과서의 도입과 후퇴라는 사실을 근거로, 학교 정책의 흔들림 속에서 가정이 할 수 있는 일을 정리했습니다.",
 lf=dict(video_id="korea-ai-longform", title="한국은 AI교과서를 넣었다 뺐다, 그래서 가정이 답이다", subtitle="AI 디지털교과서의 도입과 후퇴, 그리고 가정의 답",
   description="한국은 AI 디지털교과서를 학교에 넣었다가, 넉 달 만에 보조교재로 물러섰습니다. 정책은 요동쳤죠.\n하지만 어떤 교과서 논쟁과도 무관하게, 아이의 '다시 묻는 힘'은 가정이 지킬 수 있습니다."),
 shorts=[
  dict(video_id="korea-lost-decade-m3", copy="학교는 흔들려도 가정이", title="우리 아이 AI교육, 학교만 믿어도 될까?"),
  dict(video_id="korea-lost-decade-v2", copy="다시 묻는 힘", title="AI에게 정답을 빨리 받는 게, 왜 위험할까?"),
  dict(video_id="korea-lost-decade", copy="AI 없이 너라면?", title="AI 시대, 한국 부모가 오늘 딱 하나 한다면?"),
 ],
)
C["germany"]=dict(slug="germany", vslug="germany-ai-education", flag="🇩🇪", pill="독일 심층",
 h1="독일은 왜 AI보다 '신뢰와 기반'을 먼저 깔았나",
 subtitle="디지털팍트로 인프라·교사부터, 프라이버시를 앞세운 분권형",
 angle="미국처럼 연방·주로 나뉜 분권형이지만, 독일은 <span class=\"coral\">프라이버시와 신뢰를 먼저 세우고 인프라·교사부터</span> 다집니다.",
 lf_caption="독일 편 · 인프라·교사·프라이버시를 먼저",
 tl_desc="독일은 화려한 AI 커리큘럼보다, 학교의 기반과 교사, 그리고 데이터 신뢰를 먼저 놓았습니다.",
 timeline=[
  ("2019","디지털팍트 슐레","연방과 주가 함께 65억 유로를 투입해 학교 디지털 인프라·교사 연수에 착수. 역사상 최대 규모.","S1"),
  ("2019~2024","최대 규모 디지털 투자","기기·네트워크 등 기반을 전국 학교에 깔며 토대를 마련.","S1"),
  ("상시","GDPR·EU AI법","아동 데이터 보호와 투명성의 강한 규칙이 AI 도입의 전제.","S2"),
  ("표준","정보(Informatik) 교육 표준","하위·상위 중등 정보 표준으로 프로그래밍·데이터·기술 이해의 틀 마련.","S3"),
  ("2025~2030","디지털팍트 2.0","약 59억 달러 규모로 유지·지원·현대적 학습환경까지 포함해 확장.","S4"),
 ],
 layers=[
  ("① 연방 (Bund)","디지털팍트","예산과 인프라, 방향을 지원한다. 다만 교육 내용은 직접 정하지 않는다."),
  ("② 주 (Länder)","교육 주권","교육은 주의 권한. 정보(Informatik) 교과와 시수, AI 도입 속도는 주마다 다르다."),
  ("③ 학교·교사","현장","깔린 인프라 위에서 실제로 쓴다. 교사의 AI 역량 연수가 최대 관건이며 도시·농촌 격차가 과제다.","S5"),
 ],
 korea5=[
  ("기술보다 신뢰를 먼저","독일은 데이터 보호·신뢰를 앞세웠다. 집에서도 '무엇을 AI에 알려줘도 되는지'부터 정한다."),
  ("기반부터 탄탄히","화려함보다 기반. 집에서도 도구보다 '왜 그렇게 되는지' 원리를 먼저."),
  ("서두르지 않기","독일도 전국 필수화를 서두르지 않았다. 집에서도 '많이'보다 '탄탄하게'."),
  ("결정은 사람에게","분권형이라도 판단은 사람 몫. 마지막 선택은 아이가 하게 한다."),
  ("안전을 습관으로","개인정보 안전을 늘 대화의 기본으로 둔다."),
 ],
 sources=[
  ("S1","DigitalPakt Schule — largest joint investment in digital education","Eurydice (EU)","https://eurydice.eacea.ec.europa.eu/news/germany-digital-pact-20-expands-digital-education-infrastructure"),
  ("S2","Germany — AI in Education","U.S. Commerce (trade.gov)","https://www.trade.gov/market-intelligence/germany-ai-education"),
  ("S3","New Standards for Lower Secondary Education in Informatics in Germany","Springer","https://link.springer.com/chapter/10.1007/978-3-032-01222-7_1"),
  ("S4","Digital Pact 2.0 expands digital education infrastructure","Eurydice (EU)","https://eurydice.eacea.ec.europa.eu/news/germany-digital-pact-20-expands-digital-education-infrastructure"),
  ("S5","What is Germany's digital pact for schools","The Local","https://www.thelocal.de/20240516/what-is-germanys-digital-pact-for-schools-and-how-does-it-affect-pupils"),
 ],
 srcnote="독일을 '느린 나라'로 단순화하지 않고, 연방·주 분권 속에서 프라이버시·신뢰·기반을 먼저 세우는 접근으로 정리했습니다.",
 lf=dict(video_id="germany-ai-longform", title="독일은 왜 AI보다 신뢰와 기반을 먼저 깔았나", subtitle="디지털팍트로 인프라·교사부터, 프라이버시를 앞세운 분권형",
   description="독일은 화려한 AI 커리큘럼보다 인프라와 교사, 데이터 신뢰를 먼저 놓았습니다. 한국 가정도 기술보다 안전과 기반을 먼저 세울 수 있습니다.\n\n▶ 심층 페이지: https://ai-early-education.pages.dev/world-cases/germany"),
 shorts=[
  dict(video_id="germany-ai-short-1", copy="신뢰를 먼저", title="독일은 왜 AI보다 '이것'을 먼저 깔았을까?"),
  dict(video_id="germany-ai-short-2", copy="기반부터 탄탄히", title="우리 아이가 AI에 개인정보를 넣고 있다면?"),
  dict(video_id="germany-ai-short-3", copy="안전을 습관으로", title="AI를 안전하게 쓰는 아이들은 이것부터 다르다"),
 ],
)
C["japan"]=dict(slug="japan", vslug="japan-ai-education", flag="🇯🇵", pill="일본 심층",
 h1="일본은 왜 기기와 프로그래밍을 먼저 깔았나",
 subtitle="GIGA 1인 1기기 + 프로그래밍 필수, 생성형 AI는 비판적으로",
 angle="일본은 <span class=\"coral\">기기와 프로그래밍을 먼저 깔고(GIGA), 생성형 AI는 비판적 사고로</span> 신중하게 다룹니다.",
 lf_caption="일본 편 · GIGA 1인 1기기와 프로그래밍, 비판적 AI",
 tl_desc="일본은 AI를 서두르기 전에, 기기와 논리적 사고(프로그래밍)의 토대를 먼저 전국에 깔았습니다.",
 timeline=[
  ("2019","GIGA 스쿨","약 2.3조 엔을 투입해 2023년까지 초·중학생 1인 1기기와 고속망을 구축.","S1"),
  ("2020","프로그래밍 초등 필수","초등 5학년부터 프로그래밍 필수화. 산수·과학 속에서 논리적 사고로 배운다.","S2"),
  ("2023","생성형 AI 가이드","MEXT가 학교의 생성형 AI 사용 가이드 발표. 비판적 사용이 핵심.","S3"),
  ("2025","AI 추진법 + 교사 연수","AI 추진법과 'AI교육 액셀러레이터'로 교사 약 5만 명 연수.","S4"),
  ("2025","가이드 개정","프라이버시(APPI)·공정성·투명성을 강화해 개정.","S3"),
 ],
 layers=[
  ("① 국가 (MEXT)","방향·가이드","GIGA·프로그래밍 필수·생성형 AI 가이드로 큰 방향을 정한다."),
  ("② 인프라 (GIGA)","1인 1기기","전국 초·중학생에게 기기와 고속망을 먼저 깔아 기반을 만들었다."),
  ("③ 교실","교과 접목","별도 AI 과목이 아니라 산수·과학·통합학습에 프로그래밍을 녹이고, 생성형 AI는 비판적으로 쓴다.","S5"),
 ],
 korea5=[
  ("논리적 사고를 먼저","일본은 프로그래밍으로 '순서대로 생각하는 힘'을 길렀다. 집에서도 '어떤 순서로?'를 먼저."),
  ("기기보다 활용","기기를 깔되 중요한 건 활용. 집에서도 도구보다 '무엇을 위해 쓰는지'."),
  ("비판적으로 검증","일본이 강조한 'AI 출력 검증'을, 집에서 '이거 진짜일까?'로."),
  ("시행착오를 격려","원하는 결과를 끌어내려 이리저리 해보는 과정을 칭찬한다."),
  ("윤리도 함께","얼굴인식 같은 사례처럼 '이래도 될까?'를 아이와 이야기한다."),
 ],
 sources=[
  ("S1","Japan's GIGA School Program — ICT in Schools","The Government of Japan","https://www.japan.go.jp/kizuna/2021/04/ict_in_schools.html"),
  ("S2","Japan Makes Coding Mandatory Starting in Elementary School","Strata-gee","https://www.strata-gee.com/japan-makes-coding-mandatory-for-all-students-starting-in-elementary-school/"),
  ("S3","Guideline for the Use of Generative AI in Primary and Secondary Schools","MEXT (Japan)","https://www.mext.go.jp/content/20250422-mxt_shuukyo01-000030823_001.pdf"),
  ("S4","New School Guidelines in Japan emphasize AI education","The AI Track","https://theaitrack.com/school-guidelines-in-japan-ai-education/"),
  ("S5","ICT in Schools Equips Students with Life Skills","The Government of Japan","https://www.japan.go.jp/kizuna/2021/04/ict_in_schools.html"),
 ],
 srcnote="일본을 '기술 강국'으로만 보지 않고, 기기·논리적 사고를 먼저 깔고 생성형 AI는 비판적 사고로 신중히 다루는 접근으로 정리했습니다.",
 lf=dict(video_id="japan-ai-longform", title="일본은 왜 기기와 프로그래밍을 먼저 깔았나", subtitle="GIGA 1인 1기기 + 프로그래밍 필수, 생성형 AI는 비판적으로",
   description="일본은 AI를 서두르기 전에 기기와 논리적 사고의 토대를 먼저 깔았습니다. 한국 가정도 '순서대로 생각하기'부터, AI는 그다음 비판적으로.\n\n▶ 심층 페이지: https://ai-early-education.pages.dev/world-cases/japan"),
 shorts=[
  dict(video_id="japan-ai-short-1", copy="논리적 사고 먼저", title="일본은 왜 아이에게 AI를 '나중에' 가르칠까?"),
  dict(video_id="japan-ai-short-2", copy="AI 출력 검증", title="AI 답 그대로 믿는 아이 vs 의심하는 아이, 뭐가 다를까?"),
  dict(video_id="japan-ai-short-3", copy="순서대로 생각하기", title="아이에게 AI를 시키기 전, 순서가 있다?"),
 ],
)

def render(cfg):
    tl="".join(f"""<div class="tl-item"><div class="tl-year">{y}</div><div class="tl-body"><h4>{t}</h4><p>{d} <span class="src">[{s}]</span></p></div></div>""" for y,t,d,s in cfg["timeline"])
    layers="".join(f"""<div class="card"><div class="lyr-h">{L[0]}<span>{L[1]}</span></div><p>{L[2]}{(' <span class=\"src\">['+L[3]+']</span>') if len(L)>3 else ''}</p></div>""" for L in cfg["layers"])
    k5="".join(f"""<div class="card phil"><div class="pic">🏠</div><div><h4>{t}</h4><p>{d}</p></div></div>""" for t,d in cfg["korea5"])
    eff="".join(f"""<div class="card phil"><div class="pic">{ic}</div><div><h4>{t}</h4><p>{d}</p></div></div>""" for ic,t,d in EFFECTS)
    qs="".join(f"<li>{q}</li>" for q in Q10)
    scards="".join(f"""<a class="card country" href="/videos/{cfg['vslug']}.html">
<div class="thumb" style="aspect-ratio:9/16;max-height:280px">{embed(s['video_id'],s['title'])}</div>
<div class="body"><div class="flag">📱 {s['copy']}</div><p>{s['title']}</p></div></a>""" for s in cfg["shorts"])
    srcs="".join(f'<li><a href="{u}" target="_blank" rel="noopener">{pub} — {t}</a> <span class="src">[{i}]</span></li>' for i,t,pub,u in cfg["sources"])
    lf=cfg["lf"]
    body=f"""<main>
{CR.side_rail(cfg['slug'],f"/world-cases/{cfg['slug']}.html")}
<section class="page-hero"><div class="wrap">
{CR.breadcrumb(cfg['slug'],"1편 · 정책과 방침")}
<div class="pill">{cfg['flag']} 세계 사례 · {cfg['pill']}</div>
<h1 style="font-size:34px">{cfg['h1']}</h1>
<p class="sub">{cfg['subtitle']}</p>
<p style="max-width:780px;color:var(--navy2);font-weight:600">{cfg['angle']}</p>
{episode_nav(cfg['slug'],"1")}
</div></section>

<section class="block" style="padding-top:12px"><div class="wrap">
{embed(lf['video_id'],lf['title'])}
<p class="center" style="margin-top:12px;color:var(--muted)">{cfg['lf_caption']}</p>
</div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">타임라인 · 흐름으로 본다</h2>
<p class="sec-desc">{cfg['tl_desc']}</p>
<div class="timeline">{tl}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">운영 구조 · 세 층으로 본다</h2>
<div class="grid g3">{layers}</div></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">한국 가정에서 배울 점</h2>
<p class="sec-desc">나라의 방식은 달라도, 향하는 곳은 같습니다 — 아이가 스스로 다시 묻는 힘.</p>
<div class="grid g3">{k5}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">그럼, 아이에게 무엇이 생기나</h2>
<p class="sec-desc">'다시 묻기' 습관 하나가 아이를 바꿉니다. 나라가 제도로 기른 힘을, 우리는 집에서 이렇게 기릅니다.</p>
<div class="grid g3">{eff}</div></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">부모가 아이와 해볼 질문 10</h2>
<ol class="qlist">{qs}</ol></div></section>

<section class="block"><div class="wrap">
<h2 class="sec-title">쇼츠로 빠르게</h2>
<div class="grid g5">{scards}</div></div></section>

<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title" style="font-size:22px">출처</h2>
<p class="sec-desc">{cfg['srcnote']}</p>
<ul class="srclist">{srcs}</ul></div></section>


</main>"""
    return BS.page("cases","../",f"{cfg['h1']} | AI 조기교육",f"{cfg['subtitle']} — {cfg['h1']}",body)

def video_detail(cfg):
    lf=cfg["lf"]
    scards="".join(f"""<a class="card" href="#" style="pointer-events:none"><div class="thumb" style="aspect-ratio:9/16;max-height:320px;overflow:hidden;border-radius:12px">{embed(s['video_id'],s['title'])}</div>
<p style="margin-top:8px;font-size:14px;font-weight:600">{s['title']}</p></a>""" for s in cfg["shorts"])
    body=f"""<main>
<section class="block" style="padding-top:22px"><div class="wrap">
<p style="color:var(--muted);font-size:14px"><a href="/videos.html">영상관</a> › {cfg['pill'].replace(' 심층','')} AI교육</p>
{embed(lf['video_id'],lf['title'])}
<h1 style="margin-top:18px">{lf['title']}</h1>
<p style="color:var(--navy2);font-weight:600">{lf['subtitle']}</p>
<p style="white-space:pre-line;color:var(--ink)">{lf['description']}</p>
<a class="btn btn-primary" href="/world-cases/{cfg['slug']}.html">{cfg['pill'].replace(' 심층','')} 편 심층 페이지 보기 →</a>
</div></section>
<section class="block" style="background:var(--cream2)"><div class="wrap">
<h2 class="sec-title">이 주제의 쇼츠</h2>
<div class="grid g5">{scards}</div></div></section>
</main>"""
    return BS.page("cases","../",f"{lf['title']} | 영상",lf['subtitle'],body)

NAMES={"china":("중국","🇨🇳"),"usa":("미국","🇺🇸"),"uk":("영국","🇬🇧"),"singapore":("싱가포르","🇸🇬"),"korea":("한국","🇰🇷"),"germany":("독일","🇩🇪"),"japan":("일본","🇯🇵")}
def episode_nav(slug,current):
    name,flag=NAMES[slug]
    eps=[("1","정책·방침",f"/world-cases/{slug}.html"),("2","실제 교실 운영",f"/world-cases/{slug}-2.html"),("3","우리 집 주간 적용",f"/world-cases/{slug}-3.html")]
    out=[]
    for n,t,href in eps:
        on = (n==current)
        base="display:inline-block;border-radius:20px;padding:7px 15px;font-size:13px;font-weight:700;text-decoration:none;border:1.5px solid"
        if href and not on: out.append(f'<a href="{href}" style="{base} #E4D8C4;color:#8a6f45;background:#fff">{n}편 · {t}</a>')
        elif on: out.append(f'<span style="{base} #E0684A;color:#fff;background:#E0684A">{n}편 · {t}</span>')
        else: out.append(f'<span style="{base} #eadfca;color:#b9a98c;background:#faf5ea">{n}편 · {t} · 준비중</span>')
    return '<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">'+''.join(out)+'</div>'
def practice_page(slug):
    name,flag=NAMES[slug]
    body=f"""<main>
{CR.side_rail(slug,f"/world-cases/{slug}-2.html")}
<section class="page-hero"><div class="wrap">
{CR.breadcrumb(slug,"2편 · 실제 교실 운영")}
<div class="pill">{flag} 세계 사례 · {name} 2편</div>
<h1 style="font-size:32px">{name}은 <span class="coral">실제로</span> 어떻게 가르치나</h1>
<p class="sub">정책을 넘어 — 학년별로, 매주, 교실에서 실제로 돌아가는 방식</p>
{episode_nav(slug,"2")}
</div></section>
{CR.reality_html(slug)}
</main>"""
    return BS.page("cases","../",f"{name}은 실제로 어떻게 가르치나 · 2편 | AI 조기교육",f"{name}의 실제 교실 운영 — 학년별·주간 수업 방식과 도구. 세계 AI교육법 시리즈 2편.",body)
def apply_page(slug):
    name,flag=NAMES[slug]
    body=f"""<main>
{CR.side_rail(slug,f"/world-cases/{slug}-3.html")}
<section class="page-hero"><div class="wrap">
{CR.breadcrumb(slug,"3편 · 우리 집 주간 적용")}
<div class="pill">{flag} 세계 사례 · {name} 3편</div>
<h1 style="font-size:32px">{name} 방식, <span class="coral">우리 집</span>에 이렇게</h1>
<p class="sub">세계의 방법을 우리 아이의 한 주 습관으로 — 저녁 대화 10분이면 충분합니다</p>
{episode_nav(slug,"3")}
</div></section>
{CR.apply_html(slug)}
</main>"""
    return BS.page("cases","../",f"{name} 방식, 우리 집에 이렇게 · 3편 | AI 조기교육",f"{name}의 AI교육 방식을 우리 아이 주간 습관으로. 요일별 루틴과 무료 자료. 세계 AI교육법 시리즈 3편.",body)
def year_page(slug):
    name,flag=NAMES[slug]
    body=f"""<main>
{CR.side_rail(slug,f"/world-cases/{slug}-year.html")}
<section class="page-hero"><div class="wrap">
{CR.breadcrumb(slug,"1년 커리큘럼")}
<div class="pill">{flag} 세계 사례 · {name} 심화</div>
<h1 style="font-size:31px">{name}은 <span class="coral">1년 동안 매주</span> 이렇게 가르친다</h1>
<p class="sub">실제 공개된 커리큘럼으로 따라가는, 학년 한 해의 주차별 수업</p>
{episode_nav(slug,"2")}
</div></section>
{CR.year_html(slug)}
<section class="block" style="background:var(--cream2)"><div class="wrap"><div class="cta-band" style="background:linear-gradient(135deg,#E6F4EA,#D3EFDC)">
<div><h3>🏠 그래서, 집에서는 어떻게? · 실전판</h3><p>커리큘럼을 아는 것과, 집에서 실제로 가르치는 건 다릅니다. 이 1년 과정을 단원마다 <b>집에서 따라하는 활동</b>으로 바꿨어요.</p></div>
<a class="btn btn-lg" href="/world-cases/{slug}-home.html">집 실전판 보기 →</a></div></div></section>
</main>"""
    return BS.page("cases","../",f"{name}은 1년 동안 매주 이렇게 가르친다 | AI 조기교육",f"{name}의 학년 한 해 주차별 커리큘럼(실제 공개 자료). 세계 AI교육법 심화편.",body)
def homeyear_page(slug):
    name,flag=NAMES[slug]
    body=f"""<main>
{CR.side_rail(slug,f"/world-cases/{slug}-home.html")}
<section class="page-hero"><div class="wrap">
{CR.breadcrumb(slug,"집 실전판")}
<div class="pill">{flag} 세계 사례 · {name} 집 실전판</div>
<h1 style="font-size:31px">{name} 1년 과정, <span class="coral">우리 집</span>에서 이렇게 따라한다</h1>
<p class="sub">책에 든 커리큘럼을, 우리 아이에게 실제로 가르치는 구체적 방법</p>
{episode_nav(slug,"3")}
</div></section>
{CR.homeyear_html(slug)}
</main>"""
    return BS.page("cases","../",f"{name} 1년 과정, 우리 집에서 이렇게 따라한다 | AI 조기교육",f"{name}의 학년 1년 커리큘럼을 집에서 단원별로 따라하는 구체 활동. 세계 AI교육법 집 실전판.",body)
def write_all_practice():
    for slug in NAMES:
        BS.write(f"world-cases/{slug}-2.html",practice_page(slug))
        BS.write(f"world-cases/{slug}-3.html",apply_page(slug))
        if slug in CR.YEAR:
            BS.write(f"world-cases/{slug}-year.html",year_page(slug))
        if slug in CR.HOMEYEAR:
            BS.write(f"world-cases/{slug}-home.html",homeyear_page(slug))
        if slug in CR.ROADMAP:
            BS.write(f"world-cases/{slug}-roadmap.html",roadmap_page(slug))
        if slug in CR.PROG12:
            BS.write(f"world-cases/{slug}-8yo-12weeks.html",program_page(slug))
            BS.write(f"free/{slug}-12weeks-workbook.html",program_workbook(slug))
    print("2편·3편(+1년 커리큘럼·집 실전판·학년별 로드맵·12주 프로그램·워크북) 생성 완료")
def program_workbook(slug):
    """12주 워크북 뷰어 — 상단 고정바 + 좌측 주차 목차(sticky·scroll-spy) + 중앙 A4 문서 + 우측 빠른작업.
    인쇄 시 문서만 출력(@media print). 데이터=CR.PROG12."""
    p=CR.PROG12[slug]; name,flag=NAMES[slug]
    EXTRA={1:("아이가 순서를 빠뜨리지 않고 말했나요?","한 단계만 더 잘게 쪼개서 다시 말해볼까?"),
     2:("틀린 곳을 스스로 찾았나요?","어디를 고치면 될지 네 말로 다시 말해줄래?"),
     3:("반복되는 부분을 묶어서 말했나요?","'3번 반복'처럼 한 번에 말해볼까?"),
     4:("'만약 ~라면'을 써서 말했나요?","다른 경우라면 어떻게 할지 하나만 더 정해볼까?"),
     5:("고양이가 아이 명령대로 움직였나요?","걸음 수를 바꾸면 어떻게 될까? 바꿔서 다시 해볼까?"),
     6:("원하는 말과 소리가 나왔나요?","다른 말로 바꿔서 다시 시켜볼까?"),
     7:("캐릭터가 계속 움직이나요?","더 빠르게(느리게) 하려면 뭘 고칠까?"),
     8:("점수가 잘 올라가나요?","더 재밌게 만들 한 가지를 정해 다시 바꿔볼까?"),
     9:("표와 그래프가 맞게 그려졌나요?","다른 질문으로 한 번 더 조사해볼까?"),
     10:("나눈 규칙을 말로 설명했나요?","헷갈리는 카드 하나로 규칙을 다시 정해볼까?"),
     11:("'어떻게 아는지' 추측을 말했나요?","다른 AI를 찾아 같은 질문을 해볼까?"),
     12:("이상한 부분을 하나 찾았나요?","'이렇게 바꿔줘'라고 정확히 다시 말해볼까?")}
    SITE_HEADER=BS.header("free","../")
    SITE_FOOTER=BS.footer("../").replace("</body></html>","")
    FREETOC="".join(
        (f'<a class="wt-a{" on" if u=="/free/uk-12weeks-workbook.html" else ""}" href="{u}">{lb}</a>' if u else f'<span class="wt-a" style="color:#c4b59a">{lb} <small style="font-size:9.5px">준비중</small></span>')
        for lb,u in BS.FREE_ITEMS)
    part_of=lambda n:"3부 · 데이터와 AI 생각" if n>=9 else("2부 · 직접 만들기" if n>=5 else "1부 · 컴퓨팅적 사고")
    weeks=p["weeks"]
    # 좌측 목차
    toc='<a class="wt-a" href="#intro">시작 안내</a>'
    toc+="".join(f'<a class="wt-a" href="#wk{w[0]}" data-w="{w[0]}"><span class="wt-n">{w[0]}</span>{w[1]}</a>' for w in weeks)
    toc+='<a class="wt-a" href="#done">마무리 · 수료</a>'
    # 모바일 주차 선택
    opts='<option value="intro">시작 안내</option>'+"".join(f'<option value="wk{w[0]}">{w[0]}주 · {w[1]}</option>' for w in weeks)+'<option value="done">마무리 · 수료</option>'
    # 주차 카드
    cards=""
    for i,w in enumerate(weeks):
        n=w[0]; chk,reask=EXTRA[n]
        prv=f'<a class="wn-btn" href="#wk{n-1}">← {n-1}주 {weeks[i-1][1]}</a>' if i>0 else f'<a class="wn-btn" href="#intro">← 시작 안내</a>'
        nxt=f'<a class="wn-btn nx" href="#wk{n+1}">다음 · {n+1}주 {weeks[i+1][1]} →</a>' if i<len(weeks)-1 else '<a class="wn-btn nx" href="#done">마무리 · 수료 →</a>'
        prompt_row=('<div class="wb-row"><b>💡 예시 프롬프트</b><span>"우주에서 피아노 치는 고양이를 그려줘" → 결과를 보고 → "배경을 바닷속으로 바꿔줘"</span></div>' if n==12 else '')
        cards+=f"""<section class="wb-card" id="wk{n}">
<header class="wb-h no-print" onclick="this.parentElement.classList.toggle('fold')">
<span class="wb-badge">{n}주</span><div><small>{part_of(n)}</small><h2>{w[1]}</h2></div><span class="wb-fold">▾</span></header>
<div class="wb-h print-only"><span class="wb-badge">{n}주</span><div><small>{part_of(n)}</small><h2>{w[1]}</h2></div></div>
<div class="wb-body">
<div class="wb-row"><b>🎯 이번 주 목표</b><span>{w[2]}</span></div>
<div class="wb-row"><b>🧰 준비물</b><span>{w[3].replace('준비물: ','')}</span></div>
<div class="wb-say">💬 <b>부모가 이렇게 물어봐요</b> — "{w[4]}"</div>
{prompt_row}
<div class="wb-row"><b>👀 결과를 보고 체크</b><span>{chk}</span></div>
<div class="wb-row"><b>🔁 다시 묻기 문장</b><span>"{reask}"</span></div>
<div class="wb-rec"><div class="wb-rl">✍️ 우리가 한 것 · 발견한 것</div><div class="wb-lines"></div></div>
<div class="wb-why">🔗 왜 하나요 — {w[5]}</div>
<div class="wb-nav no-print">{prv}{nxt}</div>
</div></section>"""
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>만 8세 12주 홈 프로그램 워크북 | AI 조기교육</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">
<link rel="stylesheet" href="../styles/main.css">
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#F6EEDF;font-family:"Pretendard","Malgun Gothic",sans-serif;color:#2B2016;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
a{{color:inherit}}
.wbv-top{{position:sticky;top:57px;z-index:60;background:#fff;border-bottom:1px solid #EADFCE;box-shadow:0 2px 8px rgba(0,0,0,.06);display:flex;align-items:center;gap:14px;padding:9px 16px;flex-wrap:wrap}}
.wbv-top a,.wbv-top button{{text-decoration:none;font-weight:700;font-size:12.8px;color:#5a4a35;background:#fff;border:1px solid #EADFCE;border-radius:9px;padding:7px 11px;cursor:pointer}}
.wbv-top a:hover,.wbv-top button:hover{{background:#FBF3E4}}
.wbv-title{{margin:0 auto;font-weight:900;font-size:14.5px;color:#2B3A55}}
.wbv-top .pri{{background:#E0684A;color:#fff;border-color:#E0684A}}
.wbv-grid{{max-width:1280px;margin:0 auto;padding:18px 16px;display:flex;gap:20px;align-items:flex-start}}
.wbv-toc{{width:216px;flex:none;position:sticky;top:122px;background:#FFF9EF;border:1px solid #EAD9BE;border-radius:14px;padding:12px 8px;max-height:calc(100vh - 142px);overflow:auto}}
.wt-t{{font-weight:800;font-size:13.5px;color:#2B3A55;padding:4px 10px 9px;border-bottom:2px solid #F0E6D2;margin-bottom:6px}}
.wt-a{{display:flex;align-items:center;gap:7px;padding:6px 9px;margin:1px 0;border-radius:8px;text-decoration:none;color:#5a4a35;font-size:12.4px;font-weight:600}}
.wt-a:hover{{background:#FDECE5}}
.wt-a.on{{background:#E0684A;color:#fff}}
.wt-n{{width:20px;height:20px;border-radius:50%;background:#F0E6D2;color:#8a6f45;display:grid;place-items:center;font-size:10.5px;font-weight:900;flex:none}}
.wt-a.on .wt-n{{background:#fff;color:#E0684A}}
.wbv-doc{{flex:1;min-width:0;max-width:820px;margin:0 auto}}
.wbv-quick{{width:172px;flex:none;position:sticky;top:122px}}
.wq{{background:#FFF9EF;border:1px solid #EAD9BE;border-radius:14px;padding:12px 10px}}
.wq-t{{font-weight:800;font-size:12.5px;color:#2B3A55;margin-bottom:8px}}
.wq a,.wq button{{display:block;width:100%;text-align:left;margin:4px 0;padding:8px 10px;border:1px solid #EADFCE;border-radius:9px;background:#fff;font-size:12px;font-weight:700;color:#5a4a35;text-decoration:none;cursor:pointer}}
.wq a:hover,.wq button:hover{{background:#FDECE5}}
.wb-card{{background:#fff;border:1px solid #EADFCE;border-radius:14px;box-shadow:0 3px 10px rgba(43,32,22,.06);margin-bottom:16px;overflow:hidden}}
.wb-h{{display:flex;align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid #F5EDE0;cursor:pointer}}
.wb-h small{{color:#9b8a6e;font-weight:700;font-size:11px}}
.wb-h h2{{margin:1px 0 0;font-size:18px}}
.wb-badge{{width:44px;height:44px;border-radius:13px;background:#E0684A;color:#fff;display:grid;place-items:center;font-weight:900;font-size:14px;flex:none}}
.wb-fold{{margin-left:auto;color:#c4b59a;transition:transform .15s}}
.wb-card.fold .wb-body{{display:none}}
.wb-card.fold .wb-fold{{transform:rotate(-90deg)}}
.wb-body{{padding:16px 22px 18px}}
.wb-row{{display:flex;gap:10px;padding:6px 0;font-size:13.8px;line-height:1.55}}
.wb-row b{{flex:none;width:132px;color:#2B3A55;font-size:12.8px}}
.wb-say{{background:#EEF7EF;border:1px solid #cfe6d6;border-radius:10px;padding:10px 14px;margin:8px 0;font-size:13.8px}}
.wb-rec{{margin:10px 0 4px}}
.wb-rl{{font-weight:800;font-size:12.8px;margin-bottom:5px}}
.wb-lines{{height:74px;background-image:repeating-linear-gradient(#fff,#fff 23px,#D8C9AE 24px,#fff 25px);border:1.5px solid #E4D8C4;border-radius:9px}}
.wb-why{{font-size:11.5px;color:#9b8a6e;border-top:1px solid #f2ecdf;padding-top:8px;margin-top:8px}}
.wb-nav{{display:flex;justify-content:space-between;gap:10px;margin-top:12px;flex-wrap:wrap}}
.wn-btn{{text-decoration:none;font-size:12px;font-weight:700;color:#8a6f45;border:1px solid #EADFCE;border-radius:9px;padding:7px 11px}}
.wn-btn.nx{{color:#fff;background:#E0684A;border-color:#E0684A}}
.wb-intro img{{width:100%;height:230px;object-fit:cover;display:block}}
.wb-intro .in{{padding:18px 22px}}
.wb-track{{display:flex;gap:5px;flex-wrap:wrap;margin-top:10px}}
.wb-track span{{width:30px;height:30px;border:2px solid #E0684A;color:#E0684A;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:12.5px}}
.wb-sel{{display:none;margin:0 16px 4px;padding:10px;border:1.5px solid #E0684A;border-radius:10px;font:inherit;width:calc(100% - 32px);background:#fff}}
#wbTop{{position:fixed;right:18px;bottom:18px;z-index:70;background:#2B3A55;color:#fff;border:0;border-radius:50%;width:44px;height:44px;font-size:17px;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25)}}
.print-only{{display:none}}
@media(max-width:1060px){{.wbv-quick{{display:none}}}}
@media(max-width:840px){{.wbv-toc{{display:none}}.wb-sel{{display:block}}.wbv-title{{display:none}}}}
@page{{size:A4;margin:12mm}}
@media print{{
.no-print,.wbv-top,.wbv-toc,.wbv-quick,#wbTop,.wb-sel,header.mgh,footer.site,.mg-mob,.mg-dd{{display:none!important}}
.print-only{{display:flex}}
body{{background:#fff}}
.wbv-grid{{padding:0;display:block}}
.wbv-doc{{max-width:none}}
.wb-card{{box-shadow:none;border:0;border-radius:0;margin:0;break-after:page}}
.wb-card:last-of-type{{break-after:auto}}
.wb-card.fold .wb-body{{display:block}}
}}
</style></head><body>
{SITE_HEADER}
<div class="wbv-top no-print">
<a href="/free-kit.html">← 무료 자료</a>
<a href="/world-cases/{slug}-8yo-12weeks.html">12주 홈 프로그램</a>
<span class="wbv-title">📘 만 8세 초등 · 12주 홈 프로그램 워크북</span>
<button onclick="wbAll()">전체 접기/펼치기</button>
<button class="pri" onclick="window.print()">🖨 인쇄 / PDF 저장</button>
<a href="/start-guide.html">시작 가이드</a>
<a href="/parent-resources.html">자료실</a>
</div>
<select class="wb-sel no-print" onchange="location.hash=this.value">{opts}</select>
<div class="wbv-grid">
<aside class="wbv-toc no-print"><div class="wt-t">📚 12주 목차</div>{toc}<div class="wt-t" style="margin-top:14px">📥 무료 자료</div>{FREETOC}</aside>
<main class="wbv-doc">
<section class="wb-card wb-intro" id="intro">
<img src="/assets/program/workbook-cover.png" alt="아이와 부모가 함께 배우는 모습">
<div class="in"><h1 style="margin:0 0 6px;font-size:23px">만 8세 초등 · 12주 홈 프로그램</h1>
<p style="margin:0;color:#7c6a4d;font-size:13.5px">영국 KS2 방식을 우리 집에서 · 주 1회 15분 · 대부분 무료</p>
<div class="wb-say" style="margin-top:12px"><b>이렇게 쓰세요</b> — 매주 한 장씩 아이와 함께 하고, '우리가 한 것'을 적어요. 결과물이 아니라 <b>함께 해보고 다시 묻는 과정</b>이 목표. 한 주를 마치면 아래 번호를 색칠!</div>
<div class="wb-track">{"".join(f"<span>{i}</span>" for i in range(1,13))}</div>
</div></section>
{cards}
<section class="wb-card" id="done"><div class="wb-body" style="text-align:center;padding:34px 22px">
<div style="font-size:52px">🎓</div><h2 style="margin:8px 0">12주, 정말 잘했어요!</h2>
<p style="color:#7c6a4d;font-size:13.5px">순서대로 생각하고, 스스로 만들고, AI에게 '다시 묻는' 힘의 씨앗을 가졌어요.</p>
<p style="margin-top:14px;font-weight:700">🏅 수료 · 이름 ____________ &nbsp;· 가장 재미있던 주 ___주</p>
<p style="color:#9b8a6e;font-size:11.5px;margin-top:16px">© 2026 AI조기교육 · ai-early-education.pages.dev</p>
</div></section>
</main>
<aside class="wbv-quick no-print"><div class="wq"><div class="wq-t">⚡ 바로 하기</div>
<button onclick="window.print()">🖨 인쇄 · PDF 저장</button>
<a href="/free/question-cards.html" target="_blank" rel="noopener">🃏 질문 카드 보기</a>
<a href="/free/first-prompts.html" target="_blank" rel="noopener">💡 프롬프트 20개</a>
<a href="/free/worksheet.html" target="_blank" rel="noopener">📝 대화 연습지</a>
<a href="/start-guide.html">🚀 시작 가이드</a>
</div></aside>
</div>
<button id="wbTop" class="no-print" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" title="위로">↑</button>
<script>
function wbAll(){{var cs=document.querySelectorAll('.wb-card:not(.wb-intro)');var anyOpen=[...cs].some(function(c){{return !c.classList.contains('fold')&&c.id!=='done';}});
 cs.forEach(function(c){{if(c.id!=='done')c.classList.toggle('fold',anyOpen);}});}}
(function(){{var secs=[...document.querySelectorAll('.wb-card[id]')];var links=[...document.querySelectorAll('.wt-a')];
function spy(){{var y=window.scrollY+120,cur=secs[0].id;
 secs.forEach(function(s){{if(s.offsetTop<=y)cur=s.id;}});
 links.forEach(function(a){{a.classList.toggle('on',a.getAttribute('href')==='#'+cur);}});}}
window.addEventListener('scroll',spy);spy();
}})();
</script>
{SITE_FOOTER}
</body></html>"""

def program_page(slug):
    name,flag=NAMES[slug]
    body=f"""<main>
{CR.side_rail(slug,f"/world-cases/{slug}-8yo-12weeks.html")}
<section class="page-hero"><div class="wrap">
{CR.breadcrumb(slug,"만 8세 12주 프로그램")}
<div class="pill">{flag} 세계 사례 · {name} 실전 프로그램</div>
<h1 style="font-size:30px">만 8세 초등, <span class="coral">12주 홈 프로그램</span></h1>
<p class="sub">{name} KS2 방식을 우리 집에서 — 주 1회 15분, 대부분 무료·준비물 없음</p>
{episode_nav(slug,"3")}
</div></section>
{CR.program_html(slug)}
<section class="block" style="padding:6px 0 40px"><div class="wrap center">
<a class="btn btn-primary btn-lg" href="/free/{slug}-12weeks-workbook.html" target="_blank" rel="noopener">🖨 12주 워크북 열기 (인쇄·PDF)</a>
</div></section>
</main>"""
    return BS.page("cases","../",f"만 8세 초등 12주 홈 프로그램 | AI 조기교육",f"{name} KS2 방식 기반, 만 8세 아이와 집에서 하는 12주 실전 프로그램. 주 1회 15분, 무료. 순서→만들기→AI 생각.",body)
def roadmap_page(slug):
    name,flag=NAMES[slug]
    body=f"""<main>
<section class="page-hero"><div class="wrap">
{CR.breadcrumb(slug,"학년별 로드맵")}
<div class="pill">{flag} 세계 사례 · {name} 학년별 로드맵</div>
<h1 style="font-size:31px">{name}: 우리 아이 <span class="coral">나이</span>엔 뭘 배우나</h1>
<p class="sub">만 5~16세, 학교가 하는 것과 집에서 할 것을 나이별로</p>
{episode_nav(slug,"2")}
</div></section>
{CR.roadmap_html(slug)}
<section class="block" style="padding:6px 0 40px"><div class="wrap center">
<a class="btn btn-primary btn-lg" href="/world-cases/{slug}-8yo-12weeks.html">만 8세라면 · 12주 홈 프로그램 →</a>
</div></section>
</main>"""
    return BS.page("cases","../",f"{name}: 우리 아이 나이엔 뭘 배우나 (학년별 로드맵) | AI 조기교육",f"{name}의 컴퓨팅·AI 교육을 만 5~16세 학년별로. 학교가 하는 것과 집에서 할 것. 세계 AI교육법 심화.",body)
if __name__=="__main__":
    import sys
    which=sys.argv[1:] or ["uk","singapore","korea"]
    for k in which:
        cfg=C[k]
        BS.write(f"world-cases/{cfg['slug']}.html",render(cfg))
        BS.write(f"videos/{cfg['vslug']}.html",video_detail(cfg))
        print(f"{cfg['flag']} {k} 심층 페이지 + 영상 상세 생성 완료")
    write_all_practice()
