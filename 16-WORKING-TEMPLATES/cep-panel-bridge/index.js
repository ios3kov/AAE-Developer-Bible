(function () {
  var cs = new CSInterface();
  var status = document.getElementById('status');

  function callHost(method, params) {
    var req = {
      version: 1,
      requestId: String(Date.now()),
      method: method,
      params: params || {}
    };
    var json = JSON.stringify(req);
    var arg = JSON.stringify(json); // safely quoted JS string literal
    cs.evalScript('$._aeBible.dispatch(' + arg + ')', function (raw) {
      try {
        var res = JSON.parse(raw);
        status.textContent = JSON.stringify(res, null, 2);
      } catch (e) {
        status.textContent = 'Bad host response: ' + raw;
      }
    });
  }

  document.getElementById('rename').addEventListener('click', function () {
    callHost('renameSelected', { prefix: 'Bible_' });
  });
})();
