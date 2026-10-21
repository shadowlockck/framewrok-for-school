const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const ts = require('typescript');

const source = fs.readFileSync(path.join(__dirname, '../src/api/client.ts'), 'utf8');

function loadClient(fetch) {
  const compiled = ts.transpileModule(
    source.replace('import.meta.env.VITE_API_URL', 'undefined'),
    { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 } },
  );
  const context = { exports: {}, fetch, console };
  vm.runInNewContext(compiled.outputText, context);
  return context.exports;
}

const report = { reporter_role: 'student', incident_description: 'Повідомлення про подію' };

test('manifest failure is surfaced instead of activating demo modules', async () => {
  const client = loadClient(async () => ({ ok: false, status: 500 }));
  await assert.rejects(client.fetchManifest(), /Manifest request failed: 500/);
});

test('manifest returns the modules provided by the server', async () => {
  const expected = { school: { name: 'Ліцей' }, modules: { legal: false }, navigation: [] };
  const client = loadClient(async () => ({ ok: true, json: async () => expected }));
  const manifest = await client.fetchManifest();
  assert.equal(manifest.modules.legal, false);
  assert.equal(manifest.navigation.length, 0);
});

test('server acknowledgment confirms the report', async () => {
  const client = loadClient(async () => ({ ok: true }));
  const result = await client.submitConfidentialReport(report);
  assert.equal(result.success, true);
});

test('network failure does not claim that a confidential report was saved', async () => {
  const client = loadClient(async () => { throw new TypeError('Failed to fetch'); });
  const result = await client.submitConfidentialReport(report);
  assert.equal(result.success, false);
  assert.match(result.message, /не надіслано/);
});
