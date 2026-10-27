"use strict";
const $=id=>document.getElementById(id);
let selected=null;
const escapeHTML=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
async function api(path,method="GET",payload){
 const headers={"Content-Type":"application/json"};
 const token=localStorage.getItem("film-studio-token");
 if(token)headers["X-Studio-Token"]=token;
 const result=await fetch("/api"+path,{method,headers,body:payload===undefined?undefined:JSON.stringify(payload)});
 const data=await result.json().catch(()=>({}));
 if(!result.ok)throw Error(data.detail||("Lỗi HTTP "+result.status));
 return data;
}
function handle(error){alert("Lỗi: "+error.message)}
async function refresh(){
 const projects=await api("/projects");
 $("projectList").innerHTML=projects.map(p=>'<div class="project '+(p.id===selected?"active":"")+'" data-id="'+escapeHTML(p.id)+'"><strong>'+escapeHTML(p.title)+'</strong><div class="hint">'+p.scene_count+' cảnh</div></div>').join("");
 document.querySelectorAll(".project").forEach(el=>el.onclick=()=>choose(el.dataset.id).catch(handle));
}
async function choose(id){
 selected=id;const p=await api("/projects/"+id);
 $("editor").hidden=false;$("selectedTitle").textContent=p.title;$("script").value=p.script||"";
 $("characters").innerHTML=p.characters.map(c=>'<div class="character"><strong>'+escapeHTML(c.name)+'</strong><p>'+escapeHTML(c.appearance)+'</p></div>').join("");
 $("scenes").innerHTML=p.scenes.map(s=>'<div class="scene"><div class="meta">Cảnh '+s.order+' · '+Number(s.duration||5)+' giây · '+escapeHTML(s.camera)+'</div><strong>'+escapeHTML(s.title)+'</strong><p>'+escapeHTML(s.description)+'</p></div>').join("");
 $("renderResult").textContent="";await refresh();
}
$("newProject").onsubmit=async e=>{e.preventDefault();try{const p=await api("/projects","POST",{title:$("newTitle").value});$("newTitle").value="";await choose(p.id)}catch(err){handle(err)}};
$("saveScript").onclick=async()=>{if(!selected)return;try{const p=await api("/projects/"+selected);await api("/projects/"+selected,"PUT",{title:p.title,script:$("script").value});alert("Đã lưu")}catch(err){handle(err)}};
$("splitScenes").onclick=async()=>{if(!selected)return;try{await api("/projects/"+selected+"/scenes/from-script","POST",{script:$("script").value});await choose(selected)}catch(err){handle(err)}};
$("characterForm").onsubmit=async e=>{e.preventDefault();if(!selected)return;try{await api("/projects/"+selected+"/characters","POST",{name:$("charName").value,appearance:$("charAppearance").value,voice:$("charVoice").value});e.target.reset();await choose(selected)}catch(err){handle(err)}};
$("audit").onclick=async()=>{if(!selected)return;try{$("quality").textContent=JSON.stringify(await api("/projects/"+selected+"/quality"),null,2)}catch(err){handle(err)}};
$("shotlist").onclick=async()=>{if(!selected)return;try{const data=await api("/projects/"+selected+"/shotlist");const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="ke-hoach-quay.json";a.click();URL.revokeObjectURL(a.href)}catch(err){handle(err)}};
$("render").onclick=async()=>{if(!selected)return;try{$("renderResult").textContent="Đang dựng MP4 minh họa...";const d=await api("/projects/"+selected+"/render","POST",{});$("renderResult").innerHTML='<a href="'+encodeURI(d.download_url)+'" download>Tải phim MP4</a>'}catch(err){handle(err)}};
refresh().catch(handle);
