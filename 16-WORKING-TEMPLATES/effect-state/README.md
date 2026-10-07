# Versioned state: portable persistence lesson

Evidence: **SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED**. `VersionedState.h` is a
portable codec, not an arbitrary callback dispatcher, SDK handle adapter or effect.
It demonstrates bytes, validation, v1→v2 migration and publish-after-validation.

Use with [state/arbitrary walkthrough](../../02-EFFECT-PLUGINS/02-PARAMETERS-UI.md#13-сохраняемое-состояние-и-arbitrary-data).
The caller must validate state before encoding (amount ≤4000, mode ≤1); a decode
failure leaves the previous output untouched. Unknown schema is reported separately
from corruption. No runtime cache, refcon or native pointer enters persisted bytes.

```bash
c++ -std=c++17 -Wall -Wextra -Werror scripts/test_versioned_state.cpp -o .build/state-test
.build/state-test
```

This test concerns authored byte serialization only, not Adobe handle ownership,
host callback dispatch, saved project compatibility or Undo. Integrating it requires
implementing every applicable arbitrary callback against the target SDK, allocating
SDK handles and following the separately documented ownership transfers.
