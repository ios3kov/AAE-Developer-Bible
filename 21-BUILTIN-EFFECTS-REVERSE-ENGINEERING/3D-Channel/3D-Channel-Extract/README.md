# 3D Channel Extract — investigation index

**Full-effect acceptance remains OPEN. No new user AE run is requested.** Existing measurements are preserved, but acquisition statuses must not be read as a completed plug-in acceptance.

**Current editorial priority, 2026-09-30:** write the Bible from the supplied SDK. Native readout-adapter development is paused, not completed or deleted. The source-reviewed [auxiliary-channel chapter](../../../02-EFFECT-PLUGINS/08-AUXILIARY-CHANNELS.md) explains the public contract; the [SDK source record](../../../18-SDK-HEADER-TOOLS/05-SUPPLIED-SDK-25.6.md) identifies the supplied headers and review limits. Neither document is a new native-effect test.

- [Native readout contract and offline gate](HOST-CHANNEL-READOUT-CONTRACT.md): implemented capture-content validator for 16 typed checks, identity/descriptor/raw-byte consistency and cleanup reporting. 41 synthetic regression tests; native collector, SDK compilation and AE execution remain NOT RUN. Further collector implementation is paused.
- [Input qualification result, 2026-09-30](INPUT-QUALIFICATION-2026-09-30.md): four controlled EXRs, 20 portable tests and independent OpenEXR decoding of all 30 planes / 61,440 values passed. File-input milestone only; AE importer qualification remains NOT RUN.
- [Auxiliary fixture candidate and acceptance design](AUXILIARY-FIXTURE-CANDIDATE.md): known values, separate missing-data/nonfinite/alpha inputs, seven proposed semantic families and the uninstalled candidate map. UNCP is not claimed covered.
- [Evidence audit and corrections, 2026-09-30](EVIDENCE-AUDIT-2026-09-30.md): current authoritative interpretation of prior runs; all six supplied ZIPs and 30 images reviewed, original evidence preserved, full-effect claims withdrawn.
- [Numerical observations](NUMERICAL-OBSERVATIONS-2026-09-30.md): scoped nested-composition Z-Depth results from the original 28-case report.
- [Edge sampling and frame exports](EDGE-AND-RENDER-PROBE.md): collector history, actual file precision, decoded AA comparisons and output-pipeline limitations. Not a new run request.
- [Runtime acceptance protocol](RUNTIME-ACCEPTANCE-MACOS-AE25.6.md): retained observations and remaining test gates.
- [Corrected static function map](FILTERMAIN-FUNCTION-MAP-MACOS-AE25.6.md): corrected selector byte offset, datatype literals and UNCP interpretation; partial reconstruction, not finished independent code.
- [Mega v01 withdrawal](MEGA-PROBE.md): why forced selector writes and capability placeholders do not validate all channels.
- [Chronological binary evidence](BINARY-EVIDENCE-MACOS-AE25.6.md): historical record; superseded interpretations must not override the current audit.

Importer qualification remains a requirement before future all-channel acceptance, not an instruction to launch another probe now. The candidate map is not installed. Historical versions remain in Git; original artifacts remain unchanged.
