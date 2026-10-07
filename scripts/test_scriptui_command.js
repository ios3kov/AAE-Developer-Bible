// Fake-host control-flow tests only; not ScriptUI rendering or AE execution.
const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const source = fs.readFileSync(path.join(__dirname,
  '../20-REFERENCE-IMPLEMENTATIONS/Scripts/ScriptUI-Panel/AEDeveloperBiblePanel.jsx'), 'utf8');
function run(options = {}) {
  const log = {begin:0, end:0, writes:0, layout:0};
  const controls = [];
  function Panel() {}
  function Window() {
    this.layout = {layout(){log.layout++;}, resize(){}};
    this.center = this.show = function() {};
    this.add = function(type, unused, text) {
      const control = {text, enabled:true, add:this.add};
      controls.push({type, control}); return control;
    };
  }
  function CompItem() {}
  const comp = new CompItem();
  const layers = [0,1,2].map((index) => {
    const layer = {};
    Object.defineProperty(layer, 'name', {set(value) {
      if (options.writeFail && index === 1) throw Error('write failed');
      log.writes++; layer.current = value;
    }}); return layer;
  });
  comp.selectedLayers = options.empty ? [] : layers;
  const project = {activeItem:options.wrongType ? {} : comp,
    renderQueue:{rendering:!!options.busy}};
  const app = {project:options.noProject ? null : project,
    beginUndoGroup(){log.begin++; if(options.beginFail)throw Error('begin failed');},
    endUndoGroup(){log.end++; if(options.endFail)throw Error('end failed');}};
  vm.runInNewContext(source, {app, CompItem, Panel, Window});
  const button = controls.find(x => x.type === 'button').control;
  const status = controls.find(x => x.type === 'statictext').control;
  button.onClick();
  assert.strictEqual(button.enabled, true);
  assert.strictEqual(log.layout, 1);
  return {log, status, layers};
}
for (const option of ['noProject','wrongType','busy','empty']) {
  const {log}=run({[option]:true});
  assert.strictEqual(log.begin,0); assert.strictEqual(log.writes,0);
}
const success=run();
assert.strictEqual(success.log.writes,3); assert.strictEqual(success.log.end,1);
assert.strictEqual(success.status.text,'Renamed 3/3 layer(s)');
assert.deepStrictEqual(success.layers.map(x=>x.current),['Layer_1','Layer_2','Layer_3']);
const partial=run({writeFail:true});
assert.strictEqual(partial.log.writes,1); assert.strictEqual(partial.log.end,1);
assert.match(partial.status.text,/Stopped after 1\/3.*write failed/);
const begin=run({beginFail:true});
assert.strictEqual(begin.log.end,0); assert.strictEqual(begin.log.writes,0);
const end=run({endFail:true});
assert.strictEqual(end.log.writes,3); assert.match(end.status.text,/Stopped after 3\/3.*Undo close/);
console.log('ScriptUI rename command portable safety: 8 scenarios PASS (not AE execution)');
