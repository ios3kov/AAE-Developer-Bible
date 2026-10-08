# Как компоненты общаются друг с другом и с After Effects

Это центральный архитектурный раздел AE Developer Bible. Он отвечает не только чем вызвать API, но и:

- кто инициирует вызов;
- на каком thread он допустим;
- кто владеет данными;
- что считается transport/application error;
- какой state persistent;
- какой bridge подходит для control plane, а какой — для heavy data.

## Карта

~~~text
                           +-----------------------+
                           |     After Effects     |
                           | project + render host |
                           +----+-------------+----+
                                |             |
                        PF_Cmd  |             | PICA suites / hooks
                                v             v
                         +------+----+   +----+------+
                         |  Effect   |   |   AEGP    |
                         +----+------+   +----+------+
                              |               |
                 generic call |               | publish/acquire suite
                              +-------+-------+
                                      |
                                native bridge

        +-------------+      evalScript      +----------------+
        | CEP/HTML UI | -------------------> | ExtendScript   |
        +------+------+                      +-------+--------+
               |                                     |
               +-------------- CEP events -----------+
                                                     |
                                                     v
                                              AE scripting DOM
~~~

## Выбор канала

| Need | Preferred direction |
|---|---|
| panel changes project | panel → ExtendScript/host panel API |
| AEGP calls one effect instance | AEGP_EffectCallGeneric when appropriate |
| native modules share service | published PICA suite |
| native needs scripting-only capability | AEGP Utility ExecuteScript |
| UI controls heavy native compute | small control protocol; heavy data stays native/helper |
| cross-process helper | explicit versioned IPC |
| ExtendScript to another message-enabled Adobe application | BridgeTalk with explicit target and response contract |

Ни один bridge не должен превращаться в скрытую render dependency.

## ExtendScript между приложениями

**ExtendScript ↔ другая message-enabled application** —
[BridgeTalk: target identity, callback lifecycle и timeout](05-SCRIPT-TO-AE.md#bridgetalk).
BridgeTalk перечисляет и адресует поддерживающие messaging приложения; одно
наличие ExtendScript не подтверждает все interapplication capabilities.
[Source scope](https://github.com/docsforadobe/javascript-tools-guide/blob/ac6839049e17f4652d301e7d28f8f0d3d5fbb66a/docs/interapplication-communication/index.md).

## Control plane vs data plane

~~~text
control:
commands / IDs / state / progress / errors

data:
pixels / audio / large binary buffers / ML tensors
~~~

JSON/evalScript подходит в основном для control plane. Heavy binary data нельзя без причины гонять через string-based bridge.

## Главные инварианты

1. size/version проверяются до payload.
2. Raw host pointers не переживают documented lifetime.
3. Acquire имеет matching release; checkout — checkin; lock — unlock.
4. Host API не считается thread-safe без явного обещания.
5. Transport error и domain error — разные вещи.
6. Async result имеет request/generation ID и может стать stale.
7. Render-affecting state видим dependency/cache model After Effects.
8. Panel DOM не persistent source of truth.
9. Independently shipped components делают version handshake.
10. Undocumented AE internal IPC не stable API.

## Разделы

1. [01-AE-TO-EFFECT.md](01-AE-TO-EFFECT.md)
2. [02-AE-TO-AEGP.md](02-AE-TO-AEGP.md)
3. [03-AEGP-TO-EFFECT.md](03-AEGP-TO-EFFECT.md)
4. [04-PLUGIN-TO-PLUGIN-PICA.md](04-PLUGIN-TO-PLUGIN-PICA.md)
5. [05-SCRIPT-TO-AE.md](05-SCRIPT-TO-AE.md)
6. [06-CEP-TO-EXTENDSCRIPT.md](06-CEP-TO-EXTENDSCRIPT.md)
7. [07-NATIVE-TO-SCRIPT-PANEL.md](07-NATIVE-TO-SCRIPT-PANEL.md)
8. [08-THREADING-BOUNDARIES.md](08-THREADING-BOUNDARIES.md)
9. [09-DATA-OWNERSHIP.md](09-DATA-OWNERSHIP.md)

## Source/verification status

Native bridge chapters 03/04 используют SDK25.6 `AEGP_EffectSuite5`, SPBasicSuite,
SPSuitesSuite и reviewed sample patterns Sweetie/Checkout/ProjDumper/Shifter.
Исторические Suite4 call shapes сохраняются только с compatibility boundary.

См. [source-review record](../18-SDK-HEADER-TOOLS/14-PICA-BRIDGES-LEGACY-SDK25.6.md).

Chapters 05–09 дополнены architecture/lifetime/thread rules. CEP main-thread behavior опирается на Adobe CEP cookbook; AEGP ExecuteScript/idle wake-up details должны всё равно сверяться с headers target SDK перед shipping.

Source review и documentation review не равны host verification.
