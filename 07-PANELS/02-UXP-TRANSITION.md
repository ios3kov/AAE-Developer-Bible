# UXP transition for After Effects

This is a dated migration plan, not an assumption that After Effects already exposes the same UXP API surface as Photoshop, Premiere or Media Encoder.

## Adobe timeline snapshot — 2026-10-01

Adobe's 2026-09-24 developer announcement states:

- After Effects UXP public beta: planned by November 2026;
- AE, Illustrator and Media Encoder stop accepting new CEP Marketplace submissions and move CEP disabled-by-default in December 2028;
- Adobe plans at least two years from a host's UXP public beta before removing CEP from new versions;
- CEP retirement across flagship Creative Cloud desktop apps begins at the end of 2029;
- ExtendScript is not affected by that CEP retirement announcement.

These dates are planning inputs, not immutable API contracts. Re-check Adobe's host-specific UXP documentation before release decisions.

## Published documentation — проверка 2026-10-02

[Официальная AE UXP страница](https://developer.adobe.com/after-effects/uxp/) и [After Effects API Reference](https://developer.adobe.com/after-effects/uxp/after-effects-api/) уже доступны. Старая заметка стороннего KB от апреля 2026 о неналичии этой страницы больше не описывает текущий web state.

| Наблюдение | Что оно позволяет утверждать |
|---|---|
| Announcement: public beta by November 2026 | Датированный план Adobe |
| AE-specific documentation опубликована и содержит Min Version notes | Можно изучать описанные контракты с их member/version boundaries |
| Конкретный host/build действительно исполнил API | Нужен отдельный runtime record; в Bible сейчас NOT RUN |

Наличие страницы не подтверждает GA, доступность beta в пользовательской установке или поддержку всех перечисленных APIs. Landing page сама относит развитие документации к beta. Заимствовать из Premiere/Photoshop пропущенные возможности нельзя. [Область внешнего review](../EXTERNAL-SOURCES-REVIEW-2026-10-02.md) сохранена отдельно.

## Do not assume cross-host parity

A UXP feature existing in Photoshop, Premiere or Media Encoder does not prove that the same API exists in After Effects.

Before migrating a feature, verify AE-specific support for:

- project/items/compositions/layers/properties;
- render queue;
- filesystem;
- networking;
- persistent storage;
- dialogs and panels;
- events and notifications;
- native/hybrid bridge;
- packaging and Marketplace rules.

The beta is evidence only for the APIs the beta actually exposes.

## Architecture before migration

Make the shell replaceable now:

~~~text
UI components
      ↓
Command / domain layer
      ↓
AeBridge interface
   ┌───────────────┐
   │               │
CepAeBridge   FutureUxpAeBridge
   │               │
ExtendScript   AE UXP APIs / supported bridge
~~~

The domain layer should not import window.cep, CSInterface, Node filesystem modules or UXP APIs directly.

## Work to do before AE UXP beta

1. Put every evalScript call behind one bridge.
2. Use versioned command/response payloads.
3. Separate filesystem/network/storage adapters.
4. Remove business logic from DOM event handlers.
5. Keep pure transforms as plain JavaScript data logic where possible.
6. Add contract tests for bridge commands and error envelopes.
7. Inventory every CEP-only capability used by the product.
8. Record performance-sensitive flows that cannot tolerate extra serialization.

This work is useful even if Adobe changes the rollout dates.

## Migration inventory

Maintain a product table:

| Capability | CEP implementation | Required in AE UXP | Blocking? | Verified |
|---|---|---|---|---|
| project edits | ExtendScript dispatcher | project API or supported script bridge | yes | pending |
| filesystem | Node/CEP adapter | AE UXP filesystem path | yes | pending |
| web auth | browser/network adapter | AE UXP network/webview pattern | maybe | pending |
| native compute | helper/native bridge | supported hybrid/native path | yes for heavy tools | pending |

Do not mark a row supported based on generic UXP documentation. Record the exact AE host/version that was tested.

## Hybrid/native products

For products with C++ effects, AEGPs or helpers, the migration is larger than swapping UI widgets.

Keep the contract between UI and native code:

- explicit;
- versioned;
- small;
- independent of CEP DOM types;
- independent of UXP object instances.

A good command protocol can survive multiple panel runtimes.

## After the beta becomes available

Migration sequence:

~~~text
AE UXP beta available
→ inventory required APIs
→ build a thin proof for each blocker
→ compare behavior and performance
→ decide dual-runtime support window
→ package/test clean installs
→ only then migrate production users
~~~

Do not migrate because of the announcement alone. Also do not wait until CEP becomes disabled-by-default before starting proofs.

## Distribution transition

Plan for a period where the product may ship:

- a CEP package for older supported AE versions;
- a UXP package for newer versions;
- the same native plug-in binaries where compatible;
- one product/versioning policy across both shells.

Logs and support reports should identify which shell and protocol version produced the failure.

## Verification boundary

The timeline is based on Adobe's 2026-09-24 announcement; AE-specific published documentation was checked on 2026-10-02. Public beta/GA availability in a concrete installation and host execution were not verified. No runtime capability is marked PASS from publication alone.
