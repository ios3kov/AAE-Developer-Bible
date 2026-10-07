# AEIO reference workspace

Status: **IO/FBIO sample-derived workspace plan / RUNTIME-NOT-CLAIMED**.

Materialize the licensed SDK sample with scripts/materialize_sdk_examples.py. The Bible does not publish a fake registration-only AEIO and call it working.

## Why AEIO is larger than a registrar

After Effects registers an AEIO function block whose callbacks implement the actual importer/exporter lifecycle.

Depending on direction/capability this can include:

- file sniffing/verification;
- input/output spec creation;
- spec disposal;
- metadata;
- frame retrieval;
- audio retrieval;
- output state;
- frame/audio writing;
- auxiliary channels;
- color information.

A module that registers but cannot satisfy its callback block is not a useful reference implementation.

## Source of truth

Read:

- 04-AEIO/README.md;
- 14-NATIVE-INTEGRATIONS/08-AEIO.md;
- 18-SDK-HEADER-TOOLS/12-AEIO-ARTISAN-SDK25.6.md;
- exact IO/FBIO sample from the target SDK.

The supplied 25.6 review records AEIO_ModuleInfo, AEIO_FunctionBlock4 and the current reviewed IO suite generations. Recheck target headers before shipping.

## Build sequence

~~~text
materialize exact sample
→ build/load untouched
→ exercise sample format
→ freeze baseline evidence
→ replace one callback family
→ retest
→ repeat
~~~

Do not replace registration, file parser, frame decode and output writing all in one step.

## Input implementation order

A practical importer order:

1. identify/sniff supported file;
2. create input spec;
3. expose dimensions/time/metadata;
4. retrieve one deterministic frame;
5. add seeking/random frame order;
6. add audio if required;
7. add color/auxiliary metadata;
8. error/corruption handling;
9. performance/cache.

## Output implementation order

1. create output spec;
2. validate settings;
3. open target;
4. write deterministic frame;
5. close/finalize safely;
6. add audio/metadata;
7. cancellation/failure rollback;
8. multiple frames/long render.

## Ownership

Host owns InSpec/OutSpec identity; module owns its attached options/private resources
according to each API contract. Do not dispose the host spec as a codec object.

The [IO reading route](../../../04-AEIO/README.md#exact-io-sample-reading-walkthrough)
records HAS_AUX_DATA advertised but auxiliary provider callback slots unassigned.
Strip unimplemented capabilities rather than treating sample flags as certification.

Never keep callback-scoped buffers or host handles after their documented lifetime.

For file handles/resources, define who closes them on:

- success;
- cancellation;
- parse error;
- output write error;
- AE shutdown.

## Error handling

Malformed media is untrusted input.

Validate sizes, counts, offsets, allocation arithmetic and file bounds before reading/allocating.

Do not let a corrupt file crash the host.

## Product validation cases

### Import

- valid minimal file;
- wrong extension but valid signature if sniffing supports it;
- truncated header;
- impossible dimensions/count;
- missing payload;
- random seek order;
- repeated frame;
- save/reopen project;
- missing source file.

### Export

- one frame;
- long sequence;
- cancel;
- disk full/write failure simulation where practical;
- invalid destination;
- overwrite policy;
- close/finalize failure.

## Spec/options state

When adapting IO/FBIO, make the state machine explicit before replacing callbacks:

```text
host spec
→ attached live options/private state
→ parser/decoder or encoder state
→ flat options for persistence
→ disposal/finalization
```

Do not replace parser, options ownership and frame I/O simultaneously; preserve a known reference shell while changing one layer at a time.

## Verification boundary

This is a source/workspace plan based on the licensed SDK samples. Registration alone is not a complete product implementation, but Bible does not require compiling/running this workspace for editorial completion. Runtime support is claimed only when a product has separate evidence.
