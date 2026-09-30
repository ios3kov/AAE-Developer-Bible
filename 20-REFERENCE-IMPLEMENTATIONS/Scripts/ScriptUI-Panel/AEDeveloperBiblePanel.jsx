(function AEDeveloperBiblePanel(thisObj) {
    function buildUI(host) {
        var win = (host instanceof Panel) ? host : new Window("palette", "AE Bible Panel", undefined, {resizeable:true});
        var group = win.add("group");
        group.orientation = "column";
        group.alignChildren = ["fill", "top"];
        var btn = group.add("button", undefined, "Rename selected layers");
        btn.onClick = function () {
            app.beginUndoGroup("AE Bible Rename");
            try {
                var comp = app.project && app.project.activeItem;
                if (!(comp instanceof CompItem)) throw new Error("Open a composition first.");
                var layers = comp.selectedLayers;
                for (var i = 0; i < layers.length; i++) layers[i].name = "Layer_" + (i + 1);
            } catch (e) {
                alert(e.toString());
            } finally {
                app.endUndoGroup();
            }
        };
        win.onResizing = win.onResize = function () { this.layout.resize(); };
        return win;
    }
    var ui = buildUI(thisObj);
    if (ui instanceof Window) { ui.center(); ui.show(); }
})(this);
