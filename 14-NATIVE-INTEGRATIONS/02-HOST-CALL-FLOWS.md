# Host call flows

## Effect

```text
AE loads module / reads PiPL
        |
        v
PluginDataEntryFunction* -> registers effect metadata
        |
        v
EffectMain(PF_Cmd_GLOBAL_SETUP)
        |
        v
EffectMain(PF_Cmd_PARAM_SETUP)
        |
        +---- per instance ---> SEQUENCE_SETUP / RESETUP / FLATTEN / SETDOWN
        |
        +---- render ----------> FRAME_SETUP -> RENDER -> FRAME_SETDOWN
        |                       or SMART_PRE_RENDER -> SMART_RENDER
        |
        +---- UI --------------> EVENT / USER_CHANGED_PARAM / UPDATE_PARAMS_UI
        |
        v
GLOBAL_SETDOWN
```

Главное: plug-in **не крутит свой loop** и не «спрашивает AE, есть ли работа». AE вызывает plug-in тогда, когда render graph или UI нуждается в нём.

## AEGP

```text
AE launch
  |
  v
AEGP EntryPointFunc(pica_basicP, version, plugin_id, global_refcon)
  |
  +-- register CommandHook
  +-- register UpdateMenuHook
  +-- register IdleHook
  +-- register DeathHook
  +-- optionally RegisterIO / RegisterArtisan / panel callbacks
  |
  v
EntryPointFunc returns
  |
  v
AE later invokes registered hooks
  |
  v
hook -> acquire/call AEGP suites -> mutate/query AE
```

AEGP entry point — регистрационная фаза. Основная работа происходит позднее в hooks.

## AEIO

```text
AE launch -> AEGP entry -> AEGP_RegisterIO()
                       |
                       v
User imports file -> VerifyFileImportable -> InitInSpecFromFile
                       |
                       v
AE asks metadata / frame / audio through AEIO function block

Render/output -> AE creates OutSpec -> AEIO callbacks -> encoded file
```

## Artisan

```text
AE launch -> AEGP entry -> AEGP_RegisterArtisan()
                       |
                       v
User selects renderer for composition
                       |
                       v
AE creates render context -> Artisan callbacks -> rendered 3D result
```

## BlitHook

```text
AE Composition panel displays frame
              |
              v
         BlitHook callback
              |
              v
     consume/copy/send frame
```

Это display-time stream, не замена normal Effect/Render Queue pipeline.
