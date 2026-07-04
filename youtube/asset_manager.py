#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""콘텐츠 파일 관리자 + 검수실 — YouTube Studio/Drive 스타일.
영상·이미지·문서 산출물을 표로 관리: 필터·검색·체크박스·일괄작업·삭제(휴지통)·복원·최종본 지정·안전장치.
★영구삭제 전 휴지통. 보호파일/최종본/홈페이지사용/업로드대기/youtube없는영상은 삭제 차단.
실행: python youtube/asset_manager.py → http://127.0.0.1:8972"""
import json, os, glob, subprocess, urllib.parse, mimetypes, re, threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.dirname(HERE)
QF=os.path.join(HERE,"upload_queue.json"); PORT=8972; _lock=threading.Lock()
DATA=os.path.join(REPO,"data"); LOGS=os.path.join(REPO,"logs")
IDX=os.path.join(DATA,"production_assets.json"); TRASH=os.path.join(DATA,"trash_manifest.json"); DLOG=os.path.join(LOGS,"asset_delete.log")
for d in (DATA,LOGS): os.makedirs(d,exist_ok=True)
COUNTRY={"china":"중국","usa":"미국","uk":"영국","singapore":"싱가포르","korea":"한국","":"공통"}
def jload(p,dflt):
    try: return json.load(open(p,encoding="utf-8"))
    except Exception: return dflt
def jsave(p,o): json.dump(o,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
def now(): return datetime.now().strftime("%Y-%m-%d %H:%M")
def rel(p):
    try: return os.path.relpath(p,REPO).replace("\\","/")
    except Exception: return p
def size_h(n):
    for u in ("B","KB","MB","GB"):
        if n<1024: return f"{n:.0f}{u}" if u=="B" else f"{n:.1f}{u}"
        n/=1024
    return f"{n:.1f}TB"
def html_embed_ids():
    ids=set()
    for f in glob.glob(os.path.join(REPO,"videos*.html"))+glob.glob(os.path.join(REPO,"videos","*.html"))+glob.glob(os.path.join(REPO,"world-cases","*.html")):
        try: ids|=set(re.findall(r"embed/([A-Za-z0-9_-]{11})",open(f,encoding="utf-8").read()))
        except Exception: pass
    return ids
def html_text():
    t=""
    for f in glob.glob(os.path.join(REPO,"*.html"))+glob.glob(os.path.join(REPO,"videos","*.html"))+glob.glob(os.path.join(REPO,"world-cases","*.html")):
        try: t+=open(f,encoding="utf-8").read()
        except Exception: pass
    return t

# ---------- 상태 저장(overrides) ----------
def state(): return jload(IDX,{"_schema":"assets-v1","overrides":{}})
def save_state(s): jsave(IDX,s)
def trash(): return jload(TRASH,{"items":[]})
def save_trash(t): jsave(TRASH,t)
def is_trashed(aid): return any(x["id"]==aid for x in trash()["items"])

# ---------- 인덱싱 ----------
def index():
    ov=state()["overrides"]; eids=html_embed_ids(); htext=html_text()
    q=jload(QF,{"queue":[]})["queue"]; qmap={it.get("mp4_path",""):it for it in q}
    trashed={x["id"] for x in trash()["items"]}
    out=[]
    # 1) 영상 (upload_queue)
    for it in q:
        p=it.get("mp4_path",""); aid="q:"+it["video_id"]
        if aid in trashed: continue
        yid=it.get("youtube_id") or ""
        hp="connected" if yid and yid in eids else ("pending" if yid else "none")
        o=ov.get(aid,{})
        st=o.get("status") or _vstatus(it)
        out.append({"id":aid,"title":it.get("title",it["video_id"]),"type":"video",
          "subtype":"short" if it.get("shorts") else "longform","path":p,
          "thumbnail_path":it.get("thumbnail_path",""),"project":it.get("package_id",""),
          "country":it.get("country",""),"created_at":it.get("created_at",""),
          "duration":it.get("duration"),"size":_size(p),
          "status":st,"is_final":o.get("is_final",False),
          "is_protected":it.get("status")=="ready_to_upload" and not yid,
          "is_used_by_homepage":hp=="connected","youtube_id":yid,"youtube_url":it.get("youtube_url",""),
          "studio_url":it.get("studio_url",""),"page_url":it.get("page_url","") or it.get("detail_page",""),
          "upload_status":it.get("upload_status",it.get("status","")),"public_status":it.get("public_status",""),
          "homepage_status":hp,"upload_queue_id":it["video_id"],"local_exists":os.path.exists(_abs(p)),
          "ratio":"9:16" if it.get("shorts") else "16:9","views":it.get("views"),"comments":it.get("comments"),
          "notes":o.get("notes","")})
    # 2) 이미지 (포스터/썸네일)
    for f in glob.glob(os.path.join(REPO,"assets","*","poster","*.jpg"))+glob.glob(os.path.join(REPO,"assets","*","poster","*.png")):
        rp=rel(f); aid="img:"+rp
        if aid in trashed: continue
        o=ov.get(aid,{}); used=os.path.basename(f) in htext
        pkg=rp.split("/")[1] if "/" in rp else ""
        out.append({"id":aid,"title":os.path.basename(f),"type":"image","subtype":"poster","path":rp,
          "thumbnail_path":rp,"project":pkg,"country":"","created_at":_mtime(f),"duration":None,
          "size":_size(rp),"status":o.get("status","draft"),"is_final":o.get("is_final",False),
          "is_protected":False,"is_used_by_homepage":used,"youtube_id":"","youtube_url":"","studio_url":"",
          "page_url":"","upload_status":"","public_status":"","homepage_status":"connected" if used else "none",
          "local_exists":True,"ratio":"","views":None,"comments":None,"notes":o.get("notes","")})
    # 3) 문서 (plan/metadata/facts/sources)
    docs=(glob.glob(os.path.join(REPO,"production","*_plan.json"))+glob.glob(os.path.join(REPO,"production","*_metadata.json"))
          +glob.glob(os.path.join(REPO,"facts","*.json"))+glob.glob(os.path.join(REPO,"sources","*.json"))
          +glob.glob(os.path.join(REPO,"production","*_pacing.json"))+glob.glob(os.path.join(REPO,"production","voice_profiles.json")))
    for f in docs:
        rp=rel(f); aid="doc:"+rp
        if aid in trashed: continue
        prot=("/facts/" in "/"+rp or "/sources/" in "/"+rp or "_plan.json" in rp)
        sub=("facts" if "/facts/" in "/"+rp else "sources" if "/sources/" in "/"+rp else
             "plan" if "_plan" in rp else "metadata" if "_metadata" in rp else "config")
        o=ov.get(aid,{})
        out.append({"id":aid,"title":os.path.basename(f),"type":"doc","subtype":sub,"path":rp,
          "thumbnail_path":"","project":"","country":"","created_at":_mtime(f),"duration":None,"size":_size(rp),
          "status":o.get("status","draft"),"is_final":o.get("is_final",False),"is_protected":prot,
          "is_used_by_homepage":False,"youtube_id":"","youtube_url":"","studio_url":"","page_url":"",
          "upload_status":"","public_status":"","homepage_status":"none","local_exists":True,"ratio":"",
          "views":None,"comments":None,"notes":o.get("notes","")})
    return out
def _vstatus(it):
    us=it.get("upload_status",it.get("status",""))
    if us=="quota_exceeded": return "quota"
    if us=="failed": return "failed"
    if us=="superseded": return "dup"
    if us=="published" or it.get("public_status")=="public": return "public"
    if us=="uploaded_private": return "private"
    if us=="ready_to_upload": return "upload_wait"
    return "draft"
def _abs(p): return p if os.path.isabs(p) else os.path.join(REPO,p)
def _size(p):
    a=_abs(p); return os.path.getsize(a) if os.path.exists(a) else 0
def _mtime(f):
    try: return datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M")
    except Exception: return ""

def summary(items):
    return {"video":sum(1 for i in items if i["type"]=="video"),"image":sum(1 for i in items if i["type"]=="image"),
      "doc":sum(1 for i in items if i["type"]=="doc"),
      "review":sum(1 for i in items if i["status"] in("draft","final_cand")),
      "upload_wait":sum(1 for i in items if i["status"]=="upload_wait"),
      "trash_cand":sum(1 for i in items if i["status"]=="trash_cand"),
      "final":sum(1 for i in items if i["is_final"]),"trash":len(trash()["items"])}

# ---------- 안전 삭제 ----------
def find(aid):
    for it in index():
        if it["id"]==aid: return it
    return None
def can_delete(it):
    if it["is_protected"]: return False,"보호 파일(plan/facts/sources 또는 업로드대기)"
    if it["is_final"]: return False,"최종본으로 지정됨"
    if it["is_used_by_homepage"]: return False,"홈페이지에서 사용 중"
    if it["type"]=="video":
        if it["upload_status"]=="ready_to_upload" and not it["youtube_id"]: return False,"업로드 대기(유튜브 없음)"
        if not it["youtube_id"] and it["local_exists"]: return False,"아직 업로드 안 된 영상"
    return True,""
def do_trash(ids):
    with _lock:
        t=trash(); res={"trashed":[],"blocked":[]}
        for aid in ids:
            it=find(aid)
            if not it: res["blocked"].append({"id":aid,"why":"없음"}); continue
            ok,why=can_delete(it)
            if not ok: res["blocked"].append({"id":aid,"title":it["title"],"why":why}); continue
            t["items"].append({"id":aid,"title":it["title"],"type":it["type"],"path":it["path"],
              "trashed_at":now(),"origin":it.get("project","")})
            open(DLOG,"a",encoding="utf-8").write(f"[{now()}] TRASH {aid} {it['path']}\n")
            res["trashed"].append(aid)
        save_trash(t); return res
def do_restore(ids):
    with _lock:
        t=trash(); t["items"]=[x for x in t["items"] if x["id"] not in ids]; save_trash(t)
        open(DLOG,"a",encoding="utf-8").write(f"[{now()}] RESTORE {ids}\n"); return {"ok":True}
def do_purge(ids):
    with _lock:
        t=trash(); killed=[]
        for x in list(t["items"]):
            if x["id"] in ids:
                fp=_abs(x["path"])
                # 재확인: 큐 ready/보호 재검사(질의 시점)
                try:
                    if os.path.exists(fp) and os.path.realpath(fp).startswith(os.path.realpath(REPO)):
                        os.remove(fp); killed.append(x["path"])
                except Exception as e: killed.append(f"실패 {x['path']}:{e}")
                open(DLOG,"a",encoding="utf-8").write(f"[{now()}] PURGE {x['id']} {x['path']}\n")
                t["items"]=[y for y in t["items"] if y["id"]!=x["id"]]
        save_trash(t); return {"ok":True,"deleted":killed}
def set_override(ids,patch):
    with _lock:
        s=state()
        for aid in ids: s["overrides"].setdefault(aid,{}).update(patch)
        save_state(s); return {"ok":True,"n":len(ids)}
def do_queue_register(ids):
    # 영상 자산을 upload_queue에 ready_to_upload로 (이미 큐면 no-op)
    with _lock:
        q=jload(QF,{"queue":[]}); n=0
        for aid in ids:
            it=find(aid)
            if it and it["type"]=="video" and it.get("upload_queue_id"):
                for x in q["queue"]:
                    if x["video_id"]==it["upload_queue_id"] and x.get("status")not in("ready_to_upload","uploaded_private","published"):
                        x["status"]="ready_to_upload"; x["upload_status"]="ready_to_upload"; n+=1
        jsave(QF,q); return {"ok":True,"n":n}
def open_folder(aid):
    it=find(aid)
    if not it: return {"ok":False,"error":"없음"}
    fp=_abs(it["path"])
    try:
        if os.path.exists(fp): subprocess.Popen(["explorer","/select,",os.path.normpath(fp)])
        else: subprocess.Popen(["explorer",os.path.normpath(os.path.dirname(fp))])
        return {"ok":True}
    except Exception as e: return {"ok":False,"error":str(e)}

def detect_candidates():
    """중복·실패·구버전 자동 탐지. 삭제 가능(안전)한 것만 후보로. 반환: {id:reason}"""
    items=index(); cands={}
    # 1) 같은 제목 영상 그룹 → 최신본(최종본/업로드된 최신) 1개만 남기고 구버전 후보
    groups={}
    for it in items:
        if it["type"]=="video": groups.setdefault(it["title"].strip(),[]).append(it)
    def verkey(x):
        m=re.search(r'-v(\d+)', x["path"]); v=int(m.group(1)) if m else 0
        return (1 if x["is_final"] else 0, 1 if x["youtube_id"] else 0, v, x.get("created_at",""), x["path"])
    for title,g in groups.items():
        if len(g)<2: continue
        keeper=sorted(g,key=verkey)[-1]   # 최종본>업로드됨>높은버전>최신
        for x in g:
            if x["id"]==keeper["id"]: continue
            ok,_=can_delete(x)
            if ok: cands[x["id"]]=f"구버전 · 최신본 있음(유지: {keeper['path'].split('/')[-1]})"
    # 2) superseded(대체됨) / failed(실패) 전역
    for it in items:
        if it["id"] in cands: continue
        us=it.get("upload_status","")
        ok,_=can_delete(it)
        if not ok: continue
        if us=="superseded": cands[it["id"]]="대체된 구버전(superseded)"
        elif us=="failed": cands[it["id"]]="실패 렌더"
    # 3) 이미지: 홈페이지 미사용 + 같은 폴더 중복 썸네일(옛 버전) — 안전한 것만
    imgs=[it for it in items if it["type"]=="image" and not it["is_used_by_homepage"]]
    bygroup={}
    for it in imgs:
        base=re.sub(r'-v?\d+(\.\w+)$', r'\1', it["path"]); bygroup.setdefault(base,[]).append(it)
    for base,g in bygroup.items():
        if len(g)<2: continue
        keep=sorted(g,key=lambda x:x.get("created_at",""))[-1]
        for x in g:
            if x["id"]!=keep["id"] and x["id"] not in cands:
                ok,_=can_delete(x)
                if ok: cands[x["id"]]="중복 의심 썸네일(구버전)"
    return cands
def do_detect():
    c=detect_candidates()
    with _lock:
        s=state()
        for aid,why in c.items(): s["overrides"].setdefault(aid,{}).update({"status":"trash_cand","notes":"삭제후보: "+why})
        save_state(s)
    return {"ok":True,"count":len(c),"items":[{"id":k,"reason":v} for k,v in c.items()]}

HTML=open(os.path.join(HERE,"_assets.html"),encoding="utf-8").read() if os.path.exists(os.path.join(HERE,"_assets.html")) else "NO_HTML"

class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def _j(self,o,c=200): self._send(c,"application/json; charset=utf-8",json.dumps(o,ensure_ascii=False).encode())
    def _send(self,c,ct,d):
        if isinstance(d,str): d=d.encode()
        self.send_response(c); self.send_header("Content-Type",ct); self.send_header("Content-Length",str(len(d))); self.end_headers()
        try: self.wfile.write(d)
        except Exception: pass
    def _body(self):
        n=int(self.headers.get("Content-Length",0))
        try: return json.loads(self.rfile.read(n) or b"{}")
        except Exception: return {}
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); qs=urllib.parse.parse_qs(u.query)
        if u.path=="/": self._send(200,"text/html; charset=utf-8",HTML)
        elif u.path=="/api/assets":
            items=index(); self._j({"assets":items,"summary":summary(items)})
        elif u.path=="/api/trash": self._j({"items":trash()["items"]})
        elif u.path=="/api/meta":
            self._j(find(qs.get("id",[""])[0]) or {})
        elif u.path=="/thumb":
            p=qs.get("p",[""])[0]; fp=_abs(p)
            if p and os.path.exists(fp) and os.path.realpath(fp).startswith(os.path.realpath(REPO)):
                self._send(200,mimetypes.guess_type(fp)[0] or "image/jpeg",open(fp,"rb").read())
            else: self._send(404,"text/plain","no")
        elif u.path=="/media":
            aid=qs.get("id",[""])[0]; it=find(aid); fp=_abs(it["path"]) if it else ""
            if it and os.path.exists(fp): self._range(fp)
            else: self._send(404,"text/plain","no")
        else: self._send(404,"text/plain","404")
    def _range(self,fp):
        sz=os.path.getsize(fp); rng=self.headers.get("Range"); s,e=0,sz-1
        if rng:
            m=re.match(r"bytes=(\d+)-(\d*)",rng)
            if m: s=int(m.group(1)); e=int(m.group(2)) if m.group(2) else sz-1
        ln=e-s+1; ct=mimetypes.guess_type(fp)[0] or "video/mp4"
        self.send_response(206 if rng else 200); self.send_header("Content-Type",ct); self.send_header("Accept-Ranges","bytes")
        if rng: self.send_header("Content-Range",f"bytes {s}-{e}/{sz}")
        self.send_header("Content-Length",str(ln)); self.end_headers()
        with open(fp,"rb") as f:
            f.seek(s); rem=ln
            while rem>0:
                c=f.read(min(65536,rem))
                if not c: break
                try: self.wfile.write(c)
                except Exception: break
                rem-=len(c)
    def do_POST(self):
        p=urllib.parse.urlparse(self.path).path; b=self._body(); ids=b.get("ids") or ([b["id"]] if b.get("id") else [])
        if p=="/api/trash-item": self._j(do_trash(ids))
        elif p=="/api/restore": self._j(do_restore(ids))
        elif p=="/api/purge": self._j(do_purge(ids))
        elif p=="/api/final": self._j(set_override(ids,{"is_final":bool(b.get("value",True)),"status":"final" if b.get("value",True) else "draft"}))
        elif p=="/api/hold": self._j(set_override(ids,{"status":"hold"}))
        elif p=="/api/mark-trash-cand": self._j(set_override(ids,{"status":"trash_cand"}))
        elif p=="/api/queue-register": self._j(do_queue_register(ids))
        elif p=="/api/detect-candidates": self._j(do_detect())
        elif p=="/api/open-folder": self._j(open_folder(b.get("id","")))
        else: self._send(404,"text/plain","404")

if __name__=="__main__":
    print(f"콘텐츠 파일 관리자: http://127.0.0.1:{PORT}")
    ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
