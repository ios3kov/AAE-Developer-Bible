# Panels: CEP now, UXP next

## Status — 2026-09-30

Adobe объявила UXP для After Effects 24 сентября 2026. Public beta для AE запланирована **к ноябрю 2026**.

CEP остаётся используемым сейчас, но Adobe объявила multi-year transition и retirement CEP к концу 2029.

## Strategy

Новый panel product, который должен выйти до зрелого UXP AE API:

```text
UI shell (CEP today)
       ↓
App services / commands  ← framework-agnostic
       ↓
AE bridge adapter (ExtendScript/native)
       ↓
After Effects
```

UXP migration тогда меняет shell/bridge, а не весь продукт.

## Do not

- завязывать domain model на `window.cep`;
- раскидывать `evalScript()` по UI components;
- хранить единственный source of truth в DOM;
- делать direct filesystem/network access частью business logic без adapter abstraction.
