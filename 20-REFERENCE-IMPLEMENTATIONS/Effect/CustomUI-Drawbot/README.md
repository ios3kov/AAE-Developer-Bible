# Custom UI / Drawbot starter

Status: **sample-derived / host-test-required**.

Use this with Adobe's Custom ECW UI / Drawbot-capable sample shell. The stable pattern is:

`PF_Cmd_EVENT` → inspect `PF_EventExtra` → acquire `PF_EffectCustomUISuite` → obtain `DRAWBOT_DrawRef` → acquire Drawbot supplier/surface/path suites → draw → release temporary Drawbot objects.

Do not cache per-event Drawbot surface/path handles globally. See `02-EFFECT-PLUGINS/02-PARAMETERS-UI.md` and the official SDK guide's Custom UI & Drawbot section.
