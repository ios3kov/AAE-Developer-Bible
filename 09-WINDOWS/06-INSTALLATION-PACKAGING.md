# Windows — installation and packaging

## Adobe common install path

After Effects SDK Guide рекомендует installer'у получать common plug-in path из registry, например family key:

```text
HKLM\SOFTWARE\Adobe\After Effects\[version]\CommonPluginInstallPath
```

AE-specific path также доступен через соответствующий Adobe registry value.

Не полагаться только на hardcoded `C:\Program Files\...` в production installer.

## Installer technology

Подойдут, в зависимости от продукта:
- MSI/WiX;
- signed bootstrapper;
- Inno Setup/другая зрелая installer system.

Technology менее важна, чем корректные upgrade/uninstall/signing semantics.

## Installer tests

- fresh install;
- upgrade N-1 → N;
- downgrade policy;
- repair;
- uninstall;
- multiple AE versions installed;
- no AE installed;
- no admin rights;
- x64/ARM64 architecture selection;
- antivirus/SmartScreen behavior;
- long/Unicode user/profile paths where applicable.
