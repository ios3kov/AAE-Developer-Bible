/* Offline guard test. Does not emulate or execute Adobe's renderer. */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');
const file = path.join(__dirname, 'ACX_Mega_Probe.jsx');
const code = fs.readFileSync(file, 'utf8').replace(/^#target[^\n]*\n/, '');
let messages = [];
const context = vm.createContext({alert: value => messages.push(String(value))});
// Any attempt to access app/project/File/Folder fails; only an alert is allowed.
vm.runInContext(code, context, {timeout: 1000, filename: file});
assert.equal(messages.length, 1);
assert.match(messages[0], /withdrawn/i);
assert.match(messages[0], /No new run is required/);
console.log('PASS: withdrawn Mega entry point only reports its status; no AE/filesystem access.');
