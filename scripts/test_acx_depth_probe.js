/* Portable control-flow/safety tests only. No Adobe pixel algorithm is emulated. */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');
const scriptPath = process.argv[2] || path.join(__dirname, 'ACX_Depth_Probe.jsx');
const code = fs.readFileSync(scriptPath, 'utf8').replace(/^#target[^\n]*\n/, '');
new vm.Script(code, {filename: scriptPath});
const mock = String.raw`
var opts = OPTIONS;
var log = {mutations:0, removed:0, undo:0, files:{}, alerts:[], samples:0, originalChanged:0};
var clock = 1000000;
function Date() {}
Date.prototype.getTime = function () { clock += opts.timeout ? 100000 : 1; return clock; };
function Property(value, index, cloned) {
  this.value=value;this.propertyIndex=index;this.name='p'+index;this.matchName='param-'+index;
  this.hasMin=false;this.hasMax=false;this.canSetExpression=true;this.expression='';this.numKeys=0;
  this.valueAtTime=function(){return this.value;};
  this.setValue=function(v){if(!cloned){log.originalChanged++;} if(opts.setFail){throw Error('setter failure');}
    if(!(opts.ignoreClamp && index===5))this.value=v;};
}
function Effect(cloned) {
  this.matchName='ADBE AUX CHANNEL EXTRACT';this.numProperties=6;this.enabled=true;
  var vals=[1,5000,0,0,1,0], props=vals.map(function(v,i){return new Property(v,i+1,cloned);});
  this.property=function(i){return props[i-1];};
}
function Source() {this.name='DEPTH_SOURCE';this.renderer='Classic 3D';this.resolutionFactor=[1,1];}
function CompItem(cloned) {
  this.name='DEPTH_TEST';this.numLayers=opts.multiLayer?2:1;this.duration=10;this.time=0;
  var effect=new Effect(cloned), src=new Source();Object.setPrototypeOf(src,CompItem.prototype);
  var layer={index:1,source:src,threeDLayer:false,inPoint:0,outPoint:10,collapseTransformation:true,
    enabled:true,width:1920,height:1080,property:function(){return {numProperties:1,property:function(){return effect;}};}};
  this.layer=function(){return layer;};
  this.duplicate=function(){log.mutations++;return new CompItem(true);};
  this.remove=function(){log.removed++;if(opts.cleanupFail)throw Error('remove failed');};
  this.layers={addText:function(){
    layer.index=2;
    var text={expression:'',expressionError:'',expressionEnabled:false,valueAtTime:function(){
      log.samples++;
      if(opts.exprFail){this.expressionError='expression rejected';throw Error(this.expressionError);}
      if(opts.malformed)return {text:'nonsense'};
      var P=JSON.parse(this.expression.match(/var P=(\[[\s\S]*?\]);var rows/)[1]);
      return {text:P.map(function(p){return [p[0],p[1],opts.nonfinite?'NaN':0.25,0.5,0.75,1].join(',');}).join('\r')};
    }};
    return {property:function(){return {property:function(){return text;}};}};
  }};
}
var original=new CompItem(false), actualBits=16;
var project={numItems:opts.duplicateComp?2:1,item:function(){return original;},renderQueue:{rendering:!!opts.busy},
  file:{name:'3dextract.aep'},workingSpace:'',linearBlending:false,expressionEngine:'javascript-1.0'};
Object.defineProperty(project,'bitsPerChannel',{get:function(){return actualBits;},set:function(v){
  if(!opts.ignoreBits || v===16)actualBits=v;
}});
var app={project:project,version:'25.6',buildNumber:101,
  beginUndoGroup:function(){log.undo++;},endUndoGroup:function(){log.undo--;},
  save:function(){throw Error('unexpected save');}};
var $={os:'MOCK-NOT-AE'};var LayerQuality={BEST:1};
function Folder(p){this.fsName=p;this.exists=!!opts.collision;}
Folder.desktop={fsName:'/mock/desktop'};
Folder.prototype.create=function(){return !opts.folderFail;};
Folder.prototype.execute=function(){};
function File(p){this.fsName=p;this.error='test';}
File.prototype.open=function(){return !opts.writeDenied;};
File.prototype.write=function(s){if(opts.writeFail)return false;log.files[this.fsName]=s;return true;};
File.prototype.close=function(){return !opts.closeFail;};
function alert(s){log.alerts.push(s);}
`;
function run(options) {
  const ctx = vm.createContext({OPTIONS:options});
  vm.runInContext(mock, ctx);
  vm.runInContext(code, ctx, {timeout:4000});
  const states=Object.values(ctx.log.files).map(v=>JSON.parse(v));
  return {log:ctx.log, report:states[states.length-1], bits:ctx.project.bitsPerChannel};
}
let count=0;
function test(name, fn){fn();count++;console.log('PASS '+name);}
test('syntax and forbidden destructive APIs',()=>{
  assert(!/app\.project\.save\s*\(|project\.save\s*\(|app\.purge\s*\(|executeCommand\s*\(|close\(CloseOptions/.test(code));
});
test('28 cases, 45 samples, and original fixture untouched',()=>{
  const r=run({});assert.equal(r.report.status,'COLLECTED');assert.equal(r.report.cases.length,28);
  assert(r.report.cases.every(x=>x.samples.length===45&&x.status==='RECORDED'));
  assert.equal(r.log.originalChanged,0);assert.equal(r.bits,16);assert.equal(r.log.removed,1);assert.equal(r.log.undo,0);
  assert(!JSON.stringify(r.report).includes('"status":"PASS"'));
});
test('Clamp OFF only attempted at 32 bpc',()=>{
  const r=run({});const c=r.report.cases.filter(x=>x.id==='clamp_off_request');
  assert.equal(c.length,1);assert.equal(c[0].bpc,32);
});
test('ignored Clamp request recorded, not declared working',()=>{
  const r=run({ignoreClamp:true});assert.equal(r.report.cases[27].clampRequestApplied,false);
});
test('permissions failure happens before project duplication',()=>{
  const r=run({writeDenied:true});assert.equal(r.log.mutations,0);assert.equal(r.bits,16);
  assert(r.log.alerts[0].includes('ERROR'));
});
test('write and close failures do not run tests',()=>{
  for(const opt of [{writeFail:true},{closeFail:true}]) {const r=run(opt);assert.equal(r.log.mutations,0);assert.equal(r.log.samples,0);}
});
test('ambiguous input and busy host rejected',()=>{
  for(const opt of [{duplicateComp:true},{multiLayer:true},{busy:true},{collision:true},{folderFail:true}]) {
    const r=run(opt);assert.equal(r.log.mutations,0);assert.equal(r.log.samples,0);
  }
});
test('expression failure stops once and restores state',()=>{
  const r=run({exprFail:true});assert.equal(r.report.status,'ERROR');assert.equal(r.log.samples,1);
  assert.equal(r.log.removed,1);assert.equal(r.bits,16);assert.equal(r.log.undo,0);
});
test('malformed sample rows stop once, not silently accepted',()=>{
  const r=run({malformed:true});assert.equal(r.report.status,'ERROR');assert.equal(r.log.samples,1);assert.equal(r.bits,16);
});
test('setter and bit-depth failure restore original state',()=>{
  for(const opt of [{setFail:true},{ignoreBits:true}]) {
    const r=run(opt);assert.equal(r.report.status,'ERROR');assert.equal(r.log.samples,0);assert.equal(r.bits,16);assert.equal(r.log.removed,1);
  }
});
test('cleanup error cannot produce COLLECTED',()=>{
  const r=run({cleanupFail:true});assert.equal(r.report.status,'ERROR');assert(r.report.cleanupErrors.length>0);
});
test('non-finite observations retained explicitly',()=>{
  const r=run({nonfinite:true});assert.equal(r.report.cases[0].samples[0].rgba[0],'NaN');
});
test('soft budget stops between calls and restores state',()=>{
  const r=run({timeout:true});assert.equal(r.report.status,'ERROR');assert.equal(r.bits,16);assert.equal(r.log.removed,1);
});
console.log(count+' portable tests passed; AE host behavior NOT RUN.');
