$._aeBible = $._aeBible || {};

$._aeBible.dispatch = function (json) {
    // ExtendScript does not guarantee a native JSON global. Load a vetted
    // ES3-compatible JSON implementation at bootstrap if the host lacks it.
    if (typeof JSON === "undefined" || !JSON.parse || !JSON.stringify) {
        return '{"ok":false,"requestId":null,"error":{"message":"JSON_UNAVAILABLE: load an ES3 JSON polyfill"}}';
    }
    var req = null;
    var out = { ok: false, requestId: null };
    try {
        req = JSON.parse(json);
        out.requestId = req.requestId || null;
        if (req.version !== 1) throw new Error("Unsupported protocol version");

        if (req.method === "renameSelected") {
            var comp = app.project && app.project.activeItem;
            if (!(comp instanceof CompItem)) throw new Error("NO_ACTIVE_COMP");
            var layers = comp.selectedLayers;
            if (!layers || layers.length === 0) throw new Error("NO_SELECTED_LAYERS");

            var prefix = (req.params && req.params.prefix) ? String(req.params.prefix) : "";
            app.beginUndoGroup("AE Bible: Rename Selected");
            try {
                for (var i = 0; i < layers.length; i++) {
                    layers[i].name = prefix + layers[i].name;
                }
            } finally {
                app.endUndoGroup();
            }
            out.ok = true;
            out.result = { changed: layers.length };
        } else {
            throw new Error("UNKNOWN_METHOD");
        }
    } catch (e) {
        out.ok = false;
        out.error = { message: e.toString() };
    }
    return JSON.stringify(out);
};
