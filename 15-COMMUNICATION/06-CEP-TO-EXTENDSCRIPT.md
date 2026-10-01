# CEP panel <-> ExtendScript

CEP has two separate JavaScript environments:

~~~text
CEP HTML/JS runtime
        |
        | CSInterface.evalScript(script, callback)
        v
After Effects ExtendScript engine
        |
        v
AE scripting DOM
~~~

The panel cannot directly use app.project, and ExtendScript cannot directly manipulate the panel's HTML DOM.

## Panel -> AE

The fundamental bridge is CSInterface.evalScript.

Simple form:

~~~js
var cs = new CSInterface();

cs.evalScript('$._myTool.ping()', function (result) {
    console.log(result);
});
~~~

A production product should not create different executable script strings throughout the UI.

Bad:

~~~js
cs.evalScript('doThing("' + userText + '")');
~~~

Quotes, backslashes and attacker-controlled text can turn data into source code.

## One dispatcher

Centralize bridge calls:

~~~js
function callAe(message, done) {
    var json = JSON.stringify(message);
    var arg = JSON.stringify(json);

    cs.evalScript('$._myTool.dispatch(' + arg + ')', function (raw) {
        done(raw);
    });
}
~~~

ExtendScript side:

~~~jsx
$._myTool = $._myTool || {};

$._myTool.dispatch = function (raw) {
    var request = null;

    try {
        request = JSON.parse(raw);
        return JSON.stringify(Dispatcher.handle(request));
    } catch (e) {
        return JSON.stringify({
            ok: false,
            requestId: request && request.requestId,
            error: {
                code: "UNHANDLED",
                message: e.toString()
            }
        });
    }
};
~~~

Keep dispatch separate from actual command implementations.

## Request contract

~~~json
{
  "protocol": 1,
  "requestId": "42",
  "command": "renameSelected",
  "payload": {
    "name": "Hero"
  }
}
~~~

Validate:

- protocol version;
- command allowlist;
- required payload fields;
- string/number ranges;
- file path policy;
- maximum payload size where appropriate.

Unknown commands must fail closed.

## Response envelope

Success:

~~~json
{
  "ok": true,
  "requestId": "42",
  "result": {
    "changed": 3
  }
}
~~~

Failure:

~~~json
{
  "ok": false,
  "requestId": "42",
  "error": {
    "code": "NO_COMP",
    "message": "No active composition"
  }
}
~~~

An empty, malformed or non-JSON callback result is a transport/protocol failure, not a successful command that returned "nothing".

## Main-thread scheduling

Adobe's CEP 12 cookbook states that evalScript and manifest ScriptPath JSX execute in the host application's ExtendScript engine on the host main thread. It also notes that CEP events depend on host main-thread scheduling.

Therefore:

- avoid long single evalScript calls;
- do not call evalScript on every UI repaint;
- batch related reads and writes;
- split long jobs into explicit chunks;
- keep pure CPU work in the panel/helper where appropriate;
- keep large binary data out of the JSX string bridge.

The callback is asynchronous from the CEP JavaScript API perspective. The host-side work is still a synchronous script operation.

## AE / ExtendScript -> panel

ExtendScript cannot access the CEP browser DOM directly. Use CEP/CSXS events when host-side code needs to notify the panel.

Conceptual flow:

~~~text
ExtendScript/native source
→ CSXS / PlugPlug event
→ CEP event bus
→ CSInterface.addEventListener(...)
→ panel reducer/state update
~~~

Prefer events as invalidation signals.

Good:

~~~json
{
  "protocol": 1,
  "type": "selectionChanged",
  "revision": 183
}
~~~

The panel then requests one normalized state snapshot.

Avoid sending hundreds of tiny mutation events whose correctness depends on timing/order.

## Request IDs and stale replies

Rapid UI interaction can create overlapping requests.

Track:

- request ID;
- project/context revision;
- panel instance lifetime;
- expected protocol version.

If the user changes context before a late callback returns, ignore the stale response instead of painting old state into the new UI.

## File paths

CEP JavaScript, ExtendScript and the OS may represent paths differently.

At the boundary:

- define whether the protocol carries native paths or file URIs;
- normalize in one adapter;
- validate before touching disk;
- reject traversal when a command should remain inside a product-owned directory;
- test Unicode and long paths.

Do not scatter path conversion through every command.

## Large data

Do not send frames, large binary caches or megabytes of analysis through repeated evalScript strings.

For large payloads use a deliberate data plane:

- product-owned file plus atomic completion/rename;
- external helper protocol;
- native storage/cache;
- another supported IPC path.

CEP/JSX should remain the control plane.

## Timeouts and lifecycle

evalScript does not provide a complete request timeout/cancellation model by itself.

A bridge layer should track:

- request start time;
- whether the panel is still alive;
- whether a late callback may be ignored;
- protocol version;
- expected response schema.

Timeout in the UI does not mean the host-side operation was magically cancelled. Design cancellation separately.

## Security

Treat every bridge message as untrusted input.

Never:

- concatenate user/remote strings into executable JSX;
- expose "run arbitrary JSX" as a production API;
- dispatch command names without an allowlist;
- accept arbitrary helper executable paths;
- write secrets into bridge logs.

## Debugging order

When a command fails:

1. confirm the panel handler ran;
2. log request ID and command without secrets;
3. confirm the evalScript callback fired;
4. validate returned JSON;
5. inspect the ExtendScript error code/message;
6. reproduce the dispatcher command in a tiny JSX harness;
7. only then debug the larger UI.

This separates browser, bridge and AE failures.

## Reference implementation

See 16-WORKING-TEMPLATES/cep-panel-bridge/.

Its existence is implementation evidence, not host verification. Release-quality acceptance still needs installation, panel open/reload, success/failure commands, host restart and clean uninstall on the supported matrix.
