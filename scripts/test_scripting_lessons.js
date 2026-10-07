// Portable safety/control-flow tests, not Adobe host or pixel validation.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const source = fs.readFileSync(path.join(__dirname,
  '../16-WORKING-TEMPLATES/jsx-tool/import-and-queue.jsx'), 'utf8');
function run(options = {}) {
  const log = {undo:0, imported:0, removed:[], alerts:[], reacquired:0};
  const output = {exists:!!options.collision, fsName:'/owned/new.mov'};
  function FootageItem() {this.width=640;this.height=360;this.pixelAspect=1;
    this.remove=()=>log.removed.push('footage');}
  const item = new FootageItem();
  const comp = {layers:{add(){if(options.layerFail)throw Error('layer');}},
    remove(){if(options.compCleanupFail)throw Error('comp cleanup');log.removed.push('comp');}};
  const oldModule = {templates:['Example'],applyTemplate(){
    if(options.templateFail)throw Error('template');}};
  const freshModule = {};
  const rq = {render:true,outputModule(){log.reacquired++;return log.reacquired===1?oldModule:freshModule;},
    remove(){log.removed.push('queue');}};
  const project = {renderQueue:{rendering:!!options.busy,items:{add(){return rq;}}},
    items:{addComp(){return comp;}},importFile(){log.imported++;return item;}};
  const context = {
    app:{project:options.noProject?null:project,
      beginUndoGroup(){log.undo++;},endUndoGroup(){log.undo--;}},
    File:{openDialog(){return options.cancel?null:{exists:true};},saveDialog(){return output;}},
    ImportOptions:function(){this.canImportAs=()=>!options.unsupported;},
    ImportAsType:{FOOTAGE:1},FootageItem,
    alert(message){log.alerts.push(message);},
    prompt(){return options.badTemplate?'Missing':'Example';}
  };
  vm.runInNewContext(source, context);
  assert.strictEqual(log.undo,0);
  return {log,rq,oldModule,freshModule,output};
}
for (const opt of ['noProject','busy','collision','cancel','unsupported']) {
  const {log}=run({[opt]:true});assert.strictEqual(log.imported,0);
}
const ok=run();
assert.strictEqual(ok.rq.render,false);
assert.strictEqual(ok.log.reacquired,2);
assert.strictEqual(ok.freshModule.file,ok.output);
assert.strictEqual(ok.oldModule.file,undefined);
assert.deepStrictEqual(ok.log.removed,[]);
for (const opt of ['badTemplate','templateFail'])
  assert.deepStrictEqual(run({[opt]:true}).log.removed,['queue','comp','footage']);
assert.deepStrictEqual(run({layerFail:true,compCleanupFail:true}).log.removed,[]);
assert.deepStrictEqual(run({layerFail:true}).log.removed,['comp','footage']);
console.log('Scripting import/queue portable safety: PASS (not AE execution)');
