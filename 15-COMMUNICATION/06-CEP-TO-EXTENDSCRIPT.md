# CEP panel <-> ExtendScript

На production AE 26.5 CEP остаётся рабочим panel runtime; UXP announced, но AE public beta заявлена позже 2026.

## HTML/JS -> AE

Основной bridge:

```js
const cs = new CSInterface();
cs.evalScript('$._myTool.renameSelected()', function(result) {
  console.log(result);
});
```

Вызванный код выполняется в ExtendScript engine host application.

## AE/ExtendScript -> panel

CEP events / CSXS events:

```text
ExtendScript/native side -> event dispatch -> CSInterface.addEventListener(...) -> panel JS
```

CEP также поддерживает `dispatchEvent/addEventListener` между extensions; native point product communication uses PlugPlug event infrastructure where host supports it.

## Production protocol

Не строить API из строк-конкатенаций типа:

```js
cs.evalScript('doThing("' + userText + '")');
```

Вместо этого сериализовать JSON, escape один раз и иметь одну dispatcher function:

```js
cs.evalScript('$._myTool.dispatch(' + JSON.stringify(JSON.stringify(msg)) + ')', cb);
```

ExtendScript разбирает JSON и возвращает JSON envelope.

## Response envelope

```json
{"ok":true,"requestId":"42","result":{"changed":3}}
```

или

```json
{"ok":false,"requestId":"42","error":{"code":"NO_COMP","message":"No active comp"}}
```

См. `16-WORKING-TEMPLATES/cep-panel-bridge/`.
