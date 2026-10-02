# CEP development

CEP is Adobe's legacy HTML/CSS/JavaScript extension runtime for Creative Cloud desktop hosts. In After Effects it remains a practical production panel technology in October 2026, but Adobe has announced a phased transition to UXP.

The correct architecture is neither "rewrite everything immediately" nor "assume CEP will live forever". Keep the shell replaceable.

## Runtime model

A CEP extension has two JavaScript worlds:

~~~text
CEP HTML/JS engine
    |
    | CSInterface.evalScript(...)
    v
host ExtendScript engine
    |
    v
After Effects scripting DOM
~~~

The CEP browser DOM is not the AE scripting DOM. The host scripting engine is reached through the CEP bridge.

## Core bundle

Typical source layout:

~~~text
MyPanel/
├── CSXS/
│   └── manifest.xml
├── index.html
├── js/
│   ├── CSInterface.js
│   ├── bridge.js
│   └── app.js
├── css/
└── jsx/
    ├── bootstrap.jsx
    └── dispatcher.jsx
~~~

After Effects host ID in CEP manifests is AEFT.

Keep bridge.js and dispatcher.jsx small and explicit. Business logic should not be scattered across DOM handlers and executable evalScript strings.

## Сверка manifest и bootstrap по первоисточнику

Не смешивайте версии: `ExtensionManifest Version` описывает schema, `HostList` — целевой AE, `RequiredRuntime Name="CSXS"` — CEP runtime; product version задаётся отдельно. [CEP 12 Cookbook](https://github.com/Adobe-CEP/CEP-Resources/blob/ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6/CEP_12.x/Documentation/CEP%2012%20HTML%20Extension%20Cookbook.md) сопоставляет `AEFT` 25.0 с CEP 12, но содержит и старые manifest examples. Их числа не являются готовой support matrix вашего продукта.

Проверяйте по слоям:

1. Manifest допускает нужный host/runtime и содержит путь к HTML entry.
2. HTML загружает подходящий `CSInterface.js`; `Vulcan.js` нужен при использовании его API. `CEPEngine_extensions.js` встроен в CEP engine, подключать копию как обычный HTML script не требуется.
3. Host JSX загружен через manifest `ScriptPath` либо явный `evalScript`/`$.evalFile` bootstrap; путь относится к фактической установленной extension.
4. Малый read-only вызов подтверждает достижимость dispatcher; только после этого проверяется command protocol.

Источники: тот же Cookbook и [Adobe CEP README](https://github.com/Adobe-CEP/CEP-Resources/blob/ab5e4e3e53a42fad08e1225a22a991bb1ffe73f6/README.md), проверены **2026-10-02**. Здесь описан diagnostic workflow без заявления о установленной extension. JSON/polyfill bootstrap и контролируемые protocol failures остаются отдельной задачей [блока 2](../COMPLETION-PLAN.md).

## Panel -> AE

CEP uses CSInterface.evalScript to execute ExtendScript in the host.

A production panel should centralize that bridge and send structured commands rather than constructing ad-hoc script text throughout the UI.

Never concatenate user input directly into executable ExtendScript.

## AE -> panel

ExtendScript cannot directly manipulate the CEP HTML DOM. CEP events provide the normal notification mechanism.

Conceptually:

~~~text
ExtendScript/native side
    -> CSXS / PlugPlug event
    -> CSInterface.addEventListener(...)
    -> panel state update
~~~

Use events for small notifications and invalidation. If a large state snapshot is required, notify once and request the normalized state rather than emitting hundreds of tiny mutation events.

## Main-thread boundary

Adobe's CEP 12 cookbook documents that scripts invoked by evalScript run in the host application's ExtendScript engine on the host main thread. CEP events also depend on host main-thread scheduling.

Consequences:

- do not make one enormous evalScript request;
- do not poll AE dozens of times per animation frame;
- batch related reads and writes;
- keep large binary or CPU-heavy data out of string-based JSX messaging;
- split long host work into meaningful chunks;
- return compact structured results.

The callback is asynchronous from the panel API perspective. The host operation itself is still host-side synchronous scripting.

## Extension folders

macOS system:

    /Library/Application Support/Adobe/CEP/extensions

macOS user:

    ~/Library/Application Support/Adobe/CEP/extensions

Windows system:

    C:\Program Files (x86)\Common Files\Adobe\CEP\extensions

Windows user:

    %AppData%\Roaming\Adobe\CEP\extensions

These are CEP extension locations, not native .plugin/.aex locations.

## Unsigned development mode

CEP development commonly uses PlayerDebugMode under the matching CSXS major-version preference or registry key.

Do not copy a random CSXS.9, CSXS.11 or CSXS.12 command from an old tutorial. The key must match the CEP runtime used by the host under test.

Debug mode is a development convenience, not a shipping trust model.

## Debugging layers

Useful layers:

1. browser devtools for HTML/JS;
2. .debug host/port configuration where applicable;
3. CSXS / CEP logs;
4. ExtendScript-side error envelope and logging;
5. AE host behavior.

A blank panel can result from manifest mismatch, CEP runtime policy, JS startup failure, missing JSX or a broken bridge. Debug the layers independently.

## Packaging

Adobe's CEP resources include ZXPSignCMD and ZXP packaging/signing documentation.

A release pipeline should distinguish source from the signed artifact:

~~~text
source
→ production build
→ manifest/version validation
→ package
→ sign
→ clean install test
→ archive checksums
~~~

Do not modify a signed package after signing.

## Security

Treat the panel UI as an input boundary.

- validate messages crossing UI -> JSX/native;
- never concatenate remote/user text into executable source;
- never eval downloaded code;
- allowlist helper/native commands;
- normalize and validate paths;
- keep secrets out of frontend source;
- define network policy;
- treat downloaded code differently from downloaded data.

Node/CEF capabilities vary by CEP runtime and configuration. Core business logic should not depend on an accidental global that exists in only one host/runtime combination.

## Production protocol

Request example:

~~~json
{
  "protocol": 1,
  "requestId": "42",
  "command": "renameSelected",
  "payload": {"name": "Hero"}
}
~~~

Success:

~~~json
{
  "ok": true,
  "requestId": "42",
  "result": {"changed": 3}
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

Localized human text must not be the only machine-readable error contract.

## Transition status — 2026-10-01

Adobe announced on 2026-09-24 that:

- After Effects UXP public beta is planned by November 2026;
- new CEP Marketplace submissions for AE stop and CEP becomes disabled-by-default in December 2028;
- CEP retirement across flagship Creative Cloud desktop apps begins at the end of 2029;
- ExtendScript itself is not part of that CEP retirement announcement.

Therefore the correct 2026 strategy is to isolate CEP-specific code so the shell can be replaced when the actual After Effects UXP API surface is available and verified.

See:

- 02-UXP-TRANSITION.md
- ../15-COMMUNICATION/06-CEP-TO-EXTENDSCRIPT.md

## Verification boundary

CEP architecture and the dated migration plan are source-reviewed. This Bible does not yet claim a CEP panel host run across the full support matrix.
