# After Effects scripting object model

After Effects scripting exposes the host through an ExtendScript object graph. It is a high-level automation API for project structure, timeline state, properties, import and render queue. It is not the same API surface as Effect or AEGP suites.

## Mental map

~~~text
app
└── project
    ├── items
    │   ├── CompItem
    │   │   └── layers
    │   │       └── PropertyGroup / Property
    │   │           ├── transforms
    │   │           ├── effects
    │   │           ├── masks
    │   │           ├── text animators
    │   │           └── markers / keyframes
    │   ├── FootageItem
    │   └── FolderItem
    └── renderQueue
        └── RenderQueueItem
            └── OutputModule(s)
~~~

## Collections are 1-based

AE scripting collections are not normal JavaScript arrays. Items, layers, render-queue entries and many property groups use indices starting at 1.

~~~jsx
var firstItem = app.project.item(1);
var firstLayer = comp.layer(1);
~~~

Make conversion explicit when code moves between zero-based JavaScript arrays and one-based AE collections.

## Validate type before use

An active item can be absent, a composition, footage or a folder. Never cast by assumption.

~~~jsx
var item = app.project.activeItem;

if (!(item instanceof CompItem)) {
    throw new Error("Open or select a composition first.");
}
~~~

Apply the same rule to layers, footage, output modules and optional properties.

## Stable targeting

Display names may be localized, changed by Adobe or renamed by the user. For effects and properties, prefer stable match-name identifiers where the scripting API exposes them.

~~~jsx
var effects = layer.property("ADBE Effect Parade");
var slider = effects.property("ADBE Slider Control");
~~~

Use visible names for presentation. Do not make them the only machine identity in a production tool.

For product-owned layers or objects, keep your own stable identifier in deliberate project metadata instead of relying only on a layer name such as "Controller".

## Structural mutation can invalidate references

Indexed property groups are a classic scripting trap. Adding, moving or removing children can rebuild a group and invalidate object references saved earlier.

Risky:

~~~jsx
var fx = layer.property("ADBE Effect Parade");
var a = fx.addProperty("ADBE Slider Control");
fx.addProperty("ADBE Color Control");
// saved reference a may no longer be valid
~~~

Safer:

~~~jsx
var fx = layer.property("ADBE Effect Parade");
var a = fx.addProperty("ADBE Slider Control");
var aIndex = a.propertyIndex;

fx.addProperty("ADBE Color Control");

a = fx.property(aIndex); // reacquire after structural mutation
~~~

Treat host objects as host-owned references, not immortal JavaScript objects.

## Undo groups are not database transactions

For user-triggered mutations, group related operations:

~~~jsx
app.beginUndoGroup("Build Rig");

try {
    // validate, then mutate
} finally {
    app.endUndoGroup();
}
~~~

This gives the user coherent undo history. It does not mean an exception automatically rolls the project back.

If partial mutation is unacceptable:

1. validate prerequisites before the first edit;
2. collect errors before running a batch;
3. create resources in a controlled order;
4. explicitly clean up product-owned resources on failure where possible.

Put undo ownership at the command boundary instead of opening nested undo groups in low-level helpers.

## Defensive scripting checklist

Before a destructive or cast-like assumption, verify:

- app.project exists;
- active item exists and is the expected type;
- layer/property index is in range;
- property/effect exists;
- canSetExpression, canVaryOverTime, canAddProperty or another capability is true when relevant;
- input file exists before import/read;
- project has a path before code depends on project.file;
- output directory exists and is writable;
- render-queue references are reacquired after structural changes when required;
- cancel leaves the project in a deliberate state.

For batch tools, validate as much as possible before the first project mutation.

## Command layer instead of UI-driven scripting

Do not bury the entire product in a button callback.

Prefer:

~~~text
UI event
  -> validate plain command
  -> command/service function
  -> AE scripting DOM
  -> normalize plain result
  -> UI renders result
~~~

The command function should remain callable from ScriptUI, CEP, a JSX harness or a future UXP adapter without rewriting the operation.

## Long operations

Host-side ExtendScript can block interactive work. Avoid one giant call that performs expensive file parsing, networking or computation and then mutates the project.

Split work into:

1. pure/external computation where practical;
2. short host mutations;
3. explicit progress and cancellation checkpoints for genuinely long jobs.

When CEP invokes ExtendScript through evalScript, the host-side script runs on the host main thread. A long script call can starve both AE interaction and CEP event scheduling.

## Version gates

New scripting methods arrive in specific AE versions. Prefer feature detection where possible.

~~~jsx
if (typeof someObject.someNewMethod === "function") {
    someObject.someNewMethod();
} else {
    // supported fallback or clear compatibility error
}
~~~

Use app.version only when behavior cannot be detected directly.

A compatibility statement should name AE versions actually tested, not merely versions whose API documentation contains the method.

## Boundary with expressions

Scripts mutate project state and perform automation. Expressions are evaluated as part of property evaluation and should not be used as a substitute for project orchestration.

See:

- 03-EXPRESSIONS-VS-SCRIPTS.md
- ../15-COMMUNICATION/05-SCRIPT-TO-AE.md

## Verification boundary

This chapter is documentation of the public scripting model and safe architecture patterns. It does not claim that every fragment has been executed in every supported AE version. Host execution remains a separate acceptance gate.
