# After Effects scripting object model

Mental map:

```text
app
└── project
    ├── items
    │   ├── CompItem
    │   │   └── layers
    │   │       └── properties / effects / masks / markers
    │   ├── FootageItem
    │   └── FolderItem
    └── renderQueue
        └── RenderQueueItem
            └── OutputModule(s)
```

## Stable targeting

UI display names могут быть локализованы/переименованы. Для effects/properties, где API предоставляет match-name semantics, предпочитать стабильный programmatic identifier.

## Defensive scripting

Перед каждым cast-like assumption:
- item exists?;
- type expected?;
- layer index valid?;
- property exists?;
- canSetExpression/canVaryOverTime etc. если применимо?;
- project saved, если требуется path?

## Version gates

Новые scripting methods появляются в конкретных AE versions. Если продукт заявляет старый AE, feature detection/version gate обязателен.
