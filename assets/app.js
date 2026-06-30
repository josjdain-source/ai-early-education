// before/after 원본 사진 blur 토글 (기본=blur ON, 공개 안전)
function toggleBlur(btn){
  const s=btn.closest('.src'); if(!s) return;
  if(s.classList.contains('blurred')){ s.classList.remove('blurred'); s.classList.add('shown'); btn.textContent='다시 가리기'; }
  else { s.classList.add('blurred'); s.classList.remove('shown'); btn.textContent='원본 예시 보기'; }
}

// 공용 렌더 — 데이터(JSON)만 늘리면 카드가 자동 추가됨. 정적 호스팅용(빌드 불필요).
async function getJSON(path){ try{ const r=await fetch(path); return await r.json(); }catch(e){ return null; } }

const ICON = { "door-sign":"🚪","keyring":"🔑","sticker":"✨","profile":"📱","emotion":"😊","family":"💌",
  "default":"🎨" };
function lessonIcon(id){ for(const k in ICON){ if(id.includes(k)) return ICON[k]; } return ICON.default; }

const STATUS_LABEL = { draft:"준비 중(초안)", ready:"바로 보기", link_needed:"링크 입력 필요",
  coming:"곧 추가", planned:"준비 중(기획)", available:"다운로드 가능" };
function tag(status){ const t=STATUS_LABEL[status]||status; return `<span class="tag ${status}">${t}</span>`; }

// 메인 공개용 — 1편 대표 + '다음엔 이렇게도' 응용 카드 몇 개만(전체 10편 목록 노출 X)
async function renderApplications(elId, ids){
  const el=document.getElementById(elId); if(!el) return;
  const d=await getJSON('/data/lessons.json'); if(!d) return;
  const byId={}; (d.lessons||[]).forEach(l=>byId[l.id]=l);
  el.innerHTML=ids.map(id=>byId[id]).filter(Boolean).map(l=>`
    <div class="card"><div class="body">
      <div class="ic">${l.icon||'🎨'}</div>
      <h3>${(l.title||'').replace('사진 한 장으로 ','')}</h3>
      <div class="desc">${l.summary||''}</div>
      <div class="row">${tag(l.status)}</div>
    </div></div>`).join('');
}

// 홈 히어로 영상 — door-sign-01의 공식 video_file을 읽어 연결(단일 소스, JSON만 바꾸면 자동 반영)
async function renderHeroVideo(elId){
  const el=document.getElementById(elId); if(!el) return;
  const d=await getJSON('/data/lessons.json'); if(!d) return;
  const L=(d.lessons||[]).find(x=>x.id==='door-sign-01'); if(!L) return;
  if(L.youtube_url){
    const m=L.youtube_url.match(/(?:youtu\.be\/|v=|shorts\/)([\w-]{6,})/);
    if(m){ el.innerHTML=`<div class="ph video" style="padding:0;overflow:hidden;border:0"><iframe width="100%" height="100%" src="https://www.youtube.com/embed/${m[1]}" frameborder="0" allowfullscreen></iframe></div>`; return; }
  }
  if(L.video_file){
    const src='/'+L.video_file.replace(/^\//,'');
    el.innerHTML=`<video class="localvid" controls preload="metadata" playsinline poster="/assets/process-a-ask.png" src="${src}"></video>`;
  }
}

// 메인/만들기 목록
async function renderLessons(elId, limit){
  const el=document.getElementById(elId); if(!el) return;
  const d=await getJSON('/data/lessons.json'); if(!d){ el.innerHTML='<p class="muted">목록을 불러오지 못했어요.</p>'; return; }
  let list=d.lessons||[]; if(limit) list=list.slice(0,limit);
  el.innerHTML=list.map((l,i)=>`
    <a class="card" href="${l.page||'#'}">
      <div class="thumb">${l.icon||lessonIcon(l.id)}</div>
      <div class="body">
        <h3>${(l.episode?l.episode+'편 · ':'')}${l.title}</h3>
        ${l.subtitle?`<div class="muted" style="font-size:12.5px;margin:-2px 0 2px">${l.subtitle}</div>`:''}
        <div class="desc">${l.summary||''}</div>
        <div class="row">${tag(l.status)}${l.youtube_url?'<span class="tag ready">영상</span>':''}</div>
      </div>
    </a>`).join('');
}

// 준비물(카테고리별)
async function renderMaterials(elId){
  const el=document.getElementById(elId); if(!el) return;
  const list=await getJSON('/data/materials.json'); if(!list){ el.innerHTML='<p class="muted">불러오지 못했어요.</p>'; return; }
  const cats={}; (list.materials||list).forEach(m=>{ (cats[m.category]=cats[m.category]||[]).push(m); });
  el.innerHTML=Object.entries(cats).map(([cat,items])=>`
    <section style="padding:18px 0">
      <h2 class="sec">${cat}</h2>
      <div class="grid">${items.map(m=>`
        <div class="card"><div class="body">
          <h3>${m.name}</h3>
          <div class="desc">${m.use||''}</div>
          <div class="row">${tag(m.status)}</div>
          ${m.affiliate_url
            ? `<a class="btn primary" href="${m.affiliate_url}" target="_blank" rel="nofollow sponsored">준비물 보러가기</a>`
            : `<button class="btn disabled" disabled>링크 입력 필요</button>`}
        </div></div>`).join('')}</div>
    </section>`).join('');
}

// 무료 도안/템플릿
async function renderTemplates(elId){
  const el=document.getElementById(elId); if(!el) return;
  const d=await getJSON('/data/templates.json'); if(!d){ el.innerHTML='<p class="muted">불러오지 못했어요.</p>'; return; }
  el.innerHTML=(d.templates||[]).map(t=>`
    <div class="card">
      <div class="thumb">${t.preview?`<img src="${t.preview}" alt="${t.name}" style="object-fit:contain;height:100%">`:'🖨️'}</div>
      <div class="body">
        <h3>${t.name}</h3>
        <div class="desc">${t.summary||''}</div>
        <div class="row">${tag(t.status)}<span class="muted">${t.format||''}</span></div>
        ${t.status==='available'&&t.file
          ? `<a class="btn primary" href="${t.file}" download>도안 다운로드</a>`
          : `<button class="btn disabled" disabled>곧 추가돼요</button>`}
      </div>
    </div>`).join('');
}
