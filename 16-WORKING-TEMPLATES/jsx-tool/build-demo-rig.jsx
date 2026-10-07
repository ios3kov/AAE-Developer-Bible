// SOURCE EXAMPLE / RUNTIME-NOT-CLAIMED. Run on a disposable project only.
// ES3 host syntax. Creates a new comp; never deletes pre-existing items.
(function () {
    if (!app.project) { alert("Open a disposable project first"); return; }
    var comp = null, opened = false;
    try {
        app.beginUndoGroup("Bible: Create Demo Rig"); opened = true;
        comp = app.project.items.addComp("Bible Demo Rig", 640, 360, 1, 2, 25);
        var control = comp.layers.addNull(); control.name = "Bible Control";
        var effects = control.property("ADBE Effect Parade");
        if (!effects.canAddProperty("ADBE Slider Control")) throw new Error("Slider unavailable");
        var slider = effects.addProperty("ADBE Slider Control");
        slider.name = "Bible Amount";
        slider.property(1).setValue(50);
        var text = comp.layers.addText("AE Developer Bible");
        var source = text.property("ADBE Text Properties").property("ADBE Text Document");
        var doc = source.value; doc.fontSize = 32; source.setValue(doc);
        var opacity = text.property("ADBE Transform Group").property("ADBE Opacity");
        opacity.setValueAtTime(0, 0); opacity.setValueAtTime(1, 100);
        opacity.setInterpolationTypeAtKey(1, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
        opacity.setInterpolationTypeAtKey(2, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
        // Script resolves matchNames; expression uses product-controlled names.
        opacity.expression = 'thisComp.layer("Bible Control").effect("Bible Amount")(1)';
        opacity.valueAtTime(0, false);
        if (!opacity.expressionEnabled || opacity.expressionError) throw new Error(opacity.expressionError || "Expression disabled");
        var marker = new MarkerValue("Bible start");
        text.property("ADBE Marker").setValueAtTime(0, marker);
        var masks = text.property("ADBE Mask Parade");
        if (!masks.canAddProperty("ADBE Mask Atom")) throw new Error("Mask unavailable");
        var mask = masks.addProperty("ADBE Mask Atom");
        var shape = new Shape();
        shape.vertices = [[0,0],[640,0],[640,360],[0,360]];
        shape.inTangents = [[0,0],[0,0],[0,0],[0,0]];
        shape.outTangents = [[0,0],[0,0],[0,0],[0,0]]; shape.closed = true;
        mask.property("ADBE Mask Shape").setValue(shape);
        comp.openInViewer();
    } catch (e) {
        // Explicit compensation applies only to the newly created comp.
        var cleanup = "";
        if (comp) { try { comp.remove(); } catch (c) { cleanup = "\nCleanup: " + c.toString(); } }
        alert("Bible rig failed: " + e.toString() + cleanup);
    } finally {
        if (opened) app.endUndoGroup();
    }
})();
