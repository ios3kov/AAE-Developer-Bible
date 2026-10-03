(function () {
    var MAX_MESSAGE_CHARS = 65536;
    var MAX_PREFIX_CHARS = 256;

    var JSON_UNAVAILABLE =
        '{"protocol":1,"requestId":null,"ok":false,' +
        '"error":{"code":"JSON_UNAVAILABLE",' +
        '"message":"Load a vetted ES3-compatible JSON implementation.",' +
        '"outcome":"notApplied"}}';

    var SERIALIZATION_FAILED =
        '{"protocol":1,"requestId":null,"ok":false,' +
        '"error":{"code":"RESPONSE_SERIALIZATION_FAILED",' +
        '"message":"Could not serialize the host response.",' +
        '"outcome":"mayHaveApplied"}}';

    function owns(object, name) {
        return Object.prototype.hasOwnProperty.call(object, name);
    }

    function isObject(value) {
        return value !== null &&
            Object.prototype.toString.call(value) === "[object Object]";
    }

    function text(error) {
        try {
            if (error && typeof error.message === "string") {
                return error.message;
            }
            return String(error);
        } catch (ignored) {
            return "Unprintable host error";
        }
    }

    function failure(id, code, message, outcome) {
        return {
            protocol: 1,
            requestId: id,
            ok: false,
            error: {
                code: code,
                message: message,
                outcome: outcome
            }
        };
    }

    function success(id, result) {
        return {
            protocol: 1,
            requestId: id,
            ok: true,
            result: result
        };
    }

    function serialize(envelope) {
        try {
            var raw = JSON.stringify(envelope);

            if (typeof raw !== "string" ||
                    raw.length > MAX_MESSAGE_CHARS) {
                return SERIALIZATION_FAILED;
            }

            return raw;
        } catch (error) {
            return SERIALIZATION_FAILED;
        }
    }

    function renameSelected(req) {
        var prefix = req.payload.prefix;
        var layers;
        var names = [];
        var i;

        // No mutation is performed during this preparation phase.
        try {
            var comp = app.project && app.project.activeItem;

            if (!(comp instanceof CompItem)) {
                return failure(
                    req.requestId,
                    "NO_ACTIVE_COMP",
                    "No active composition.",
                    "notApplied"
                );
            }

            layers = comp.selectedLayers;

            if (!layers || layers.length === 0) {
                return failure(
                    req.requestId,
                    "NO_SELECTED_LAYERS",
                    "No selected layers.",
                    "notApplied"
                );
            }

            if (prefix.length === 0) {
                return success(req.requestId, { changed: 0 });
            }

            for (i = 0; i < layers.length; i++) {
                names[i] = prefix + layers[i].name;
            }
        } catch (error) {
            return failure(
                req.requestId,
                "TARGET_READ_FAILED",
                text(error),
                "notApplied"
            );
        }

        var opened = false;
        var changed = 0;
        var attemptedMutation = false;
        var primaryError = null;
        var cleanupError = null;

        try {
            app.beginUndoGroup("AE Bible: Prefix Selected Layer Names");
            opened = true;

            for (i = 0; i < layers.length; i++) {
                // An assignment that throws may have uncertain effects.
                attemptedMutation = true;
                layers[i].name = names[i];
                changed += 1;
            }
        } catch (error) {
            primaryError = text(error);
        } finally {
            if (opened) {
                try {
                    app.endUndoGroup();
                } catch (error) {
                    cleanupError = text(error);
                }
            }
        }

        if (primaryError !== null || cleanupError !== null) {
            var out = failure(
                req.requestId,
                primaryError !== null
                    ? "COMMAND_FAILED"
                    : "UNDO_CLOSE_FAILED",
                primaryError !== null
                    ? primaryError
                    : cleanupError,
                attemptedMutation
                    ? "mayHaveApplied"
                    : "notApplied"
            );

            out.error.details = {
                // Number of assignments that returned without throwing.
                // Not proof of rollback or of final project state.
                changedBeforeError: changed
            };

            if (cleanupError !== null) {
                out.error.details.cleanupError = cleanupError;
            }

            return out;
        }

        return success(req.requestId, { changed: changed });
    }

    function handle(raw) {
        var req;
        var id = null;

        if (typeof raw !== "string" ||
                raw.length > MAX_MESSAGE_CHARS) {
            return failure(
                null,
                "INVALID_REQUEST",
                "Request must be a bounded JSON string.",
                "notApplied"
            );
        }

        try {
            req = JSON.parse(raw);
        } catch (error) {
            return failure(
                null,
                "INVALID_JSON",
                "Request is not valid JSON.",
                "notApplied"
            );
        }

        if (!isObject(req)) {
            return failure(
                null,
                "INVALID_REQUEST",
                "Request must be an object.",
                "notApplied"
            );
        }

        if (owns(req, "requestId") &&
                typeof req.requestId === "string" &&
                req.requestId.length > 0 &&
                req.requestId.length <= 128) {
            id = req.requestId;
        }

        if (id === null ||
                !owns(req, "protocol") ||
                typeof req.protocol !== "number" ||
                !owns(req, "command") ||
                typeof req.command !== "string" ||
                req.command.length === 0 ||
                !owns(req, "payload") ||
                !isObject(req.payload)) {
            return failure(
                id,
                "INVALID_REQUEST",
                "Invalid request fields.",
                "notApplied"
            );
        }

        if (req.protocol !== 1) {
            return failure(
                id,
                "UNSUPPORTED_PROTOCOL",
                "Only protocol 1 is supported.",
                "notApplied"
            );
        }

        if (req.command === "ping") {
            return success(id, {
                ready: true,
                protocol: 1,
                commands: ["ping", "renameSelected"]
            });
        }

        if (req.command !== "renameSelected") {
            return failure(
                id,
                "UNKNOWN_COMMAND",
                "Unknown command.",
                "notApplied"
            );
        }

        if (!owns(req.payload, "prefix") ||
                typeof req.payload.prefix !== "string" ||
                req.payload.prefix.length > MAX_PREFIX_CHARS) {
            return failure(
                id,
                "INVALID_PAYLOAD",
                "prefix must be a string of at most 256 UTF-16 code units.",
                "notApplied"
            );
        }

        return renameSelected(req);
    }

    $._aeBible = $._aeBible || {};

    $._aeBible.dispatch = function (raw) {
        if (typeof JSON === "undefined" ||
                JSON === null ||
                typeof JSON.parse !== "function" ||
                typeof JSON.stringify !== "function") {
            return JSON_UNAVAILABLE;
        }

        var envelope;

        try {
            envelope = handle(raw);
        } catch (error) {
            // Unexpected failure: conservatively do not claim no mutation.
            envelope = failure(
                null,
                "INTERNAL_ERROR",
                "Could not complete the response: " + text(error),
                "mayHaveApplied"
            );
        }

        return serialize(envelope);
    };
}());
