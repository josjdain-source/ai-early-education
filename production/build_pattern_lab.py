# -*- coding: utf-8 -*-
"""YouTube Pattern Lab — 우리 채널 데이터 역추적 모델 데이터 생성.
공식 알고리즘 주장 X. Viral Test Score(제목·내용 기반, 지금 계산 가능) + 채널지표(null, 데이터 유입시 갱신) + algorithm_guess(제목 역추적 가설)."""
import io, sys, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"C:/Users/admin/Desktop/ai-craft-kids"

# ── Viral Test Score 루브릭(키워드 휴리스틱 = 재현가능·투명) ──
STOP_STRONG = ["큰일", "위험한 이유", "꼭 해야", "놓치는", "하면 안 되는", "안 되는 말"]
STOP_MED    = ["왜", "이것", "한 가지", "무엇을", "진짜", "의외", "달라야"]
PAIN_DIRECT = ["우리 아이", "우리 애", "부모가", "부모", "아이에게", "아이가", "집에서", "오늘", "엄마", "아빠"]
CURIOSITY   = ["왜", "무엇을", "이것", "한 가지", "이렇게", "어떻게", "?", "먼저"]
POLICY      = ["정책", "커리큘럼", "제도", "교과서", "취업난", "잃어버린", "10년", "도입", "국가전략", "시간표를"]
ABSTRACT    = ["미래교육", "리터러시", "디지털 역량", "디지털 역", "역량", "생태계", "패러다임"]

def has(t, ws): return any(w in t for w in ws)
def cnt(t, ws): return sum(1 for w in ws if w in t)

def viral_score(title, has_action, duration, structured_flow, national_compare):
    """title=제목, has_action=부모 오늘 행동 한 문장 있음, duration=초, structured_flow=문제→이유→해결 완결, national_compare=국가비교형"""
    s = {}
    # + Stop Power (0~3)
    s["stop_power"] = 3 if has(title, STOP_STRONG) else (2 if has(title, STOP_MED) else 0)
    # + Personal Pain (0~2)  — 국가비교면 개인화 약함
    if national_compare: s["personal_pain"] = 1 if has(title, PAIN_DIRECT) else 0
    else: s["personal_pain"] = 2 if has(title, PAIN_DIRECT) else 1
    # + Curiosity Gap (0~2)  — 답을 다 말하면 감(궁금증 없음)
    reveals = national_compare and not has(title, ["?", "왜", "무엇을"])
    s["curiosity_gap"] = 0 if reveals else (2 if has(title, CURIOSITY) else 1)
    # + Watch Completion (0~2)  — 45~60초 문제→이유→해결 완결
    s["watch_completion"] = 2 if (structured_flow and duration <= 65) else (1 if structured_flow else 0)
    # + Clear Takeaway (0~2)
    s["clear_takeaway"] = 2 if has_action else 1
    # - Boring Policy (0~-3)
    pol = cnt(title, POLICY); s["boring_policy"] = -min(3, pol * 2) if pol else 0
    # - Abstract Education Talk (0~-2)
    s["abstract_talk"] = -2 if has(title, ABSTRACT) else 0
    # - Clickbait Mismatch (0~-2) — 제목만 세고 내용 약할 때(우리 검수본은 매칭 양호 → 0)
    s["clickbait_mismatch"] = 0
    s["total"] = sum(s.values())
    return s

def guess(title, s, national_compare):
    """제목 역추적 가설(실제 지표 null이므로 '제목 패턴'만으로 추정). 지표 들어오면 갱신."""
    g = {"exposure_problem": False, "hook_problem": False, "retention_problem": False,
         "topic_problem": False, "conversion_problem": False, "likely_reason": ""}
    reasons = []
    if s["stop_power"] <= 0: g["hook_problem"] = True; reasons.append("첫 훅 약함(Stop Power 0)")
    if s["personal_pain"] <= 0: g["topic_problem"] = True; reasons.append("Personal Pain 낮음—'내 얘기'로 안 느껴질 위험")
    if s["curiosity_gap"] <= 0: g["hook_problem"] = True; reasons.append("제목이 답을 다 말해 궁금증 없음")
    if s["boring_policy"] < 0: g["topic_problem"] = True; reasons.append("정책/거대담론 단어—쇼츠에서 약한 패턴")
    if s["clear_takeaway"] <= 1 and not reasons: g["conversion_problem"] = True; reasons.append("부모 오늘 행동 연결 약함")
    if not reasons:
        g["likely_reason"] = "제목 역추적상 강한 패턴(훅·개인화·궁금증·행동 모두 확보). 실제 지표로 확인 필요."
    else:
        g["likely_reason"] = "제목 역추적 가설: " + " · ".join(reasons) + " (※실제 노출·시청지속 데이터 유입 시 갱신)"
    return g

NULL_METRICS = {"impressions": None, "initial_test_views": None, "swipe_away_rate": None,
    "avg_view_duration": None, "retention_percent": None, "rewatch_rate": None,
    "comments": None, "shares": None, "link_clicks": None, "subscriber_gain": None}

# ── 재분류 대상: 우리 5개 승인 쇼츠(핵심) + 발행 국가쇼츠(대조군) ──
VIDEOS = [
 # (id, title, has_action, dur, structured, national, pattern_type)
 ("shorts-parent-005", "AI를 이렇게 쓰면 아이가 큰일납니다", True, 55, True, False, "반전/부모행동"),
 ("shorts-parent-001", "아이에게 AI를 시키기 전 꼭 해야 할 질문", True, 45, True, False, "질문형"),
 ("shorts-parent-002", "AI 답이 이상할 때 부모가 하면 안 되는 말", True, 45, True, False, "부모행동/반전"),
 ("shorts-parent-003", "AI 답을 그대로 믿는 아이가 위험한 이유", True, 45, True, False, "위험/궁금증"),
 ("shorts-levels-001", "아이 나이별 AI교육은 이렇게 달라야 합니다", True, 50, True, False, "연령별/정보"),
 ("china-short-s1", "중국은 왜 초등학생에게까지 AI를 가르칠까?", False, 55, True, True, "국가비교"),
 ("us-short-s1", "미국 아이들은 AI를 '쓰는' 게 아니라 무엇을 할까?", False, 55, True, True, "국가비교"),
 ("korea-lost-decade", "한국의 잃어버린 AI 10년, 청년의 취업난", False, 55, True, True, "정책/거대담론"),
]

records = []
for vid, title, act, dur, struct, natl, ptype in VIDEOS:
    s = viral_score(title, act, dur, struct, natl)
    rec = {"video_id": vid, "title": title, "pattern_type": ptype,
           "viral_test_score": s, **NULL_METRICS,
           "algorithm_guess": guess(title, s, natl)}
    records.append(rec)
records.sort(key=lambda r: r["viral_test_score"]["total"], reverse=True)

MODEL = {
 "_manifesto": "이 연구소는 유튜브 공식 알고리즘을 안다고 주장하지 않습니다. 공식 설명은 참고만 하고, 우리 채널의 실제 성과 데이터로 패턴을 추정합니다.",
 "stance": {"공식 원칙": "참고자료", "우리 데이터": "판단 기준", "반복 실험": "알고리즘 추정"},
 "data_status": "채널 신생 — 노출·조회·시청지속 등 실제 지표는 아직 null. 현재는 제목·내용 기반 Viral Test Score로 사전추정, 데이터 유입 시 지표·algorithm_guess 갱신.",
 "core_questions": [
   "1. 유튜브가 이 영상을 처음에 얼마나 노출했는가? (impressions/initial_test_views)",
   "2. 노출된 사람이 멈췄는가? (swipe_away_rate ↔ Stop Power)",
   "3. 멈춘 사람이 끝까지 봤는가? (retention_percent/avg_view_duration ↔ Watch Completion)",
   "4. 보고 나서 반응했는가? (comments/shares/subscriber_gain)",
   "5. 비슷한 제목 패턴이 반복해서 먹히는가? (pattern_type 승률)",
   "6. 부모가 오늘 할 행동으로 연결됐는가? (link_clicks ↔ Clear Takeaway)"],
 "viral_test_score_formula": {
   "plus": {
     "Stop Power": "첫 1초에 손가락을 멈추게 하는가? 강한 단어: 큰일납니다·위험한 이유·꼭 해야 할 질문·놓치는 한 가지 (0~3)",
     "Personal Pain": "부모가 '이거 우리 애 얘긴데?'라고 느끼는가? (0~2)",
     "Curiosity Gap": "제목이 답을 다 말하지 않고 궁금증을 남기는가? (0~2)",
     "Watch Completion": "45~60초 안에 문제→이유→해결이 완결되는가? (0~2)",
     "Clear Takeaway": "부모가 오늘 아이에게 할 한 문장이 있는가? (0~2)"},
   "minus": {
     "Boring Policy": "정책·커리큘럼·제도 설명으로 보이면 감점 (0~-3)",
     "Abstract Education Talk": "미래교육·AI리터러시·디지털 역량 같은 추상어만 있으면 감점 (0~-2)",
     "Clickbait Mismatch": "제목은 센데 내용이 약하면 감점 (0~-2)"},
   "formula": "Viral Test = Stop Power + Personal Pain + Curiosity Gap + Watch Completion + Clear Takeaway − Boring Policy − Abstract Education Talk − Clickbait Mismatch"},
 "priors": [
   {"pattern": "질문형 · 부모 행동형", "verdict": "현재 최고 패턴", "tier": "S"},
   {"pattern": "반전형", "verdict": "안정적", "tier": "A"},
   {"pattern": "국가 비교형", "verdict": "중간 이상", "tier": "B"},
   {"pattern": "사회문제 · 정책 설명형", "verdict": "쇼츠에서 약함", "tier": "D"}],
 "rules_of_thumb": [
   "제목에 부모·아이·오늘 행동이 가까울수록 강함.",
   "제목에 취업난·정책·거대 담론이 들어가면 약해질 가능성 높음.",
   "공식 설명은 너무 일반적이고 실제 추천 로직은 비공개 → 우리 데이터로만 판단."],
 "next_title_levers": ["Stop Power(강한 첫 단어)", "Personal Pain(우리 애 얘기)", "Clear Takeaway(오늘 할 한 문장)"],
 "videos": records,
 "field_schema_ref": {"metrics": list(NULL_METRICS.keys()),
   "algorithm_guess": ["exposure_problem","hook_problem","retention_problem","topic_problem","conversion_problem","likely_reason"]},
}
os.makedirs(f"{ROOT}/content_bank", exist_ok=True)
json.dump(MODEL, open(f"{ROOT}/content_bank/pattern_lab.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("pattern_lab.json 생성. Viral Test Score 순위:")
for r in records:
    print(f"  {r['viral_test_score']['total']:>3}  [{r['pattern_type']}] {r['title'][:34]}")
