(function AEDeveloperBiblePanel(thisObj) {
    // Synchronous command; no widget dependency or retained selection references.
    function renameSelectedLayers(prefix) {
        var result = {ok:false, changed:0, total:0, error:null, cleanupError:null};
        var project = app.project, opened = false;
        try {
            if (typeof prefix !== "string" || !prefix.length || /[\r\n]/.test(prefix))
                throw new Error("Use a non-empty single-line prefix.");
            if (!project || project.renderQueue.rendering) throw new Error("Project missing or busy.");
            var comp = project.activeItem;
            if (!(comp instanceof CompItem)) throw new Error("Open a composition first.");
            var selected = comp.selectedLayers;
            if (!selected || selected.length === 0) throw new Error("Select at least one layer.");
            var targets = [], names = [];
            for (var i = 0; i < selected.length; i++) {
                targets.push(selected[i]);
                names.push(prefix + (i + 1));
            }
            result.total = targets.length;
            if (app.project !== project || project.activeItem !== comp || project.renderQueue.rendering)
                throw new Error("Target context changed.");
            app.beginUndoGroup("AE Bible Rename"); opened = true;
            for (var j = 0; j < targets.length; j++) {
                targets[j].name = names[j];
                result.changed++;
            }
            result.ok = true;
        } catch (e) {
            result.error = e.toString();
        } finally {
            if (opened) {
                try { app.endUndoGroup(); }
                catch (c) { result.cleanupError = c.toString(); result.ok = false; }
            }
        }
        return result;
    }

    function buildUI(host) {
        var win = (host instanceof Panel)
            ? host
            : new Window("palette", "AE Bible Panel", undefined, {resizeable:true});

        var group = win.add("group");
        group.orientation = "column";
        group.alignChildren = ["fill", "top"];

        var btn = group.add("button", undefined, "Rename selected layers");
        var status = group.add("statictext", undefined, "Ready");

        btn.onClick = function () {
            btn.enabled = false;
            try {
                var result = renameSelectedLayers("Layer_");
                status.text = (result.ok ? "Renamed " : "Stopped after ") + result.changed +
                    "/" + result.total + " layer(s)" +
                    (result.error ? ": " + result.error : "") +
                    (result.cleanupError ? "; Undo close: " + result.cleanupError : "");
            } catch (e) {
                status.text = "Error: " + e.toString();
            } finally {
                btn.enabled = true;
            }
        };

        win.onResizing = win.onResize = function () {
            this.layout.resize();
        };

        return win;
    }

    var ui = buildUI(thisObj);
    ui.layout.layout(true);
    if (ui instanceof Window) {
        ui.center();
        ui.show();
    }
})(this);
