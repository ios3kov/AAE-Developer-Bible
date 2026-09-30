# Windows — Visual Studio setup

## Start from Adobe sample

Adobe SDK Guide прямо советует не реконструировать Windows effect project с нуля: custom PiPL resource generation step легко потерять.

Для effect plug-in:
1. скопировать Skeleton/closest sample;
2. открыть solution в поддерживаемой Visual Studio;
3. собрать untouched sample;
4. убедиться, что `.aex` реально загружается AE;
5. только потом переименовывать и менять код.

## Configurations

Минимум:
- Debug x64;
- Release x64;
- ARM64 equivalents, если поддерживаются.

Сохранять PDB каждого released build в symbol archive.

## Output during development

SDK Guide показывает common dev path вида:

```text
C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\
```

Но для installer path использовать Adobe registry guidance, а не предполагать, что одна строка подходит всегда.

## Build hygiene

- warning level высокий для собственного кода;
- `/permissive-`/conformance changes вводить осознанно;
- runtime library setting единообразно по зависимостям;
- no accidental Debug CRT dependency in Release;
- dependency audit before packaging.
