# Bug report template

## Summary

One sentence describing the observable failure.

## Impact

- severity:
- user workflow blocked:
- data/project corruption risk:
- crash/hang:
- workaround:

## Artifact identity

- plug-in version:
- internal build:
- git SHA if internal:
- binary SHA-256:
- installer/package version:
- panel/native protocol version if relevant:

## Environment

- After Effects version/build:
- AE Beta/GA:
- OS version/build:
- CPU architecture:
- CPU:
- GPU:
- GPU driver:
- RAM:
- MFR on/off:
- GPU backend:
- project bit depth:
- render mode: preview / render queue / aerender
- install path:

## Reproduction

Preconditions:

1.
2.

Steps:

1.
2.
3.

Frequency:

- [ ] always
- [ ] often
- [ ] rare
- [ ] happened once

Approximate rate if known:

## Expected

State the measurable/observable expected behavior.

## Actual

State the exact observed behavior.

## First failing version

- last known good:
- first known bad:
- unknown:

## Isolation

- [ ] reproduces after AE restart
- [ ] reproduces in minimal project
- [ ] reproduces with MFR off
- [ ] reproduces with GPU off
- [ ] reproduces after cache purge
- [ ] reproduces after clean plug-in reinstall
- [ ] compared with known-good/Adobe sample where relevant

Result of isolation:

## Artifacts

- minimal project:
- source media:
- rendered output:
- golden/diff report:
- plug-in log:
- AE log:
- macOS .ips / Windows dump:
- thread sample if hang:
- installer log:
- screenshot/video:
- symbol archive reference:

## Crash/hang

If crash:

- crashing module:
- top symbolized frames:
- exception/code:
- dSYM/PDB match confirmed: yes/no

If hang:

- timeout duration:
- thread dump/sample attached: yes/no
- last known operation/request ID:

## Privacy

- project/media safe to share: yes/no
- redactions required:
- dump contains sensitive data warning acknowledged:

## Investigation notes

Facts only. Separate observed evidence from hypotheses.

## Resolution

- root cause:
- fix commit:
- regression test:
- affected versions:
- release containing fix:
