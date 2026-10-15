/* Run against the real local app with Ollama deliberately stopped. No API mocks. */
const{chromium}=require('playwright');const fs=require('node:fs/promises');
(async()=>{
 const dir=process.argv[2]||'.local-reports/onboarding-failure-smoke';await fs.mkdir(dir,{recursive:true});
 const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1280,height:900}});
 try{
 await page.goto('http://127.0.0.1:7863');
 await page.getByRole('button',{name:'Check local model',exact:true}).click();
 await page.getByText('Ollama is not reachable locally.',{exact:false}).waitFor();
 await page.getByRole('button',{name:'Load sample public excerpt (CNS; fictional applicant)',exact:true}).click();
 await page.getByText('CNS excerpt loaded.',{exact:false}).waitFor();
 const method=page.locator('fieldset').filter({has:page.getByText('Analysis method',{exact:true})}).first();
 await method.getByRole('radio',{name:'Rule baseline (NO AI)',exact:true}).check();
 const go=page.getByRole('button',{name:'Analyze public announcement',exact:true});await go.click();
 await page.getByRole('heading',{name:'REVIEW REQUIRED',exact:true}).waitFor();
 await page.getByText('Rule baseline — NO AI',{exact:true}).waitFor();
 await page.getByTestId('download-link').waitFor();
 await method.getByRole('radio',{name:'Live local Gemma',exact:true}).check();
 await page.getByTestId('download-link').waitFor({state:'hidden'});
 await go.click();await page.getByRole('heading',{name:'Analysis unavailable',exact:true}).waitFor();
 if(await page.getByTestId('download-link').count())throw Error('Stale download on real live failure');
 await page.getByText('No result or download was fabricated.',{exact:false}).waitFor();
 await page.getByRole('heading',{name:'Analysis unavailable',exact:true}).scrollIntoViewIfNeeded();
 await page.screenshot({path:dir+'/offline-failure.png'});
 await fs.writeFile(dir+'/checks.json',JSON.stringify({ollama_deliberately_stopped:true,manual_status_unreachable:true,explicit_no_ai_success:true,live_connection_failure_clears_download:true,no_fallback:true},null,2));
 console.log('PASS real offline diagnostic, explicit NO AI, live failure and stale report clearing');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
