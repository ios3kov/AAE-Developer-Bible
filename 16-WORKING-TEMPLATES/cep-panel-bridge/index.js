(function () {
  var cs = new CSInterface();
  var status = document.getElementById('status');
  var sequence = 0;
  var latestRequestId = null;

  function callHost(command, payload) {
    sequence += 1;

    var requestId = String(Date.now()) + "-" + String(sequence);
    latestRequestId = requestId;

    var req = {
      protocol: 1,
      requestId: requestId,
      command: command,
      payload: payload || {}
    };

    var json = JSON.stringify(req);
    var arg = JSON.stringify(json); // safely quoted JS string literal

    cs.evalScript('$._aeBible.dispatch(' + arg + ')', function (raw) {
      var res;

      try {
        res = JSON.parse(raw);
      } catch (e) {
        if (requestId === latestRequestId) {
          status.textContent = 'Bad host response: ' + raw;
        }
        return;
      }

      // A newer UI request superseded this reply.
      if (res.requestId !== latestRequestId) {
        return;
      }

      status.textContent = JSON.stringify(res, null, 2);
    });
  }

  document.getElementById('rename').addEventListener('click', function () {
    callHost('renameSelected', { prefix: 'Bible_' });
  });
})();
