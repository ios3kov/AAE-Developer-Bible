#target aftereffects
/* AE Developer Bible -- ACX-EDGE-20260930-02.
 * Adaptive edge sampling + six one-frame Render Queue exports, not the old 28-case batch.
 * Run in an idle, open DEPTH_TEST fixture. Only a disposable outer comp is edited.
 * No save, preference changes, cache purge, source edits, binary patches or MFR claims.
 * Uses installed output templates, inspected by actual Format; never invents a template.
 * Runtime validation is pending. See EDGE-AND-RENDER-PROBE.md for evidence boundaries.
 */
(function () {
    var BUILD = "ACX-EDGE-20260930-02", MATCH = "ADBE AUX CHANNEL EXTRACT";
    var start = new Date().getTime(), runId = BUILD + "-" + start + "-" + Math.floor(Math.random()*1000000);
    var project = app.project, scratch = null, ownRQ = null, out = null, initialBpc = null, undo = false;
    var suspended = [], fatal = null, probeText = null, layer = null, time = 0, sampleSerial = 0;
    var report = {schema:2, build:BUILD, runId:runId, status:"PREFLIGHT", cases:[], exports:[],
        cleanupErrors:[], outputTemplates:[], limitations:[
            "RECORDED/EXPORTED are acquisition states, not full-effect acceptance PASS.",
            "sampleImage is alpha-weighted area sampling; fractional sample positions are not raw pixels.",
            "Render Queue exports include outer-layer transforms and output-module color/precision processing.",
            "Project bpc is not necessarily the exported file precision; inspect image headers after collection.",
            "No private FourCC trace, loaded binary hash, cold-cache or MFR/concurrent-render proof.",
            "A soft 300-second budget is checked between host calls, not a watchdog for a hung AE.",
            "Temporary edits can mark the project dirty; the original AEP is never saved by this script."
        ]};
    function quote(s) {
        return '"'+String(s).replace(/[\\"\x00-\x1f\u2028\u2029]/g,function(c){
            return c==='"'||c==='\\'?'\\'+c:'\\u'+('0000'+c.charCodeAt(0).toString(16)).slice(-4);
        })+'"';
    }
    function json(v) {
        var a=[],k;
        if(v===null||typeof v==='undefined'){return 'null';}
        if(typeof v==='string'){return quote(v);}
        if(typeof v==='number'){return isFinite(v)?String(v):quote(String(v));}
        if(typeof v==='boolean'){return String(v);}
        if(v instanceof Array){for(k=0;k<v.length;k++){a.push(json(v[k]));}return '['+a.join(',')+']';}
        for(k in v){if(v.hasOwnProperty(k)){a.push(quote(k)+':'+json(v[k]));}}return '{'+a.join(',')+'}';
    }
    function optional(o,k){try{return typeof o[k]==='undefined'?null:o[k];}catch(e){return 'UNAVAILABLE: '+e;}}
    function budget(){if(new Date().getTime()-start>300000){throw Error('Soft time budget exceeded between host calls.');}}
    function checkpoint(){
        if(!out){return;}
        report.elapsedMs=new Date().getTime()-start;
        var f=new File(out.fsName+'/report.json');f.encoding='UTF-8';
        if(!f.open('w')){throw Error('Cannot write report; allow script file access in AE preferences.');}
        var ok=f.write(json(report)+'\n'),closed=f.close();
        if(!ok||!closed){throw Error('Report write/close failed.');}
    }
    function effect(l){
        var p=l.property('ADBE Effect Parade');
        if(!p||p.numProperties!==1||p.property(1).matchName!==MATCH){throw Error('Only 3D Channel Extract must be on the test layer.');}
        var e=p.property(1),i;
        if(e.numProperties<6){throw Error('Unexpected effect layout.');}
        for(i=1;i<=6;i++){if(typeof e.property(i).value!=='number'){throw Error('Unexpected parameter '+i);}}
        return e;
    }
    function params(e){var a=[],i,p;for(i=1;i<=6;i++){p=e.property(i);a.push(p.valueAtTime(time,false));}return a;}
    function state(aa){
        var e=effect(layer);
        e.enabled=true;layer.collapseTransformation=false;
        e.property(2).setValue(5000);e.property(3).setValue(0);
        e.property(4).setValue(aa);e.property(6).setValue(0);
        if(project.bitsPerChannel===32){e.property(5).setValue(1);}
        var p=params(e);
        if(p[0]!==1||p[1]!==5000||p[2]!==0||p[3]!==aa||p[5]!==0||layer.collapseTransformation||!e.enabled||
            (project.bitsPerChannel===32&&p[4]!==1)){throw Error('Requested depth state was overridden; refusing to measure another state.');}
        return p;
    }
    function expression(points){
        return '// '+runId+'-'+(++sampleSerial)+'\nvar L=thisComp.layer('+layer.index+');var P='+json(points)+';var rows=[];\n'+
            'for(var i=0;i<P.length;i++){var c=L.sampleImage(P[i],[0.5,0.5],true,'+time+');'+
            "rows.push([P[i][0],P[i][1],c[0],c[1],c[2],c[3]].join(','));}rows.join('\\n');";
    }
    function parse(text,points){
        var lines=String(text).split(/\r\n|\n|\r/),a=[],i,j,p,v;
        if(lines.length!==points.length){throw Error('Unexpected sample count.');}
        for(i=0;i<lines.length;i++){
            p=lines[i].split(',');v=[];
            if(p.length!==6||Number(p[0])!==points[i][0]||Number(p[1])!==points[i][1]){throw Error('Malformed sample row '+i);}
            for(j=2;j<6;j++){
                if(!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$|^[+-]?Infinity$|^NaN$/i.test(p[j])){throw Error('Invalid RGBA value.');}
                v.push(Number(p[j]));
            }
            a.push({point:points[i],rgba:v});
        }return a;
    }
    function sample(points){
        var all=[],offset,chunk,doc,part,j;
        for(offset=0;offset<points.length;offset+=96){
            budget();report.samplingCheckpoint={serial:sampleSerial+1,offset:offset,total:points.length};checkpoint();
            chunk=points.slice(offset,offset+96);probeText.expression=expression(chunk);probeText.expressionEnabled=true;
            doc=probeText.valueAtTime(time,false);
            if(probeText.expressionError){throw Error(probeText.expressionError);}
            part=parse(doc.text,chunk);for(j=0;j<part.length;j++){all.push(part[j]);}
        }return all;
    }
    function scanlines(w,h){
        var lines=[],axis,k,step,p,fixed,n,max;
        for(axis=0;axis<2;axis++){for(k=1;k<=3;k++){
            fixed=Math.round((axis?w:h)*k/4);max=axis?h:w;
            step=16;p=[];
            for(n=0;n<max;n+=step){p.push(axis?[fixed,n]:[n,fixed]);}
            if((axis?p[p.length-1][1]:p[p.length-1][0])!==max-1){p.push(axis?[fixed,max-1]:[max-1,fixed]);}
            lines.push({axis:axis===0?'horizontal':'vertical',points:p});
        }}return lines;
    }
    function delta(a,b){var d=0,k;for(k=0;k<4;k++){if(!isFinite(a[k])||!isFinite(b[k])){return null;}d=Math.max(d,Math.abs(a[k]-b[k]));}return d;}
    function edgePoints(lines,w,h){
        var brackets=[],selected=[],points=[],seen={},i,j,d,a,b,k,n,t,p,key;
        for(i=0;i<lines.length;i++){for(j=1;j<lines[i].samples.length;j++){
            a=lines[i].samples[j-1];b=lines[i].samples[j];d=delta(a.rgba,b.rgba);
            if(d!==null&&d>0.02){brackets.push({axis:lines[i].axis,a:a.point,b:b.point,change:d});}
        }}
        brackets.sort(function(x,y){return y.change-x.change;});
        for(i=0;i<brackets.length&&selected.length<16;i++){
            a=brackets[i];selected.push(a);k=a.axis==='horizontal'?0:1;
            // Pixel centers and quarter-offset area samples on BOTH sides of each detected transition.
            for(n=Math.max(0,a.a[k]-2);n<=Math.min((k===0?w:h)-1,a.b[k]+2);n++){
                for(t=0;t<4;t++){
                    p=[a.a[0],a.a[1]];p[k]=n+t/4;
                    if(p[0]>w-1||p[1]>h-1){continue;}
                    key=p[0]+','+p[1];if(!seen[key]){seen[key]=true;points.push(p);}
                }
            }
        }
        return {threshold:0.02,bracketsFound:brackets.length,selected:selected,points:points,
            note:'At most 16 transition brackets on six scanlines, not exhaustive edge coverage.'};
    }
    function compare(a,b){
        var max=0,changed=0,nonfinite=0,i,d;
        if(a.length!==b.length){throw Error('Different edge sample counts.');}
        for(i=0;i<a.length;i++){
            if(json(a[i].point)!==json(b[i].point)){throw Error('Unpaired edge locations.');}
            d=delta(a[i].rgba,b[i].rgba);if(d===null){nonfinite++;continue;}
            if(d>0){changed++;}max=Math.max(max,d);
        }
        return {pairedLocations:a.length,changedLocations:changed,maxAbsRGBA:max,nonfinitePairs:nonfinite,
            interpretation:'Descriptive comparison only. No change is not proof that anti-aliasing is absent.'};
    }
    function classify(settings){
        var f=String(settings.Format||'').toLowerCase();
        if(/openexr/.test(f)){return {kind:'exr',ext:'exr',rank:400};}
        if(/tiff/.test(f)){return {kind:'tiff',ext:'tif',rank:300};}
        if(/png/.test(f)){return {kind:'png',ext:'png',rank:200};}
        if(/photoshop/.test(f)){return {kind:'psd',ext:'psd',rank:100};}
        return null;
    }
    function selectTemplate(inventory,bpc){
        var best=null,i,x,c,depth,score;
        for(i=0;i<inventory.length;i++){
            x=inventory[i];if(!x.settings){continue;}c=classify(x.settings);if(!c){continue;}
            depth=String(x.settings.Depth||'');
            // Preserve >=16-bpc container capacity for 16-bit projects; float capacity for 32.
            if(bpc===32&&c.kind!=='exr'&&!/float|32\s*bit/i.test(depth)){continue;}
            if(bpc===16&&c.kind!=='exr'&&!/float|trillions|16\s*bit|32\s*bit/i.test(depth)){continue;}
            score=c.rank+(/alpha|\+/.test(String(x.settings.Channels||'').toLowerCase()+depth)?10:0);
            if(!best||score>best.score){best={name:x.name,kind:c.kind,ext:c.ext,score:score,settings:x.settings};}
        }return best;
    }
    function inspectTemplates(){
        var names=ownRQ.outputModule(1).templates,i,s;
        if(names.length>128){throw Error('More than 128 output templates; export inspection budget exceeded.');}
        for(i=0;i<names.length;i++){
            budget();s={name:names[i]};
            try{ownRQ.outputModule(1).applyTemplate(names[i]);s.settings=ownRQ.outputModule(1).getSettings(GetSettingsFormat.STRING);}
            catch(e){s.error=String(e);}
            report.outputTemplates.push(s);
        }
    }
    function suspendQueue(){
        var rq=project.renderQueue,i,item;
        // Inspect all queued callbacks before touching any existing flag.
        for(i=1;i<=rq.numItems;i++){
            item=rq.item(i);if(item===ownRQ){continue;}
            if(item.status===RQItemStatus.QUEUED&&item.onStatusChanged){throw Error('Existing queued item has a callback; export blocked without changing it.');}
        }
        for(i=1;i<=rq.numItems;i++){
            item=rq.item(i);if(item===ownRQ){continue;}
            if(item.status===RQItemStatus.QUEUED){
                suspended.push(item);item.render=false;
                if(item.render||item.status!==RQItemStatus.UNQUEUED){throw Error('Could not safely suspend existing queue.');}
            }
        }
    }
    function onlyOwnedQueued(){
        var rq=project.renderQueue,i,item;
        for(i=1;i<=rq.numItems;i++){item=rq.item(i);if(item!==ownRQ&&item.status===RQItemStatus.QUEUED){throw Error('Another queued item appeared; refusing render.');}}
    }
    function signature(file,kind){
        file.encoding='BINARY';if(!file.open('r')){throw Error('Cannot read exported frame.');}
        var b=file.read(8),closed=file.close(),ok=false;
        if(!closed){throw Error('Cannot close exported frame.');}
        if(kind==='exr'){ok=b.substr(0,4)==='\x76\x2f\x31\x01';}
        if(kind==='png'){ok=b==='\x89PNG\r\n\x1a\n';}
        if(kind==='tiff'){ok=b.substr(0,4)==='II\x2a\x00'||b.substr(0,4)==='MM\x00\x2a';}
        if(kind==='psd'){ok=b.substr(0,4)==='8BPS';}
        if(!ok){throw Error('Exported frame signature does not match selected format.');}
    }
    function renderOne(bpc,aa,choice){
        var r={bpc:bpc,aa:aa,status:'RUNNING',time:time,framesRequested:1};report.exports.push(r);checkpoint();
        var folder=new Folder(out.fsName+'/frame_'+bpc+'bpc_AA'+aa);
        if(folder.exists||!folder.create()){throw Error('Cannot create unique frame directory.');}
        r.parametersBefore=state(aa);ownRQ=project.renderQueue.items.add(scratch);ownRQ.render=false;
        ownRQ.setSettings({'Quality':'Best','Effects':'All On','Resolution':'Full','Color Depth':bpc+' bits per channel'});
        ownRQ.timeSpanStart=time;ownRQ.timeSpanDuration=scratch.frameDuration*0.5;ownRQ.skipFrames=0;
        if(ownRQ.numOutputModules!==1){throw Error('Expected exactly one owned output module.');}
        r.renderSettings=ownRQ.getSettings(GetSettingsFormat.STRING);
        if(String(r.renderSettings['Color Depth']).indexOf(String(bpc))<0||r.renderSettings.Quality!=='Best'||
            r.renderSettings.Effects!=='All On'||r.renderSettings.Resolution!=='Full'){
            throw Error('Render settings readback differs from requested depth/quality.');
        }
        ownRQ.outputModule(1).applyTemplate(choice.name);
        var om=ownRQ.outputModule(1),settable=om.getSettings(GetSettingsFormat.STRING_SETTABLE),clean={};
        if(settable.hasOwnProperty('Crop')){clean.Crop=false;}
        if(settable.hasOwnProperty('Resize')){clean.Resize=false;}
        om.setSettings(clean); // Reacquire after changing settings: AE can invalidate the previous object.
        om=ownRQ.outputModule(1);om.postRenderAction=PostRenderAction.NONE;om.includeSourceXMP=false;
        om.file=new File(folder.fsName+'/frame_[#####].'+choice.ext);
        r.outputTemplate=choice.name;r.outputSettings=ownRQ.outputModule(1).getSettings(GetSettingsFormat.STRING);
        var fmt=classify(r.outputSettings),crop=String(r.outputSettings.Crop),resize=String(r.outputSettings.Resize);
        if(!fmt||fmt.kind!==choice.kind||/^(true|on|1)$/i.test(crop)||/^(true|on|1)$/i.test(resize)){
            throw Error('Unexpected output format, crop or resize.');
        }
        if(ownRQ.outputModule(1).file.parent.fsName!==folder.fsName){throw Error('Output path escaped the run directory.');}
        onlyOwnedQueued();ownRQ.render=true;checkpoint();budget();project.renderQueue.render();
        r.queueStatus=String(ownRQ.status);r.elapsedSeconds=ownRQ.elapsedSeconds;
        if(ownRQ.status!==RQItemStatus.DONE){throw Error('Render stopped or failed; no further frames will be attempted.');}
        var entries=folder.getFiles(),images=[],i,f;
        for(i=0;i<entries.length;i++){
            f=entries[i];if(f instanceof File&&new RegExp('\\.'+choice.ext+'$','i').test(f.name)){images.push(f);}
        }
        if(images.length!==1||images[0].length<=8){throw Error('DONE without exactly one nonempty expected image (found '+images.length+').');}
        signature(images[0],choice.kind);
        r.file={relativePath:folder.name+'/'+images[0].name,bytes:images[0].length,format:choice.kind,
            integrity:'signature screened; full decode, component precision and hashes pending offline analysis'};
        r.parametersAfter=params(effect(layer));
        if(json(r.parametersAfter)!==json(r.parametersBefore)){throw Error('Effect settings changed during render.');}
        r.status='EXPORTED';ownRQ.remove();ownRQ=null;checkpoint();
    }
    function main(){
        var c=null,i,j,item,e,p,original,scan,points=[],all,offset,selected,depths=[8,16,32],d,aa,r,pair,choice;
        if(!project||project.renderQueue.rendering){throw Error('Open an idle test project.');}
        for(i=1;i<=project.renderQueue.numItems;i++){
            item=project.renderQueue.item(i);
            if(item.status===RQItemStatus.RENDERING||item.status===RQItemStatus.WILL_CONTINUE){throw Error('A render is active or paused.');}
        }
        for(i=1;i<=project.numItems;i++){
            item=project.item(i);if(item instanceof CompItem&&item.name==='DEPTH_TEST'){if(c){throw Error('Ambiguous DEPTH_TEST.');}c=item;}
        }
        if(!c||c.numLayers!==1){throw Error('DEPTH_TEST must contain exactly one precomp layer.');}
        original=c.layer(1);e=effect(original);
        if(!(original.source instanceof CompItem)||original.threeDLayer){throw Error('A 2D precomp layer is required.');}
        if(original.source.useProxy){throw Error('Disable the source proxy before a controlled depth test.');}
        time=Math.round(c.time/c.frameDuration)*c.frameDuration;
        if(time<0||time>=c.duration||time<original.inPoint||time>=original.outPoint){throw Error('Playhead must be inside the source layer duration.');}
        if(e.property(1).valueAtTime(time,false)!==1){throw Error('Expected Z-Depth selection; disabled popup will not be forced.');}
        if(original.width<1||original.height<1||original.width>8192||original.height>8192){throw Error('Fixture dimensions outside this probe budget.');}
        initialBpc=project.bitsPerChannel;
        report.environment={aeVersion:app.version,aeBuild:optional(app,'buildNumber'),os:$.os,
            project:project.file?project.file.name:'UNSAVED',dirtyAtStart:optional(project,'dirty'),initialBpc:initialBpc,
            workingSpace:optional(project,'workingSpace'),linearizeWorkingSpace:optional(project,'linearizeWorkingSpace'),
            linearBlending:optional(project,'linearBlending'),expressionEngine:optional(project,'expressionEngine'),
            gpuSetting:String(optional(project,'gpuAccelType')),sourceRenderer:original.source.renderer,
            sourceResolution:original.source.resolutionFactor,sourceComp:original.source.name,
            originalCollapse:original.collapseTransformation,requestedTime:c.time,frameAlignedTime:time,
            frameDuration:c.frameDuration,initialParameters:params(e),
            outerComp:{width:c.width,height:c.height,pixelAspect:c.pixelAspect},
            sourceLayer:{width:original.width,height:original.height,startTime:original.startTime,stretch:original.stretch},
            loadedBinaryIdentity:'NOT MEASURED'};
        out=new Folder(Folder.desktop.fsName+'/AE_Edge_Render_'+runId);
        if(out.exists||!out.create()){throw Error('Cannot create unique report folder.');}
        report.status='RUNNING';checkpoint(); // Verify file access before project mutation.
        app.beginUndoGroup(BUILD);undo=true;
        scratch=c.duplicate();scratch.name='__'+runId;scratch.resolutionFactor=[1,1];scratch.preserveNestedResolution=false;
        layer=scratch.layer(1);layer.locked=false;layer.enabled=true;layer.quality=LayerQuality.BEST;
        e=effect(layer);for(i=1;i<=6;i++){p=e.property(i);if(p.canSetExpression){p.expression='';}while(p.numKeys){p.removeKey(1);}}
        var sampler=scratch.layers.addText('');sampler.name='__ACX_EDGE_SAMPLER';sampler.enabled=false;sampler.guideLayer=true;
        probeText=sampler.property('ADBE Text Properties').property('ADBE Text Document');
        project.bitsPerChannel=32;if(project.bitsPerChannel!==32){throw Error('Cannot set discovery depth to 32 bpc.');}
        state(0);scan=scanlines(layer.width,layer.height);
        for(i=0;i<scan.length;i++){for(j=0;j<scan[i].points.length;j++){points.push(scan[i].points[j]);}}
        all=sample(points);offset=0;
        for(i=0;i<scan.length;i++){scan[i].samples=all.slice(offset,offset+scan[i].points.length);offset+=scan[i].points.length;}
        report.discovery={bpc:32,aa:0,black:5000,white:0,scanlines:scan};selected=edgePoints(scan,layer.width,layer.height);report.edges=selected;
        if(!selected.points.length){report.edgeStatus='BLOCKED_NO_TRANSITIONS';}
        else{
            for(d=0;d<depths.length;d++){
                project.bitsPerChannel=depths[d];if(project.bitsPerChannel!==depths[d]){throw Error('Bpc write rejected.');}pair=[];
                for(aa=0;aa<=1;aa++){
                    r={id:'edge_AA'+aa,bpc:depths[d],aa:aa,status:'RUNNING'};report.cases.push(r);checkpoint();
                    r.parametersBefore=state(aa);r.samples=sample(selected.points);r.parametersAfter=params(effect(layer));
                    if(json(r.parametersBefore)!==json(r.parametersAfter)){throw Error('Parameters changed during sampling.');}
                    r.status='RECORDED';pair.push(r);checkpoint();
                }
                pair[1].comparisonWithAA0=compare(pair[0].samples,pair[1].samples);
            }
            report.edgeStatus='RECORDED';
        }
        app.endUndoGroup();undo=false; // Do not hold an undo group across Render Queue rendering.
        // Probe only this disposable queue item. No existing output template is edited or saved.
        ownRQ=project.renderQueue.items.add(scratch);ownRQ.render=false;
        inspectTemplates();ownRQ.remove();ownRQ=null;checkpoint();
        try{suspendQueue();}catch(queueError){report.exportStatus='BLOCKED';report.exportError=String(queueError);return;}
        report.exportStatus='RUNNING';
        for(d=0;d<depths.length;d++){
            budget();project.bitsPerChannel=depths[d];if(project.bitsPerChannel!==depths[d]){throw Error('Bpc write rejected before export.');}
            choice=selectTemplate(report.outputTemplates,depths[d]);
            if(!choice){
                for(aa=0;aa<=1;aa++){report.exports.push({bpc:depths[d],aa:aa,status:'BLOCKED',reason:'No suitable installed image template for requested precision; inventory retained.'});}
                continue;
            }
            for(aa=0;aa<=1;aa++){renderOne(depths[d],aa,choice);}
        }
        report.exportStatus='EXPORTED';
        for(i=0;i<report.exports.length;i++){if(report.exports[i].status!=='EXPORTED'){report.exportStatus='PARTIAL';}}
    }
    try{
        main();report.status=report.edgeStatus==='RECORDED'&&report.exportStatus==='EXPORTED'?'COLLECTED':'PARTIAL';
    }catch(e){
        fatal=String(e);report.error=fatal;report.status='ERROR';
        if(report.exports.length&&report.exports[report.exports.length-1].status==='RUNNING'){
            report.exports[report.exports.length-1].status='ERROR';report.exports[report.exports.length-1].error=fatal;
        }
    }finally{
        if(ownRQ){try{ownRQ.remove();ownRQ=null;}catch(e1){report.cleanupErrors.push('Queue item: '+e1);}}
        for(var s=0;s<suspended.length;s++){
            try{suspended[s].render=true;if(!suspended[s].render||suspended[s].status!==RQItemStatus.QUEUED){throw Error('Restore readback failed.');}}
            catch(e2){report.cleanupErrors.push('Existing queue restore: '+e2);}
        }
        if(scratch){try{scratch.remove();}catch(e3){report.cleanupErrors.push('Temporary comp: '+e3);}}
        if(initialBpc!==null){try{project.bitsPerChannel=initialBpc;if(project.bitsPerChannel!==initialBpc){throw Error('Restore readback failed.');}}
            catch(e4){report.cleanupErrors.push('Bpc restore: '+e4);}}
        if(undo){try{app.endUndoGroup();}catch(e5){report.cleanupErrors.push('Undo: '+e5);}}
        if(report.cleanupErrors.length){report.status='ERROR';}
        try{checkpoint();}catch(ioError){report.status='ERROR';fatal=String(ioError);}
    }
    var message='ACX edges / render: '+report.status+'\n';
    if(out){message+='Папка результатов: '+out.fsName+'\n';}
    if(fatal){message+='Ошибка: '+fatal+'\n';}
    if(report.cleanupErrors.length){message+='ВНИМАНИЕ: восстановление состояния не завершено.\n';}
    message+='Исходный AEP не сохранён скриптом. Пришлите папку результатов целиком (ZIP).';
    alert(message);if(out){try{out.execute();}catch(ignored){}}
})();
