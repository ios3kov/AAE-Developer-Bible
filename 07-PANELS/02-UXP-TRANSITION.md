# UXP transition for After Effects

## Published Adobe timeline snapshot

As announced 2026-09-24:
- After Effects UXP public beta: planned by **November 2026**;
- AE/Illustrator/Media Encoder: stop accepting new CEP marketplace submissions and move CEP disabled-by-default together in **December 2028**;
- overall CEP retirement: **end of 2029**.

Timelines can change; re-check Adobe announcement/release docs before product planning.

## What to do before AE UXP beta

1. Separate domain/business logic from CEP APIs.
2. Wrap filesystem/network/storage behind interfaces.
3. Put all `evalScript` calls in one bridge module.
4. Use typed/versioned command payloads.
5. Remove implicit Node globals from core logic.
6. Add contract tests for bridge commands.
7. Maintain UI components with minimal CEP-specific code.

## Migration readiness scorecard

Good:

```text
React/UI → CommandBus → AeBridge interface
                         ├─ CepAeBridge
                         └─ FutureUxpAeBridge
```

Bad:

```text
button onclick → window.cep + fs + evalScript + business rule + DOM mutation
```

## Rule after beta launches

Не мигрировать по announcement alone. Сначала проверить, что AE UXP beta/GA покрывает конкретно ваши requirements: host DOM/API, filesystem, networking, native bridge, packaging, marketplace/distribution.
