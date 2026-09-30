# BlitHook

BlitHook получает frames, когда они выводятся/«blit»-ятся в Composition panel.

## Mental model

```text
render/cache -> AE display pipeline -> Composition panel
                                |
                                +--> BlitHook
```

Он полезен для external display / monitoring / frame consumer behavior.

## Не путать

- не Effect: не участвует в обычном per-layer effect stack;
- не AEIO: не декодирует/кодирует media file format;
- не Artisan: не становится 3D renderer;
- не Render Queue replacement.

## Performance rule

Display callback нельзя блокировать тяжёлой синхронной работой. Если frame надо отправить наружу, копировать/queue минимально необходимое и отдавать тяжёлую работу worker/service с корректным lifetime management.
