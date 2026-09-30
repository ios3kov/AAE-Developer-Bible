# Windows — code signing

## Tool

Microsoft SignTool входит в Windows SDK и используется для Authenticode signing/verification/timestamping.

Современные SignTool версии требуют явно задавать digest algorithms; SHA-256 — нормальный baseline.

## Conceptual command

```bat
signtool sign /fd SHA256 /td SHA256 /tr <RFC3161_TIMESTAMP_URL> /a MyPlugin.aex
```

Actual certificate selection (`/a`, `/n`, `/sha1`, PFX, Trusted Signing etc.) зависит от вашей release infrastructure.

## Verify

```bat
signtool verify /pa /v MyPlugin.aex
```

## Sign what ships

Подписывать:
- `.aex`;
- helper `.exe/.dll`;
- installer executable/MSI as applicable.

Signing должен быть после final binary mutation. Любой post-sign patch invalidates signature.

## Certificate security

- private key не хранить в repo;
- CI credentials isolated;
- access only release jobs;
- timestamp releases so signatures remain verifiable after certificate expiry, subject to trust policy.
