$._aeBible = $._aeBible || {};

$._aeBible.dispatch = function (json) {
    // ExtendScript does not guarantee a native JSON global. Load a vetted
    // ES3-compatible JSON implementation at bootstrap if the host lacks it.
    if (typeof JSON === "undefined" || !JSON.parse || !JSON.stringify) {
        return '{"ok":false,"requestId":null,"error":{"code":"JSON_UNAVAILABLE","message":"Load an ES3-compatible JSON polyfill"}}';
    }

    var req = null;
    var out = { ok: false, requestId: null };

    try {
        req = JSON.parse(json);
        out.requestId = req.requestId || null;

        if (req.version !== 1) {
            throw { code: "UNSUPPORTED_VERSION", message: "Unsupported protocol version" };
        }

        if (!req.command) {
            throw { code: "MISSING_COMMAND", message: "Missing command" };
        }

        if (req.command === "renameSelected") {
            var comp = app.project && app.project.activeItem;

            if (!(comp instanceof CompItem)) {
                throw { code: "NO_ACTIVE_COMP", message: "No active composition" };
            }

            var layers = comp.selectedLayers;

            if (!layers || layers.length === 0) {
                throw { code: "NO_SELECTED_LAYERS", message: "No selected layers" };
            }

            var prefix = (req.payload && req.payload.prefix) ? String(req.payload.prefix) : "";

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
            throw { code: "UNKNOWN_COMMAND", message: "Unknown command" };
        }
    } catch (e) {
        out.ok = false;
        out.error = {
            code: e && e.code ? String(e.code) : "HOST_ERROR",
            message: e && e.message ? String(e.message) : e.toString()
        };
    }

    return JSON.stringify(out);
};
