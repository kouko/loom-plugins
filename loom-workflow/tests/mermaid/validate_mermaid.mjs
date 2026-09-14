// Parse every ```mermaid block in the loom-visualization skill's templates/
// and references/ with Mermaid's own parser.
//
// Usage:
//   node validate_mermaid.mjs              # every templates/*.md, references/*.md
//   node validate_mermaid.mjs a.md b.md    # only the named files
//
// Prints `OK <file>:<line>` or `FAIL <file>:<line> <first error line>` per
// block (line = the opening fence). Exits 1 on any failure, on zero blocks,
// or when the parser accepts a known-bad block (the check would be vacuous).
//
// Mermaid needs a DOM for several diagram types (DOMPurify hooks), so jsdom
// globals are installed before mermaid is imported.
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { JSDOM } from 'jsdom';

const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false, logLevel: 'fatal' });

const SKILL_DIR = resolve(dirname(fileURLToPath(import.meta.url)), '../../skills/loom-visualization');
const KNOWN_BAD = 'flowchart TD\n    A -> B\n';

async function parseError(text) {
  try {
    const ok = await mermaid.parse(text);
    return ok === false ? 'parse returned false' : null;
  } catch (err) {
    return String(err?.message ?? err).split('\n').find((l) => l.trim()) ?? 'unknown error';
  }
}

function defaultFiles() {
  const files = [];
  for (const sub of ['templates', 'references']) {
    const dir = join(SKILL_DIR, sub);
    for (const name of readdirSync(dir).filter((n) => n.endsWith('.md')).sort()) {
      files.push({ path: join(dir, name), label: `${sub}/${name}` });
    }
  }
  return files;
}

function extractBlocks(text) {
  const lines = text.split('\n');
  const blocks = [];
  for (let i = 0; i < lines.length; i++) {
    // First word of the info string decides, as in the page renderer:
    // ```mermaid title is a mermaid block.
    const open = lines[i].match(/^\s*(`{3,}|~{3,})mermaid(\s.*)?$/);
    if (!open) continue;
    const fence = open[1];
    const body = [];
    let j = i + 1;
    for (; j < lines.length; j++) {
      const t = lines[j].trim();
      if (t[0] === fence[0] && /^(`{3,}|~{3,})$/.test(t) && t.length >= fence.length) break;
      body.push(lines[j]);
    }
    blocks.push({ line: i + 1, text: body.join('\n') });
    i = j;
  }
  return blocks;
}

if ((await parseError(KNOWN_BAD)) === null) {
  console.log('FAIL self-test: parser accepted `flowchart TD / A -> B`; the parser check is vacuous');
  process.exit(1);
}

const args = process.argv.slice(2);
const files = args.length ? args.map((p) => ({ path: resolve(p), label: p })) : defaultFiles();

let total = 0;
let failed = 0;
for (const file of files) {
  for (const block of extractBlocks(readFileSync(file.path, 'utf8'))) {
    total++;
    const error = await parseError(block.text);
    if (error === null) {
      console.log(`OK ${file.label}:${block.line}`);
    } else {
      failed++;
      console.log(`FAIL ${file.label}:${block.line} ${error}`);
    }
  }
}

if (total === 0) {
  console.log('FAIL no mermaid blocks found');
  process.exit(1);
}
console.log(`${total - failed}/${total} mermaid blocks parsed`);
process.exit(failed ? 1 : 0);
