/* Actual final usability UI, local Chromium + Gemma. No intercepted model replies or edited video. */
const {chromium}=require('playwright');
const fs=require('node:fs/promises'),path=require('node:path'),crypto=require('node:crypto');
const base=path.resolve(process.argv[2]||'.local-reports/usability-release');
const url=process.argv[3]||'http://127.0.0.1:7864';
(async()=>{
 await fs.mkdir(base,{recursive:true});
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000},recordVideo:{dir:base,size:{width:1440,height:1000}},acceptDownloads:true});
 const page=await context.newPage(),events=[],errors=[]; const started=Date.now();
 const note=(name,data={})=>events.push({name,seconds:(Date.now()-started)/1000,...data});
 page.on('pageerror',e=>errors.push(e.message));
 const sample=page.getByRole('button',{name:'Load sample public excerpt (CNS; fictional applicant)',exact:true});
 const go=page.getByRole('button',{name:'Analyze public announcement',exact:true});
 const plan=page.getByRole('button',{name:/Application Readiness Dossier — plan and source evidence/});
 const source=page.getByLabel('Eligibility, exclusions, amounts, deadlines and application instructions',{exact:true});
 const answer=async(q,v)=>page.locator('fieldset').filter({has:page.getByText(q,{exact:true})}).getByRole('radio',{name:v,exact:true}).check();
 const first='First author of the submitted work?',presenter='Presenting author / presenter of the work?';
 try{
  await page.goto(url);await sample.waitFor();
  await page.getByRole('button',{name:'Check local model',exact:true}).click();
  await page.getByText('Local Gemma is available:',{exact:false}).waitFor();
  note('model_checked');await page.screenshot({path:path.join(base,'welcome.png')});await page.waitForTimeout(2500);
  await sample.click();await page.getByText('CNS excerpt loaded.',{exact:false}).waitFor();
  if(await page.getByTestId('download-link').count())throw Error('Preloaded outputs');
  note('fictional_editable_profile_loaded');
  const gns=(await fs.readFile('.source-cache/v04/gns_travel.paragraphs.txt','utf8')).split('\n');
  for(const scenario of [
   {id:'supported',first:'Yes',presenter:'Yes',heading:'REVIEW REQUIRED',expected:'2 MATCH | 0 NOT MATCH | 0 UNKNOWN | 0 INFO'},
   {id:'contradiction',first:'No',presenter:'Yes',heading:'CONTRADICTIONS TO RESOLVE',expected:'1 MATCH | 1 NOT MATCH | 0 UNKNOWN | 0 INFO'},
   {id:'unknown',first:'Yes',presenter:'Unknown',heading:'REVIEW REQUIRED',expected:'1 MATCH | 0 NOT MATCH | 1 UNKNOWN | 0 INFO'},
   {id:'historical-exclusion',text:[63,65,66,76].map(n=>gns[n-1]).join('\n'),heading:'REVIEW REQUIRED'}
  ]){
   if(scenario.text){
    await page.getByLabel('Opportunity title',{exact:true}).fill('GNS FENS 2026 travel grant — historical excerpts; deadline passed');
    await page.getByRole('textbox',{name:/Official announcement link/}).fill('https://nwg-info.de/en/node/14775');
    await source.fill(scenario.text);
   }else{await answer(first,scenario.first);await answer(presenter,scenario.presenter);}
   await go.scrollIntoViewIfNeeded();note('start_'+scenario.id);await go.click();
   await page.waitForFunction(()=>[...document.querySelectorAll('button')].some(b=>b.textContent.trim()==='Analyze public announcement'&&b.disabled));
   if(await sample.isEnabled())throw Error('Inputs not locked');
   await page.getByRole('heading',{name:scenario.heading,exact:true}).waitFor({timeout:310000});
   await page.waitForFunction(()=>[...document.querySelectorAll('button')].some(b=>b.textContent.trim()==='Analyze public announcement'&&!b.disabled));
   note('complete_'+scenario.id);
   await page.getByRole('heading',{name:scenario.heading,exact:true}).evaluate(el=>el.scrollIntoView({block:'start'}));
   await page.screenshot({path:path.join(base,scenario.id+'-overview.png')});
   await page.waitForTimeout(3500);await plan.click();
   const dossier=page.locator('#readiness-dossier');
   await dossier.getByRole('heading',{name:'Application Readiness Dossier',exact:true}).evaluate(el=>el.scrollIntoView({block:'start'}));
   await page.waitForTimeout(500);await page.screenshot({path:path.join(base,scenario.id+'.png')});
   const visible=await dossier.innerText();
   if(!visible.includes('A. Potential application blockers')||!visible.includes('E. Final pre-application checklist'))throw Error('Incomplete dossier');
   if(scenario.id==='historical-exclusion'&&(!visible.includes('Possible exclusion or exception')||!visible.includes('February 13, 2026')||!visible.includes('PAST')))throw Error('Source warnings/date missing');
   if(scenario.id==='unknown'&&!visible.includes('Check the designated presenter'))throw Error('Missing fact action');
   await page.waitForTimeout(4500);
   await dossier.getByRole('heading',{name:'C. Application materials and deadlines',exact:true}).evaluate(el=>el.scrollIntoView({block:'start'}));
   await page.waitForTimeout(3500);
   for(const [id,suffix] of [['dossier-download','dossier'],['evidence-download','report']]){
    const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#'+id).getByTestId('download-link').click()]);
    const file=path.join(base,scenario.id+'-'+suffix+'.md');await download.saveAs(file);
    const bytes=await fs.readFile(file),md=bytes.toString();
    if(suffix==='report'&&(!md.includes('**Mode:** gemma')||(scenario.expected&&!md.includes(scenario.expected))))throw Error('Report mode/count mismatch');
    if(suffix==='dossier'&&!md.includes('## E. Final pre-application checklist'))throw Error('Dossier download incomplete');
    const input=await source.inputValue();
    if(suffix==='dossier'){
     const sections=md.split(/### Source passage \d+\n\n/).slice(1);
     for(const section of sections){const m=section.match(/^Characters (\d+):(\d+)\n\n([\s\S]*?)\n*$/);if(!m||input.slice(+m[1],+m[2])!==m[3].replace(/\\([\\`*_{}\[\]()#+.!|>~\-])/g,'$1').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'\"').replace(/&#x27;/g,"'").replace(/&amp;/g,'&'))throw Error('Downloaded source span mismatch');}
    }
    note('download_'+scenario.id+'_'+suffix,{bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex')});
   }
   await plan.click();
  }
  await page.getByLabel('Opportunity title',{exact:true}).fill('Edited — both downloads must clear');
  await page.getByText('Inputs changed. Analyze again before using or downloading a report.',{exact:true}).waitFor();
  await page.waitForFunction(()=>!document.querySelector('[data-testid=download-link]')&&!document.querySelector('#readiness-dossier').innerText.trim(),null,{timeout:3000});
  note('edit_invalidates_both_outputs');
  await sample.click();await page.getByText('CNS excerpt loaded.',{exact:false}).waitFor();
  if(await page.getByTestId('download-link').count())throw Error('Stale sample download');
  if(errors.length)throw Error(errors.join(';'));
  await fs.writeFile(path.join(base,'events.json'),JSON.stringify({browser:browser.version(),recording:'Actual continuous headless Chromium; local Gemma 1B; no model mocks, video edits or speed changes',scope:'Three fictional CNS profiles plus historical GNS excerpts; not complete announcement analysis',events,page_errors:errors},null,2));
 }finally{const video=page.video();await context.close();if(video)console.log('VIDEO',await video.path());await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
