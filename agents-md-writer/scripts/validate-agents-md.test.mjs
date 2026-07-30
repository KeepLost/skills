import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const validatorPath = join(scriptDirectory, 'validate-agents-md.mjs');

function createWorkspace() {
  return mkdtempSync(join(tmpdir(), 'validate-agents-md-test-'));
}

function removeWorkspace(workspace) {
  rmSync(workspace, { recursive: true, force: true });
}

function writeTextFixture(workspace, name, content) {
  const path = join(workspace, name);
  writeFileSync(path, content, 'utf8');
  return path;
}

function writeBytesFixture(workspace, name, content) {
  const path = join(workspace, name);
  writeFileSync(path, content);
  return path;
}

function runValidator(args) {
  return spawnSync(process.execPath, [validatorPath, ...args], {
    cwd: scriptDirectory,
    encoding: 'utf8',
  });
}

function assertMeasurement(result, expected) {
  assert.equal(result.status, expected.status);
  assert.equal(result.stderr, '');
  assert.equal(
    result.stdout,
    `${expected.verdict} lines=${expected.lines}/300 characters=${expected.characters}/10000 path=${JSON.stringify(expected.path)}\n`,
  );
}

function assertOperationalError(result) {
  assert.equal(result.status, 2);
  assert.equal(result.stdout, '');
  assert.match(result.stderr, /^ERROR .+\n$/);
}

test('passes when content has exactly 300 logical lines', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const path = writeTextFixture(workspace, 'exact-300-lines.md', Array.from({ length: 300 }, () => 'x').join('\n'));

    // When
    const result = runValidator([path]);

    // Then
    assertMeasurement(result, { status: 0, verdict: 'PASS', lines: 300, characters: 599, path });
  } finally {
    removeWorkspace(workspace);
  }
});

test('passes when content has exactly 10000 Unicode code points', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const content = 'a'.repeat(10_000);
    const path = writeTextFixture(workspace, 'exact-10000-code-points.md', content);

    // When
    const result = runValidator([path]);

    // Then
    assertMeasurement(result, { status: 0, verdict: 'PASS', lines: 1, characters: 10_000, path });
  } finally {
    removeWorkspace(workspace);
  }
});

test('fails when content has 301 logical lines', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const path = writeTextFixture(workspace, 'too-many-lines.md', Array.from({ length: 301 }, () => 'x').join('\n'));

    // When
    const result = runValidator([path]);

    // Then
    assertMeasurement(result, { status: 1, verdict: 'FAIL', lines: 301, characters: 601, path });
  } finally {
    removeWorkspace(workspace);
  }
});

test('fails when content has 10001 Unicode code points including non-BMP emoji', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const content = `${'a'.repeat(9_999)}😀😀`;
    const path = writeTextFixture(workspace, 'too-many-code-points.md', content);

    // When
    const result = runValidator([path]);

    // Then
    assertMeasurement(result, { status: 1, verdict: 'FAIL', lines: 1, characters: 10_001, path });
  } finally {
    removeWorkspace(workspace);
  }
});

test('normalizes CRLF and lone CR exactly like LF for logical lines', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const lfPath = writeTextFixture(workspace, 'lf-newlines.md', 'one\ntwo\nthree');
    const crlfPath = writeTextFixture(workspace, 'crlf-newlines.md', 'one\r\ntwo\r\nthree');
    const crPath = writeTextFixture(workspace, 'cr-newlines.md', 'one\rtwo\rthree');

    // When
    const lfResult = runValidator([lfPath]);
    const crlfResult = runValidator([crlfPath]);
    const crResult = runValidator([crPath]);

    // Then
    assertMeasurement(lfResult, { status: 0, verdict: 'PASS', lines: 3, characters: 13, path: lfPath });
    assertMeasurement(crlfResult, { status: 0, verdict: 'PASS', lines: 3, characters: 13, path: crlfPath });
    assertMeasurement(crResult, { status: 0, verdict: 'PASS', lines: 3, characters: 13, path: crPath });
  } finally {
    removeWorkspace(workspace);
  }
});

test('strips one leading BOM before measuring content', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const path = writeTextFixture(workspace, 'leading-bom.md', '\uFEFFone');

    // When
    const result = runValidator([path]);

    // Then
    assertMeasurement(result, { status: 0, verdict: 'PASS', lines: 1, characters: 3, path });
  } finally {
    removeWorkspace(workspace);
  }
});

test('counts an empty file as zero logical lines without a phantom trailing line', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const path = writeTextFixture(workspace, 'empty-file.md', '');

    // When
    const result = runValidator([path]);

    // Then
    assertMeasurement(result, { status: 0, verdict: 'PASS', lines: 0, characters: 0, path });
  } finally {
    removeWorkspace(workspace);
  }
});

test('reports invalid UTF-8 as an operational error', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const path = writeBytesFixture(workspace, 'invalid-utf8.md', Buffer.from([0x66, 0x80, 0x67]));

    // When
    const result = runValidator([path]);

    // Then
    assertOperationalError(result);
  } finally {
    removeWorkspace(workspace);
  }
});

test('reports missing arguments as an operational error', () => {
  // Given
  const args = [];

  // When
  const result = runValidator(args);

  // Then
  assertOperationalError(result);
});

test('reports extra arguments as an operational error', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const firstPath = writeTextFixture(workspace, 'first-extra-arg.md', 'one');
    const secondPath = writeTextFixture(workspace, 'second-extra-arg.md', 'two');

    // When
    const result = runValidator([firstPath, secondPath]);

    // Then
    assertOperationalError(result);
  } finally {
    removeWorkspace(workspace);
  }
});

test('reports a missing path as an operational error', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const path = join(workspace, 'missing-input.md');

    // When
    const result = runValidator([path]);

    // Then
    assertOperationalError(result);
  } finally {
    removeWorkspace(workspace);
  }
});

test('reports a non-file path as an operational error', () => {
  const workspace = createWorkspace();
  try {
    // Given
    const path = workspace;

    // When
    const result = runValidator([path]);

    // Then
    assertOperationalError(result);
  } finally {
    removeWorkspace(workspace);
  }
});
