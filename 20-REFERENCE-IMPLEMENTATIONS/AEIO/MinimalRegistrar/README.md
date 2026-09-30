# Minimal AEIO registrar

Status: **host-test-required**.

AEIO is not just a single entry function: After Effects asks the module to register an `AEIO_FunctionBlock` whose callbacks implement file sniffing, spec creation/disposal, metadata, frame/audio retrieval and (for output modules) writing.

Use the closest AEIO SDK sample as the binary/project shell, then implement one callback group at a time. The complete lifecycle and callback categories are in `04-AEIO/README.md` and `14-NATIVE-INTEGRATIONS/08-AEIO.md`.

A "registration-only" source file is intentionally not labelled working because a host-loadable AEIO that cannot satisfy its function block is not useful.
