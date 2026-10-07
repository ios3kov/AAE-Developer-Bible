# Block 10 — scripting and expression operations

Added ES3 source demo: comp/null/text, slider, keys/interpolation, expression
resolution, mask/marker and created-comp-only failure compensation. Chapters map
rename/import/replace/queue operations, property invalidation, Unicode file handling,
settings and bounded scheduled cancellation. UI remains an operation shell.

Source basis: existing scripting guide review; exact object/matchName routes follow
AE scripting object model, not browser JS. Source/runtime boundary remains explicit.
No AE execution or all-version support claim. Host correctness and each render
output still require reader-product fixtures; expression resolution is not full QA.

Follow-up source review: demo originally replaced keyed opacity with slider-only
expression; now adds slider to animated value with clamp and checks canSetExpression.
Expected t=0/1 values documented. Busy render queue refuses entry. No host result
or keyframe-ease implementation inferred.
