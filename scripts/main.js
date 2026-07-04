// AI 조기교육 — 네비/영상 필터
(function(){
  // 영상관 카테고리 필터
  var f=document.getElementById('filters');
  if(f){
    f.addEventListener('click',function(e){
      var b=e.target.closest('button'); if(!b) return;
      f.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on');
      var cat=b.getAttribute('data-f');
      document.querySelectorAll('#vgrid .vcard').forEach(function(c){
        c.style.display=(cat==='전체'||c.getAttribute('data-cat')===cat)?'':'none';
      });
    });
  }
  // 모바일 네비 링크 클릭 시 닫기
  var nav=document.getElementById('nav');
  if(nav){ nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');});}); }
})();
