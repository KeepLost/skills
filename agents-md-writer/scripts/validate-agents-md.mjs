import { readFileSync, statSync } from 'node:fs';
import { TextDecoder } from 'node:util';

const [, , ...args] = process.argv;

function error(reason) {
  process.stderr.write(`ERROR ${reason}\n`);
  process.exitCode = 2;
}

function measure(text) {
  const normalized = text.replace(/\r\n?/g, '\n');
  const lines = normalized.length === 0 ? 0 : normalized.endsWith('\n') ? normalized.split('\n').length - 1 : normalized.split('\n').length;
  const characters = Array.from(normalized).length;
  return { lines, characters };
}

try {
  if (args.length !== 1) {
    error('usage');
  } else {
    const [path] = args;
    const stats = statSync(path);

    if (!stats.isFile()) {
      error('not-a-file');
    } else {
      const bytes = readFileSync(path);
      const decoder = new TextDecoder('utf-8', { fatal: true });
      let text = decoder.decode(bytes);

      if (text.startsWith('\uFEFF')) {
        text = text.slice(1);
      }

      const { lines, characters } = measure(text);
      const verdict = lines <= 300 && characters <= 10_000 ? 'PASS' : 'FAIL';
      process.stdout.write(`${verdict} lines=${lines}/300 characters=${characters}/10000 path=${JSON.stringify(path)}\n`);
      process.exitCode = verdict === 'PASS' ? 0 : 1;
    }
  }
} catch {
  error('read');
}
