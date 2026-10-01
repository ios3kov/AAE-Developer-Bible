(function AEDeveloperBiblePanel(thisObj) {
    function renameSelectedLayers() {
        var comp = app.project && app.project.activeItem;
        if (!(comp instanceof CompItem)) throw new Error("Open a composition first.");

        var layers = comp.selectedLayers;
        if (!layers || layers.length === 0) throw new Error("Select at least one layer.");

        app.beginUndoGroup("AE Bible Rename");
        try {
            for (var i = 0; i < layers.length; i++) {
                layers[i].name = "Layer_" + (i + 1);
            }
        } finally {
            app.endUndoGroup();
        }

        return layers.length;
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
            try {
                var changed = renameSelectedLayers();
                status.text = "Renamed " + changed + " layer(s)";
            } catch (e) {
                status.text = "Error: " + e.toString();
            }
        };

        win.onResizing = win.onResize = function () {
            this.layout.resize();
        };

        return win;
    }

    var ui = buildUI(thisObj);
    if (ui instanceof Window) {
        ui.center();
        ui.show();
    }
})(this);
