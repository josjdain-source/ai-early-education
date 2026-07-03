#!/usr/bin/env python3
"""
capture_evidence.py — AI 조기교육 데일리 관측소: 공식 자료 자동 캡처기

핵심 원칙:
- AI 생성 이미지로 공식 페이지를 흉내내지 않는다. 본문 화면은 반드시 실제 브라우저 캡처.
- 상단 출처 메타 바는 '생성 증거'가 아니라 우리가 붙인 출처 라벨(캡처 메타데이터).
- 문구를 페이지에서 못 찾으면 failed/partial로 정직하게 기록(가짜 캡처 금지).

사용:
  python scripts/capture_evidence.py \
    --manifest assets/ai-early-education/singapore-evidence/evidence_manifest.json \
    --outdir  assets/ai-early-education/singapore-evidence \
    [--only C03,C04] [--date 2026-07-04] [--headed]

Playwright(내장 Chromium)는 Chrome의 Google 자동번역이 없어 원문 언어가 유지된다.
"""
import argparse, json, os, sys, datetime, re

from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

BAR_H = 84
KFONT = r"C:\Windows\Fonts\malgun.ttf"      # 한국어 렌더용(있으면)
LFONT = r"C:\Windows\Fonts\arial.ttf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def substrings(highlight):
    """visible_highlight_text('A | B | C')를 검색 후보로 분해. 길수록 먼저."""
    parts = [p.strip() for p in re.split(r"\s*\|\s*", highlight or "") if p.strip()]
    cands = []
    for p in parts:
        cands.append(p)
        words = p.split()
        if len(words) >= 6:                 # 긴 문구는 앞부분 부분탐색도 후보로
            cands.append(" ".join(words[:6]))
        if len(words) >= 4:
            cands.append(" ".join(words[:4]))
    # 중복 제거(순서 유지)
    seen, out = set(), []
    for c in cands:
        if c.lower() not in seen:
            seen.add(c.lower()); out.append(c)
    return out

def compose_source_bar(png_path, source_name, url, date, verify_note):
    """실제 페이지 캡처 위에 출처 라벨 바를 합성."""
    page_img = Image.open(png_path).convert("RGB")
    W = page_img.width
    bar = Image.new("RGB", (W, BAR_H), (24, 26, 42))
    d = ImageDraw.Draw(bar)
    f1 = load_font(KFONT, 22); f2 = load_font(LFONT, 17); f3 = load_font(LFONT, 15)
    d.text((16, 8),  f"Source: {source_name}", font=f1, fill=(255, 255, 255))
    d.text((16, 38), f"URL: {url}", font=f2, fill=(150, 200, 255))
    d.text((16, 60), f"Captured: {date}  |  {verify_note}  |  (출처 라벨=우리가 부착, 아래=실제 페이지 캡처)",
           font=f3, fill=(180, 180, 190))
    out = Image.new("RGB", (W, BAR_H + page_img.height), (255, 255, 255))
    out.paste(bar, (0, 0)); out.paste(page_img, (0, BAR_H))
    out.save(png_path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--only", default="")   # e.g. "C03,C04"
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        man = json.load(f)
    only = {x.strip() for x in args.only.split(",") if x.strip()}
    os.makedirs(args.outdir, exist_ok=True)

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        ctx = browser.new_context(
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()

        for it in man["items"]:
            cid = it.get("cut_id", "")
            fn  = it.get("filename", "")
            if only and cid not in only:
                continue
            if it.get("capture_status") == "skip" or it.get("verification_status") == "not_found":
                results.append((cid, "skip", "verification=not_found/skip")); continue
            if not fn or fn.startswith("("):
                results.append((cid, "skip", "no filename")); continue

            url = it.get("source_url", "")
            highlight = it.get("visible_highlight_text") or it.get("highlight_text") or ""
            outpath = os.path.join(args.outdir, fn)
            status, note, confirmed = "failed", "", ""
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(2500)
                # 쿠키/배너 있으면 무시(캡처엔 영향 적음). 번역 팝업 없음(내장 크로미움).
                found_loc = None
                for cand in substrings(highlight):
                    try:
                        loc = page.get_by_text(cand, exact=False).first
                        if loc.count() > 0:
                            loc.scroll_into_view_if_needed(timeout=4000)
                            found_loc = cand; break
                    except Exception:
                        continue
                if found_loc:
                    status = "captured" if found_loc == substrings(highlight)[0] else "partial"
                    confirmed = found_loc
                    note = "text found on page (full)" if status == "captured" else "text found (partial match)"
                else:
                    status = "failed"; note = "highlight text NOT found on page"
                    confirmed = ""
                # 문구를 못 찾아도 페이지 자체는 실제로 열렸으므로 참고 캡처는 남기되 status는 failed로 정직 표기
                page.wait_for_timeout(600)
                page.screenshot(path=outpath, full_page=False)
                compose_source_bar(outpath, it.get("source_name", ""), url, args.date, note)
                size = os.path.getsize(outpath)
                if size == 0:
                    status, note = "failed", "0-byte file"
            except Exception as e:
                status, note = "failed", f"error: {type(e).__name__}: {e}"[:200]

            # manifest 갱신(정직)
            it["capture_status"] = status
            it["actual_capture_file"] = fn if status in ("captured", "partial") else ""
            it["captured_at"] = args.date if status in ("captured", "partial") else None
            it["visible_text_confirmed"] = confirmed
            it["capture_method"] = "automated_browser_playwright"
            it["caution"] = (it.get("caution", "") + f" | [auto {args.date}] {note}").strip(" |")
            results.append((cid, status, note))

        browser.close()

    with open(args.manifest, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)

    print("=== capture results ===")
    for cid, st, nt in results:
        print(f"{cid:14s} {st:9s} {nt}")
    ok = sum(1 for _, s, _ in results if s in ("captured", "partial"))
    print(f"--- captured/partial: {ok} / attempted: {len(results)} ---")

if __name__ == "__main__":
    main()
