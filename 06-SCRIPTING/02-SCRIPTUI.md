# ScriptUI

Практический command layer: [demo rig](../16-WORKING-TEMPLATES/jsx-tool/build-demo-rig.jsx).
UI вызывает reusable operation, а не копирует host mutations в каждый handler.
Для long batch progress обновляется между bounded chunks; Cancel запрещает новые
chunks, не обещает rollback. Каждая chunk повторно проверяет project/target и
generation; закрытая Panel не получает late update. Dockable Panel и floating
Window имеют разные show/layout пути; scripted command не должен зависеть от них.

ScriptUI is the ExtendScript UI toolkit used for dialogs, palettes and classic script panels. It remains useful when the product is mainly AE automation and does not require a modern web-style application shell.

## Use when

- UI is small or medium;
- the tool is mostly scripting automation;
- minimal packaging matters;
- a dialog, palette or simple dockable panel is enough;
- classic controls and layout are acceptable.

## Avoid when

- complex virtualized lists or grids;
- account, browser or web workflows;
- modern responsive UI;
- large application state;
- heavy asynchronous networking;
- a product is already structured as a full panel application.

For those cases use a panel runtime and keep ScriptUI for small utilities.

## Dialog, palette and dockable panel

Common standalone windows:

~~~jsx
var dlg = new Window("dialog", "My Tool");
~~~

~~~jsx
var win = new Window("palette", "My Tool", undefined, { resizeable: true });
~~~

A reusable dockable ScriptUI panel should allow the same builder to receive either a host-provided Panel or create a Window.

~~~jsx
function buildUI(thisObj) {
    var root = (thisObj instanceof Panel)
        ? thisObj
        : new Window("palette", "My Tool", undefined, { resizeable: true });

    // create controls on root
    return root;
}
~~~

Keep UI construction separate from After Effects operations.

## Layout discipline

Prefer ScriptUI layout managers to hard-coded pixel coordinates.

Typical hierarchy:

~~~text
root
└── group(column)
    ├── group(row): inputs
    ├── status / progress
    └── group(row): actions
~~~

For resizable panels, use layout resize handling rather than manually repositioning every control.

Do not assume fonts, DPI, control metrics or platform rendering are identical on macOS and Windows.

## Architecture

Even a small script should separate:

~~~text
ScriptUI callbacks
    ↓
commands
    ↓
validation + AE scripting DOM
    ↓
plain result object
    ↓
render status in UI
~~~

Bad architecture is a 300-line button callback containing project traversal, file I/O, mutation, error dialogs and UI updates.

Better:

~~~jsx
button.onClick = function () {
    var result = Commands.buildRig(readForm());
    renderResult(result);
};
~~~

This separation makes later migration to CEP or UXP much cheaper.

## Long-running work

ScriptUI does not turn ExtendScript into a worker-thread environment. A long synchronous loop freezes the tool and can make AE appear hung.

For long jobs:

- validate before starting;
- update progress at sensible intervals;
- expose a cancel flag where the workflow allows it;
- chunk work instead of repainting on every item;
- move CPU-heavy independent work outside ExtendScript when that fits the product architecture.

app.scheduleTask can help defer or chunk script work, but it is a scheduling primitive, not a general concurrency model. It also introduces lifecycle and global-state concerns because scheduled code must remain resolvable later.

## Errors and cleanup

UI callbacks must not leave controls permanently disabled after an exception.

~~~jsx
button.enabled = false;

try {
    var result = Commands.run();
    status.text = result.message;
} catch (e) {
    status.text = "Error: " + e.toString();
} finally {
    button.enabled = true;
}
~~~

For batch tools, prefer a status area or aggregated error report over an alert for every recoverable validation issue.

## Persistence

Do not make transient widget state the only source of truth for important product state.

Separate:

- UI state: selected tab, temporary text, expanded sections;
- project state: data that legitimately belongs in the AE project;
- user preferences: explicit settings layer;
- secrets or licensing credentials: never embedded in JSX source.

## Migration rule

A ScriptUI tool is migration-ready when its AE operations can run without ScriptUI objects being present.

If command functions accept plain input and return plain output, the same command layer can later sit behind:

- a CEP evalScript dispatcher;
- a JSX test harness;
- a future UXP or other host adapter.

## Verification boundary

This chapter documents architecture and common ScriptUI patterns. Exact layout and event behavior is host/platform dependent and must be verified on the AE/OS versions claimed by the product.
