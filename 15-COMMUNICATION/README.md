# Как компоненты общаются друг с другом и с After Effects

Это центральный раздел архитектуры AE Developer Bible.

## Карта

```text
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
```

## Разделы

- [`01-AE-TO-EFFECT.md`](01-AE-TO-EFFECT.md)
- [`02-AE-TO-AEGP.md`](02-AE-TO-AEGP.md)
- [`03-AEGP-TO-EFFECT.md`](03-AEGP-TO-EFFECT.md)
- [`04-PLUGIN-TO-PLUGIN-PICA.md`](04-PLUGIN-TO-PLUGIN-PICA.md)
- [`05-SCRIPT-TO-AE.md`](05-SCRIPT-TO-AE.md)
- [`06-CEP-TO-EXTENDSCRIPT.md`](06-CEP-TO-EXTENDSCRIPT.md)
- [`07-NATIVE-TO-SCRIPT-PANEL.md`](07-NATIVE-TO-SCRIPT-PANEL.md)
- [`08-THREADING-BOUNDARIES.md`](08-THREADING-BOUNDARIES.md)
- [`09-DATA-OWNERSHIP.md`](09-DATA-OWNERSHIP.md)
