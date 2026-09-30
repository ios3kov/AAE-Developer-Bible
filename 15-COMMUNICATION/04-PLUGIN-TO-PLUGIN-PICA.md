# Plug-in -> Plug-in через published PICA suite

Если несколько native modules должны использовать общую службу, предпочтительный in-process contract — versioned suite.

## Provider

AEGP/native provider публикует структуру function pointers под стабильным suite name/version.

## Consumer

Effect/AEGP делает `AcquireSuite(name, version, ...)`, вызывает функции и `ReleaseSuite`.

## ABI rules

- C-compatible structs/function pointers;
- fixed-width primitive types where possible;
- caller-owned / callee-owned memory documented explicitly;
- no C++ exceptions across boundary;
- no STL types across boundary;
- version every incompatible change;
- old suite version сохранять, пока поддерживаются старые consumers.

## Failure mode

Consumer обязан нормально переживать `suite unavailable`: disable optional feature или показать понятную ошибку, а не dereference null pointer.
