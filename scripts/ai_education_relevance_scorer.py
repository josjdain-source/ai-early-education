#!/usr/bin/env python3
"""
ai_education_relevance_scorer.py — 조기교육 연결성 점수(0~5) 부여.

규칙: ai_news_relevance_rules.md 기반. 키워드/카테고리 휴리스틱.
자동 점수는 '후보'이며 사람 승인 게이트 앞단이다. 확정 아님.
"""

# 연결 영역 키워드(가중치 신호)
AREA_KW = {
    "학습 도구": ["learn", "learning", "tutor", "study", "교육", "학습", "수업"],
    "검색/정보 확인": ["search", "information", "fact", "검색", "정보"],
    "숙제/평가": ["homework", "assessment", "assignment", "exam", "숙제", "과제", "평가", "시험"],
    "감정/친밀감/의존": ["emotion", "companion", "friend", "relationship", "depend", "감정", "친밀", "동반", "의존", "companionship"],
    "AI 로봇/장난감/기기": ["robot", "humanoid", "toy", "device", "on-device", "로봇", "장난감", "기기"],
    "영상/이미지 생성": ["image", "video", "generate", "생성", "이미지", "영상"],
    "개인정보/안전": ["privacy", "safety", "child protection", "개인정보", "안전", "보호"],
    "미래 직업/진로": ["career", "future job", "workforce", "진로", "직업"],
}
CHILD_KW = ["child", "children", "kid", "student", "elementary", "preschool", "K-12", "minor",
            "아이", "어린이", "초등", "학생", "유아", "미성년"]
BIZ_KW = ["earnings", "stock", "shares", "revenue", "valuation", "funding", "IPO",
          "실적", "주가", "투자", "매출", "시가총액"]

def score_item(category, text, title=""):
    """0~5 점수 + 연결 영역 + 근거. text=제목+스니펫 합친 소문자 대상."""
    t = f"{title} {text}".lower()
    areas = [a for a, kws in AREA_KW.items() if any(k.lower() in t for k in kws)]
    has_child = any(k.lower() in t for k in CHILD_KW)
    has_biz = any(k.lower() in t for k in BIZ_KW)
    emotional = "감정/친밀감/의존" in areas

    # 기본 점수
    if has_biz and not areas and not has_child:
        return 0, [], "기업 실적/투자 중심, 교육 연결 없음"
    if not areas and not has_child:
        return 1, [], "일반 AI 소식, 아이 교육 연결 약함"
    s = 2
    if any(a in areas for a in ["숙제/평가", "학습 도구"]) or has_child:
        s = 3
    if emotional or "개인정보/안전" in areas or "AI 로봇/장난감/기기" in areas:
        s = 4
    if has_child and (emotional or "학습 도구" in areas or "숙제/평가" in areas or category in
                      ("official_policy", "international_org", "student_project", "ai_companion", "ai_education_product")):
        s = 5
    # 공식/연구 카테고리는 교육 신호 있으면 최소 3 보장
    if category in ("official_policy", "international_org", "government_dataset", "academic_research",
                    "conference_or_workshop") and (areas or has_child):
        s = max(s, 3)
    reason = f"연결영역={areas or '없음'}, 아동언급={has_child}, 감정={emotional}, 기업지표={has_biz}"
    return s, areas, reason

def parent_question(areas):
    m = {
        "감정/친밀감/의존": "AI 친구·상담자를 아이에게 어디까지 허용할까?",
        "숙제/평가": "AI 답 확인법·AI 생성물 구분법을 어떻게 가르칠까?",
        "AI 로봇/장난감/기기": "앱 하나가 아니라 생활 환경 전체로 AI를 이해시켜야 할까?",
        "개인정보/안전": "아이 개인정보·대화 로그를 어떻게 보호할까?",
        "검색/정보 확인": "아이가 AI 검색 결과를 그대로 믿지 않게 하려면?",
        "학습 도구": "나이에 맞는 AI 사용 방식을 어떻게 정할까?",
    }
    for a in areas:
        if a in m:
            return m[a]
    return "이 변화가 우리 아이 교육에 어떤 의미일까?"
