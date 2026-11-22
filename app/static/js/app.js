const TaskFlow = (() => {
 let tasks = [], modal;
 const csrf = () => document.querySelector('meta[name="csrf-token"]')?.content || document.querySelector('input[name="csrf_token"]')?.value || '';
 async function api(url, options={}) {
   const headers = {'Content-Type':'application/json', 'X-CSRFToken':csrf(), ...(options.headers||{})};
   const response = await fetch(url,{...options,headers});
   const data = response.status===204 ? {} : await response.json().catch(()=>({error:'Unexpected server response'}));
   if(!response.ok) throw new Error(data.error || 'Request failed');
   return data;
 }
 function escapeHtml(value=''){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
 async function load(){const host=document.getElementById('taskList');host.innerHTML='<div class="text-center py-4 text-muted">Loading tasks…</div>';try{tasks=await api('/api/tasks');render();}catch(e){host.innerHTML=`<div class="alert alert-danger">${escapeHtml(e.message)}</div>`;}}
 function render(){const term=(document.getElementById('taskSearch').value||'').toLowerCase();const rows=tasks.filter(t=>(t.title+' '+t.description).toLowerCase().includes(term));const host=document.getElementById('taskList');if(!rows.length){host.innerHTML='<div class="text-center py-5 text-muted">No tasks found. Create your first task to get started.</div>';return;}
 host.innerHTML=`<table class="table"><thead><tr><th>Task</th><th>Status</th><th>Priority</th><th>Due date</th><th class="text-end">Actions</th></tr></thead><tbody>${rows.map(t=>`<tr><td><div class="task-title">${escapeHtml(t.title)}</div><div class="small text-muted">${escapeHtml(t.description).slice(0,75)}</div></td><td><span class="pill status-${t.status}">${t.status.replace('_',' ')}</span></td><td><span class="priority-${t.priority} fw-semibold text-capitalize">${t.priority}</span></td><td class="text-muted small">${t.due_date||'—'}</td><td class="text-end text-nowrap"><button class="action-btn" title="Edit" onclick="TaskFlow.edit(${t.id})">✎</button><button class="action-btn text-danger" title="Delete" onclick="TaskFlow.remove(${t.id})">×</button></td></tr>`).join('')}</tbody></table>`;}
 function prepareCreate(){document.getElementById('taskForm').reset();document.getElementById('taskId').value='';document.getElementById('modalTitle').textContent='Create task';document.getElementById('formError').textContent='';}
 function edit(id){const t=tasks.find(x=>x.id===id);if(!t)return;document.getElementById('taskId').value=t.id;for(const k of ['title','description','status','priority','due_date'])document.getElementById(k).value=t[k]||'';document.getElementById('modalTitle').textContent='Edit task';document.getElementById('formError').textContent='';modal.show();}
 async function save(event){event.preventDefault();const id=document.getElementById('taskId').value;const payload={};for(const k of ['title','description','status','priority','due_date'])payload[k]=document.getElementById(k).value;const btn=document.getElementById('saveTask');btn.disabled=true;btn.textContent='Saving…';try{await api(id?`/api/tasks/${id}`:'/api/tasks',{method:id?'PUT':'POST',body:JSON.stringify(payload)});modal.hide();await load();}catch(e){document.getElementById('formError').textContent=e.message;}finally{btn.disabled=false;btn.textContent='Save task';}}
 async function remove(id){if(!confirm('Delete this task permanently?'))return;try{await api(`/api/tasks/${id}`,{method:'DELETE'});await load();}catch(e){alert(e.message);}}
 function init(){modal=new bootstrap.Modal(document.getElementById('taskModal'));document.getElementById('taskForm').addEventListener('submit',save);document.getElementById('taskSearch').addEventListener('input',render);load();}
 return {init,edit,remove,prepareCreate};
})();
function prepareCreate(){TaskFlow.prepareCreate();}
