# CEP -> ExtendScript JSON bridge

Standalone logic files for a CEP panel.

To package as an actual extension, add:
- Adobe `CSInterface.js` from the CEP Resources version you target;
- `CSXS/manifest.xml` matching the AE/CEP versions you support;
- load `host/index.jsx` from manifest or panel startup;
- load a vetted ES3-compatible JSON polyfill before `host/index.jsx` when ExtendScript has no `JSON` global (do not rely on another panel having installed one);
- signing/packaging config.

The important reusable piece is the **single dispatcher protocol**. It avoids arbitrary code generation and gives every call a version + request ID + JSON response.
