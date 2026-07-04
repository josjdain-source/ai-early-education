#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""업로드 검수대 — 사람이 '승인' 누른 영상만 유튜브(아이와 AI교실)에 비공개 업로드.
자동 업로드 금지. upload_queue.json의 ready_to_upload 항목을 카드로 보여주고, 버튼 클릭 시에만 업로드.
실행: python youtube/upload_desk.py  → http://127.0.0.1:8971"""
import json, os, subprocess, urllib.parse, mimetypes, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.dirname(HERE)
QF=os.path.join(HERE,"upload_queue.json"); PORT=8971
PYEXE="python"
def load(): return json.load(open(QF,encoding="utf-8"))
def ap(p): return p if os.path.isabs(p) else os.path.join(REPO,p)
_lock=threading.Lock()

def card(it):
    vid=it["video_id"]; st=it["status"]; url=it.get("youtube_url") or ""
    mp4=ap(it.get("mp4_path","")); exists=os.path.exists(mp4)
    thumb=f"/poster?p={urllib.parse.quote(it.get('thumbnail_path',''))}" if it.get("thumbnail_path") else ""
    kind="쇼츠" if it.get("shorts") else "롱폼"
    if st=="ready_to_upload":
        btn=(f'<button class="go" onclick="up(this,\'{vid}\')">✅ 승인하고 업로드</button>' if exists
             else '<span class="warn">⚠️ 로컬 mp4 없음(정리됨)</span>')
        badge='<span class="b ready">업로드 대기</span>'
    elif st=="uploaded_private":
        btn=f'<a class="link" href="https://studio.youtube.com/video/{url.rstrip("/").split("/")[-1]}/edit" target="_blank">🔒 스튜디오에서 공개 승인 →</a>'
        badge='<span class="b done">업로드됨·비공개</span>'
    elif st in ("approved_public","published"):
        btn=f'<a class="link" href="{url}" target="_blank">▶ 공개됨</a>'; badge='<span class="b pub">공개</span>'
    else:
        btn=''; badge=f'<span class="b">{st}</span>'
    img=f'<img src="{thumb}" loading="lazy">' if thumb else '<div class="noimg">🎬</div>'
    return f"""<div class="card" id="c_{vid}">
<div class="thumb {'v' if it.get('shorts') else ''}">{img}</div>
<div class="meta"><div class="row">{badge}<span class="kind">{kind}</span></div>
<h3>{it['title']}</h3>
<p class="vid">{vid}</p>
<div class="act">{btn}</div><div class="msg" id="m_{vid}"></div></div></div>"""

def page():
    q=load()["queue"]; ready=[it for it in q if it["status"]=="ready_to_upload"]
    priv=[it for it in q if it["status"]=="uploaded_private"]; other=[it for it in q if it["status"] not in ("ready_to_upload","uploaded_private")]
    def sec(t,items): return f'<h2>{t} <span class="cnt">{len(items)}</span></h2><div class="grid">{"".join(card(i) for i in items)}</div>' if items else ""
    body=sec("① 업로드 대기 — 승인하면 올라갑니다",ready)+sec("② 업로드됨(비공개) — 스튜디오에서 공개 승인",priv)+sec("③ 기타",other)
    return f"""<!doctype html><html lang=ko><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>업로드 검수대 · 아이와 AI교실</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#14171f;color:#e8e6df;font-family:"Malgun Gothic",system-ui,sans-serif}}
header{{padding:18px 24px;background:#1b2029;border-bottom:1px solid #2a303c;position:sticky;top:0;z-index:5}}
header h1{{margin:0;font-size:19px}}header p{{margin:4px 0 0;color:#8b93a3;font-size:13px}}
.wrap{{max-width:1100px;margin:0 auto;padding:20px 24px 60px}}
h2{{font-size:16px;margin:26px 0 12px;color:#cdd3df}}.cnt{{color:#8b93a3;font-weight:400;font-size:13px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.card{{background:#1b2029;border:1px solid #2a303c;border-radius:14px;overflow:hidden;display:flex;flex-direction:column}}
.thumb{{aspect-ratio:16/9;background:#0e1116;display:grid;place-items:center;overflow:hidden}}
.thumb.v{{aspect-ratio:1/1}}.thumb img{{width:100%;height:100%;object-fit:cover}}.noimg{{font-size:34px}}
.meta{{padding:12px 14px}}.row{{display:flex;gap:8px;align-items:center;margin-bottom:6px}}
.b{{font-size:11px;padding:2px 8px;border-radius:8px;background:#333a48}}.b.ready{{background:#3a2f10;color:#e3b24c}}.b.done{{background:#12303a;color:#5bb7d1}}.b.pub{{background:#12341f;color:#6bd18a}}
.kind{{font-size:11px;color:#8b93a3}}h3{{margin:0 0 4px;font-size:14.5px;line-height:1.35}}.vid{{margin:0 0 10px;color:#6b7280;font-size:11px}}
.go{{background:#e3b24c;color:#1a1a1a;border:0;border-radius:9px;padding:9px 14px;font-weight:700;cursor:pointer;font-size:13.5px;width:100%}}
.go:hover{{background:#f0c265}}.go:disabled{{opacity:.5;cursor:wait}}
.link{{color:#5bb7d1;text-decoration:none;font-size:13px;font-weight:600}}.warn{{color:#e0894f;font-size:12.5px}}
.msg{{margin-top:8px;font-size:12.5px}}.ok{{color:#6bd18a}}.err{{color:#e06a5a}}
</style></head><body>
<header><h1>🎬 업로드 검수대 · 아이와 AI교실</h1><p>자동 업로드 없음. 여기서 <b>승인</b>한 것만 비공개로 올라갑니다. 최종 공개는 유튜브 스튜디오에서.</p></header>
<div class="wrap">{body}</div>
<script>
async function up(btn,vid){{btn.disabled=true;btn.textContent='업로드 중…';const m=document.getElementById('m_'+vid);m.textContent='';
try{{const r=await fetch('/upload',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{video_id:vid}})}});const d=await r.json();
if(d.ok){{m.innerHTML='<span class=ok>✅ 업로드됨(비공개): <a href="'+d.url+'" target=_blank>'+d.url+'</a> — 스튜디오에서 공개하세요</span>';btn.textContent='완료';}}
else{{m.innerHTML='<span class=err>❌ '+d.error+'</span>';btn.disabled=false;btn.textContent='다시 승인';}}
}}catch(e){{m.innerHTML='<span class=err>❌ '+e+'</span>';btn.disabled=false;btn.textContent='다시 승인';}}}}
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def _send(self,code,ctype,data):
        self.send_response(code); self.send_header("Content-Type",ctype); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        u=urllib.parse.urlparse(self.path)
        if u.path=="/": self._send(200,"text/html; charset=utf-8",page().encode("utf-8"))
        elif u.path=="/poster":
            p=urllib.parse.parse_qs(u.query).get("p",[""])[0]; fp=ap(p)
            if p and os.path.exists(fp) and os.path.commonpath([os.path.realpath(fp),REPO])==REPO:
                self._send(200,mimetypes.guess_type(fp)[0] or "image/jpeg",open(fp,"rb").read())
            else: self._send(404,"text/plain","no")
        else: self._send(404,"text/plain",b"404")
    def do_POST(self):
        if urllib.parse.urlparse(self.path).path!="/upload": return self._send(404,"text/plain",b"404")
        n=int(self.headers.get("Content-Length",0)); vid=json.loads(self.rfile.read(n) or b"{}").get("video_id","")
        with _lock:
            try:
                r=subprocess.run([PYEXE,os.path.join(HERE,"upload_to_aiclassroom.py"),"--id",vid],cwd=REPO,capture_output=True,text=True,timeout=600)
                out=(r.stdout or "")+(r.stderr or "")
            except Exception as e: out=f"실행 오류: {e}"
        url=""
        for tok in out.replace("\n"," ").split():
            if "youtu.be/" in tok or "youtube.com/watch" in tok: url=tok.strip("().,"); break
        if url: res={"ok":True,"url":url}
        elif "uploadLimitExceeded" in out or "exceeded the number of videos" in out: res={"ok":False,"error":"유튜브 일일 업로드 한도 초과. 리셋(약 24시간) 후 다시 승인하세요."}
        elif "채널 가드" in out and "거부" in out: res={"ok":False,"error":"채널 가드: 대상 채널 불일치"}
        else: res={"ok":False,"error":("업로드 실패: "+out.strip()[-180:]) if out.strip() else "알 수 없는 오류"}
        self._send(200,"application/json; charset=utf-8",json.dumps(res,ensure_ascii=False).encode("utf-8"))

if __name__=="__main__":
    print(f"업로드 검수대: http://127.0.0.1:{PORT}  (승인한 것만 업로드)")
    ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
