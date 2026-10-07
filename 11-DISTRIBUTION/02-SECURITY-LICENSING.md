# Security and licensing architecture

Security and licensing run inside or next to a large creative host process. Protecting revenue must not make After Effects unstable.

## Primary rule

### Bible authored material versus product licensing

[NOTICE](../NOTICE.md) records the owner's 2026-10-07 decision: no reuse license
granted for authored prose/examples. Public availability/editorial completion does
not grant copying/adaptation rights. Vendor SDK samples/headers and third-party
assets retain their own terms; use a locally licensed SDK and do not republish it.
This decision is separate from the runtime entitlement architecture below.

Licensing failure should degrade the product deliberately.

It should not:

- crash AE;
- deadlock render threads;
- corrupt a project;
- block every frame on the network;
- display UI from an unsafe render callback;
- delete user data.

## Never put network licensing in the render hot path

Do not perform per frame:

- license-server HTTP calls;
- disk-wide license scans;
- expensive crypto handshakes;
- modal dialogs;
- long global mutex waits.

Resolve entitlement state outside the hot loop and expose a small immutable/cached state to render code.

If state can expire, define when it is safely refreshed.

## Threading

A render callback may run concurrently under MFR.

License state read by render code should therefore be:

- immutable snapshot;
- atomic small state;
- otherwise synchronized without holding a lock across host calls.

Do not make one global license mutex serialize all render frames.

## Offline behavior

Define before implementation:

- normal offline grace;
- first activation while offline;
- server outage;
- certificate/TLS failure;
- machine hardware change;
- clock rollback;
- license revoked;
- subscription expires;
- render farm/headless usage;
- user signs out;
- product update while offline.

"Try the server and see" is not a policy.

## Failure classes

Differentiate:

~~~text
VALID
INVALID
EXPIRED
OFFLINE_GRACE
SERVER_UNAVAILABLE
CLOCK_SUSPECT
COMPONENT_ERROR
~~~

Do not collapse a server outage into "pirated license".

This improves both UX and support diagnostics.

## Secrets

Client software is not a trusted secret vault.

Anything embedded in:

- .aex/.plugin;
- CEP JavaScript;
- JSX;
- helper executable;
- local config

can potentially be extracted.

Never ship:

- server master API keys;
- admin credentials;
- private signing keys;
- database passwords;
- a symmetric key whose compromise grants universal licenses.

Use server-side authority where a true secret is required.

## Panel security

For CEP/UXP-style UI:

- do not expose arbitrary "execute script" endpoints;
- validate command payloads;
- allowlist helper operations;
- validate downloaded data before native parsing;
- do not trust remote HTML/JS as product code;
- keep auth tokens out of logs.

A local panel is still an input surface into AE.

## Helper IPC security

If a helper listens on localhost or a named pipe/socket:

- authenticate or bind access appropriately for the threat model;
- version the protocol;
- validate length/count/offset fields;
- cap message size;
- reject unknown opcodes;
- prevent arbitrary file execution;
- decide whether another local process may issue commands.

"localhost" is not the same as "trusted".

## Update security

If the product auto-downloads updates:

~~~text
fetch metadata
→ validate channel/version
→ download artifact
→ verify signature/hash against trusted metadata
→ stage
→ install
~~~

Never execute an update solely because a URL returned HTTP 200.

Prefer platform code signing plus your own signed update metadata where appropriate.

## Tamper resistance

Obfuscation and anti-debugging can raise reverse-engineering cost, but cannot turn a client binary into a secure server.

Aggressive protection must not:

- break AE debugging/support;
- trigger false positives;
- destabilize MFR/GPU;
- block legitimate offline users;
- make crash dumps unusable.

Host stability wins.

## Privacy

Collect only diagnostics/telemetry needed by a defined purpose.

Document:

- what is collected;
- when;
- retention;
- opt-in/opt-out policy where applicable;
- whether project names/paths/content are ever included.

Avoid uploading creative content as "debug data" by accident.

## Logging

Safe licensing logs can include:

- product/build;
- state code;
- anonymized/account-safe entitlement identifier if policy allows;
- server response class;
- request correlation ID;
- timestamp.

Do not log:

- auth tokens;
- full license keys;
- passwords;
- private project content.

## Render farm policy

Decide explicitly whether headless/aerender/render-node use is:

- included;
- separately licensed;
- machine-counted;
- floating;
- offline-token based.

Do not discover this only when a customer's farm hangs because a render process attempted interactive login.

## Verification boundary

This chapter is architectural guidance. A real licensing implementation requires its own threat model, privacy review, failure-injection tests and host stability tests.
