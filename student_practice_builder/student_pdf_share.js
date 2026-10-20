/* Student Practice Builder: local, no-upload PDF for native iPad file sharing.
 * The installed CPMPageFlow is the sole authority for page boundaries.
 * PDF rasterization uses those same measured pages, never a second paginator.
 * Browser Print remains the accessible PDF/print fallback.
 */
(()=>{'use strict';
 let currentFile=null, preparing=null, epoch=0, wake=null;
 const choose=()=>document.getElementById('notability');
 const note=(message)=>{const el=document.getElementById('status');if(el)el.textContent=message;};
 function invalidatePracticeShare(){
   epoch++;currentFile=null;
   const b=choose();if(b){b.disabled=true;b.textContent='Notability';}
 }
 const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
 const point=(v)=>Number.parseFloat(v)||0;
 function isVisible(el){
   if(!el||!el.isConnected)return false;
   for(let n=el;n&&n.nodeType===1;n=n.parentElement){
     if(n.id==='practicePages')break; // hidden offscreen while measuring
     const s=getComputedStyle(n);
     if(s.display==='none'||s.visibility==='hidden'||point(s.opacity)===0)return false;
   }
   return true;
 }
 function imageLoaded(src){return new Promise((resolve,reject)=>{
   const image=new Image();image.onload=()=>resolve(image);image.onerror=()=>reject(Error('Unable to rasterize a worksheet figure'));
   image.src=src;
 });}
 async function paintFigure(ctx,el,offset,ratio){
   const rect=el.getBoundingClientRect();
   if(rect.width<1||rect.height<1||!isVisible(el))return;
   let source='';let temporary='';
   try{
     if(el.localName==='img')source=el.currentSrc||el.src;
     else{
       const clone=el.cloneNode(true);
       clone.setAttribute('xmlns','http://www.w3.org/2000/svg');
       clone.setAttribute('xmlns:xlink','http://www.w3.org/1999/xlink');
       clone.setAttribute('width',String(Math.ceil(rect.width)));
       clone.setAttribute('height',String(Math.ceil(rect.height)));
       const cache=document.getElementById('MJX-SVG-global-cache');
       // MathJax's global glyph paths live elsewhere in the document.
       if(el.closest('mjx-container')&&cache){
         const defs=document.createElementNS('http://www.w3.org/2000/svg','defs');
         cache.querySelectorAll('defs > *, symbol, path[id]').forEach(node=>defs.append(node.cloneNode(true)));
         clone.insertBefore(defs,clone.firstChild);
       }
       const xml=new XMLSerializer().serializeToString(clone);
       temporary=URL.createObjectURL(new Blob([xml],{type:'image/svg+xml;charset=utf-8'}));
       source=temporary;
     }
     const img=await imageLoaded(source);
     const x=(rect.left-offset.left)*ratio,y=(rect.top-offset.top)*ratio;
     ctx.drawImage(img,x,y,rect.width*ratio,rect.height*ratio);
   }finally{if(temporary)URL.revokeObjectURL(temporary);}
 }
 function paintText(ctx,page,origin,ratio){
   const walker=document.createTreeWalker(page,NodeFilter.SHOW_TEXT);
   while(walker.nextNode()){
     const node=walker.currentNode,container=node.parentElement;
     if(!container||!isVisible(container)||container.closest('svg,mjx-container,mjx-assistive-mml,script,style,template'))continue;
     const str=node.textContent||'';
     if(!str.trim())continue;
     const s=getComputedStyle(container);
     const size=point(s.fontSize)||16;
     const color=s.color;
     ctx.fillStyle=color||'#202020';
     ctx.font=(s.fontStyle||'normal')+' '+(s.fontWeight||'400')+' '+size*ratio+'px '+(s.fontFamily||'Arial');
     const reg=/\S+/g;let match;
     while((match=reg.exec(str))){
       const range=document.createRange();range.setStart(node,match.index);range.setEnd(node,match.index+match[0].length);
       const box=range.getBoundingClientRect();
       if(box.width<.2||box.height<.2)continue;
       const word=s.textTransform==='uppercase'?match[0].toUpperCase():match[0];
       ctx.fillText(word,(box.left-origin.left)*ratio,(box.bottom-origin.top-size*.18)*ratio);
     }
   }
 }
 async function paintPage(paper,ratio=2.4){
   const rect=paper.getBoundingClientRect();
   const canvas=document.createElement('canvas');
   canvas.width=Math.round(rect.width*ratio);canvas.height=Math.round(rect.height*ratio);
   const ctx=canvas.getContext('2d',{alpha:false});
   if(!ctx)throw Error('Canvas rendering unavailable');
   ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);
   for(const el of paper.querySelectorAll('.sheet-heading,.lesson-section-divider,.sheet-footer,.question-top,.data-table th,.data-table td')){
     if(!isVisible(el))continue;
     const b=el.getBoundingClientRect(),s=getComputedStyle(el);
     const x=(b.left-rect.left)*ratio,y=(b.top-rect.top)*ratio;
     if(s.backgroundColor!=='rgba(0, 0, 0, 0)'&&s.backgroundColor!=='transparent'){
       ctx.fillStyle=s.backgroundColor;ctx.fillRect(x,y,b.width*ratio,b.height*ratio);
     }
     if(el.classList.contains('lesson-section-divider')){
       ctx.fillStyle='#143960';ctx.fillRect(x,y,4*ratio,b.height*ratio);
       ctx.fillStyle='#bad0e0';ctx.fillRect(x,y+b.height*ratio-1.4*ratio,b.width*ratio,1.4*ratio);
     }else if(el.classList.contains('sheet-heading')){
       ctx.fillStyle='#315977';ctx.fillRect(x,y+b.height*ratio-2*ratio,b.width*ratio,2*ratio);
     }
     if(el.matches('.data-table td,.data-table th')){
       ctx.strokeStyle='#8d9eac';ctx.lineWidth=.7*ratio;ctx.strokeRect(x,y,b.width*ratio,b.height*ratio);
     }
   }
   // Light ruled workspace replaces the excessive blank 3.17-inch area.
   for(const el of paper.querySelectorAll('.question-workspace')){
     if(!isVisible(el))continue;
     const b=el.getBoundingClientRect();ctx.fillStyle='#eef2f4';
     for(let y=25;y<b.height-3;y+=26){
       ctx.fillRect((b.left-rect.left)*ratio,(b.top-rect.top+y)*ratio,b.width*ratio,.75*ratio);
     }
   }
   paintText(ctx,paper,rect,ratio);
   for(const el of paper.querySelectorAll('img,svg')){
     if(el.closest('svg')&&!el.matches('svg'))continue;
     if(el.closest('svg')&&el.closest('svg')!==el)continue;
     await paintFigure(ctx,el,rect,ratio);
   }
   // JPEG encoding limits memory on school iPads while keeping 200+ dpi.
   const data=canvas.toDataURL('image/jpeg',.86);
   const bytes=Uint8Array.from(atob(data.slice(data.indexOf(',')+1)),x=>x.charCodeAt(0));
   const width=canvas.width,height=canvas.height;
   canvas.width=0;canvas.height=0;
   return {bytes,width,height};
 }
 const ascii=s=>new TextEncoder().encode(s);
 function pdfFromJpegs(images){
   const objs=[null,null],pageRefs=[];
   for(const image of images){
     const pageNum=objs.length+1,contentNum=pageNum+1,imageNum=pageNum+2;
     pageRefs.push(pageNum+' 0 R');
     objs.push(ascii('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /XObject << /Im0 '+imageNum+' 0 R >> >> /Contents '+contentNum+' 0 R >>'));
     const ops='q 612 0 0 792 0 0 cm /Im0 Do Q';
     objs.push(ascii('<< /Length '+ops.length+' >>\nstream\n'+ops+'\nendstream'));
     const prefix=ascii('<< /Type /XObject /Subtype /Image /Width '+image.width+' /Height '+image.height+' /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length '+image.bytes.length+' >>\nstream\n');
     const suffix=ascii('\nendstream');
     const combined=new Uint8Array(prefix.length+image.bytes.length+suffix.length);
     combined.set(prefix,0);combined.set(image.bytes,prefix.length);combined.set(suffix,prefix.length+image.bytes.length);
     objs.push(combined);
   }
   objs[0]=ascii('<< /Type /Catalog /Pages 2 0 R >>');
   objs[1]=ascii('<< /Type /Pages /Kids ['+pageRefs.join(' ')+'] /Count '+pageRefs.length+' >>');
   const parts=[ascii('%PDF-1.4\n%\xE2\xE3\xCF\xD3\n')],offsets=[0];let total=parts[0].length;
   const add=v=>{parts.push(v);total+=v.length};
   objs.forEach((obj,i)=>{offsets.push(total);add(ascii((i+1)+' 0 obj\n'));add(obj);add(ascii('\nendobj\n'));});
   const xref=total;
   add(ascii('xref\n0 '+(objs.length+1)+'\n0000000000 65535 f \n'));
   for(let i=1;i<offsets.length;i++)add(ascii(String(offsets[i]).padStart(10,'0')+' 00000 n \n'));
   add(ascii('trailer\n<< /Size '+(objs.length+1)+' /Root 1 0 R >>\nstartxref\n'+xref+'\n%%EOF\n'));
   return new Blob(parts,{type:'application/pdf'});
 }
 async function prepareSharePDF(ticket){
   try{
     const done=await prepareStudentWorksheet();
     if(!done||ticket!==epoch)return;
     const root=document.getElementById('practicePages');
     const priorVisibility=root.style.visibility;
     root.style.setProperty('visibility','visible','important');
     const sheets=[...root.querySelectorAll(':scope > .paper')];
     const images=[];
     try{
       if(!sheets.length)throw Error('No measured worksheet pages');
       for(const sheet of sheets){
         if(ticket!==epoch)return;
         images.push(await paintPage(sheet));
         await sleep(0);
       }
     }finally{root.style.visibility=priorVisibility;}
     if(ticket!==epoch)return;
     const pdf=pdfFromJpegs(images);
     if(pdf.size<1000)throw Error('Generated PDF was empty');
     const file=new File([pdf],'Algebra_1_Practice.pdf',{type:'application/pdf'});
     if(!navigator.canShare({files:[file]}))throw Error('Device cannot share PDF files');
     currentFile=file;
     const b=choose();if(b){b.disabled=false;b.textContent='Notability';}
     note('Worksheet ready to print or share with Notability ('+sheets.length+' pages).');
   }catch(err){
     if(ticket!==epoch)return;
     note('PDF file sharing is unavailable ('+String(err?.message||err)+'). Print Worksheet remains available.');
     const b=choose();if(b){b.disabled=false;b.textContent='Notability / Print';}
   }
 }
 function scheduleStudentSharePDF(){
   invalidatePracticeShare();const ticket=epoch;
   const b=choose();if(!b)return;
   if(!navigator.share||!navigator.canShare){
     b.disabled=false;b.textContent='Notability / Print';return;
   }
   note('Preparing printable pages and native Notability PDF…');
   preparing=new Promise(resolve=>{
     clearTimeout(wake);wake=setTimeout(()=>{prepareSharePDF(ticket).finally(resolve);},250);
   });
 }
 function sharePracticePDF(){
   if(currentFile&&navigator.share&&navigator.canShare?.({files:[currentFile]})){
     // No awaits: Apple Web Share must be invoked directly inside the tap.
     navigator.share({files:[currentFile],title:'Algebra 1 Practice',text:'Practice worksheet'})
       .catch(err=>{if(err?.name!=='AbortError')note('Share failed. Please use Print Worksheet.');});
   }else{
     // Native Print/PDF is the safe fallback; never share a link in place of a PDF.
     printStudentWorksheet();
   }
 }
 window.scheduleStudentSharePDF=scheduleStudentSharePDF;
 window.invalidatePracticeShare=invalidatePracticeShare;
 window.sharePracticePDF=sharePracticePDF;
 window.waitForSharePreparation=()=>preparing||Promise.resolve();
})();
