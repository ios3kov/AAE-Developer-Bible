(function () {
  "use strict";

  var status = document.getElementById("status");
  var renameButton = document.getElementById("rename");

  if (!status || !renameButton) {
    throw new Error("Missing required panel elements");
  }

  var cs;
  var sequence = 0;
  var sessionId = String(new Date().getTime()) + "-" +
    String(Math.random()).slice(2);

  var busy = false;
  var blocked = true;
  var closed = false;

  // Product policy, not a CEP transport limit.
  var MAX_MESSAGE_CHARS = 65536;
  var WAIT_MS = 15000;

  function show(message) {
    status.textContent = message;
  }

  function updateButton() {
    renameButton.disabled = busy || blocked || closed;
  }

  function isObject(value) {
    return value !== null &&
      Object.prototype.toString.call(value) === "[object Object]";
  }

  function owns(object, name) {
    return Object.prototype.hasOwnProperty.call(object, name);
  }

  function fail(message) {
    throw new Error(message);
  }

  function stringLiteral(text) {
    return JSON.stringify(text)
      .replace(/\u2028/g, "\\u2028")
      .replace(/\u2029/g, "\\u2029");
  }

  function validateRequest(req) {
    if (!isObject(req) ||
        req.protocol !== 1 ||
        typeof req.requestId !== "string" ||
        req.requestId.length === 0 ||
        req.requestId.length > 128 ||
        !isObject(req.payload)) {
      fail("INVALID_REQUEST");
    }

    if (req.command !== "ping" && req.command !== "renameSelected") {
      fail("UNKNOWN_COMMAND");
    }

    if (req.command === "renameSelected" &&
        (!owns(req.payload, "prefix") ||
         typeof req.payload.prefix !== "string" ||
         req.payload.prefix.length > 256)) {
      fail("INVALID_PAYLOAD");
    }
  }

  function makeSource(req) {
    validateRequest(req);

    var raw = JSON.stringify(req);

    if (typeof raw !== "string" || raw.length > MAX_MESSAGE_CHARS) {
      fail("REQUEST_TOO_LARGE");
    }

    // This fixed fallback does not require JSON in ExtendScript.
    var unavailable =
      '{"protocol":1,"requestId":null,"ok":false,' +
      '"error":{"code":"BOOTSTRAP_FAILED",' +
      '"message":"Host dispatcher is not loaded.",' +
      '"outcome":"notApplied"}}';

    return "(function () {" +
      "if (!$._aeBible || " +
      "typeof $._aeBible.dispatch !== 'function') {" +
      "return " + stringLiteral(unavailable) + ";" +
      "}" +
      "return $._aeBible.dispatch(" + stringLiteral(raw) + ");" +
      "}())";
  }

  function parseResponse(raw, request) {
    if (typeof raw !== "string" || raw.length > MAX_MESSAGE_CHARS) {
      fail("MALFORMED_RESPONSE");
    }

    if (raw === "EvalScript error." ||
        (typeof EvalScript_ErrMessage !== "undefined" &&
         raw === EvalScript_ErrMessage)) {
      fail("BRIDGE_EXECUTION_FAILED");
    }

    var res;

    try {
      res = JSON.parse(raw);
    } catch (error) {
      fail("MALFORMED_RESPONSE: invalid JSON");
    }

    if (!isObject(res) ||
        !owns(res, "protocol") || res.protocol !== 1 ||
        !owns(res, "requestId") ||
        !owns(res, "ok") || typeof res.ok !== "boolean") {
      fail("MALFORMED_RESPONSE: invalid envelope");
    }

    if (res.ok) {
      if (res.requestId !== request.requestId ||
          !owns(res, "result") ||
          owns(res, "error") ||
          !isObject(res.result)) {
        fail("MALFORMED_RESPONSE: invalid success");
      }

      if (request.command === "ping") {
        if (res.result.ready !== true ||
            res.result.protocol !== 1) {
          fail("MALFORMED_RESPONSE: invalid handshake");
        }
      } else {
        var changed = res.result.changed;

        if (typeof changed !== "number" ||
            !isFinite(changed) ||
            changed < 0 ||
            Math.floor(changed) !== changed) {
          fail("MALFORMED_RESPONSE: invalid changed count");
        }
      }

      return res;
    }

    if (owns(res, "result") ||
        !owns(res, "error") ||
        !isObject(res.error) ||
        typeof res.error.code !== "string" ||
        res.error.code.length === 0 ||
        typeof res.error.message !== "string" ||
        (res.error.outcome !== "notApplied" &&
         res.error.outcome !== "mayHaveApplied")) {
      fail("MALFORMED_RESPONSE: invalid error");
    }

    if (res.requestId === null) {
      // Only these failures may occur before request correlation.
      switch (res.error.code) {
        case "BOOTSTRAP_FAILED":
        case "JSON_UNAVAILABLE":
        case "INVALID_JSON":
        case "INVALID_REQUEST":
          if (res.error.outcome !== "notApplied") {
            fail("MALFORMED_RESPONSE: invalid pre-dispatch outcome");
          }
          break;

        case "INTERNAL_ERROR":
        case "RESPONSE_SERIALIZATION_FAILED":
          if (res.error.outcome !== "mayHaveApplied") {
            fail("MALFORMED_RESPONSE: invalid failure outcome");
          }
          break;

        default:
          fail("MALFORMED_RESPONSE: missing correlation");
      }
    } else if (res.requestId !== request.requestId) {
      fail("MALFORMED_RESPONSE: requestId mismatch");
    }

    return res;
  }

  function request(command, payload) {
    if (busy || closed || (blocked && command !== "ping")) {
      return;
    }

    var req = {
      protocol: 1,
      requestId: sessionId + ":" + String(++sequence),
      command: command,
      payload: payload
    };

    var source;

    try {
      source = makeSource(req);
    } catch (error) {
      show("Запрос не отправлен: " + String(error));
      return;
    }

    busy = true;
    updateButton();

    var settled = false;

    function finish() {
      if (settled || closed) {
        return false;
      }

      settled = true;
      clearTimeout(timer);
      busy = false;
      return true;
    }

    function unknownOutcome(message) {
      blocked = true;
      show(
        message + "\n" +
        "Автоматического повтора нет. Проверьте состояние проекта. " +
        "Для продолжения после проверки перезагрузите панель."
      );
      updateButton();
    }

    // A local waiting policy, not a host execution deadline.
    var timer = setTimeout(function () {
      if (!finish()) {
        return;
      }

      unknownOutcome(
        command === "ping"
          ? "Handshake не подтверждён."
          : "REQUEST_TIMEOUT: исход изменения неизвестен."
      );
    }, WAIT_MS);

    show(command === "ping"
      ? "Проверка host bridge…"
      : "Добавление префикса выбранным слоям…");

    try {
      cs.evalScript(source, function (raw) {
        if (!finish()) {
          // A late callback does not reverse a previous timeout.
          return;
        }

        var res;

        try {
          res = parseResponse(raw, req);
        } catch (error) {
          unknownOutcome(
            "Не удалось подтвердить результат: " + String(error)
          );
          return;
        }

        if (!res.ok) {
          if (command === "ping" ||
              res.error.outcome === "mayHaveApplied") {
            blocked = true;
          }

          show(JSON.stringify(res, null, 2));

          if (blocked) {
            show(status.textContent + "\n" +
              "Изменения заблокированы. Устраните причину и проверьте " +
              "проект перед перезагрузкой панели.");
          }

          updateButton();
          return;
        }

        if (command === "ping") {
          blocked = false;
          show(
            "Bridge готов. Это не подтверждает исход команд " +
            "из предыдущей сессии панели."
          );
        } else {
          show("Изменено слоёв: " + String(res.result.changed));
        }

        updateButton();
      });
    } catch (error) {
      if (finish()) {
        unknownOutcome("Ошибка вызова bridge: " + String(error));
      }
    }
  }

  renameButton.addEventListener("click", function () {
    request("renameSelected", { prefix: "Bible_" });
  });

  window.addEventListener("unload", function () {
    closed = true;
    // Closing the UI does not cancel submitted host work.
  });

  updateButton();

  try {
    cs = new CSInterface();
  } catch (error) {
    show("CSInterface недоступен: " + String(error));
    return;
  }

  request("ping", {});
}());
