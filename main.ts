// news-image-20261121 round 4: "The World Today" for Saturday 21 November 2026.
// The front page is drawn by tools/draw_frontpage.py (Pillow, system DejaVu
// fonts, no network, no clock, no randomness), so the program is fully
// deterministic: two runs write byte-identical entry.png files.
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const run = spawnSync(
  "python3",
  [join(repoDir, "tools", "draw_frontpage.py")],
  {
    cwd: repoDir,
    env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
    stdio: "inherit",
  },
);
if (run.error) {
  throw run.error;
}
if (run.status !== 0) {
  throw new Error(`draw_frontpage.py exited with status ${run.status}`);
}
const entry = join(outDir, "entry.png");
if (!existsSync(entry)) {
  throw new Error(`expected output missing: ${entry}`);
}
console.log(`wrote ${entry}`);
