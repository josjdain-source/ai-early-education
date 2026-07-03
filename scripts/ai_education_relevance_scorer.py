#!/usr/bin/env python3
"""
ai_education_relevance_scorer.py — 조기교육 연결성 점수(0~5) 정밀화 v2.

3층 신호(A 강한 교육 / B 중간 연결 / C 일반 기술) + 카테고리 전용 룰 + 감점.
목표: 일반 ML/LLM 논문·빅테크 기업뉴스를 과잉 등록하지 않고,
      아동·학생·부모·학교·감정·companion·tutor와 실제 연결되는 것만 3+.
자동 점수는 '후보'이며 사람 승인이 최종.

테스트: python scripts/ai_education_relevance_scorer.py --test
"""
import re, sys, json, os

# ── A. 강한 교육 직접 신호 (있으면 3+, 아동+맥락이면 4~5)
A_STRONG = [
    "children", "kids", " child", "child ", "student", "students", "school", "classroom",
    "teacher", "parent", "homework", "assessment", "ai tutor", "tutoring", "ai companion",
    "educational ai", "k-12", "k12", "elementary", "preschool", "kindergarten",
    "literacy", "child safety", "minors", "emotional dependency",
    "teaching assistant", "exam grading", "grading", "exam ", "learners", "pedagogy", "curriculum",
    "아이", "어린이", "초등", "학생", "학교", "교실", "교사", "부모", "학부모", "숙제",
    "유아", "미성년", "리터러시", "튜터", "채점", "학습평가",
]
# ── B. 중간 교육 연결 신호 (2~3)
B_MID = [
    "generative ai guidance", "responsible ai use", "responsible use", "ai safety",
    "privacy", "misinformation", "media literacy", "digital literacy", "classroom use",
    "learning platform", "student work", "academic integrity", "ai in education",
    "개인정보", "안전", "미디어 리터러시", "디지털 리터러시", "과제 윤리", "교육",
]
# ── C. 일반 AI 기술 신호 (기본 0~1)
C_TECH = [
    "model release", "benchmark", "chip", "gpu", "data center", "datacenter", "agent",
    "robotics", "revenue", "enterprise", "developer api", "coding assistant",
    "video generation", "image generation", "inference", "training run", "fine-tune",
]
# ── 감점 (교육 약하면 0~1로 눌림)
NEG = [
    "stock", "shares", "revenue", "earnings", "valuation", "chip supply", "enterprise sales",
    "benchmark only", "coding benchmark", "data center", "cloud revenue", "gaming gpu",
    "ipo", "funding round", "acquisition", "merger", "주가", "실적", "매출", "인수합병", "투자유치",
]
# ── 감정/AI companion 전용 (교육 직접신호 없어도 parent_awareness/future_risk 후보)
COMPANION = [
    "ai companion", "emotional ai", "companion robot", "humanoid robot", "child robot",
    "virtual friend", "ai friend", "ai girlfriend", "ai boyfriend", "dependency",
    "attachment", "children emotion", "social robot", "감성 로봇", "동반자 로봇", "가상 친구", "의존",
]
# ML 전문용어(교육 아님) — 이 표현이 있고 실제 교육 맥락이 없으면 억제
ML_JARGON = ["knowledge distillation", "student-teacher", "teacher network", "student network",
             "teacher model", "student model", "teacher-student"]
REAL_EDU_CTX = ["children", "child ", " child", "kids", "school", "classroom", "homework",
                "parent", "k-12", "k12", "preschool", "kindergarten", "literacy", "tutor",
                "아이", "어린이", "초등", "학교", "교실", "숙제", "부모", "유아", "튜터"]
CHILD = ["child", "children", "kid", "kids", "student", "elementary", "preschool", "k-12", "k12",
         "minor", "아이", "어린이", "초등", "학생", "유아", "미성년"]
CONTEXT_LIFT = ["child", "children", "student", "school", "parent", "homework", "safety",
                "privacy", "tutor", "companion", "emotional", "아이", "학생", "학교", "부모", "숙제"]

def _hits(t, kws):
    return [k for k in kws if k in t]

def score_item(category, text, title=""):
    t = f"{title} {text}".lower()
    # ML 전문용어(student-teacher distillation 등) + 실제 교육 맥락 없음 → 교육 아님, 0~1
    if any(j in t for j in ML_JARGON) and not any(x in t for x in REAL_EDU_CTX):
        return 1, [], "ML jargon(student-teacher/distillation), 교육 맥락 없음"
    a, b, c = _hits(t, A_STRONG), _hits(t, B_MID), _hits(t, C_TECH)
    neg, comp = _hits(t, NEG), _hits(t, COMPANION)
    has_child = any(k in t for k in CHILD)
    lift = _hits(t, CONTEXT_LIFT)

    reasons = []
    # ── 감정/companion 전용 룰 (교육 직접신호 없어도 인지 후보)
    if comp:
        s = 4 if has_child else 3
        return s, ["감정/친밀감/의존"], f"companion 신호={comp[:3]} child={has_child} (hype_risk 상향 권장)"

    # ── 카테고리 전용 기본 룰
    is_research = category in ("academic_research", "conference_or_workshop", "nonprofit_or_research")
    is_bigtech = category in ("ai_company_news", "ai_lab_release", "ai_model_release", "ai_robotics",
                              "ai_hardware", "ai_agent", "ai_search", "ai_safety_company", "ai_education_product")
    is_news = category == "news_media"
    is_official = category in ("official_policy", "international_org", "government_dataset")

    # 기본 점수
    if is_research:
        # 일반 ML/LLM 논문 0~1. A신호(education/student/child/tutor 등) 있어야 3+
        if a:
            s = 4 if (has_child and (b or "tutor" in t or "assessment" in t)) else 3
        elif b and has_child:
            s = 3
        else:
            s = 1
        reasons.append(f"research: A={a[:3]} child={has_child}")
    elif is_bigtech:
        # 빅테크 기본 1. 아동/학교/교육 연결 있을 때만 3+
        if a or (comp):
            s = 4 if has_child else 3
        elif b and (has_child or lift):
            s = 3 if has_child else 2
        else:
            s = 1
        reasons.append(f"bigtech: A={a[:3]} lift={lift[:3]} child={has_child}")
    elif is_news:
        # 뉴스: 교육/학생/학교/부모/아동/안전 연결 시만 3+. 실적/제품발표 0~1
        if a:
            s = 4 if has_child else 3
        elif b and (has_child or lift):
            s = 3 if has_child else 2
        else:
            s = 1
        reasons.append(f"news: A={a[:3]} child={has_child}")
    elif is_official:
        # 공식: 교육 신호 있으면 최소 3(정책은 대개 교육 맥락)
        if a or b:
            s = max(3, 4 if has_child else 3)
        else:
            s = 2
        reasons.append(f"official: A={a[:3]} B={b[:2]}")
    else:
        # 기타(유튜브/학교/학생/부모커뮤니티 등)
        if a:
            s = 4 if has_child else 3
        elif b:
            s = 2
        else:
            s = 1
        reasons.append(f"other: A={a[:3]} B={b[:2]}")

    # ── 5점 승격: 아동 + (tutor/companion/homework/assessment/emotional)
    if has_child and any(k in t for k in ["tutor", "companion", "homework", "assessment", "emotional",
                                          "숙제", "튜터", "감정"]):
        s = 5
    # ── 감점: 일반 기술 신호(C)만 강하고 교육 연결 없으면 눌림
    if neg and not a and not (b and (has_child or lift)):
        s = min(s, 1); reasons.append(f"감점 neg={neg[:3]}")
    if c and not a and not b and not has_child:
        s = min(s, 1); reasons.append("일반 기술만")

    # 연결 영역
    areas = _areas(t)
    return s, areas, " | ".join(reasons)

AREA_KW = {
    "학습 도구": ["tutor", "classroom", "curriculum", "literacy", "교육", "학습", "수업", "리터러시"],
    "검색/정보 확인": ["misinformation", "fact-check", "검색 결과", "정보 확인"],
    "숙제/평가": ["homework", "assessment", "grading", "exam", "academic integrity", "숙제", "과제", "평가", "시험"],
    "감정/친밀감/의존": ["emotion", "companion", "attachment", "dependency", "감정", "친밀", "동반", "의존"],
    "AI 로봇/장난감/기기": ["robot", "humanoid", "toy", "on-device", "로봇", "장난감", "기기"],
    "영상/이미지 생성": ["image generation", "video generation", "이미지 생성", "영상 생성"],
    "개인정보/안전": ["privacy", "safety", "child protection", "개인정보", "안전", "보호"],
    "미래 직업/진로": ["career", "workforce", "진로", "직업"],
}
def _areas(t):
    return [a for a, kws in AREA_KW.items() if any(k in t for k in kws)]

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

# ── 테스트 러너
def _run_tests():
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "ops", "ai-early-education", "scorer_test_cases.json")
    cases = json.load(open(p, encoding="utf-8"))["cases"]
    passed = failed = 0
    fails = []
    for c in cases:
        s, areas, why = score_item(c["source_category"], c.get("snippet", ""), c["title"])
        ok = c["expected_min_score"] <= s <= c["expected_max_score"]
        if ok:
            passed += 1
        else:
            failed += 1
            fails.append((c["title"][:50], s, c["expected_min_score"], c["expected_max_score"], c["reason"]))
    print(f"=== scorer test: {passed}/{len(cases)} passed, {failed} failed ===")
    for t, s, lo, hi, r in fails:
        print(f"  FAIL score={s} expected[{lo},{hi}] :: {t} ({r})")
    return failed == 0

if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.exit(0 if _run_tests() else 1)
