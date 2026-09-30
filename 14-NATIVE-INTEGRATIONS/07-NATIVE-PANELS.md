# Native dockable panels

AEGP может создать панель, которая dock/resize ведёт себя как стандартные панели AE. SDK sample **Panelator** демонстрирует этот путь.

## Когда native panel оправдана

- нужна tight native integration;
- нужен C++ UI/rendering path без browser runtime;
- UI маленький, специализированный и долгоживущий;
- команда готова поддерживать platform-specific windowing/painting lifecycle.

## Когда не нужна

Для обычного продуктового panel UX это значительно дороже, чем HTML panel. В 2026 для уже выпускаемого AE panel UI практический production путь остаётся CEP с архитектурой, готовой к UXP migration.

## Архитектура

```text
Native panel callback
     |
     +--> local UI state
     |
     +--> AEGP suites (main thread)
     |
     +--> pure C++ core (can be separated)
```

Нельзя обращаться к project model из произвольного worker thread только потому, что UI написан на C++.
