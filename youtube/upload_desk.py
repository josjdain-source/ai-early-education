#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""아이와 AI교실 영상 스튜디오 — YouTube Studio 스타일 로컬 영상 관리.
검수 → 승인(비공개 업로드) → 공개대기 → 홈페이지 연결 → 성과까지 한 화면에서.
★자동 업로드/자동 공개 금지. 사람이 '승인'한 것만 private 업로드. 실행: python youtube/upload_desk.py → http://127.0.0.1:8971"""
import json, os, subprocess, urllib.parse, mimetypes, threading, glob, re
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.dirname(HERE)
QF=os.path.join(HERE,"upload_queue.json"); PORT=8971; PYEXE="python"
_lock=threading.Lock()
COUNTRY_NAME={"china":"중국","usa":"미국","uk":"영국","singapore":"싱가포르","korea":"한국","":"공통"}
def load_q(): return json.load(open(QF,encoding="utf-8"))
def save_q(q): json.dump(q,open(QF,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
def ap(p): return p if os.path.isabs(p) else os.path.join(REPO,p)

def embedded_ids():
    ids=set()
    for f in glob.glob(os.path.join(REPO,"videos*.html"))+glob.glob(os.path.join(REPO,"videos","*.html"))+glob.glob(os.path.join(REPO,"world-cases","*.html")):
        try:
            for m in re.findall(r"embed/([A-Za-z0-9_-]{11})",open(f,encoding="utf-8").read()): ids.add(m)
        except Exception: pass
    return ids

def enrich(it,eids):
    mp=ap(it.get("mp4_path","")); local=os.path.exists(mp)
    yid=it.get("youtube_id") or ""
    hp="none"
    if yid: hp="connected" if yid in eids else "pending"
    desc=(it.get("description","") or "").strip().replace("\n"," ")
    return {**it,
      "local_exists":local, "homepage_status":hp,
      "desc2":(desc[:90]+"…") if len(desc)>90 else desc,
      "country_name":COUNTRY_NAME.get(it.get("country",""),it.get("country","")),
      "created":it.get("created_at","")}

def summary(items):
    return {
      "ready":sum(1 for i in items if i["upload_status"]=="ready_to_upload"),
      "private":sum(1 for i in items if i["upload_status"]=="uploaded_private"),
      "pubwait":sum(1 for i in items if i["upload_status"]=="uploaded_private"),
      "hpwait":sum(1 for i in items if i.get("youtube_id") and i["homepage_status"]!="connected"),
      "quota":sum(1 for i in items if i["upload_status"]=="quota_exceeded"),
      "failed":sum(1 for i in items if i["upload_status"]=="failed"),
      "total":len(items)}

# ---------- 액션 ----------
def do_upload(vid):
    with _lock:
        try:
            r=subprocess.run([PYEXE,os.path.join(HERE,"upload_to_aiclassroom.py"),"--id",vid],cwd=REPO,capture_output=True,text=True,timeout=900)
            out=(r.stdout or "")+(r.stderr or "")
        except Exception as e: out=f"실행 오류: {e}"
        q=load_q(); it=next((x for x in q["queue"] if x["video_id"]==vid),None)
        if it is None: return {"ok":False,"error":"항목 없음"}
        url=""
        for tok in out.replace("\n"," ").split():
            if "youtu.be/" in tok or "watch?v=" in tok: url=tok.strip("().,"); break
        if url:
            yid=url.rstrip("/").split("/")[-1].replace("watch?v=","")
            it.update({"youtube_url":url,"youtube_id":yid,"studio_url":f"https://studio.youtube.com/video/{yid}/edit",
                       "status":"uploaded_private","upload_status":"uploaded_private","public_status":"private",
                       "visibility":"private","uploaded_at":datetime.now().strftime("%Y-%m-%d %H:%M"),"error_message":""})
            save_q(q); return {"ok":True,"url":url}
        if "uploadLimitExceeded" in out or "exceeded the number of videos" in out:
            it["upload_status"]="quota_exceeded"; it["error_message"]="유튜브 일일 업로드 한도 초과"; save_q(q)
            return {"ok":False,"quota":True,"error":"유튜브 일일 업로드 한도 초과 — 내일 다시 승인하세요."}
        it["upload_status"]="failed"; it["error_message"]=out.strip()[-200:]; save_q(q)
        return {"ok":False,"error":("업로드 실패: "+out.strip()[-160:]) if out.strip() else "알 수 없는 오류"}

def do_verify():
    with _lock:
        try:
            r=subprocess.run([PYEXE,os.path.join(HERE,"verify_public.py")],cwd=REPO,capture_output=True,text=True,timeout=120)
            out=(r.stdout or "")+(r.stderr or "")
        except Exception as e: return {"ok":False,"error":str(e)}
        # verify_public 출력 파싱: "name (id): public/unlisted/private"
        q=load_q(); changed=0
        for it in q["queue"]:
            yid=it.get("youtube_id")
            if not yid: continue
            m=re.search(re.escape(yid)+r"\):\s*(\w+)",out)
            if m:
                ps=m.group(1); it["public_status"]=ps
                if ps=="public": it["upload_status"]="published"; it["status"]="published"
                it["last_checked_at"]=datetime.now().strftime("%Y-%m-%d %H:%M"); changed+=1
        save_q(q); return {"ok":True,"checked":changed,"raw":out.strip()[-500:]}

def do_stats():
    with _lock:
        import sys
        sys.path.insert(0,r"C:/Users/admin/Desktop/유튜브쇼츠/동영상제작")
        try:
            import youtube_upload as YU
            YU.TOKEN=os.path.join(HERE,"token_aiclassroom.json")
            ds=os.path.join(HERE,"client_secret_aiclassroom.json")
            if os.path.exists(ds): YU.CLIENT_SECRET=ds; YU.CLIENT_SECRET_WEB=os.path.join(HERE,"__no_web__.json")
            yt=YU.build("youtube","v3",credentials=YU._creds())
            q=load_q(); ids=[it["youtube_id"] for it in q["queue"] if it.get("youtube_id")]
            got={}
            for i in range(0,len(ids),50):
                r=yt.videos().list(part="statistics,status",id=",".join(ids[i:i+50])).execute()
                for v in r.get("items",[]): got[v["id"]]=v
            n=0
            for it in q["queue"]:
                v=got.get(it.get("youtube_id"))
                if v:
                    s=v.get("statistics",{}); it["views"]=int(s.get("viewCount",0)); it["comments"]=int(s.get("commentCount",0))
                    it["public_status"]=v.get("status",{}).get("privacyStatus",it.get("public_status"))
                    it["last_checked_at"]=datetime.now().strftime("%Y-%m-%d %H:%M"); n+=1
            save_q(q); return {"ok":True,"updated":n}
        except Exception as e: return {"ok":False,"error":str(e)[:200]}

def do_remove(vid):
    with _lock:
        q=load_q(); q["queue"]=[x for x in q["queue"] if x["video_id"]!=vid]; save_q(q); return {"ok":True}

def do_rebuild():
    try:
        r=subprocess.run([PYEXE,"build_site.py"],cwd=REPO,capture_output=True,text=True,timeout=180)
        return {"ok":r.returncode==0,"out":(r.stdout or r.stderr)[-300:]}
    except Exception as e: return {"ok":False,"error":str(e)}

FPB="C:/Users/admin/Desktop/ffmpeg-8.1.1-essentials_build/bin/ffprobe.exe"; DESKTOP=os.path.dirname(REPO)
try: CHANNELS=json.load(open(os.path.join(HERE,"channels_config.json"),encoding="utf-8"))["channels"]
except Exception: CHANNELS=[{"id":"aiclassroom","name":"아이와 AI교실","icon":"🎓","source":"queue"}]
_dc={}
def _dur(fp):
    if fp in _dc: return _dc[fp]
    try: d=round(float(subprocess.run([FPB,"-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",fp],capture_output=True,text=True).stdout.strip() or 0),1)
    except Exception: d=None
    _dc[fp]=d; return d
DATA=os.path.join(REPO,"data"); LOGS=os.path.join(REPO,"logs")
for _d in (DATA,LOGS): os.makedirs(_d,exist_ok=True)
TRASHF=os.path.join(DATA,"trash_manifest.json"); OVR=os.path.join(DATA,"studio_overrides.json"); DLOG=os.path.join(LOGS,"asset_delete.log")
def _l(p,d):
    try: return json.load(open(p,encoding="utf-8"))
    except Exception: return d
def _s(p,o): json.dump(o,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
def trashed_ids(): return {x["id"] for x in _l(TRASHF,{"items":[]})["items"]}
def channel_videos(ch):
    nowts=datetime.now().timestamp(); tr=trashed_ids(); ovr=_l(OVR,{})
    if ch.get("source")=="queue":
        eids=embedded_ids(); items=[]
        for it in load_q()["queue"]:
            e=enrich(it,eids)
            if e["video_id"] in tr: continue
            fp=ap(e.get("mp4_path","")); ts=os.path.getmtime(fp) if os.path.exists(fp) else None
            e["age_h"]=round((nowts-ts)/3600,1) if ts else 9999
            e["is_final"]=ovr.get(e["video_id"],{}).get("is_final",False)
            items.append(e)
        return items
    out=[]; seen=set()
    for g in ch.get("globs",[]):
        for fp in glob.glob(g,recursive=True):
            fp=os.path.normpath(fp).replace("\\","/")
            if fp in seen or fp in tr or not fp.lower().endswith(".mp4"): continue
            seen.add(fp)
            try: mt=os.path.getmtime(fp); sz=os.path.getsize(fp)
            except Exception: continue
            out.append({"video_id":fp,"title":os.path.basename(fp),"video_type":"short","subtype":"","status":"local",
              "upload_status":"local","public_status":"","mp4_path":fp,"thumbnail_path":"","local_exists":True,
              "duration":_dur(fp),"size":sz,"created_at":datetime.fromtimestamp(mt).strftime("%Y-%m-%d %H:%M"),
              "age_h":round((nowts-mt)/3600,1),"youtube_id":"","youtube_url":"","studio_url":"","page_url":"",
              "homepage_status":"none","country":"","folder":os.path.dirname(fp),"is_final":ovr.get(fp,{}).get("is_final",False)})
    out.sort(key=lambda x:x.get("created_at",""),reverse=True); return out
def _findv(vid,chid):
    ch=next((c for c in CHANNELS if c["id"]==chid),CHANNELS[0])
    return next((v for v in channel_videos(ch) if v["video_id"]==vid),None)
def studio_can_delete(v):
    if _l(OVR,{}).get(v["video_id"],{}).get("is_final"): return False,"최종본 지정됨"
    if v.get("homepage_status")=="connected": return False,"홈페이지 사용 중"
    if v.get("upload_status")=="ready_to_upload" and not v.get("youtube_id"): return False,"업로드 대기(유튜브 없음)"
    if v.get("upload_status")=="uploaded_private" and not v.get("youtube_id"): return False,"업로드 안 됨"
    return True,""
def studio_trash(ids,chid):
    t=_l(TRASHF,{"items":[]}); res={"trashed":[],"blocked":[]}
    for vid in ids:
        v=_findv(vid,chid)
        if not v: res["blocked"].append({"id":vid,"why":"없음"}); continue
        ok,why=studio_can_delete(v)
        if not ok: res["blocked"].append({"id":vid,"title":v["title"],"why":why}); continue
        t["items"].append({"id":vid,"title":v["title"],"type":"video","path":v.get("mp4_path",vid),"trashed_at":datetime.now().strftime("%Y-%m-%d %H:%M"),"channel":chid})
        open(DLOG,"a",encoding="utf-8").write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] TRASH {vid}\n")
        res["trashed"].append(vid)
    _s(TRASHF,t); return res
def studio_restore(ids):
    t=_l(TRASHF,{"items":[]}); t["items"]=[x for x in t["items"] if x["id"] not in ids]; _s(TRASHF,t); return {"ok":True}
def studio_purge(ids):
    t=_l(TRASHF,{"items":[]}); killed=[]
    for x in list(t["items"]):
        if x["id"] in ids:
            fp=x.get("path","")
            try:
                if fp and os.path.isabs(fp) and os.path.exists(fp) and os.path.realpath(fp).startswith(os.path.realpath(DESKTOP)):
                    os.remove(fp); killed.append(fp)
                elif fp and os.path.exists(ap(fp)):
                    os.remove(ap(fp)); killed.append(fp)
            except Exception as e: killed.append(f"실패:{e}")
            open(DLOG,"a",encoding="utf-8").write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] PURGE {x['id']}\n")
            t["items"]=[y for y in t["items"] if y["id"]!=x["id"]]
    _s(TRASHF,t); return {"ok":True,"deleted":killed}
def studio_setfinal(ids,val):
    o=_l(OVR,{})
    for vid in ids: o.setdefault(vid,{})["is_final"]=bool(val)
    _s(OVR,o); return {"ok":True}
def studio_detect(chid):
    ch=next((c for c in CHANNELS if c["id"]==chid),CHANNELS[0]); vids=channel_videos(ch); cand={}
    grp={}
    for v in vids:
        base=re.sub(r'[-_]?v?\d+(\.mp4)?$','',v["title"].replace(".mp4","")).strip()
        grp.setdefault(base,[]).append(v)
    def key(v):
        m=re.search(r'v(\d+)',v["title"]); ver=int(m.group(1)) if m else 0
        fin=1 if v.get("is_final") else 0; up=1 if v.get("youtube_id") else 0
        latest=1 if "final" in v["title"].lower() else 0
        return (fin,up,latest,ver,v.get("created_at",""))
    for base,g in grp.items():
        if len(g)<2: continue
        keep=sorted(g,key=key)[-1]
        for v in g:
            if v["video_id"]==keep["video_id"]: continue
            ok,_=studio_can_delete(v)
            if ok: cand[v["video_id"]]=f"구버전 · 최신본 있음({keep['title'][:24]})"
    for v in vids:
        if v["video_id"] in cand: continue
        if v.get("upload_status")=="superseded":
            ok,_=studio_can_delete(v);  cand[v["video_id"]]="대체된 구버전" if ok else None
        if "draft" in v["title"].lower() or "실패" in v["title"] or "fail" in v["title"].lower():
            ok,_=studio_can_delete(v)
            if ok: cand[v["video_id"]]="초벌/실패 추정"
    return {k:v for k,v in cand.items() if v}

HTML=open(os.path.join(HERE,"_studio.html"),encoding="utf-8").read() if os.path.exists(os.path.join(HERE,"_studio.html")) else "STUDIO_HTML_PLACEHOLDER"

class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def _j(self,obj,code=200): self._send(code,"application/json; charset=utf-8",json.dumps(obj,ensure_ascii=False).encode())
    def _send(self,code,ctype,data):
        self.send_response(code); self.send_header("Content-Type",ctype); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def _body(self):
        n=int(self.headers.get("Content-Length",0));
        try: return json.loads(self.rfile.read(n) or b"{}")
        except Exception: return {}
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); qs=urllib.parse.parse_qs(u.query)
        if u.path=="/": self._send(200,"text/html; charset=utf-8",HTML.encode())
        elif u.path=="/api/channels":
            self._j({"channels":[{"id":c["id"],"name":c["name"],"icon":c.get("icon","📺"),"source":c.get("source")} for c in CHANNELS]})
        elif u.path=="/api/videos":
            chid=qs.get("channel",["aiclassroom"])[0]; ch=next((c for c in CHANNELS if c["id"]==chid),CHANNELS[0])
            items=channel_videos(ch)
            self._j({"videos":items,"summary":summary(items),"channel":chid,"source":ch.get("source")})
        elif u.path=="/api/trash":
            self._j({"items":_l(TRASHF,{"items":[]})["items"]})
        elif u.path=="/api/meta":
            vid=qs.get("id",[""])[0]; it=next((x for x in load_q()["queue"] if x["video_id"]==vid),{})
            self._j(it)
        elif u.path=="/poster":
            p=qs.get("p",[""])[0]; fp=ap(p)
            if p and os.path.exists(fp) and os.path.realpath(fp).startswith(os.path.realpath(REPO)):
                self._send(200,mimetypes.guess_type(fp)[0] or "image/jpeg",open(fp,"rb").read())
            else: self._send(404,"text/plain",b"no")
        elif u.path=="/video":
            vid=qs.get("id",[""])[0]
            if os.path.isabs(vid) and os.path.exists(vid) and os.path.realpath(vid).startswith(os.path.realpath(DESKTOP)):
                return self._serve_range(vid)
            it=next((x for x in load_q()["queue"] if x["video_id"]==vid),None)
            fp=ap(it.get("mp4_path","")) if it else ""
            if not (it and os.path.exists(fp)): return self._send(404,"text/plain",b"no")
            self._serve_range(fp)
        else: self._send(404,"text/plain",b"404")
    def _serve_range(self,fp):
        sz=os.path.getsize(fp); rng=self.headers.get("Range")
        start,end=0,sz-1
        if rng:
            m=re.match(r"bytes=(\d+)-(\d*)",rng)
            if m:
                start=int(m.group(1)); end=int(m.group(2)) if m.group(2) else sz-1
        length=end-start+1
        self.send_response(206 if rng else 200)
        self.send_header("Content-Type","video/mp4"); self.send_header("Accept-Ranges","bytes")
        if rng: self.send_header("Content-Range",f"bytes {start}-{end}/{sz}")
        self.send_header("Content-Length",str(length)); self.end_headers()
        with open(fp,"rb") as f:
            f.seek(start); rem=length
            while rem>0:
                chunk=f.read(min(65536,rem))
                if not chunk: break
                try: self.wfile.write(chunk)
                except Exception: break
                rem-=len(chunk)
    def do_POST(self):
        p=urllib.parse.urlparse(self.path).path; b=self._body()
        if p=="/api/upload": self._j(do_upload(b.get("video_id","")))
        elif p=="/api/verify": self._j(do_verify())
        elif p=="/api/stats": self._j(do_stats())
        elif p=="/api/remove": self._j(do_remove(b.get("video_id","")))
        elif p=="/api/rebuild": self._j(do_rebuild())
        elif p=="/api/trash-item": self._j(studio_trash(b.get("ids") or [b.get("id")], b.get("channel","aiclassroom")))
        elif p=="/api/restore": self._j(studio_restore(b.get("ids") or [b.get("id")]))
        elif p=="/api/purge": self._j(studio_purge(b.get("ids") or [b.get("id")]))
        elif p=="/api/final": self._j(studio_setfinal(b.get("ids") or [b.get("id")], b.get("value",True)))
        elif p=="/api/detect": c=studio_detect(b.get("channel","aiclassroom")); self._j({"ok":True,"count":len(c),"cands":c})
        else: self._send(404,"text/plain",b"404")

if __name__=="__main__":
    print(f"아이와 AI교실 영상 스튜디오: http://127.0.0.1:{PORT}")
    ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
