# ExtendScript -> After Effects

ExtendScript выполняется внутри scripting engine AE и работает через scripting DOM (`app`, project, items, comps, layers, properties, renderQueue...).

## Типичный flow

```jsx
app.beginUndoGroup("My Tool");
try {
    var comp = app.project.activeItem;
    if (comp && comp.numLayers > 0) {
        comp.layer(1).name = "Renamed by Tool";
    }
} finally {
    app.endUndoGroup();
}
```

## Main-thread implication

Script execution — host-side operation; длинный script блокирует interactive responsiveness. Делить тяжёлый workflow на небольшие операции, а heavy compute выносить наружу только с ясным protocol/lifetime.

## Script -> menu command

`app.executeCommand(id)` может запускать host command, но numeric command IDs не являются хорошим стабильным public contract между версиями/локалями. Использовать осторожно.

## Native -> script

AEGP Utility Suite имеет `AEGP_ExecuteScript`, поэтому native AEGP может выполнить ExtendScript, когда scripting DOM предоставляет capability, отсутствующую в C API. Это полезный, но синхронный bridge; не превращать его в основное high-frequency IPC.
