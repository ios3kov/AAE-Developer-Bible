# Release checklist

## Code

- [ ] clean working tree / tagged commit
- [ ] version/build/schema numbers correct
- [ ] compiler warnings reviewed
- [ ] no debug backdoors/test endpoints
- [ ] exceptions contained at host boundaries
- [ ] dependency licenses reviewed

## Effect correctness

- [ ] 8-bpc
- [ ] 16-bpc
- [ ] 32-bpc if claimed
- [ ] alpha/transparency
- [ ] extreme params
- [ ] animated params
- [ ] save/reopen
- [ ] old project migration

## MFR

- [ ] MFR off passes
- [ ] MFR on passes
- [ ] repeated stress run passes
- [ ] no mutable unsafe globals
- [ ] no lock held across host calls

## GPU

- [ ] CPU path passes
- [ ] every GPU backend passes
- [ ] CPU/GPU diff within defined tolerance
- [ ] CPU fallback works
- [ ] missing/unsupported GPU handled cleanly

## macOS

- [ ] arm64 slice
- [ ] x86_64 slice if claimed
- [ ] PiPL entry declarations correct
- [ ] release Developer ID signature valid
- [ ] notarization accepted
- [ ] clean-machine install/load
- [ ] dSYM archived

## Windows

- [ ] x64 build
- [ ] ARM64 build if claimed
- [ ] PiPL resource generated
- [ ] runtime dependencies packaged
- [ ] Authenticode signature valid
- [ ] installer signature valid
- [ ] clean-machine install/load
- [ ] PDB archived

## AE versions

- [ ] every supported AE version load test
- [ ] render golden project
- [ ] render queue
- [ ] MFR
- [ ] GPU
- [ ] new AE version compatibility statement accurate

## Installer

- [ ] fresh install
- [ ] upgrade
- [ ] uninstall
- [ ] multiple AE versions
- [ ] no destructive user-data deletion

## Release assets

- [ ] changelog
- [ ] known issues
- [ ] support matrix
- [ ] checksums/build manifest
- [ ] rollback artifact retained
