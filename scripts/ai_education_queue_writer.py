#!/usr/bin/env python3
"""
ai_education_queue_writer.py — update_queue 자동 등록(중복 방지, score>=min).
status는 항상 new, approved_by/applied_commit=null. published/applied 처리 절대 안 함.
"""
import json, datetime, re

def _norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())

def load_queue(path):
    return json.load(open(path, encoding="utf-8"))

def existing_keys(q):
    titles = {_norm(i.get("title", "")) for i in q["items"]}
    urls = set()
    for i in q["items"]:
        for u in re.split(r"\s*;\s*", i.get("source_url", "") or ""):
            if u.strip():
                urls.add(u.strip())
    return titles, urls

def build_item(cand, cfg, seq_date, seq_n):
    cat = cand["source_category"]
    fact_ok = cat in cfg["fact_capable_categories"]
    hi_minor = cat in cfg["high_minor_risk_categories"]
    return {
        "id": f"{cfg['queue_id_prefix']}-{seq_date}-{seq_n:02d}",
        "discovered_date": cand["discovered_date"],
        "source_id": cand["source_id"],
        "source_category": cat,
        "update_type": cand["update_type"],
        "title": cand["title"],
        "summary": cand["summary"],
        "education_relevance_score": cand["score"],
        "parent_question": cand["parent_question"],
        "affected_pages": cand.get("affected_pages", []),
        "impact_level": "high" if cand["score"] >= 5 else ("medium" if cand["score"] >= 4 else "low"),
        "status": "new",
        "source_url": cand["source_url"],
        "trust_level": cand.get("trust_level", ""),
        "can_update_site_fact": bool(fact_ok),
        "can_generate_video_topic": True,
        "privacy_risk": "high" if hi_minor else "low",
        "minor_data_risk": "high" if hi_minor else "low",
        "hype_risk": cand.get("hype_risk", "low"),
        "requires_anonymization": bool(hi_minor),
        "do_not_use_as_policy_fact": (not fact_ok),
        "reason": cand["reason"],
        "checked_by": cfg["checked_by"],
        "approved_by": None,
        "applied_commit": None,
    }

def add_candidates(queue_path, candidates, cfg, run_date, dry_run=True):
    q = load_queue(queue_path)
    titles, urls = existing_keys(q)
    added, dup, low = [], [], []
    seq_n = 90  # 자동 등록분은 90번대로(수동 UQ와 충돌 회피)
    for c in candidates:
        if c["score"] < cfg["min_score_to_queue"]:
            low.append(c["title"]); continue
        if _norm(c["title"]) in titles or (c["source_url"] and c["source_url"] in urls):
            dup.append(c["title"]); continue
        item = build_item(c, cfg, run_date.replace("-", ""), seq_n); seq_n += 1
        titles.add(_norm(c["title"])); urls.add(c["source_url"])
        q["items"].append(item); added.append(item["id"])
    if not dry_run and added:
        json.dump(q, open(queue_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return {"added": added, "duplicate": dup, "low_score": low, "wrote": (not dry_run and bool(added))}
