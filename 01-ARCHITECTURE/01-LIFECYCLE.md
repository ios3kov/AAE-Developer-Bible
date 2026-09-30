# Native plug-in lifecycle

## Effect plug-in mental model

After Effects владеет циклом вызовов. Plug-in предоставляет entry point. Host вызывает его с command selector, входными структурами, параметрами, output и дополнительными данными.

Основные фазы, которые надо мыслить раздельно:

1. **Global setup** — capabilities/flags, global allocation.
2. **Params setup** — объявление параметров.
3. **Sequence lifecycle** — state конкретного instance эффекта.
4. **Frame/render lifecycle** — setup/render/setdown конкретного кадра.
5. **UI/event commands** — отдельный event path.
6. **Global setdown** — освобождение global resources.

## Rule: state ownership

Для каждого объекта/буфера должно быть понятно:

- кто создаёт;
- кто уничтожает;
- можно ли хранить между callbacks;
- кто может обращаться concurrently;
- что происходит при duplicate/project reload;
- нужна ли serialization/flattening.

Если этого нет в design doc, баг уже заложен.

## Host boundary

Entry points и callbacks — ABI boundary. На нём:

- не пропускать C++ exceptions;
- не возвращать dangling pointers;
- переводить внутренние ошибки в корректный SDK error;
- минимизировать работу, не относящуюся к текущему command;
- логировать command + instance/frame identity в debug builds.

## AEGP mental model

AEGP после входной регистрации работает через hooks и PICA suites. Здесь важнее lifetime opaque handles и invalidation после операций host-а.

## Versioned suites

Suite acquisition — это capability check. Не считать, что функция есть только потому, что header компилируется.

Design pattern:

```text
acquire required suite version
  ├─ success → use
  └─ unavailable → fallback or explicit unsupported error
release suite
```

## What not to cache

Нельзя бездумно кэшировать:
- host opaque handles, если docs говорят об invalidation;
- frame-local worlds;
- pointers inside temporary suite-returned structures;
- render-context-specific data вне render context.
