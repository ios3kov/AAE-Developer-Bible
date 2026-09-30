# macOS — signing and notarization

## Development signing

Ad-hoc sign (`-`) подходит для local development/load testing. Это **не** release trust model.

## Release signing

Для внешней дистрибуции Apple рекомендует Developer ID signing. Plug-in bundle должен быть подписан после завершения всех изменений содержимого.

Typical verification:

```bash
codesign -vvv --deep --strict "/path/to/MyPlugin.plugin"
```

Дополнительно проверять identity/entitlements по вашему release script.

## Hardened Runtime / nested code

Если package содержит helpers, dylibs, executables:
- каждый nested code object должен быть корректно signed;
- signing order: внутри → наружу;
- release entitlements минимальны;
- `get-task-allow` не должен случайно попасть в production artifact.

## Notarization

Apple больше не принимает старый `altool` workflow. Использовать `notarytool`/актуальный Apple workflow.

Conceptual pipeline:

```text
build
→ sign nested binaries
→ sign plug-in bundle
→ package (zip/pkg/dmg as chosen)
→ submit with notarytool
→ wait/check result
→ staple ticket where applicable
→ verify Gatekeeper/signature
```

Example submit shape:

```bash
xcrun notarytool submit MyPlugin.zip \
  --keychain-profile "notary-profile" \
  --wait
```

Credentials не хранить в repository или shell history.

## Release gate

Release job падает, если:
- signature invalid;
- wrong identity;
- missing required architecture;
- notarization rejected;
- package differs after notarization/signing;
- clean machine cannot load plug-in.
