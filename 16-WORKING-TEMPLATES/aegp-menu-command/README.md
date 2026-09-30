# AEGP menu command template

Status: **drop-in pattern** for current AEGP sample project.

Start from an official AEGP sample such as Persisto/Projector. Keep its PiPL/project/export plumbing; use this file as the architecture for entry registration + command/update hooks.

The example intentionally performs a harmless operation: reports info to the user. Replace `DoWork()` with project mutation inside an undo group.
