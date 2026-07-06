# -*- coding: utf-8 -*-
"""YouTube Pattern Lab — 우리 채널 데이터 역추적 모델 데이터 생성.
공식 알고리즘 주장 X. Viral Test Score(제목·내용) + 채널지표(실측 유입시) + algorithm_guess.
★2026-07-07 정정: unLYYN(한국의 잃어버린 AI 10년·취업난) 사전예측 D(0)였으나 실제 좋아요 많음.
  핵심 = '울분을 가진 사람의 속시원한 심정 표현'(사이다). 시청자가 삭이던 좌절을 대신 터뜨려줌 → 좋아요·댓글.
  → Catharsis(울분 대변) 레버 신설. 감점은 '건조한 제도 설명'으로만 한정."""
import io, sys, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = r"C:/Users/admin/Desktop/ai-craft-kids"

# ── Viral Test Score 루브릭(키워드 휴리스틱 = 재현가능·투명) ──
STOP_STRONG = ["큰일", "위험한 이유", "꼭 해야", "놓치는", "하면 안 되는", "안 되는 말", "뼈아프", "잃어버린"]
STOP_MED    = ["왜", "이것", "한 가지", "무엇을", "진짜", "의외", "달라야"]
PAIN_DIRECT = ["우리 아이", "우리 애", "부모가", "부모", "아이에게", "아이가", "집에서", "오늘", "엄마", "아빠"]
CURIOSITY   = ["왜", "무엇을", "이것", "한 가지", "이렇게", "어떻게", "?", "먼저"]
# ★핵심 레버: 울분 대변·속시원함(사이다) — 시청자가 삭이던 좌절/후회를 대신 터뜨려줌(실측 확인)
CATHARSIS   = ["잃어버린", "뼈아프", "답답", "뒤처", "뒤쳐", "취업난", "격차", "위기", "놓친", "무너", "추락",
               "골든타임", "10년", "이래서", "결국", "속터", "속시원", "누가 이렇게"]
# ★건조한 제도 설명만 감점(감정적 국가 이슈는 제외)
DRY_POLICY  = ["제도", "커리큘럼", "교과서", "도입 절차", "국가전략", "행정", "법령", "조례", "시간표를"]
ABSTRACT    = ["미래교육", "리터러시", "디지털 역량", "디지털 역", "역량", "생태계", "패러다임"]

def has(t, ws): return any(w in t for w in ws)
def cnt(t, ws): return sum(1 for w in ws if w in t)

def viral_score(title, has_action, duration, structured_flow, national_compare):
    s = {}
    s["stop_power"] = 3 if has(title, STOP_STRONG) else (2 if has(title, STOP_MED) else 0)
    if national_compare: s["personal_pain"] = 1 if has(title, PAIN_DIRECT) else 0
    else: s["personal_pain"] = 2 if has(title, PAIN_DIRECT) else 1
    # ★울분 대변·속시원함(0~3) — 실측으로 확인된 최강 훅
    s["catharsis"] = 3 if cnt(title, CATHARSIS) >= 2 else (2 if has(title, CATHARSIS) else 0)
    reveals = national_compare and not has(title, ["?", "왜", "무엇을"])
    s["curiosity_gap"] = 0 if reveals else (2 if has(title, CURIOSITY) else 1)
    s["watch_completion"] = 2 if (structured_flow and duration <= 65) else (1 if structured_flow else 0)
    s["clear_takeaway"] = 2 if has_action else 1
    dry = cnt(title, DRY_POLICY); s["boring_policy"] = -min(3, dry * 2) if dry else 0
    s["abstract_talk"] = -2 if has(title, ABSTRACT) else 0
    s["clickbait_mismatch"] = 0
    s["total"] = sum(v for k, v in s.items())
    return s

def guess(title, s, national_compare, confirmed):
    g = {"exposure_problem": False, "hook_problem": False, "retention_problem": False,
         "topic_problem": False, "conversion_problem": False, "likely_reason": ""}
    if confirmed:
        g["likely_reason"] = ("★실측 확인: " + confirmed["engagement"] + ". " + confirmed["verdict"] +
            " 강점=울분 대변·속시원함(사이다). 시청자가 삭이던 좌절을 대신 터뜨려 좋아요·댓글을 부름.")
        return g
    reasons = []
    if s["stop_power"] <= 0 and s["catharsis"] <= 0: g["hook_problem"] = True; reasons.append("첫 훅 약함(멈춤·울분 없음)")
    if s["personal_pain"] <= 0 and s["catharsis"] <= 0: g["topic_problem"] = True; reasons.append("개인화·울분 훅 모두 약함")
    if s["curiosity_gap"] <= 0: g["hook_problem"] = True; reasons.append("제목이 답을 다 말함")
    if s["boring_policy"] < 0: g["topic_problem"] = True; reasons.append("건조한 제도 설명 단어")
    if s["clear_takeaway"] <= 1 and not reasons: g["conversion_problem"] = True; reasons.append("행동 연결 약함")
    g["likely_reason"] = ("제목 역추적상 강한 패턴(훅·개인화/울분·궁금증 확보). 실제 지표로 확인 필요."
        if not reasons else "제목 역추적 가설: " + " · ".join(reasons) + " (※실제 지표 유입 시 갱신)")
    return g

NULL_METRICS = {"impressions": None, "initial_test_views": None, "swipe_away_rate": None,
    "avg_view_duration": None, "retention_percent": None, "rewatch_rate": None,
    "comments": None, "shares": None, "link_clicks": None, "subscriber_gain": None}

CONFIRMED = {
 "korea-lost-decade": {"youtube_id": "unLYYN_aTPk",
   "engagement": "좋아요 많음(사용자 확인·정확 수치는 YouTube Studio에서 갱신 예정)",
   "verdict": "사전예측 D(0점)였으나 실제 강함 → 모델 오류 정정(울분 대변≠Boring Policy)."},
}

VIDEOS = [
 ("shorts-parent-005", "AI를 이렇게 쓰면 아이가 큰일납니다", True, 55, True, False, "반전/부모행동"),
 ("shorts-parent-001", "아이에게 AI를 시키기 전 꼭 해야 할 질문", True, 45, True, False, "질문형"),
 ("shorts-parent-002", "AI 답이 이상할 때 부모가 하면 안 되는 말", True, 45, True, False, "부모행동/반전"),
 ("shorts-parent-003", "AI 답을 그대로 믿는 아이가 위험한 이유", True, 45, True, False, "위험/궁금증"),
 ("shorts-levels-001", "아이 나이별 AI교육은 이렇게 달라야 합니다", True, 50, True, False, "연령별/정보"),
 ("aiedu-free-programs-longform", "우리가 쓰는 무료 영상 제작 프로그램, 이것만 있으면 됩니다", True, 262, True, False, "제작도구/롱폼"),
 ("china-short-s1", "중국은 왜 초등학생에게까지 AI를 가르칠까?", False, 55, True, True, "국가비교"),
 ("us-short-s1", "미국 아이들은 AI를 '쓰는' 게 아니라 무엇을 할까?", False, 55, True, True, "국가비교"),
 ("korea-lost-decade", "한국의 잃어버린 AI 10년, 청년의 취업난", False, 55, True, True, "울분 대변·사이다 (실측)"),
]

records = []
for vid, title, act, dur, struct, natl, ptype in VIDEOS:
    conf = CONFIRMED.get(vid)
    s = viral_score(title, act, dur, struct, natl)
    m = dict(NULL_METRICS)
    if conf: m["youtube_id"] = conf["youtube_id"]; m["likes"] = "많음(실측)"
    rec = {"video_id": vid, "title": title, "pattern_type": ptype,
           "data_confirmed": bool(conf), "viral_test_score": s, **m,
           "algorithm_guess": guess(title, s, natl, conf)}
    records.append(rec)
records.sort(key=lambda r: (r["data_confirmed"], r["viral_test_score"]["total"]), reverse=True)

MODEL = {
 "_manifesto": "이 연구소는 유튜브 공식 알고리즘을 안다고 주장하지 않습니다. 공식 설명은 참고만 하고, 우리 채널의 실제 성과 데이터로 패턴을 추정합니다. 사전 점수가 실제 성과와 다르면, 실제 데이터를 따릅니다.",
 "stance": {"공식 원칙": "참고자료", "우리 데이터": "판단 기준", "반복 실험": "알고리즘 추정"},
 "core_insight": "울분을 가진 사람의 속시원한 심정 표현. 시청자가 속으로 삭이던 좌절·후회를 영상이 대신 터뜨려 줄 때(사이다), 좋아요·댓글·공유가 터진다. 정보 전달보다 '얼마나 속시원하게 대변하느냐'가 엔진.",
 "data_status": "채널 신생. 대부분 지표는 아직 null이라 제목·내용 기반 Viral Test Score로 사전추정. ★단, 실측 확인된 영상(data_confirmed)은 예측보다 우선한다.",
 "real_data_findings": [
   {"video_id": "korea-lost-decade", "youtube": "https://youtube.com/shorts/unLYYN_aTPk",
    "title": "한국의 잃어버린 AI 10년, 청년의 취업난",
    "predicted": "D · 0점 (사전 휴리스틱: '정책/거대담론 약함')",
    "actual": "좋아요 많음 (실측)",
    "lesson": "핵심은 '울분을 가진 사람의 속시원한 심정 표현'. '잃어버린·취업난·뼈아프다'가 시청자의 삭인 좌절을 대신 터뜨려 속시원하게(사이다) 함 → 좋아요·댓글 폭발. 휴리스틱이 이를 Boring Policy로 잘못 감점했던 것.",
    "action": "다음 제목·대본에 '울분 대변→속시원함' 구조를 적극 활용(잃어버린·뒤처짐·취업난·뼈아프다·이래서 안 된다 → 대신 시원하게 짚어줌)."}],
 "core_questions": [
   "1. 유튜브가 이 영상을 처음에 얼마나 노출했는가? (impressions)",
   "2. 노출된 사람이 멈췄는가? (swipe_away ↔ Stop Power/울분)",
   "3. 멈춘 사람이 끝까지 봤는가? (retention ↔ Watch Completion)",
   "4. 보고 나서 반응했는가? (likes/comments) ← 울분 대변이 여기서 폭발",
   "5. 비슷한 제목 패턴이 반복해서 먹히는가? (pattern_type 승률)",
   "6. 부모가 오늘 할 행동으로 연결됐는가? (link_clicks ↔ Clear Takeaway)"],
 "viral_test_score_formula": {
   "plus": {
     "Stop Power": "첫 1초에 손가락을 멈추게 하는가? (큰일납니다·위험한 이유·놓치는·뼈아프다) (0~3)",
     "Personal Pain": "부모가 '우리 애 얘긴데?' 느끼는가? (0~2)",
     "Catharsis (울분 대변·사이다)": "★시청자가 삭이던 좌절·후회를 대신 터뜨려 속시원하게 하는가? (잃어버린·취업난·뼈아프다·뒤처짐·이래서) — 실측 확인된 최강 훅 (0~3)",
     "Curiosity Gap": "답을 다 말하지 않고 궁금증을 남기는가? (0~2)",
     "Watch Completion": "45~60초에 문제→이유→해결이 완결되는가? (0~2)",
     "Clear Takeaway": "오늘 할 한 문장이 있는가? (0~2)"},
   "minus": {
     "Boring Policy": "★건조한 제도·커리큘럼·도입 절차 설명만 감점(감정적 국가이슈는 제외) (0~-3)",
     "Abstract Education Talk": "미래교육·리터러시·디지털 역량 추상어만 있으면 감점 (0~-2)",
     "Clickbait Mismatch": "제목은 센데 내용이 약하면 감점 (0~-2)"},
   "formula": "Viral Test = Stop Power + Personal Pain + Catharsis(울분 대변) + Curiosity Gap + Watch Completion + Clear Takeaway − Boring Policy − Abstract Talk − Clickbait Mismatch"},
 "priors": [
   {"pattern": "울분 대변·사이다형 (잃어버린·취업난·뼈아프다)", "verdict": "★실측 강함 — 속시원한 심정 대변", "tier": "S"},
   {"pattern": "질문형 · 부모 행동형", "verdict": "강함", "tier": "S"},
   {"pattern": "반전형", "verdict": "안정적", "tier": "A"},
   {"pattern": "국가 비교형", "verdict": "중간 이상", "tier": "B"},
   {"pattern": "건조한 제도·커리큘럼 설명형", "verdict": "쇼츠에서 약함", "tier": "D"}],
 "rules_of_thumb": [
   "★핵심: 정보 전달보다 '울분을 얼마나 속시원하게 대변하느냐'. 시청자가 못 하던 말을 대신 시원하게 터뜨려라.",
   "잃어버린·뒤처짐·취업난·뼈아프다는 감점이 아니라 최강 훅 — unLYYN 실측으로 확인.",
   "감점은 '건조한 제도 설명(제도·커리큘럼·도입 절차)'에만.",
   "제목에 부모·아이·오늘 행동이 가까울수록 강함.",
   "예측과 실측이 다르면 실측이 이긴다."],
 "next_title_levers": ["Catharsis(울분 대변·속시원함)", "Stop Power(강한 첫 단어)", "Personal Pain(우리 애)", "Clear Takeaway(오늘 할 한 문장)"],
 "videos": records,
 "field_schema_ref": {"metrics": list(NULL_METRICS.keys()),
   "algorithm_guess": ["exposure_problem","hook_problem","retention_problem","topic_problem","conversion_problem","likely_reason"]},
}
os.makedirs(f"{ROOT}/content_bank", exist_ok=True)
json.dump(MODEL, open(f"{ROOT}/content_bank/pattern_lab.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("pattern_lab.json 갱신(울분 대변 레버). Viral Test Score(실측 우선):")
for r in records:
    tag = " ★실측" if r["data_confirmed"] else ""
    print(f"  {r['viral_test_score']['total']:>3}  [{r['pattern_type']}] {r['title'][:28]}{tag}")
