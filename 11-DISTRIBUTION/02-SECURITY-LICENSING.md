# Security and licensing architecture

## Principle

Licensing code не должен ухудшать host stability.

## Never in render hot path

Не делать на каждый frame:
- network license call;
- filesystem license scan;
- crypto-heavy handshake;
- UI dialog;
- blocking mutex around licensing state.

License state должен быть resolved/cached безопасно вне hot loop.

## Offline behavior

Заранее определить:
- offline grace;
- machine changes;
- clock changes;
- server unavailable;
- license revoked;
- render farm / headless policy.

## Secrets

Клиентский plug-in нельзя считать secret storage. Любой embedded secret потенциально извлекаем.

Не помещать server master keys/API admin secrets в binary/panel.

## Tamper resistance

Obfuscation/anti-debugging не должна ломать AE, crash diagnostics или легальных пользователей. Stability важнее агрессивной защиты.
