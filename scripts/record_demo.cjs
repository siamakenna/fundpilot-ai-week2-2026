/* Authentic headless-browser recording. Requires Playwright and its Chromium/FFmpeg.
 * Run with NODE_PATH set to the installed Playwright modules directory.
 * No page content, model response, network route or time is mocked.
 */
const {chromium}=require('playwright');
const fs=require('node:fs/promises');
const path=require('node:path');
const base=path.resolve(process.argv[2] || '.local-reports/browser-demo');
const url=process.argv[3] || 'http://127.0.0.1:7861';
(async()=>{
 await fs.mkdir(base,{recursive:true});
 const browser=await chromium.launch({headless:true});
 const context=await browser.newContext({viewport:{width:1440,height:1000},recordVideo:{dir:base,size:{width:1440,height:1000}},acceptDownloads:true});
 const page=await context.newPage();
 const started=Date.now();const events=[];
 const note=(name)=>events.push({name,seconds:(Date.now()-started)/1000});
 try{
  await page.goto(url);await page.getByRole('button',{name:'Analyze public announcement',exact:true}).waitFor();
  await page.getByLabel('Opportunity title',{exact:true}).fill('CNS 2027 — one eligibility passage; fictional applicant');
  await page.getByLabel('Official source URL (attribution only; not fetched)',{exact:true}).fill('https://www.cogneurosociety.org/travel-award/');
  await page.getByLabel('Eligibility, exclusions, amounts, deadlines and application instructions',{exact:true}).fill('Applicants must be the first author and presenter of a poster submitted for presentation at the CNS 2027 Annual Meeting.');
  const answer=async(question,value)=>page.locator('fieldset').filter({has:page.getByText(question,{exact:true})}).getByRole('radio',{name:value,exact:true}).check();
  const first='First author of the submitted work?';const presenter='Presenting author / presenter of the work?';
  if(await page.getByLabel('Requested funding (optional; leave blank if unknown)',{exact:true}).inputValue()!=='')throw Error('Unknown amount is not blank');
  await page.waitForTimeout(4000); // viewing time, not a model latency measurement
  for(const scenario of [
   {id:'supported',first:'Yes',presenter:'Yes',expect:'REVIEW REQUIRED'},
   {id:'contradiction',first:'No',presenter:'Yes',expect:'CONTRADICTIONS TO RESOLVE'},
   {id:'unknown',first:'Yes',presenter:'Unknown',expect:'REVIEW REQUIRED'}
  ]){
   await answer(first,scenario.first);await answer(presenter,scenario.presenter);
   await page.getByRole('button',{name:'Analyze public announcement',exact:true}).scrollIntoViewIfNeeded();
   note('start_'+scenario.id);
   await page.getByRole('button',{name:'Analyze public announcement',exact:true}).click();
   await page.getByLabel('Opportunity title',{exact:true}).waitFor({state:'visible'});
   await page.waitForFunction(()=>Array.from(document.querySelectorAll('button')).some(b=>b.textContent.trim()==='Analyze public announcement'&&b.disabled));
   await page.getByRole('heading',{name:scenario.expect,exact:true}).waitFor({timeout:180000});
   await page.waitForFunction(()=>Array.from(document.querySelectorAll('button')).some(b=>b.textContent.trim()==='Analyze public announcement'&&!b.disabled));
   note('complete_'+scenario.id);
   await page.getByRole('heading',{name:scenario.expect,exact:true}).scrollIntoViewIfNeeded();
   const text=await page.locator('body').innerText();
   if(!text.includes('Live Gemma interpretation'))throw Error('Live mode not confirmed');
   await fs.writeFile(path.join(base,scenario.id+'.txt'),text);
   await page.screenshot({path:path.join(base,scenario.id+'.png'),fullPage:true});
   await page.waitForTimeout(7000);
  }
  // Click the real report anchor exposed by Gradio; inspect actual downloaded bytes.
  const link=page.getByTestId('download-link');
  if(await link.count()!==1)throw Error('Expected exactly one report download');
  const [download]=await Promise.all([page.waitForEvent('download'),link.click()]);
  const reportPath=path.join(base,'downloaded-report.md');await download.saveAs(reportPath);
  const report=await fs.readFile(reportPath,'utf8');
  if(!report.includes('**Mode:** gemma')||!report.includes('UNKNOWN')||!report.includes('MATCH'))throw Error('Downloaded report did not match the live scenario');
  note('download_verified');
  await page.screenshot({path:path.join(base,'download-verified.png'),fullPage:true});
  await page.getByText('Full evidence report and passage review checklist',{exact:true}).click();
  await page.getByRole('heading',{name:'FundPilot AI — Application readiness report',exact:true}).scrollIntoViewIfNeeded();
  await page.waitForTimeout(7000);
  // Editing after completion must invalidate the previous file, not relabel it.
  await page.getByLabel('Opportunity title',{exact:true}).fill('Changed title — report must be regenerated');
  await page.getByText('Inputs changed. Analyze again before using or downloading a report.',{exact:true}).waitFor();
  if(await page.locator('a[download]').count())throw Error('Stale report download remained');
  note('edited_input_invalidated_report');
  await fs.writeFile(path.join(base,'events.json'),JSON.stringify({url,recording:'actual headless Chromium; no model mocks, no edits or speed changes',scope:'One short official CNS passage; three fictional applicant configurations, not full-call eligibility',events},null,2));
 }finally{
  const video=page.video();await context.close();if(video)console.log('VIDEO',await video.path());await browser.close();
 }
})().catch(e=>{console.error(e);process.exitCode=1});
