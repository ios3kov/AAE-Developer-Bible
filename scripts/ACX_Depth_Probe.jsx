#target aftereffects
/* AE Developer Bible: Z-depth observation collector, build ACX-PROBE-20260930-01.
 * Run with File > Scripts > Run Script File in an open DEPTH_TEST fixture.
 * No save(), preference changes, queue rendering, cache purge or binary patches.
 * Only a disposable duplicate is edited; project bpc is restored in finally.
 * sampleImage observations are NOT raw render files or a bit-exact/MFR verdict.
 */
(function () {
    var BUILD = "ACX-PROBE-20260930-01";
    var MATCH = "ADBE AUX CHANNEL EXTRACT";
    var start = new Date().getTime();
    var runId = BUILD + "-" + start + "-" + Math.floor(Math.random() * 1000000);
    var project = app.project, scratch = null, out = null, undo = false;
    var initialBpc = null, fatal = null, reportFile = null;
    var report = {schema: 1, build: BUILD, runId: runId, status: "PREFLIGHT",
        measurement: "expression sampleImage, layer space, radius 0.5, postEffect=true",
        cases: [], cleanupErrors: [], limitations: [
            "COLLECTED means observations only, not acceptance PASS.",
            "sampleImage is alpha-weighted sampling, not a raw pixel-buffer dump.",
            "No proof of loaded binary hash, DPTH/DPAA identity, GPU or MFR execution.",
            "Clamp writes at 32 bpc are scripting requests, not proof of UI availability.",
            "The 180-second budget is checked between host calls; it cannot interrupt a hung AE.",
            "Temporary edits may leave the project dirty; the original AEP is never saved by this script."
        ]};
    function quote(s) {
        return '"' + String(s).replace(/[\\"\x00-\x1f\u2028\u2029]/g, function (c) {
            if (c === '"' || c === "\\") { return "\\" + c; }
            return "\\u" + ("0000" + c.charCodeAt(0).toString(16)).slice(-4);
        }) + '"';
    }
    function json(v) {
        var a = [], k;
        if (v === null || typeof v === "undefined") { return "null"; }
        if (typeof v === "string") { return quote(v); }
        if (typeof v === "number") { return isFinite(v) ? String(v) : quote(String(v)); }
        if (typeof v === "boolean") { return String(v); }
        if (v instanceof Array) {
            for (k = 0; k < v.length; k++) { a.push(json(v[k])); }
            return "[" + a.join(",") + "]";
        }
        for (k in v) { if (v.hasOwnProperty(k)) { a.push(quote(k) + ":" + json(v[k])); } }
        return "{" + a.join(",") + "}";
    }
    function optional(obj, key) {
        try { return typeof obj[key] === "undefined" ? null : obj[key]; }
        catch (e) { return "UNAVAILABLE: " + String(e); }
    }
    function checkpoint() {
        if (!out) { return; }
        report.elapsedMs = new Date().getTime() - start;
        reportFile = new File(out.fsName + "/report.json");
        reportFile.encoding = "UTF-8";
        if (!reportFile.open("w")) {
            throw new Error("Cannot write report. Enable Allow Scripts to Write Files and Access Network in AE Scripting preferences.");
        }
        var ok = reportFile.write(json(report) + "\n");
        var closed = reportFile.close();
        if (!ok || !closed) { throw new Error("Report write/close failed: " + reportFile.error); }
    }
    function findComp() {
        var found = null, n, item;
        for (n = 1; n <= project.numItems; n++) {
            item = project.item(n);
            if (item instanceof CompItem && item.name === "DEPTH_TEST") {
                if (found) { throw new Error("More than one DEPTH_TEST composition; no changes made."); }
                found = item;
            }
        }
        if (!found) { throw new Error("Open the test project containing DEPTH_TEST."); }
        if (found.numLayers !== 1) { throw new Error("DEPTH_TEST must contain one precomp layer. No scene changes made."); }
        return found;
    }
    function findEffect(layer) {
        var effects = layer.property("ADBE Effect Parade"), effect = null, n;
        if (!effects || effects.numProperties !== 1) {
            throw new Error("The test layer must have only 3D Channel Extract, without other effects.");
        }
        effect = effects.property(1);
        if (effect.matchName !== MATCH || effect.numProperties < 6) {
            throw new Error("3D Channel Extract with six expected parameters was not found.");
        }
        for (n = 1; n <= 6; n++) {
            if (typeof effect.property(n).value !== "number") {
                throw new Error("Unexpected parameter layout at index " + n);
            }
        }
        return effect;
    }
    function parameters(effect, time) {
        var a = [], n, p;
        for (n = 1; n <= 6; n++) {
            p = effect.property(n);
            a.push({index: n, name: p.name, matchName: p.matchName,
                value: p.valueAtTime(time, false), min: p.hasMin ? p.minValue : null,
                max: p.hasMax ? p.maxValue : null});
        }
        return a;
    }
    function expression(layerIndex, points, time, nonce) {
        return "// " + nonce + "\nvar L=thisComp.layer(" + layerIndex + ");\n" +
            "var P=" + json(points) + ";var rows=[];\n" +
            "for(var i=0;i<P.length;i++){var c=L.sampleImage(P[i],[0.5,0.5],true," + time + ");" +
            "rows.push([P[i][0],P[i][1],c[0],c[1],c[2],c[3]].join(','));}\nrows.join('\\n');";
    }
    function parseSamples(text, points) {
        var lines = String(text).split(/\r\n|\r|\n/), a = [], i, j, parts, values;
        if (lines.length !== points.length) { throw new Error("Unexpected sample count: " + lines.length); }
        for (i = 0; i < lines.length; i++) {
            parts = lines[i].split(","); values = [];
            if (parts.length !== 6 || Number(parts[0]) !== points[i][0] || Number(parts[1]) !== points[i][1]) {
                throw new Error("Malformed sample row " + i);
            }
            for (j = 2; j < 6; j++) {
                if (!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$|^[+-]?Infinity$|^NaN$/i.test(parts[j])) {
                    throw new Error("Non-numeric sample component in row " + i);
                }
                values.push(Number(parts[j]));
            }
            a.push({point: points[i], rgba: values});
        }
        return a;
    }
    try {
        if (!project || project.renderQueue.rendering) { throw new Error("Open an idle test project first."); }
        var comp = findComp(), sourceLayer = comp.layer(1), originalEffect = findEffect(sourceLayer);
        if (!(sourceLayer.source instanceof CompItem) || sourceLayer.threeDLayer) {
            throw new Error("The effect must be on a 2D precomp layer, not a 3D layer or footage.");
        }
        var time = comp.time;
        if (time < sourceLayer.inPoint || time >= sourceLayer.outPoint || time < 0 || time >= comp.duration) {
            throw new Error("Place the playhead inside the precomp layer duration before running.");
        }
        initialBpc = project.bitsPerChannel;
        report.environment = {aeVersion: app.version, aeBuild: optional(app, "buildNumber"), os: $.os,
            project: project.file ? project.file.name : "UNSAVED", initialBpc: initialBpc,
            projectDirtyAtStart: optional(project, "dirty"),
            workingSpace: optional(project, "workingSpace"), linearizeWorkingSpace: optional(project, "linearizeWorkingSpace"),
            linearBlending: optional(project, "linearBlending"), expressionEngine: optional(project, "expressionEngine"),
            projectGpuSetting: String(optional(project, "gpuAccelType")), sourceRenderer: sourceLayer.source.renderer,
            sourceResolution: sourceLayer.source.resolutionFactor, sourceComp: sourceLayer.source.name,
            originalCollapse: sourceLayer.collapseTransformation, time: time, initialParameters: parameters(originalEffect, time)};
        out = new Folder(Folder.desktop.fsName + "/AE_Depth_" + runId);
        if (out.exists || !out.create()) { throw new Error("Cannot create a unique output folder on Desktop."); }
        report.status = "RUNNING"; checkpoint(); // Permission test before changing the project.
        app.beginUndoGroup(BUILD); undo = true;
        scratch = comp.duplicate(); scratch.name = "__" + runId;
        scratch.resolutionFactor = [1, 1]; scratch.preserveNestedResolution = false;
        var layer = scratch.layer(1); layer.locked = false; layer.enabled = true;
        layer.quality = LayerQuality.BEST;
        var fx = findEffect(layer), n, p;
        // Only remove animation/expression from the disposable copy, never from the source fixture.
        for (n = 1; n <= 6; n++) {
            p = fx.property(n);
            if (p.canSetExpression) { p.expression = ""; }
            while (p.numKeys > 0) { p.removeKey(1); }
        }
        var sampler = scratch.layers.addText("");
        sampler.name = "__sampleImage_probe"; sampler.enabled = false; sampler.guideLayer = true;
        var textProperty = sampler.property("ADBE Text Properties").property("ADBE Text Document");
        var points = [], x, y;
        for (y = 0; y < 5; y++) { for (x = 0; x < 9; x++) {
            points.push([Math.round((x + 0.5) * layer.width / 9 - 0.5), Math.round((y + 0.5) * layer.height / 5 - 0.5)]);
        } }
        report.grid = {width: layer.width, height: layer.height, points: points};
        // id, black, white, invert, AA, collapse, effectEnabled, clamp-request
        var cases = [["baseline",5000,0,0,0,0,1,1], ["invert",5000,0,1,0,0,1,1],
            ["equal",1000,1000,0,0,0,1,1], ["reversed",0,5000,0,0,0,1,1],
            ["narrow",1000,2000,0,0,0,1,1], ["narrow_aa",1000,2000,0,1,0,1,1],
            ["collapse_on",5000,0,0,0,1,1,1], ["source_color_control",5000,0,0,0,0,0,1],
            ["baseline_repeat",5000,0,0,0,0,1,1], ["clamp_off_request",1000,2000,0,0,0,1,0]];
        var depths = [8,16,32], d, c, spec, record, doc, errors = 0;
        report.plannedCases = 28;
        for (d = 0; d < depths.length; d++) {
            project.bitsPerChannel = depths[d];
            if (project.bitsPerChannel !== depths[d]) { throw new Error("Project bit depth was not applied."); }
            for (c = 0; c < cases.length; c++) {
                spec = cases[c];
                if (spec[0] === "clamp_off_request" && depths[d] !== 32) { continue; }
                if (new Date().getTime() - start > 180000) { throw new Error("Soft 180-second budget exceeded between host calls."); }
                record = {id: spec[0], bpc: depths[d], status: "RUNNING", requested: spec.slice(1)};
                report.cases.push(record); checkpoint(); // A hang leaves RUNNING, never a false PASS.
                try {
                    layer.collapseTransformation = Boolean(spec[5]); fx.enabled = Boolean(spec[6]);
                    fx.property(2).setValue(spec[1]); fx.property(3).setValue(spec[2]);
                    fx.property(4).setValue(spec[4]); fx.property(6).setValue(spec[3]);
                    if (depths[d] === 32) { fx.property(5).setValue(spec[7]); }
                    record.parametersBefore = parameters(fx, time);
                    if (record.parametersBefore[1].value !== spec[1] || record.parametersBefore[2].value !== spec[2] ||
                        record.parametersBefore[3].value !== spec[4] || record.parametersBefore[5].value !== spec[3] ||
                        layer.collapseTransformation !== Boolean(spec[5]) || fx.enabled !== Boolean(spec[6])) {
                        throw new Error("Requested core settings were overridden by the host; case not sampled.");
                    }
                    // Do not force the disabled channel popup or infer a private channel FourCC.
                    record.actualCollapse = layer.collapseTransformation;
                    record.actualEffectEnabled = fx.enabled;
                    record.clampRequestApplied = depths[d] === 32 ? record.parametersBefore[4].value === spec[7] : null;
                    textProperty.expression = expression(layer.index, points, time, runId + "-" + depths[d] + "-" + c);
                    textProperty.expressionEnabled = true;
                    doc = textProperty.valueAtTime(time, false);
                    if (textProperty.expressionError) { throw new Error(textProperty.expressionError); }
                    record.samples = parseSamples(doc.text, points);
                    record.parametersAfter = parameters(fx, time);
                    record.status = "RECORDED";
                } catch (caseError) {
                    record.status = "ERROR"; record.error = String(caseError); errors++;
                    // Stop rather than repeat a failed host call or malformed sample 28 times.
                    throw caseError;
                }
                checkpoint();
            }
        }
        report.status = errors ? "PARTIAL" : "COLLECTED";
    } catch (e) {
        fatal = String(e); report.status = "ERROR"; report.error = fatal;
    } finally {
        if (scratch) { try { scratch.remove(); } catch (e1) { report.cleanupErrors.push(String(e1)); } }
        if (initialBpc !== null) {
            try {
                project.bitsPerChannel = initialBpc;
                if (project.bitsPerChannel !== initialBpc) { throw new Error("Bit-depth restore verification failed."); }
            } catch (e2) { report.cleanupErrors.push(String(e2)); }
        }
        if (undo) { try { app.endUndoGroup(); } catch (e3) { report.cleanupErrors.push(String(e3)); } }
        if (report.cleanupErrors.length) { report.status = "ERROR"; }
        try { checkpoint(); } catch (ioError) { fatal = String(ioError); report.status = "ERROR"; }
    }
    var message = "Z-Depth: " + report.status + ". Записей: " + report.cases.length + ".\n";
    if (out) { message += "Отчёт: " + out.fsName + "/report.json\n"; }
    if (fatal) { message += "Ошибка: " + fatal + "\n"; }
    if (report.cleanupErrors.length) { message += "ВНИМАНИЕ: восстановление состояния не завершено.\n"; }
    message += "Исходный .aep скрипт не сохранял. COLLECTED — сбор данных, не итоговая приёмка.";
    alert(message);
    if (out) { try { out.execute(); } catch (ignored) {} }
})();
