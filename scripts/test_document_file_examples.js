"use strict";

// Executes the actual documentation snippets with deterministic doubles only.
// This does not exercise ExtendScript, UXP, an OS filesystem, or After Effects.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");
const root = path.resolve(__dirname, "..");

function snippet(document, marker, language) {
  const text = fs.readFileSync(path.join(root, document), "utf8");
  const fences = [...text.matchAll(/^```([^\n]*)\n([\s\S]*?)^```\s*$/gm)];
  const found = fences.filter((m) => m[1] === language && m[2].includes(marker));
  assert.equal(found.length, 1, `Exactly one ${marker} snippet`);
  return found[0][2];
}

const jsxDocument = "06-SCRIPTING/01-OBJECT-MODEL.md";
const jsxCode = snippet(jsxDocument, "function readBinaryBounded(", "jsx") +
  "\n" + snippet(jsxDocument, "function writeNewUtf8(", "jsx");
const uxpCode = snippet("07-PANELS/04-UXP-PLATFORM.md", "async function exportPreset(", "javascript");

function jsx(options = {}) {
  const state = Object.assign({
    content: "abc", exists: true, parentExists: true, events: [], reads: [],
    openFails: false, closeFails: false, readFails: false, writeFails: false
  }, options);
  class File {
    constructor(uri) {
      this.absoluteURI = uri;
      this.fsName = "/owned/example";
      this.error = "";
      this.position = 0;
      this.opened = false;
    }
    get exists() { return state.exists; }
    get length() { return state.reportedLength ?? state.content.length; }
    get parent() { return state.parentMissing ? null : { exists: state.parentExists }; }
    set encoding(value) { state.events.push(["encoding", value]); this._encoding = value; }
    get encoding() { return this._encoding; }
    get eof() { return !this.opened || this.position >= state.content.length; }
    open(mode) {
      state.events.push(["open", mode]);
      if (state.openFails) { this.error = "open denied"; return false; }
      this.opened = true;
      this.encoding = "AUTO";
      this.position = state.bomSkip || 0;
      if (mode === "w") { state.exists = true; state.content = ""; }
      return true;
    }
    seek(offset, origin) {
      state.events.push(["seek", offset, origin]);
      if (state.seekFails) { this.error = "seek failed"; return false; }
      assert.equal(origin, 0);
      this.position = offset;
      return true;
    }
    read(count) {
      assert.equal(this.encoding, "BINARY");
      assert(count >= 1 && count <= 4096, "Every read is bounded");
      state.reads.push(count);
      if (state.readFails) { this.error = "primary read error"; return ""; }
      if (state.noProgress) return "";
      const chunk = state.content.slice(this.position, this.position + count);
      this.position += chunk.length;
      this.error = "";
      return chunk;
    }
    write(text) {
      assert.equal(this.encoding, "UTF-8");
      state.events.push(["write"]);
      if (state.writeFails) {
        state.content = text.slice(0, 1);
        this.error = "primary write error";
        return false;
      }
      state.content = text;
      return true;
    }
    close() {
      state.events.push(["close"]);
      assert(this.opened, "Only an acquired handle can be closed");
      this.opened = false;
      this.error = state.closeFails ? "close denied" : "";
      return !state.closeFails;
    }
  }
  const context = vm.createContext({ File });
  vm.runInContext(jsxCode, context, { filename: jsxDocument, timeout: 1000 });
  return { state, context, input: new File("file:/owned/example") };
}

test("binary reader preserves BOM bytes after open auto-detection", () => {
  const { state, context, input } = jsx({ content: "\xef\xbb\xbfA", bomSkip: 3 });
  assert.equal(context.readBinaryBounded(input, 4), "\xef\xbb\xbfA");
  assert.deepEqual(state.events, [
    ["open", "r"], ["encoding", "AUTO"], ["encoding", "BINARY"], ["seek", 0, 0], ["close"]
  ]);
});

test("binary reader rejects growth beyond stale size metadata and closes", () => {
  const { state, context, input } = jsx({ content: "x".repeat(5001), reportedLength: 2 });
  assert.throws(() => context.readBinaryBounded(input, 5000), /exceeds byte limit/);
  assert.deepEqual(state.reads, [4096, 905]);
  assert.deepEqual(state.events.at(-1), ["close"]);
});

test("binary reader accepts exact byte limit and empty input", () => {
  for (const content of ["", "a", "x".repeat(4096)]) {
    const { context, input } = jsx({ content });
    assert.equal(context.readBinaryBounded(input, content.length), content);
  }
});

test("binary reader rejects invalid limits before acquiring a handle", () => {
  const { state, context, input } = jsx();
  for (const limit of [-1, 0.1, NaN, Infinity, 2097153, "3"])
    assert.throws(() => context.readBinaryBounded(input, limit), /Invalid byte limit/);
  assert.equal(state.events.length, 0);
});

test("binary reader preserves primary error when cleanup clears or adds an error", () => {
  for (const closeFails of [false, true]) {
    const { context, input } = jsx({ readFails: true, closeFails });
    assert.throws(() => context.readBinaryBounded(input, 3), (error) => {
      assert.match(error.message, /primary read error/);
      assert.equal(error.message.includes("Close: close denied"), closeFails);
      return true;
    });
  }
});

test("binary reader does not close a handle after failed open", () => {
  const { state, context, input } = jsx({ openFails: true });
  assert.throws(() => context.readBinaryBounded(input, 3), /open denied/);
  assert.deepEqual(state.events, [["open", "r"]]);
});

test("binary reader rejects no progress and failed close", () => {
  for (const [options, pattern] of [
    [{ noProgress: true }, /Read made no progress/],
    [{ closeFails: true }, /Close: close denied/],
    [{ seekFails: true }, /seek failed/]
  ]) {
    const { state, context, input } = jsx(options);
    assert.throws(() => context.readBinaryBounded(input, 3), pattern);
    assert.deepEqual(state.events.at(-1), ["close"]);
  }
});

test("text writer rejects existing output and missing parent without truncation", () => {
  for (const options of [{}, { exists: false, parentExists: false }, { exists: false, parentMissing: true }]) {
    const { state, context, input } = jsx(options);
    assert.throws(() => context.writeNewUtf8(input, "replacement"), /Choose a new file/);
    assert.equal(state.content, "abc");
    assert.equal(state.events.length, 0);
  }
});

test("text writer applies UTF-8 after open and returns only after close", () => {
  const { state, context, input } = jsx({ exists: false });
  assert.equal(context.writeNewUtf8(input, "Текст\n"), "/owned/example");
  assert.equal(state.content, "Текст\n");
  assert.deepEqual(state.events, [["open", "w"], ["encoding", "AUTO"], ["encoding", "UTF-8"], ["write"], ["close"]]);
});

test("text writer reports partial output and primary plus cleanup failures", () => {
  const { state, context, input } = jsx({ exists: false, writeFails: true, closeFails: true });
  assert.throws(() => context.writeNewUtf8(input, "payload"), /primary write error\nClose: close denied/);
  assert.equal(state.content, "p");
  assert.deepEqual(state.events.at(-1), ["close"]);
});

test("text writer never reports success on open or close failure", () => {
  for (const options of [{ openFails: true }, { closeFails: true }]) {
    const { state, context, input } = jsx({ exists: false, ...options });
    assert.throws(() => context.writeNewUtf8(input, "payload"), /denied/);
    if (options.openFails) assert.deepEqual(state.events, [["open", "w"]]);
  }
});

function uxp(options = {}) {
  const state = { pickerCalls: 0, writes: 0, reads: 0, text: "old" };
  const formats = { utf8: Symbol("utf8") };
  const file = {
    name: "preset.json",
    async write(text, settings) {
      state.writes++;
      assert.equal(settings.format, formats.utf8);
      assert.equal(settings.append, false);
      state.text = options.writeFails ? text.slice(0, 4) : text;
      if (options.writeFails) throw Error("write rejected after partial change");
      return 999; // Documentation does not compare this number with JS string length.
    },
    async read(settings) {
      state.reads++;
      assert.equal(settings.format, formats.utf8);
      if (options.readFails) throw Error("read failed");
      return options.mismatch ? "different" : state.text;
    }
  };
  const localFileSystem = { async getFileForSaving(name, settings) {
    state.pickerCalls++;
    assert.equal(name, "preset.json");
    assert.equal(settings.types.length, 1);
    assert.equal(settings.types[0], "json");
    if (options.acquireFails) throw Error("picker unavailable");
    return options.cancel ? null : file;
  } };
  const context = vm.createContext({ require(name) {
    assert.equal(name, "uxp");
    return { storage: { localFileSystem, formats } };
  } });
  vm.runInContext(uxpCode, context, { filename: "07-PANELS/04-UXP-PLATFORM.md", timeout: 1000 });
  return { state, exportPreset: context.exportPreset };
}

test("UXP exporter validates all preset fields before selecting a file", async () => {
  const { state, exportPreset } = uxp();
  for (const args of [[null, 0], ["x".repeat(81), 0], ["x", NaN], ["x", -1], ["x", 2]])
    await assert.rejects(exportPreset(...args), /Invalid preset fields/);
  assert.equal(state.pickerCalls, 0);
});

test("UXP exporter distinguishes cancellation and access failure without writing", async () => {
  for (const [options, expected] of [[{ cancel: true }, "cancelled"], [{ acquireFails: true }, "acquire_failed"]]) {
    const { state, exportPreset } = uxp(options);
    assert.equal((await exportPreset("x", 0)).status, expected);
    assert.equal(state.writes, 0);
    assert.equal(state.reads, 0);
  }
});

test("UXP exporter reports uncertain write outcome without retry or readback", async () => {
  const { state, exportPreset } = uxp({ writeFails: true });
  assert.equal((await exportPreset("x", 0.5)).status, "write_outcome_unknown");
  assert.equal(state.writes, 1);
  assert.equal(state.reads, 0);
  assert.equal(state.text, '{"sc');
});

test("UXP exporter keeps completed write distinct from unverified readback", async () => {
  for (const options of [{ readFails: true }, { mismatch: true }]) {
    const { state, exportPreset } = uxp(options);
    assert.equal((await exportPreset("x", 1)).status, "written_unverified");
    assert.equal(state.writes, 1);
    assert.equal(state.reads, 1);
    assert.equal(JSON.parse(state.text).strength, 1);
  }
});

test("UXP exporter verifies actual text and returns selected filename", async () => {
  const { state, exportPreset } = uxp();
  const result = await exportPreset("Кадр", 0.25);
  assert.equal(result.status, "verified");
  assert.equal(result.name, "preset.json");
  assert.deepEqual(JSON.parse(state.text), { schema: 1, label: "Кадр", strength: 0.25 });
});
