# Threading boundaries

## Effect render

Effect render callbacks могут выполняться concurrent при MFR. Render code должен быть re-entrant; immutable shared resources preferable.

## Pixel iteration

Host iteration suites могут сами распараллеливать pixel callback. Pixel callback не должен зависеть от iteration order и должен быть re-entrant.

## AEGP

Считать AEGP project manipulation main-thread-only. Документация прямо предупреждает, что AEGP в целом не предоставляет обычную threading model; единственные thread-safe исключения должны быть явно документированы.

## CEP / ExtendScript

`evalScript` исполняет ExtendScript на host side; длинные script calls блокируют host scheduling. Разбивать работу.

## Golden rule

```text
worker thread:
  pure math / decode / encode / ML / filesystem / network

host callback thread:
  touch AE handles / project model / UI / suites unless specifically documented safe
```
