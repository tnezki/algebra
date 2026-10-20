/* Student-only practice interactions. Never saves answers, names or evidence. */
(function(){
  'use strict';
  // The same script is embedded by reference in the public Builder and in
  // deeply nested assigned practice pages. Resolve the bank alongside the
  // SCRIPT, never relative to the page or a body class (v140 regression).
  const poolURL = new URL('question_pool.json', document.currentScript.src).href;
  let poolPromise;
  const cursors = new Map();
  const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function pool(){
    if(!poolPromise) poolPromise=fetch(poolURL).then(r=>{if(!r.ok)throw Error('Approved practice pool unavailable');return r.json();});
    return poolPromise;
  }
  async function newQuestion(id){
    const row=document.getElementById('q'+id);
    const button=row?.querySelector('.new-version-button');
    if(!row||!button) return;
    button.disabled=true;
    try {
      const data=await pool();
      const iid=row.dataset.practiceICan;
      const candidates=data.skills?.[iid]?.questions||[];
      if(!candidates.length)throw Error('No approved examples for this skill');
      const family=candidates.find(q=>q.id===row.dataset.familyId);
      const sequence=family?.variants?.length ? family.variants : candidates;
      const key=id+':'+row.dataset.familyId;
      const cursor=cursors.get(key)||0;
      const next=sequence[cursor % sequence.length];
      cursors.set(key,cursor+1);
      const problem=row.querySelector('.problem');
      const solution=document.getElementById('s'+id);
      const original=document.getElementById('rawPrompt'+id);
      if(!problem||!solution||!original)throw Error('Question markup unavailable');
      if(window.MathJax?.typesetClear)window.MathJax.typesetClear([problem]);
      problem.innerHTML=next.prompt;
      original.innerHTML=next.prompt;
      solution.innerHTML='<b>Answer:</b> '+escapeHTML(next.answer)+'<p><b>Worked solution:</b> '+escapeHTML(next.solution)+'</p>';
      if(!family?.variants?.length){row.dataset.familyId=next.id;}
      if(window.MathJax?.typesetPromise)await window.MathJax.typesetPromise([problem]);
      const status=document.getElementById('practiceStatus');
      if(status){status.hidden=false;status.textContent='New on-screen question ready. The Notability PDF remains the originally assigned worksheet.';}
      const builderStatus=document.getElementById('status');
      if(builderStatus)builderStatus.textContent='Question '+id+' updated. Answer and worked solution match this version.';
    }catch(error){
      const status=document.getElementById('practiceStatus')||document.getElementById('status');
      if(status){status.hidden=false;status.textContent='Could not load another question: '+error.message;}
    }finally{button.disabled=false;}
  }
  window.CPMStudentPractice=Object.freeze({newQuestion});
})();
