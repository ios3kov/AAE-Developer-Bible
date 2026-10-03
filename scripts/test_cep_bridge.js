'use strict';
// Real template sources, fake DOM/AE objects: no CEP or AE runtime claim.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.join(__dirname, '../16-WORKING-TEMPLATES/cep-panel-bridge');
const hostSource = fs.readFileSync(path.join(root, 'host/index.jsx'), 'utf8');
const clientSource = fs.readFileSync(path.join(root, 'index.js'), 'utf8');
let count = 0;
function test(name, body) { body(); count++; console.log('PASS ' + name); }
function host(options = {}) {
  function CompItem() { this.selectedLayers = options.layers || [{name: 'A'}, {name: 'B'}]; }
  const comp = new CompItem();
  const calls = [];
  const app = {project: {activeItem: options.noComp ? null : comp},
    beginUndoGroup() { calls.push('begin'); if (options.beginError) throw Error('begin failed'); },
    endUndoGroup() { calls.push('end'); if (options.endError) throw Error('cleanup failed'); }};
  const context = vm.createContext({$: {}, app, CompItem});
  vm.runInContext(hostSource, context);
  if (options.noJSON) context.JSON = undefined;
  function send(payload = {prefix: 'Bible_'}, command = 'renameSelected', extra = {}) {
    return JSON.parse(context.$._aeBible.dispatch(JSON.stringify({protocol: 1, requestId: 'r1', command, payload, ...extra})));
  }
  return {context, comp, calls, send};
}
function panel(h = host(), options = {}) {
  const listeners = {}, timers = new Map(), pending = [];
  const status = {textContent: ''};
  const button = {disabled: false, addEventListener(name, fn) { listeners[name] = fn; }};
  const context = vm.createContext({document: {getElementById(id) {return id === 'status' ? status : button;}},
    window: {addEventListener(name, fn) { listeners[name] = fn; }},
    setTimeout(fn) { const id = timers.size + 1; timers.set(id, fn); return id; },
    clearTimeout(id) { timers.delete(id); },
    CSInterface: function () {this.evalScript = function (source, callback) {
      if (options.throwBridge) throw Error('transport failed');
      pending.push({source, callback});
    };}});
  vm.runInContext(clientSource, context);
  function reply(raw) {const call = pending.shift(); call.callback(raw === undefined ? vm.runInContext(call.source, h.context) : raw); return call;}
  return {status, button, pending, listeners, timers, reply, context, h};
}
test('valid selection, repeated prefix and empty no-op', () => {
 const h=host(); assert.equal(h.send().result.changed,2); assert.equal(h.send().result.changed,2);
 assert.equal(h.comp.selectedLayers[0].name,'Bible_Bible_A');
 const before=h.calls.length; assert.equal(h.send({prefix:''}).result.changed,0); assert.equal(h.calls.length,before);
});
test('malformed JSON controlled; version, types, sizes and unknown command rejected', () => {
 const h=host(); assert.equal(JSON.parse(h.context.$._aeBible.dispatch('{')).error.code,'INVALID_JSON');
 for(const raw of ['null','[]','{}', 'x'.repeat(65537)]) assert.equal(JSON.parse(h.context.$._aeBible.dispatch(raw)).error.outcome,'notApplied');
 assert.equal(h.send({},'ping',{protocol:2}).error.code,'UNSUPPORTED_PROTOCOL');
 assert.equal(h.send({},'other').error.code,'UNKNOWN_COMMAND');
 for(const prefix of [null,12,{},[],true,'x'.repeat(257)]) assert.equal(h.send({prefix}).error.code,'INVALID_PAYLOAD');
 assert.equal(h.send({prefix:'x'.repeat(256)}).ok,true);
 assert.equal(h.send({},'ping',{requestId:''}).error.code,'INVALID_REQUEST');
});
test('missing comp, selection and failed name read do not mutate', () => {
 assert.equal(host({noComp:true}).send().error.code,'NO_ACTIVE_COMP');
 assert.equal(host({layers:[]}).send().error.code,'NO_SELECTED_LAYERS');
 const h=host({layers:[{get name(){throw Error('read failed');}}]});
 assert.equal(h.send().error.code,'TARGET_READ_FAILED'); assert.deepEqual(h.calls,[]);
});
test('begin failure does not close unopened undo scope', () => {
 const h=host({beginError:true}); const r=h.send();
 assert.equal(r.error.outcome,'notApplied'); assert.deepEqual(h.calls,['begin']);
});
test('partial failure retains primary and cleanup errors', () => {
 const h=host({layers:[{name:'A'},{get name(){return 'B';},set name(v){throw Error('write failed');}}],endError:true});
 const r=h.send(); assert.equal(r.error.code,'COMMAND_FAILED'); assert.equal(r.error.message,'write failed');
 assert.equal(r.error.details.cleanupError,'cleanup failed'); assert.equal(r.error.details.changedBeforeError,1);
 assert.equal(r.error.outcome,'mayHaveApplied'); assert.equal(h.comp.selectedLayers[0].name,'Bible_A');
});
test('cleanup-only failure and serialization fallback retain uncertain outcome', () => {
 assert.equal(host({endError:true}).send().error.code,'UNDO_CLOSE_FAILED');
 const h=host(); vm.runInContext('JSON.stringify = function(){throw Error("serialize");}',h.context);
 const r=h.send(); assert.equal(r.error.code,'RESPONSE_SERIALIZATION_FAILED'); assert.equal(r.error.outcome,'mayHaveApplied');
 assert.equal(h.comp.selectedLayers[0].name,'Bible_A');
});
test('internal failure has its own code', () => {
 const h=host(); vm.runInContext('Object.prototype.toString = function(){throw Error("internal");}',h.context);
 assert.equal(h.send().error.code,'INTERNAL_ERROR');
});
test('bootstrap and missing JSON are visible with null correlation', () => {
 for(const h of [host({noJSON:true}), {context:vm.createContext({$: {}})}]) {
  const p=panel(h); p.reply(); assert.equal(p.button.disabled,true);
  assert.match(p.status.textContent,/JSON_UNAVAILABLE|BOOTSTRAP_FAILED/);
 }
});
test('one outstanding mutation, execution-time selection and repeated clicks', () => {
 const p=panel(); assert.equal(p.button.disabled,true); p.reply(); assert.equal(p.button.disabled,false);
 p.listeners.click(); p.listeners.click(); assert.equal(p.pending.length,1);
 p.h.comp.selectedLayers=[{name:'Current'}]; p.reply(); assert.equal(p.h.comp.selectedLayers[0].name,'Bible_Current');
 assert.equal(p.button.disabled,false);
});
test('malformed, mismatched and invalid result responses fail closed', () => {
 const responses=['{','EvalScript error.', JSON.stringify({protocol:1,requestId:'wrong',ok:true,result:{ready:true,protocol:1}}),
 JSON.stringify({protocol:1,requestId:null,ok:false,error:{code:'UNKNOWN_COMMAND',message:'x',outcome:'notApplied'}})];
 for(const raw of responses){const p=panel();p.reply(raw);assert.equal(p.button.disabled,true);assert.match(p.status.textContent,/Не удалось подтвердить/);}
 const p=panel();p.reply();p.listeners.click();
 const req=JSON.parse(vm.runInNewContext(p.pending[0].source,{$:{_aeBible:{dispatch(raw){return raw;}}}}));
 p.reply(JSON.stringify({protocol:1,requestId:req.requestId,ok:true,result:{changed:-1}})); assert.equal(p.button.disabled,true);
});
test('timeout and late callback cannot unblock or roll back mutation', () => {
 const p=panel(); p.reply();p.listeners.click(); const call=p.pending.shift();
 [...p.timers.values()][0](); const message=p.status.textContent;
 call.callback(vm.runInContext(call.source,p.h.context));
 assert.equal(p.status.textContent,message);assert.equal(p.button.disabled,true);assert.equal(p.h.comp.selectedLayers[0].name,'Bible_A');
});
test('unload and transport exception remain conservative', () => {
 const p=panel();p.reply();p.listeners.click();p.listeners.unload();p.reply();assert.equal(p.button.disabled,true);
 assert.equal(p.h.comp.selectedLayers[0].name,'Bible_A');
 assert.match(panel(host(),{throwBridge:true}).status.textContent,/Ошибка вызова bridge/);
});
test('confirmed no-mutation errors permit retry; uncertain host errors block', () => {
 const p=panel();p.reply();p.h.context.app.project.activeItem=null;p.listeners.click();p.reply();
 assert.match(p.status.textContent,/NO_ACTIVE_COMP/);assert.equal(p.button.disabled,false);
 for(const options of [{endError:true},{}]) {
  const q=panel(host(options));q.reply();
  if(!options.endError) vm.runInContext('JSON.stringify=function(){throw Error("serialize");}',q.h.context);
  q.listeners.click();q.reply();assert.equal(q.button.disabled,true);
  assert.match(q.status.textContent,/UNDO_CLOSE_FAILED|RESPONSE_SERIALIZATION_FAILED/);
 }
 const q=panel();q.reply();
 vm.runInContext('Object.prototype.toString=function(){throw Error("internal");}',q.h.context);
 q.listeners.click();q.reply();assert.match(q.status.textContent,/INTERNAL_ERROR/);assert.equal(q.button.disabled,true);
});
test('Unicode and script-sensitive characters roundtrip through actual client encoder', () => {
 const prefix='Ю"\\\n\u2028\u2029\'; $._injected = true; //';
 const source=clientSource.replace('prefix: "Bible_"','prefix: '+JSON.stringify(prefix));
 const p=panel(); // initialize harness, then evaluate edited fixture with same transport
 vm.runInContext(source,p.context);p.reply();p.reply();p.listeners.click();
 assert.equal(/[\u2028\u2029]/.test(p.pending[0].source),false);p.reply();
 assert.equal(p.h.comp.selectedLayers[0].name,prefix+'A');assert.equal(p.h.context.$._injected,undefined);
});
console.log(`${count} CEP bridge portable scenarios passed; AE/CEP runtime NOT RUN`);
