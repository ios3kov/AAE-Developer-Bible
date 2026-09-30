# CEP -> ExtendScript JSON bridge

Standalone logic files for a CEP panel.

To package as an actual extension, add:
- Adobe `CSInterface.js` from the CEP Resources version you target;
- `CSXS/manifest.xml` matching the AE/CEP versions you support;
- load `host/index.jsx` from manifest or panel startup;
- signing/packaging config.

The important reusable piece is the **single dispatcher protocol**. It avoids arbitrary code generation and gives every call a version + request ID + JSON response.
