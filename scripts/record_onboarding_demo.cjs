/* Authentic v0.3.1 onboarding browser capture. No fixtures, response mocking or video editing.
 * NODE_PATH must point to installed Playwright modules. See release QA docs.
 */
const {chromium}=require('playwright');
const fs=require('node:fs/promises');
const path=require('node:path');
const base=path.resolve(process.argv[2] || '.local-reports/onboarding-demo');
const url=process.argv[3] || 'http://127.0.0.1:7863';
const source='Applicants must be the first author and presenter of a poster submitted for presentation at the CNS 2027 Annual Meeting.';
(async()=>{
 await fs.mkdir(base,{recursive:true});
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000},recordVideo:{dir:base,size:{width:1440,height:1000}},acceptDownloads:true});
 const page=await context.newPage();
 const started=Date.now(),events=[],errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const note=name=>events.push({name,seconds:(Date.now()-started)/1000});
 const sample=page.getByRole('button',{name:'Load sample public excerpt (CNS; fictional applicant)',exact:true});
 const go=page.getByRole('button',{name:'Analyze public announcement',exact:true});
 const textInput=page.getByLabel('Eligibility, exclusions, amounts, deadlines and application instructions',{exact:true});
 const answer=async(question,value)=>page.locator('fieldset').filter({has:page.getByText(question,{exact:true})}).getByRole('radio',{name:value,exact:true}).check();
 const first='First author of the submitted work?', presenter='Presenting author / presenter of the work?';
 try{
  await page.goto(url);await sample.waitFor();
  await page.getByRole('button',{name:'Check local model',exact:true}).click();
  await page.getByText('Local Gemma is available:',{exact:false}).waitFor();
  note('local_model_installation_checked');
  await page.getByRole('button',{name:/How FundPilot works, results and privacy/}).click();
  await page.getByRole('heading',{name:'Understand your results',exact:true}).waitFor();
  await page.waitForTimeout(4000);
  await page.getByRole('button',{name:/How FundPilot works, results and privacy/}).click();
  await sample.click();await page.waitForFunction(s=>Array.from(document.querySelectorAll('textarea')).some(t=>t.value===s),source);
  if(await textInput.inputValue()!==source)throw Error('Sample source changed');
  if(await page.getByLabel('Requested funding (optional; leave blank if unknown)',{exact:true}).inputValue()!=='')throw Error('Sample amount not unknown');
  if(await page.getByTestId('download-link').count())throw Error('Sample loaded fabricated report');
  note('quickstart_loaded');await page.screenshot({path:path.join(base,'quickstart.png')});
  await page.waitForTimeout(4000);
  for(const scenario of [
   {id:'supported',first:'Yes',presenter:'Yes',expect:'REVIEW REQUIRED',counts:'2 MATCH | 0 NOT MATCH | 0 UNKNOWN | 0 INFO'},
   {id:'contradiction',first:'No',presenter:'Yes',expect:'CONTRADICTIONS TO RESOLVE',counts:'1 MATCH | 1 NOT MATCH | 0 UNKNOWN | 0 INFO'},
   {id:'unknown',first:'Yes',presenter:'Unknown',expect:'REVIEW REQUIRED',counts:'1 MATCH | 0 NOT MATCH | 1 UNKNOWN | 0 INFO'}
  ]){
   await answer(first,scenario.first);await answer(presenter,scenario.presenter);
   await go.scrollIntoViewIfNeeded();note('start_'+scenario.id);await go.click();
   await page.waitForFunction(()=>Array.from(document.querySelectorAll('button')).some(b=>b.textContent.trim()==='Analyze public announcement'&&b.disabled));
   if(await sample.isEnabled())throw Error('Quickstart not locked during inference');
   await page.getByRole('heading',{name:scenario.expect,exact:true}).waitFor({timeout:180000});
   await page.waitForFunction(()=>Array.from(document.querySelectorAll('button')).some(b=>b.textContent.trim()==='Analyze public announcement'&&!b.disabled));
   note('complete_'+scenario.id);
   await page.getByRole('heading',{name:scenario.expect,exact:true}).evaluate(el=>el.scrollIntoView({block:'start',behavior:'instant'}));
   await page.waitForTimeout(300);
   const body=await page.locator('body').innerText();
   if(!body.includes('Live Gemma interpretation')||!body.includes('Questions to verify before applying'))throw Error('Missing live queue');
   if(scenario.id==='supported'&&!body.includes('This is not eligibility approval.'))throw Error('Missing all-match warning');
   if(scenario.id==='contradiction'&&!body.includes('Priority 1'))throw Error('Missing contradiction priority');
   if(scenario.id==='unknown'&&!body.includes('fill any known corresponding form facts'))throw Error('Missing applicant next action');
   await fs.writeFile(path.join(base,scenario.id+'.txt'),body);
   await page.screenshot({path:path.join(base,scenario.id+'.png')});
   await page.waitForTimeout(7000);
   const [download]=await Promise.all([page.waitForEvent('download'),page.getByTestId('download-link').click()]);
   const reportPath=path.join(base,scenario.id+'-report.md');await download.saveAs(reportPath);
   const report=await fs.readFile(reportPath,'utf8');
   if(!report.includes('**Mode:** gemma')||!report.includes(scenario.counts)||!report.includes('## Questions to verify before applying'))throw Error('Actual report differs from scenario');
   note('download_verified_'+scenario.id);
  }
  await page.getByRole('button',{name:/Full evidence report and passage review checklist/}).click();
  await page.getByRole('heading',{name:'FundPilot AI — Application readiness report',exact:true}).scrollIntoViewIfNeeded();
  await page.waitForTimeout(6000);
  await page.getByLabel('Opportunity title',{exact:true}).fill('Changed title — report must be regenerated');
  await page.getByText('Inputs changed. Analyze again before using or downloading a report.',{exact:true}).waitFor();
  if(await page.getByTestId('download-link').count())throw Error('Stale download remained');
  note('edited_input_invalidated_report');
  await sample.click();await page.waitForFunction(s=>Array.from(document.querySelectorAll('textarea')).some(t=>t.value===s),source);
  if(await page.getByTestId('download-link').count())throw Error('Sample reload did not clear old download');
  note('sample_reload_verified');
  if(errors.length)throw Error('Page errors: '+errors.join('; '));
  await fs.writeFile(path.join(base,'events.json'),JSON.stringify({url,browser:browser.version(),recording:'Actual headless Chromium; no model mocks, edits or speed changes',scope:'One verified short CNS excerpt; three fictional applicant configurations, not complete announcement analysis',events,page_errors:errors},null,2));
 }finally{
  const video=page.video();await context.close();if(video)console.log('VIDEO',await video.path());await browser.close();
 }
})().catch(e=>{console.error(e);process.exit(1)});
