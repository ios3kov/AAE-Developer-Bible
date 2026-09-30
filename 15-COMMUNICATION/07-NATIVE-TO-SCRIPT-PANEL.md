# Native <-> script/panel: как собирать гибридный продукт

## Рекомендуемая layered architecture

```text
UI layer
  CEP now / UXP later
       |
       | commands + JSON
       v
Automation layer
  ExtendScript dispatcher
       |
       +---- simple project edits ----> AE scripting DOM
       |
       +---- invoke native behavior --> effect params / menu / file IPC

Native layer
  Effect plug-in / AEGP service
       |
       +---- PICA suites ---> AE C++ APIs
       +---- shared suite --> other native modules
```

## Когда нужен AEGP bridge

Если panel должен часто обращаться к high-performance native core, не заставлять ExtendScript сериализовать большие pixel/binary datasets. Panel отправляет control command; native core хранит/обрабатывает heavy data.

## IPC наружу

Когда UI/native/service находятся в разных processes, использовать явный versioned IPC:

- localhost socket / named pipe / Unix domain socket;
- child process stdin/stdout protocol;
- temporary file + atomic rename для больших batch payloads;
- shared memory только после profiling и с explicit ownership.

Нельзя считать undocumented AE internal IPC стабильным API.
