# CEP development

CEP panel — HTML/CSS/JS extension, интегрируемая в Creative Cloud host.

## Core pieces

Типичный bundle:

```text
MyPanel/
├── CSXS/manifest.xml
├── index.html
├── js/
├── css/
└── jsx/        # host-side ExtendScript bridge
```

Host id After Effects в CEP manifests: `AEFT`.

## Extension folders

macOS:
- system: `/Library/Application Support/Adobe/CEP/extensions`
- user: `~/Library/Application Support/Adobe/CEP/extensions`

Windows:
- system: `C:\Program Files (x86)\Common Files\Adobe\CEP\extensions`
- user: `%AppData%\Roaming\Adobe\CEP\extensions`

## Unsigned dev mode

CEP development commonly uses `PlayerDebugMode` under the corresponding `CSXS.<major>` preference/registry key. Версию CSXS нельзя копировать вслепую: она должна соответствовать CEP runtime host-а.

## Debugging

CEP resources include:
- `.debug` file with host/port mapping;
- CSXS logs;
- CEPHtmlEngine logs;
- browser devtools connection.

## Security

Не считать CEP panel доверенным просто потому, что он локальный:
- validate messages crossing UI ↔ JSX/native bridge;
- no arbitrary `eval` of remote content;
- escape paths/arguments;
- secrets not in frontend source;
- sign/package release artifact.
