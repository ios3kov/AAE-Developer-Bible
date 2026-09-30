(function () {
    app.beginUndoGroup("Bible: Rename Selected Layers");
    try {
        if (!app.project) throw new Error("No project");
        var comp = app.project.activeItem;
        if (!(comp instanceof CompItem)) throw new Error("Open a composition first");

        var layers = comp.selectedLayers;
        if (!layers || layers.length === 0) throw new Error("Select at least one layer");

        for (var i = 0; i < layers.length; i++) {
            layers[i].name = "Bible_" + (i + 1) + "_" + layers[i].name;
        }
        return layers.length;
    } catch (e) {
        alert("AE Developer Bible\n" + e.toString());
        return 0;
    } finally {
        app.endUndoGroup();
    }
})();
