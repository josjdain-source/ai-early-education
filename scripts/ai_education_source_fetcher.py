#!/usr/bin/env python3
"""
ai_education_source_fetcher.py — 관측소 소스 fetch 모듈.

watch_sources의 각 source에서 최신 항목(제목/스니펫/날짜)을 가져온다.
- RSS/공식 페이지: urllib로 GET 후 title/텍스트 발췌.
- search URL(youtube/news 검색): 검색 페이지는 동적이라 텍스트 발췌만(제목 목록 불확실) → status=skipped_search로 표기(가짜 결과 금지).
네트워크 실패/차단 시 status=failed. 절대 결과를 지어내지 않는다.
"""
import re, json, urllib.request, urllib.error, datetime, html

UA = {"User-Agent": "Mozilla/5.0 (compatible; AIEduObservatory/1.0)"}

def _get(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(600000)
        enc = r.headers.get_content_charset() or "utf-8"
        return raw.decode(enc, "ignore")

def _title(txt):
    m = re.search(r"<title[^>]*>(.*?)</title>", txt, re.I | re.S)
    return html.unescape(re.sub(r"\s+", " ", m.group(1)).strip())[:200] if m else ""

def _rss_items(txt, n=5):
    items = []
    for m in re.finditer(r"<(item|entry)[^>]*>(.*?)</\1>", txt, re.I | re.S):
        block = m.group(2)
        t = re.search(r"<title[^>]*>(.*?)</title>", block, re.I | re.S)
        l = re.search(r"<link[^>]*>(.*?)</link>|<link[^>]*href=\"(.*?)\"", block, re.I | re.S)
        dd = re.search(r"<(pubDate|updated|published)[^>]*>(.*?)</\1>", block, re.I | re.S)
        title = html.unescape(re.sub(r"<[^>]+>|\s+", " ", t.group(1)).strip()) if t else ""
        link = (l.group(1) or l.group(2)).strip() if l else ""
        date = dd.group(2).strip() if dd else ""
        if title:
            items.append({"title": title[:200], "link": link[:400], "date": date[:40]})
        if len(items) >= n:
            break
    return items

def _text_excerpt(txt, n=600):
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", txt, flags=re.I | re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html.unescape(re.sub(r"\s+", " ", body)).strip()
    return body[:n]

def fetch_source(src):
    """단일 source fetch. dict 반환(결과를 지어내지 않음)."""
    now = datetime.datetime.now().replace(microsecond=0).isoformat()
    url = (src.get("url") or "").split(" ; ")[0].strip()   # 여러 URL이면 첫 번째
    res = {"source_id": src.get("id"), "source_name": src.get("name"), "source_url": url,
           "source_category": src.get("source_category", ""), "fetched_at": now,
           "status": "skipped", "title": "", "snippet": "", "raw_text_excerpt": "",
           "detected_date": "", "detected_keywords": [], "error": "", "items": []}
    if not url:
        res["status"] = "skipped"; res["error"] = "no url"; return res
    is_search = any(s in url for s in ["/results?search_query=", "/search?", "search.naver", "news.google", "scholar.google", "riss.kr/search"])
    if is_search:
        # 검색 결과 페이지는 동적/JS라 신뢰 파싱 불가 → 결과 지어내지 않음
        res["status"] = "skipped_search"
        res["error"] = "search-page(dynamic): 자동 파싱 미신뢰. 사람/전용 API로 확인 필요."
        return res
    try:
        txt = _get(url)
        res["title"] = _title(txt)
        rss = _rss_items(txt) if ("<rss" in txt[:2000].lower() or "<feed" in txt[:2000].lower() or "</item>" in txt.lower()) else []
        if rss:
            res["items"] = rss
            res["snippet"] = " | ".join(i["title"] for i in rss[:3])[:400]
            res["detected_date"] = rss[0]["date"]
        else:
            res["raw_text_excerpt"] = _text_excerpt(txt)
            res["snippet"] = res["raw_text_excerpt"][:200]
        kws = [k for k in ["AI", "children", "student", "school", "parent", "generative", "robot",
                            "companion", "literacy", "감정", "학생", "초등", "부모", "교과서", "로봇"]
               if k.lower() in txt.lower()]
        res["detected_keywords"] = kws[:12]
        res["status"] = "ok"
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception) as e:
        res["status"] = "failed"; res["error"] = f"{type(e).__name__}: {e}"[:200]
    return res
