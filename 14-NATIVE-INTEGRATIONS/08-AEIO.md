# AEIO — native input/output modules

AEIO — specialized AEGP для media I/O.

## Registration

В AEGP entry point plug-in формирует:

- `AEIO_ModuleInfo` — capabilities/file type metadata;
- `AEIO_FunctionBlock*` — callback table;
- вызывает `AEGP_RegisterIO()`.

## Import lifecycle

```text
VerifyFileImportable
   -> InitInSpecFromFile
   -> AE stores InSpec/options
   -> GetInSpecInfo / dimensions / duration / alpha / audio...
   -> GetSourceVideo / audio callbacks as AE needs media
```

`AEIO_InSpecH` — opaque handle, через который AEIO и AE обмениваются import state/metadata.

## Output lifecycle

```text
AE creates OutSpec
  -> AEIO queries dimensions/time/audio/etc
  -> open/create output
  -> receive frames/audio
  -> encode/write
  -> close/finalize
```

## Default callback pattern

Если API разрешает, callback может вернуть `AEIO_Err_USE_DFLT_CALLBACK` и передать поведение AE. Это полезно и как incremental development strategy.

## Современный выбор

Для ряда обычных media importer задач Adobe рекомендует рассматривать MediaCore/Premiere importer путь, если нужен shared importer across Adobe video apps. AEIO нужен, когда нужна именно AE-specific I/O integration/capability.
