#!/usr/bin/env python3
"""
ai_education_daily_pipeline.py — AI 조기교육 데일리 관측소 자동 파이프라인.

흐름: source load → fetch → 7축 분류 → 연결성 점수(0~5) → update_type 판단
      → update_queue 자동 등록(score>=3, 중복방지, status=new) → daily_watch 생성 → run log.
자동 관측만. 자동 발행/사이트수정/영상/업로드 금지(Safety Guard).

사용:
  python scripts/ai_education_daily_pipeline.py --dry-run [--date 2026-07-05] [--only g-industry-media,int-unesco-aied] [--limit 6]
  python scripts/ai_education_daily_pipeline.py --write   [...]
"""
import argparse, json, os, datetime, sys, fnmatch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OPS = os.path.join(ROOT, "ops", "ai-early-education")
sys.path.insert(0, HERE)
import ai_education_source_fetcher as fetcher
import ai_education_relevance_scorer as scorer
import ai_education_queue_writer as qwriter

WATCH = os.path.join(OPS, "watch_sources.json")
QUEUE = os.path.join(OPS, "update_queue.json")
CFG   = os.path.join(OPS, "pipeline_config.json")
TAX   = os.path.join(OPS, "source_taxonomy.json")

AXIS = {  # source_category → 축
    "official_policy": "A", "international_org": "A", "government_dataset": "A",
    "news_media": "B",
    "academic_research": "C", "conference_or_workshop": "C", "nonprofit_or_research": "C",
    "school_practice": "D", "teacher_training": "D",
    "student_project": "E", "student_competition": "E",
    "youtube_channel": "F", "youtube_video": "F", "parent_community": "F", "education_company": "F",
    "ai_company_news": "G", "ai_lab_release": "G", "ai_model_release": "G", "ai_robotics": "G",
    "ai_hardware": "G", "ai_agent": "G", "ai_search": "G", "ai_companion": "G",
    "ai_safety_company": "G", "ai_education_product": "G",
}

def cat_of(s):
    """source_category 없으면 추론(레거시 공식 18개 대응)."""
    c = s.get("source_category")
    if c:
        return c
    st = s.get("source_type", ""); country = s.get("country", "")
    if st == "official":
        return "international_org" if country == "international" else "official_policy"
    if st == "international":
        return "international_org"
    if st == "media" or st == "news":
        return "news_media"
    if st == "research":
        return "academic_research"
    if st == "guide":
        return "nonprofit_or_research"
    if st == "video":
        return "youtube_video"
    return "unknown"

def guard_write_path(path, cfg):
    """Safety Guard: 금지 경로 쓰기 차단."""
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    for g in cfg["safety_guard"]["forbidden_write_globs"]:
        if fnmatch.fnmatch(rel, g):
            raise PermissionError(f"Safety Guard: 금지 경로 쓰기 차단 → {rel}")
    if not any(rel.startswith(p) for p in cfg["safety_guard"]["allowed_write_prefixes"]):
        raise PermissionError(f"Safety Guard: 허용되지 않은 경로 → {rel}")
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--only", default="")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    dry = not args.write   # 기본은 dry-run
    if args.dry_run: dry = True

    cfg = json.load(open(CFG, encoding="utf-8"))
    watch = json.load(open(WATCH, encoding="utf-8"))
    started = datetime.datetime.now().replace(microsecond=0).isoformat()

    only = {x.strip() for x in args.only.split(",") if x.strip()}
    srcs = [s for s in watch["sources"] if s.get("id")]
    if only: srcs = [s for s in srcs if s["id"] in only]
    if args.limit: srcs = srcs[:args.limit]

    fetches, candidates = [], []
    fetch_ok = fetch_failed = 0
    for s in srcs:
        fr = fetcher.fetch_source(s)
        fetches.append(fr)
        if fr["status"] == "ok": fetch_ok += 1
        elif fr["status"] == "failed": fetch_failed += 1
        if fr["status"] != "ok":
            continue
        # 스코어링 대상: RSS/피드의 '기사 단위' 항목만. 랜딩 페이지 제목 스크랩은 큐에 넣지 않음(노이즈 방지).
        cat = cat_of(s)
        if not fr["items"]:
            fr["no_article_item"] = True   # daily_watch에 '확인함, 신규 기사 항목 없음'으로 표기
            continue
        for it in fr["items"]:
            text = f"{it['title']} {fr.get('snippet','')} {' '.join(fr.get('detected_keywords',[]))}"
            score, areas, why = scorer.score_item(cat, text, it["title"])
            candidates.append({
                "discovered_date": args.date, "source_id": s["id"], "source_category": cat,
                "update_type": cfg["update_type_by_category"].get(cat, "source_lead"),
                "title": (it["title"] or fr["title"] or s["name"])[:180],
                "summary": f"[자동관측] {s['name']} — {fr.get('snippet','')[:200]}",
                "score": score, "areas": areas, "reason": f"auto score {score}: {why}",
                "parent_question": scorer.parent_question(areas),
                "affected_pages": s.get("related_pages", []),
                "source_url": it.get("link") or fr["source_url"],
                "trust_level": s.get("trust_level", ""), "hype_risk": s.get("hype_risk", "low"),
            })

    # 큐 등록(dry면 미기록)
    qres = qwriter.add_candidates(QUEUE, candidates, cfg, args.date, dry_run=dry)

    scored = len(candidates)
    ended = datetime.datetime.now().replace(microsecond=0).isoformat()

    # daily_watch + run log
    runlog = {
        "run_date": args.date, "started_at": started, "ended_at": ended, "mode": "dry-run" if dry else "write",
        "sources_checked": len(srcs), "fetch_success": fetch_ok, "fetch_failed": fetch_failed,
        "fetch_skipped": sum(1 for f in fetches if f["status"].startswith("skipped")),
        "items_scored": scored, "queue_added": qres["added"],
        "queue_skipped_duplicate": len(qres["duplicate"]),
        "queue_skipped_low_score": len(qres["low_score"]),
        "capture_attempted": 0, "capture_success": 0,
        "warnings": [], "errors": [f["error"] for f in fetches if f["status"] == "failed"][:20],
        "note": "자동 관측 로그. 사이트/영상/발행 반영 없음. 사람 승인 게이트 유지.",
    }

    if not dry:
        rp = guard_write_path(os.path.join(OPS, "pipeline_runs", f"{args.date}.json"), cfg)
        json.dump(runlog, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        dw = guard_write_path(os.path.join(OPS, "daily_watch", f"{args.date}.md"), cfg)
        os.makedirs(os.path.dirname(dw), exist_ok=True)
        write_daily_watch(dw, args.date, fetches, candidates, qres, cfg)

    # 요약 출력
    print(f"=== pipeline {'DRY-RUN' if dry else 'WRITE'} {args.date} ===")
    print(f"sources={len(srcs)} fetch_ok={fetch_ok} failed={fetch_failed} skipped_search={runlog['fetch_skipped']}")
    print(f"scored={scored} queue_added={len(qres['added'])} dup={len(qres['duplicate'])} low_score={len(qres['low_score'])}")
    by_axis = {}
    for c in candidates:
        a = AXIS.get(c["source_category"], "?"); by_axis.setdefault(a, []).append(c["score"])
    for a in sorted(by_axis):
        print(f"  축 {a}: {len(by_axis[a])}건, 점수 {sorted(by_axis[a], reverse=True)}")
    if qres["added"]:
        print("added ids:", qres["added"])
    if dry:
        print("(dry-run: 파일 미수정. --write로 daily_watch/pipeline_runs/queue 기록)")

def write_daily_watch(path, date, fetches, candidates, qres, cfg):
    ax_name = {"A": "공식 정책/문서", "B": "뉴스/언론", "C": "학회/논문/연구", "D": "학교 현장/교사",
               "E": "학생 프로젝트/대회", "F": "유튜브/기관/부모", "G": "AI 산업/빅테크"}
    lines = [f"# Daily Watch — {date} (자동 파이프라인)", "",
             "> 자동 관측 결과. 사이트/영상/발행 반영 없음. score≥3만 update_queue 등록(status=new). 사람 승인 게이트.", ""]
    byax = {}
    for c in candidates:
        byax.setdefault(AXIS.get(c["source_category"], "?"), []).append(c)
    for a in "ABCDEFG":
        lines.append(f"## {a}. {ax_name[a]}")
        items = byax.get(a, [])
        if not items:
            lines.append("- (오늘 확인 결과 없음/미해당)"); lines.append(""); continue
        for c in items:
            reg = "→ queue 등록" if c["score"] >= cfg["min_score_to_queue"] else "→ 보류(score<3)"
            lines.append(f"- [{c['source_id']}] score {c['score']} {reg} · {c['title'][:80]}")
            lines.append(f"    부모 질문: {c['parent_question']}  | {c['reason']}")
        lines.append("")
    checked_no_item = [f["source_id"] for f in fetches if f.get("no_article_item")]
    lines += ["## 종합", f"- queue 추가: {qres['added']}",
              f"- 중복 skip: {len(qres['duplicate'])} · 저점수 skip: {len(qres['low_score'])}",
              f"- 확인만(랜딩 페이지·신규 기사 항목 없음): {len(checked_no_item)}개 {checked_no_item[:12]}",
              f"- fetch 실패: {sum(1 for f in fetches if f['status']=='failed')} · 검색페이지 skip(동적): {sum(1 for f in fetches if f['status'].startswith('skipped'))}",
              "- ⚠️ 뉴스/유튜브/기업발표=사실 근거 아님. 미성년자 자료 캡처 금지. 사이트 반영은 사람 승인 후.", "",
              "---", "확인자: automated_pipeline · 관측 로그(비공개)."]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()
