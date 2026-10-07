// SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED. Disposable project; never calls render().
(function () {
    if (!app.project) { alert("Open a disposable project"); return; }
    if (app.project.renderQueue.rendering) { alert("Render queue is busy"); return; }
    var targetProject = app.project;
    var input = File.openDialog("Choose one still/movie, not an image sequence");
    if (!input || !input.exists) return;
    var output = File.saveDialog("Choose NEW output path matching your output template");
    if (!output || output.exists) { alert("Output must be new"); return; }
    var options = new ImportOptions(input);
    if (!options.canImportAs(ImportAsType.FOOTAGE)) { alert("Not footage"); return; }
    options.importAs = ImportAsType.FOOTAGE; options.sequence = false;
    var item = null, comp = null, rq = null, group = false;
    try {
        // File dialogs may have been open while the project/queue changed.
        if (!app.project || app.project !== targetProject || app.project.renderQueue.rendering || output.exists)
            throw new Error("Project/queue/output changed during preflight");
        app.beginUndoGroup("Bible Import/Queue"); group = true;
        item = app.project.importFile(options);
        if (!(item instanceof FootageItem) || item.width < 1 || item.height < 1)
            throw new Error("A visual source is required");
        comp = app.project.items.addComp("Bible Imported Demo", item.width, item.height,
            item.pixelAspect, 2, 25);
        comp.layers.add(item);
        rq = app.project.renderQueue.items.add(comp);
        rq.render = false;
        var om = rq.outputModule(1), names = om.templates;
        var chosen = prompt("Choose exact output template; match extension to its format:\n" + names.join("\n"), names[0]);
        var found = false;
        for (var i=0; i<names.length; ++i) if (names[i] === chosen) found = true;
        if (!found) throw new Error("Output template not selected");
        om.applyTemplate(chosen);
        om = rq.outputModule(1);
        om.file = output;
        if (!om.file || om.file.fsName !== output.fsName) throw new Error("Path readback mismatch");
        alert("Prepared DISABLED queue item; inspect format, frame range and output before enabling.\n" + om.file.fsName);
    } catch (e) {
        var failures = [];
        try { if (rq) rq.remove(); } catch (q) { failures.push(q.toString()); }
        try { if (comp) comp.remove(); } catch (c) { failures.push(c.toString()); }
        if (!failures.length) { try { if (item) item.remove(); } catch (f) { failures.push(f.toString()); } }
        alert("Failed: " + e.toString() + "\nCleanup: " + failures.join("\n"));
    } finally { if (group) app.endUndoGroup(); }
})();
