# macOS — native SDK validation

This chapter describes SDK/source validation a Mac developer can use when implementing a native product. It is not a completion requirement for AE Developer Bible.

## Run

~~~bash
cd 18-SDK-HEADER-TOOLS
./run-macos.sh "/path/to/After Effects SDK/Examples"
~~~

Use the exact SDK intended for the candidate build.

## What PASS means

A successful header-tool run means only the checks implemented by the tool passed, such as:

- supported headers were parsed with no unresolved **required-contract** diagnostics; unrelated diagnostics remain recorded;
- inventory schema/version validation passed;
- cookbook/reference suite symbols were found according to parser rules;
- the current Bible native C++ translation units passed Clang C++17 syntax/type checks;
- a machine-readable compiler report records SDK header-manifest identity, compiler identity, exact commands and per-source results.

It does not prove complete header coverage.

The indexer fails closed on unsupported declaration shapes, and full exact-SDK indexing remains a separate coverage concern.

## What PASS does not mean

It does not prove:

- resources/PiPL compile;
- link succeeds;
- arm64/x86_64 slices exist;
- nested dependencies are correct;
- bundle loads in AE;
- pixels are correct;
- MFR/GPU are safe;
- code signing is valid;
- notarization passes.

Do not promote a header/source audit into a runtime claim.

## If you are implementing a product

~~~text
header inventory + symbol check + Clang syntax/type report
→ Xcode project/resource compile
→ resource/PiPL build
→ link
→ architecture/dependency inspection
→ development sign
→ AE load/operation tests
→ release sign/package/notarize
→ quarantined clean-install test
~~~

Only run gates relevant to the current development/release stage, but keep their evidence classes separate.

## Artifact identity

`scripts/check_native.py` канонизирует SDK Examples root через `Path.resolve()`;
portable symlink-root regression проверяет одинаковый header manifest для alias
и physical path. Это filesystem symlink test, не гарантия поддержки Finder alias
files. Report хранит source Git SHA/dirty, source hashes, compiler identity/commands
и SDK header-manifest hash. `--require-clean` отказывает при dirty/unknown source;
report размещайте в ignored output, чтобы сам report не загрязнил source identity.
Header digest не идентифицирует весь SDK resource/tool/sample tree.

Сохранённая [проверка 2026-10-07](../VERIFICATION.md) относится к exact source
`ef4e90b`, не ко всем последующим documentation heads.

Record with validation:

- SDK version/build;
- tool Git SHA;
- inventory hash/path;
- plug-in source Git SHA;
- Xcode/Clang version;
- target architecture.

## SDK upgrade

When changing SDK, generate/diff inventory before accepting compiler fixes.

See 18-SDK-HEADER-TOOLS/03-SDK-DIFF-POLICY.md.

## Failure handling

If header tool fails:

1. determine whether it found a real product/reference mismatch or an unsupported parser declaration;
2. inspect the exact header;
3. improve tool coverage only when the parser can do so deterministically;
4. never add a permissive guess just to turn CI green.

## Verification boundary

The Bible has historical macOS arm64 syntax/type evidence for parts of the repository. This file does not upgrade any reference implementation to linked/signed/host-verified status.


For the SDK contract-audit method, see [SDK contract audit runbook](../18-SDK-HEADER-TOOLS/16-SDK-CONTRACT-AUDIT-RUNBOOK.md).
