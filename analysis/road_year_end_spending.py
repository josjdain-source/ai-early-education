#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""지방 도로 계약의 '연말 몰림' 분석 — 월별 집계 + 연말쏠림지수/12월집중지수 + 판정.

★원칙: 가짜 데이터/추정 수치를 만들지 않는다. 반드시 실제 CSV를 입력받아 계산한다.
데이터 출처(직접 받아 CSV 저장): 나라장터(조달청 g2b), 지방재정365(lofin.mois.go.kr),
열린재정(openfiscaldata.go.kr), 공공데이터포털(data.go.kr).

CSV 필요 컬럼(이름은 유연 매칭 — data/road_keywords.json의 *_field_candidates 참조):
  - 계약일자(YYYY-MM-DD 또는 YYYYMMDD 등)  - 계약금액(원)  - 계약명(사업명)  - (선택)발주기관

사용:
  python road_year_end_spending.py contracts.csv
  python road_year_end_spending.py contracts.csv --by-agency --out summary.csv

분류: 유지보수형/보행환경형/신규개설형/재난복구형(=낭비의심 제외). data/road_keywords.json 기준.
지표: 연말쏠림지수=10~12월/연간, 12월집중지수=12월/연간 (재난복구형 제외 금액 기준)."""
import sys, os, csv, json, re, argparse
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
KW_PATH = os.path.join(os.path.dirname(HERE), "data", "road_keywords.json")

def load_keywords():
    with open(KW_PATH, encoding="utf-8") as f:
        return json.load(f)

def norm(s):
    return re.sub(r"\s+", "", (s or "")).lower()

def pick_field(header, candidates):
    hn = {norm(h): h for h in header}
    for c in candidates:
        if norm(c) in hn:
            return hn[norm(c)]
    # 부분 포함 매칭
    for c in candidates:
        for h in header:
            if norm(c) in norm(h):
                return h
    return None

def parse_month(v):
    if not v:
        return None
    m = re.search(r"(20\d{2})[-/.\s]?(\d{1,2})", str(v))
    if m:
        mo = int(m.group(2))
        return (int(m.group(1)), mo) if 1 <= mo <= 12 else None
    m2 = re.search(r"(20\d{2})(\d{2})\d{2}", str(v))
    if m2:
        return (int(m2.group(1)), int(m2.group(2)))
    return None

def parse_amount(v):
    if v is None:
        return 0.0
    s = re.sub(r"[^\d.\-]", "", str(v))
    try:
        return float(s) if s not in ("", "-", ".") else 0.0
    except ValueError:
        return 0.0

def classify(name, KW):
    n = norm(name)
    for cat in KW["priority"]:  # disaster > new > walkway > maintenance
        for kw in KW["categories"][cat]["keywords"]:
            if norm(kw) in n:
                return cat
    return None  # 도로 관련 아님

def verdict(ratio):
    if ratio is None:
        return "-"
    p = ratio * 100
    if p < 25: return "정상 분산"
    if p < 35: return "약한 연말 집중"
    if p < 50: return "강한 연말 집중"
    return "연말 몰아쓰기 의심 패턴 (확정 아님·추가 검증 필요)"

def analyze(rows, KW, name_f, date_f, amt_f, agency_f=None, by_agency=False):
    # bucket[(scope, year)] = {month: amount}, cat_amount, disaster_amount
    scope_year = defaultdict(lambda: {"month": defaultdict(float), "disaster_month": defaultdict(float),
                                       "cat": defaultdict(float), "n": 0})
    for r in rows:
        cat = classify(r.get(name_f, ""), KW)
        if cat is None:
            continue
        ym = parse_month(r.get(date_f))
        if ym is None:
            continue
        yr, mo = ym
        amt = parse_amount(r.get(amt_f))
        scope = (r.get(agency_f) or "전체") if (by_agency and agency_f) else "전체"
        b = scope_year[(scope, yr)]
        b["cat"][cat] += amt
        b["n"] += 1
        if cat in KW["exclude_from_suspicion"]:
            b["disaster_month"][mo] += amt
        else:
            b["month"][mo] += amt
    return scope_year

def summarize(scope_year, KW):
    out = []
    for (scope, yr), b in sorted(scope_year.items()):
        annual = sum(b["month"].values())  # 재난복구 제외 금액
        q4 = sum(b["month"].get(m, 0) for m in (10, 11, 12))
        dec = b["month"].get(12, 0)
        skew = (q4 / annual) if annual > 0 else None
        deci = (dec / annual) if annual > 0 else None
        out.append({
            "지자체": scope, "연도": yr, "계약건수": b["n"],
            "연간금액(재난제외)": round(annual), "10~12월금액": round(q4), "12월금액": round(dec),
            "연말쏠림지수%": round(skew * 100, 1) if skew is not None else None,
            "12월집중지수%": round(deci * 100, 1) if deci is not None else None,
            "판정": verdict(skew),
            "재난복구금액(별도)": round(sum(b["disaster_month"].values())),
            "유지보수": round(b["cat"].get("maintenance", 0)),
            "보행환경": round(b["cat"].get("walkway", 0)),
            "신규개설": round(b["cat"].get("new", 0)),
        })
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="?", help="계약 데이터 CSV 경로")
    ap.add_argument("--by-agency", action="store_true", help="지자체(발주기관)별로 분리 집계")
    ap.add_argument("--out", help="요약 결과를 CSV로 저장")
    ap.add_argument("--encoding", default="utf-8-sig")
    a = ap.parse_args()

    KW = load_keywords()
    if not a.csv:
        print("[안내] 실제 계약 CSV를 입력하세요. 이 도구는 데이터를 지어내지 않습니다.")
        print("  예: python road_year_end_spending.py contracts.csv --by-agency")
        print("  데이터 출처: 나라장터(g2b) · 지방재정365(lofin.mois.go.kr) · 열린재정 · 공공데이터포털")
        print("  분류 키워드: data/road_keywords.json")
        return
    if not os.path.exists(a.csv):
        sys.exit(f"[오류] 파일 없음: {a.csv}")

    with open(a.csv, encoding=a.encoding, newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        name_f = pick_field(header, KW["name_field_candidates"])
        date_f = pick_field(header, KW["date_field_candidates"])
        amt_f = pick_field(header, KW["amount_field_candidates"])
        agency_f = pick_field(header, KW["agency_field_candidates"])
        if not (name_f and date_f and amt_f):
            sys.exit(f"[오류] 필요한 컬럼을 못 찾음. 발견={header}\n  계약명={name_f} 계약일자={date_f} 계약금액={amt_f}")
        rows = list(reader)

    sy = analyze(rows, KW, name_f, date_f, amt_f, agency_f, a.by_agency)
    summary = summarize(sy, KW)
    if not summary:
        print("[결과] 도로 관련 계약이 분류되지 않았습니다. 키워드/컬럼 매칭을 확인하세요.")
        return

    print(f"[입력] {len(rows)}행 · 컬럼: 계약명={name_f} 일자={date_f} 금액={amt_f} 기관={agency_f or '없음'}")
    print(f"{'지자체':<10}{'연도':<6}{'건수':>6}{'연말쏠림%':>10}{'12월집중%':>10}  판정")
    for r in summary:
        print(f"{str(r['지자체'])[:10]:<10}{r['연도']:<6}{r['계약건수']:>6}"
              f"{str(r['연말쏠림지수%']):>10}{str(r['12월집중지수%']):>10}  {r['판정']}")
    print("\n※ 이 수치는 낭비 확정이 아니라 '추가 검증이 필요한 신호'입니다. 재난복구형은 위 지수에서 제외했습니다.")

    if a.out:
        with open(a.out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
            w.writeheader(); w.writerows(summary)
        print(f"[저장] {a.out}")

if __name__ == "__main__":
    main()
