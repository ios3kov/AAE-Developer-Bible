# AEGP tools — native automation and deep AE integration

AEGP — основной C++ путь для инструментов, которые работают **с проектом**, а не только с пикселями одного эффекта.

## Что AEGP умеет

- создавать/открывать/сохранять project-level structures;
- читать/создавать compositions и project items;
- добавлять/удалять/переупорядочивать layers;
- работать с footage;
- находить и добавлять effects;
- читать/писать property streams;
- keyframes, markers, masks;
- text data;
- render queue, output modules, render options;
- preferences/persistent data;
- menu commands + command hooks;
- idle/death hooks;
- запускать ExtendScript через `AEGP_ExecuteScript`;
- получать rendered frames через Render suites;
- регистрировать специализированные AEIO/Artisan modules;
- публиковать собственные suites.

## Menu tool pattern

```text
EntryPoint
  -> GetUniqueCommand
  -> InsertMenuCommand
  -> RegisterCommandHook
  -> RegisterUpdateMenuHook

User opens menu
  -> UpdateMenuHook: enable/disable

User clicks
  -> CommandHook
     -> StartUndoGroup
     -> query selection/project
     -> mutate project
     -> EndUndoGroup
```

## UI-thread rule

AEGP не является general multithreaded API. Проектные изменения выполняются из host callback/main thread. Для фоновой тяжёлой работы отделяйте pure compute от AE handles, а commit обратно в AE делайте в разрешённом host callback.

## Native tool examples by capability

| Продуктовая задача | AEGP suites/pattern |
|---|---|
| Batch rename layers | Collection + Layer + Stream + Undo |
| Add keyframes | Stream + Keyframe |
| Build comp from files | Project + Footage + Comp + Layer |
| Render queue manager | Render Queue + RQ Item + Output Module |
| Replace footage | Footage suite |
| Inspect installed effects | Effect suite |
| Run helper JSX | Utility `AEGP_ExecuteScript` |
| Native menu action | Command + Register |
| Native service for several plugins | publish PICA suite |

См. рабочий drop-in шаблон: `16-WORKING-TEMPLATES/aegp-menu-command/`.
