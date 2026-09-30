/* Portable orchestration/safety tests. Synthetic pixels are NOT Adobe algorithm evidence. */
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const scriptPath=process.argv[2]||path.join(__dirname,'ACX_Edge_Render_Probe.jsx');
const code=fs.readFileSync(scriptPath,'utf8').replace(/^#target[^\n]*\n/,'');
new vm.Script(code,{filename:scriptPath});
const mock=String.raw`
var opts=OPTIONS, tick=1000000, log={files:{},dirs:{},renders:[],alerts:[],originalWrites:0,compRemoved:0,rqRemoved:0,undo:0,sampleCalls:0,frameRanges:[],flagWrites:[]};
function Date(){}Date.prototype.getTime=function(){tick+=opts.timeout?100000:1;return tick;};
var $={os:'MOCK-NOT-AE'},LayerQuality={BEST:1},PostRenderAction={NONE:0},GetSettingsFormat={STRING:1,STRING_SETTABLE:2};
var RQItemStatus={QUEUED:1,UNQUEUED:2,DONE:3,RENDERING:4,WILL_CONTINUE:5,USER_STOPPED:6};
function Property(v,i,clone){this.value=v;this.numKeys=0;this.canSetExpression=true;this.expression='';
 this.valueAtTime=function(){return this.value;};
 this.setValue=function(x){if(!clone)log.originalWrites++;if(opts.setterFail)throw Error('set failure');if(!(opts.ignoreAA&&i===4))this.value=x;};}
function Effect(clone){this.matchName='ADBE AUX CHANNEL EXTRACT';this.numProperties=6;this.enabled=true;
 var a=[1,5000,0,0,1,0].map(function(v,i){return new Property(v,i+1,clone);});this.property=function(i){return a[i-1];};}
function CompItem(clone){
 this.name='DEPTH_TEST';this.id=clone?99:1;this.width=1920;this.height=1080;this.pixelAspect=1;this.frameDuration=.04;this.time=.84;this.duration=3;this.numLayers=opts.multiLayer?2:1;
 var e=new Effect(clone),source=Object.create(CompItem.prototype);source.name='DEPTH_SOURCE';source.renderer='ADBE Advanced 3d';source.resolutionFactor=[1,1];source.useProxy=!!opts.proxy;
 var l={width:1920,height:1080,index:1,source:source,threeDLayer:false,inPoint:0,outPoint:3,collapseTransformation:true,enabled:true,startTime:0,stretch:100,
 property:function(){return {numProperties:1,property:function(){return e;}};}};
 this.layer=function(){return l;};this.duplicate=function(){return new CompItem(true);};
 this.remove=function(){log.compRemoved++;if(opts.cleanupFail)throw Error('comp cleanup');};
 this.layers={addText:function(){l.index=2;var prop={expression:'',expressionError:'',valueAtTime:function(){
  log.sampleCalls++;if(opts.exprFail)throw Error('expression error');if(opts.malformed)return {text:'broken'};
  var p=JSON.parse(this.expression.match(/var P=(\[[\s\S]*?\]);var rows/)[1]);
  return {text:p.map(function(v){var x=v[0],y=v[1],c=opts.noEdges?.4:(x<320.3?.2:.8);
    if(!opts.noEdges&&e.property(4).value===1&&Math.abs(x-320.3)<.75)c=.2+.6*(x-319.55)/1.5;
    return [x,y,opts.nonfinite?'NaN':c,c,c,1].join(',');}).join('\r')};
 }};return {enabled:true,guideLayer:false,property:function(){return {property:function(){return prop;}};}};}};
}
var actualBits=16,orig=new CompItem(false);
function Folder(p){this.fsName=p;this.name=p.split('/').pop();}
Object.defineProperty(Folder.prototype,'exists',{get:function(){return !!log.dirs[this.fsName]||!!opts.collision;}});
Folder.desktop={fsName:'/mock/desktop'};Folder.prototype.create=function(){if(opts.folderFail)return false;log.dirs[this.fsName]=true;return true;};
Folder.prototype.execute=function(){};
Folder.prototype.getFiles=function(){var base=this.fsName+'/';return Object.keys(log.files).filter(function(p){return p.indexOf(base)===0&&p.slice(base.length).indexOf('/')<0;}).map(function(p){return new File(p);});};
function File(p){this.fsName=p;this.name=p.split('/').pop();this.parent=new Folder(p.slice(0,p.lastIndexOf('/')));this.error='mock';}
Object.defineProperty(File.prototype,'length',{get:function(){return (log.files[this.fsName]||'').length;}});
File.prototype.open=function(mode){this.mode=mode;return !(opts.writeDenied&&mode==='w');};
File.prototype.write=function(s){if(opts.writeFail)return false;log.files[this.fsName]=s;return true;};
File.prototype.close=function(){return !opts.closeFail;};File.prototype.read=function(n){return (log.files[this.fsName]||'').slice(0,n);};
var templates=opts.noTemplates?['video']:opts.pngOnly?['png']:['video','png','float'];
var templateSettings={video:{Format:'H.264',Depth:'Millions of Colors',Channels:'RGB'},png:{Format:'PNG Sequence',Depth:'Millions of Colors+',Channels:'RGB + Alpha'},
 float:{Format:'OpenEXR Sequence',Depth:'Floating Point+',Channels:'RGB + Alpha'}};
var queue=[];
function QueueItem(comp,existing,status){
 var self=this,epoch=0,settings=templateSettings.video,outFile=null,flag=status===RQItemStatus.QUEUED;
 this.comp=comp;this.existing=existing;this.status=status||RQItemStatus.UNQUEUED;this.numOutputModules=opts.multiOutput?2:1;this.elapsedSeconds=.1;
 this.onStatusChanged=existing&&opts.callback?'existing_callback':null;
 Object.defineProperty(this,'render',{get:function(){return flag;},set:function(v){
  if(existing){log.flagWrites.push([existing,v]);if(opts.suspendFail&&!v)throw Error('suspend failed');if(opts.restoreFail&&v)throw Error('restore failed');}
  flag=v;self.status=v?RQItemStatus.QUEUED:RQItemStatus.UNQUEUED;
 }});
 this.setSettings=function(s){this.renderSettings=s;};
 this.getSettings=function(){var s=Object.assign({},this.renderSettings);if(opts.wrongDepth)s['Color Depth']='Current Settings';return s;};
 this.outputModule=function(){var myEpoch=epoch;function check(){if(myEpoch!==epoch)throw Error('stale output module');}
  var om={templates:templates,applyTemplate:function(n){check();settings=Object.assign({Crop:false,Resize:false},templateSettings[n]);epoch++;},
   getSettings:function(){check();return Object.assign({},settings);},setSettings:function(s){check();settings=Object.assign({},settings,s);epoch++;}};
  Object.defineProperty(om,'file',{get:function(){check();return outFile;},set:function(v){check();outFile=opts.escape?new File('/outside/frame.exr'):v;}});
  return om;
 };
 this.remove=function(){log.rqRemoved++;if(opts.rqCleanupFail)throw Error('queue remove');queue.splice(queue.indexOf(self),1);};
 this.doRender=function(){
  if(existing)throw Error('RENDERED ORIGINAL QUEUE ITEM');log.renders.push(comp.name);log.frameRanges.push([this.timeSpanStart,this.timeSpanDuration,actualBits]);
  if(opts.stopRender){this.status=RQItemStatus.USER_STOPPED;return;}
  this.status=RQItemStatus.DONE;flag=false;if(opts.missingOutput)return;
  var p=outFile.fsName.replace('[#####]','00021'),ext=p.split('.').pop(),magic=ext==='exr'?'\x76\x2f\x31\x01':ext==='png'?'\x89PNG\r\n\x1a\n':'8BPS';
  log.files[p]=(opts.badMagic?'BAD!':magic)+'TEST-PAYLOAD';if(opts.duplicateOutput)log.files[p.replace('00021','00022')]=magic+'TEST-PAYLOAD';
 };
}
var originalQueued=new QueueItem(orig,'queued',RQItemStatus.QUEUED),originalDone=new QueueItem(orig,'done',RQItemStatus.DONE);queue.push(originalQueued,originalDone);
var rq={rendering:!!opts.busy,item:function(i){return queue[i-1];},items:{add:function(c){var x=new QueueItem(c,false,RQItemStatus.QUEUED);queue.push(x);return x;}},
 render:function(){if(log.undo)throw Error('undo held across render');queue.slice().forEach(function(x){if(x.render)x.doRender();});}};
Object.defineProperty(rq,'numItems',{get:function(){return queue.length;}});
var project={numItems:opts.duplicateComp?2:1,item:function(){return orig;},renderQueue:rq,file:{name:'3dextract.aep'},workingSpace:'None',dirty:true};
Object.defineProperty(project,'bitsPerChannel',{get:function(){return actualBits;},set:function(v){if(!(opts.ignoreBpc&&v===32))actualBits=v;}});
var app={project:project,version:'25.6x101',buildNumber:101,beginUndoGroup:function(){log.undo++;},endUndoGroup:function(){log.undo--;}};
function alert(s){log.alerts.push(s);}
`;
function run(options={}) {
 const ctx=vm.createContext({OPTIONS:options});vm.runInContext(mock,ctx);vm.runInContext(code,ctx,{timeout:7000});
 const reports=Object.entries(ctx.log.files).filter(([p])=>p.endsWith('/report.json')).map(([,s])=>JSON.parse(s));
 return {ctx,log:ctx.log,r:reports[0]};
}
let total=0;
function test(n,f){f();total++;console.log('PASS '+n);}
function restored(x){assert.equal(x.ctx.project.bitsPerChannel,16);assert.equal(x.log.originalWrites,0);assert.equal(x.ctx.originalDone.status,x.ctx.RQItemStatus.DONE);assert.equal(x.ctx.originalQueued.status,x.ctx.RQItemStatus.QUEUED);assert.equal(x.log.undo,0);}
test('no destructive save, purge, preference, shell or MFR APIs',()=>{
 assert(!/\.save\s*\(|saveAsTemplate\s*\(|app\.purge\s*\(|executeCommand\s*\(|savePref|callSystem\s*\(|setMultiFrameRenderingConfig\s*\(/.test(code));
});
test('edge pairs and six actual queue exports, not 28 repeated cases',()=>{
 const x=run();assert.equal(x.r.status,'COLLECTED');assert.equal(x.r.cases.length,6);assert.equal(x.r.exports.length,6);assert.equal(x.log.renders.length,6);
 assert(x.r.exports.every(r=>r.status==='EXPORTED'&&r.file.bytes>8));assert(x.r.cases.every(c=>c.samples.length>0&&c.samples.length<=1344));
 assert(x.r.cases[1].comparisonWithAA0.changedLocations>0);assert(!JSON.stringify(x.r).includes('"status":"PASS"'));restored(x);
 assert.equal(x.ctx.project.renderQueue.numItems,2);assert.equal(x.log.compRemoved,1);
});
test('exactly one aligned frame per render',()=>{
 const x=run();assert(x.log.frameRanges.every(v=>v[0]===.84&&v[1]===.04));assert.deepEqual(Array.from(x.log.frameRanges,v=>v[2]),[8,8,16,16,32,32]);
});
test('scanline bounds and quarter-pixel pairs are explicit',()=>{
 const x=run();assert(x.r.edges.points.some(p=>p[0]%1!==0||p[1]%1!==0));assert(x.r.edges.points.every(p=>p[0]>=0&&p[0]<=1919&&p[1]>=0&&p[1]<=1079));
 for(let i=0;i<x.r.cases.length;i+=2)assert.deepEqual(x.r.cases[i].samples.map(s=>s.point),x.r.cases[i+1].samples.map(s=>s.point));
});
test('zero discovered edges is BLOCKED, not AA acceptance',()=>{const x=run({noEdges:true});assert.equal(x.r.status,'PARTIAL');assert.equal(x.r.edgeStatus,'BLOCKED_NO_TRANSITIONS');assert.equal(x.r.cases.length,0);restored(x);});
test('no installed image format preserves edge results and blocks exports',()=>{
 const x=run({noTemplates:true});assert.equal(x.r.status,'PARTIAL');assert.equal(x.log.renders.length,0);assert.equal(x.r.cases.length,6);assert(x.r.exports.every(r=>r.status==='BLOCKED'));restored(x);
});
test('8-bit PNG is not mislabeled as 16/32-bit output',()=>{
 const x=run({pngOnly:true});assert.equal(x.r.status,'PARTIAL');assert.equal(x.log.renders.length,2);assert(x.r.exports.filter(r=>r.bpc>8).every(r=>r.status==='BLOCKED'));restored(x);
});
test('permissions tested before editing project or queue',()=>{
 for(const opt of [{writeDenied:true},{writeFail:true},{closeFail:true},{collision:true},{folderFail:true}]){
  const x=run(opt);assert.equal(x.log.renders.length,0);assert.equal(x.log.compRemoved,0);assert.equal(x.log.flagWrites.length,0);restored(x);
 }
});
test('busy or ambiguous fixtures rejected without measurement',()=>{
 for(const opt of [{busy:true},{multiLayer:true},{duplicateComp:true},{proxy:true}]){const x=run(opt);assert.equal(x.log.sampleCalls,0);assert.equal(x.log.compRemoved,0);restored(x);}
});
test('expression failure or malformed result halts and restores',()=>{
 for(const opt of [{exprFail:true},{malformed:true}]){const x=run(opt);assert.equal(x.r.status,'ERROR');assert.equal(x.log.sampleCalls,1);assert.equal(x.log.renders.length,0);restored(x);}
});
test('wrong applied settings cannot silently continue',()=>{
 for(const opt of [{setterFail:true},{ignoreBpc:true},{ignoreAA:true}]){const x=run(opt);assert.equal(x.r.status,'ERROR');assert.equal(x.log.renders.length,0);restored(x);}
});
test('OutputModule is reacquired after settings invalidate it',()=>{const x=run();assert.equal(x.r.status,'COLLECTED');});
test('render readback mismatch, path escape or multiple outputs refuses render',()=>{
 for(const opt of [{wrongDepth:true},{escape:true},{multiOutput:true}]){const x=run(opt);assert.equal(x.r.status,'ERROR');assert.equal(x.log.renders.length,0);restored(x);}
});
test('user stopped render does not run remaining exports',()=>{const x=run({stopRender:true});assert.equal(x.r.status,'ERROR');assert.equal(x.log.renders.length,1);restored(x);});
test('DONE alone without a valid single frame is not success',()=>{
 for(const opt of [{missingOutput:true},{badMagic:true},{duplicateOutput:true}]){const x=run(opt);assert.equal(x.r.status,'ERROR');assert.equal(x.log.renders.length,1);assert.equal(x.r.exports[0].status,'ERROR');restored(x);}
});
test('only queued originals toggled; DONE and original effect untouched',()=>{
 const x=run();assert.deepEqual(Array.from(x.log.flagWrites,v=>Array.from(v)),[['queued',false],['queued',true]]);restored(x);
});
test('existing callback prevents queue mutation and render',()=>{const x=run({callback:true});assert.equal(x.r.status,'PARTIAL');assert.equal(x.r.exportStatus,'BLOCKED');assert.equal(x.log.flagWrites.length,0);restored(x);});
test('queue suspend failure does not run any export',()=>{const x=run({suspendFail:true});assert.equal(x.r.status,'PARTIAL');assert.equal(x.log.renders.length,0);restored(x);});
test('cleanup failures cannot return COLLECTED',()=>{
 for(const opt of [{cleanupFail:true},{restoreFail:true},{rqCleanupFail:true}]){const x=run(opt);assert.equal(x.r.status,'ERROR');assert(x.r.cleanupErrors.length>0);}
});
test('nonfinite observations do not create fictitious edge transitions',()=>{
 const x=run({nonfinite:true});assert.equal(x.r.edgeStatus,'BLOCKED_NO_TRANSITIONS');assert(x.r.discovery.scanlines[0].samples[0].rgba.includes('NaN'));restored(x);
});
test('soft timeout halts between calls and restores state',()=>{const x=run({timeout:true});assert.equal(x.r.status,'ERROR');assert.equal(x.log.renders.length,0);restored(x);});
console.log(total+' portable checks passed; Adobe renderer/host execution NOT RUN.');
