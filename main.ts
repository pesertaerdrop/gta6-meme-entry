// gta6-meme-x-01 entry: "Post a GTA 6 meme on X".
//
// The entry is the X post itself, not this program. All main.ts does is hand
// the post's address to the gate: it copies POST.json from the repository root
// into the output directory, where the house reads it, fetches the post from X
// and builds the dossier the judge sees (the post's first picture, then its
// text). Nothing written here is judged.
//
// Runs on Node 22 with the standard library only. No network, no clock, no
// files outside the repository: the two grading runs write identical bytes.
// Outside the grader, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for
// /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

// Validate POST.json before copying: the house only accepts a real X status
// address, so a missing or malformed url should fail loudly here instead of
// passing a broken pointer through the gate.
let postUrl: unknown;
try {
  postUrl = (JSON.parse(readFileSync(source, "utf8")) as { url?: unknown }).url;
} catch (error) {
  console.error(`could not read POST.json from ${botDir}: ${(error as Error).message}`);
  process.exit(1);
}

const statusPattern = /^https:\/\/(x\.com|twitter\.com)\/[^/]+\/status\/\d+$/;
if (typeof postUrl !== "string" || !statusPattern.test(postUrl)) {
  console.error(`POST.json has no valid X status url: ${JSON.stringify(postUrl)}`);
  process.exit(1);
}

try {
  copyFileSync(source, target);
} catch (error) {
  console.error(`could not copy POST.json from ${botDir}: ${(error as Error).message}`);
  process.exit(1);
}

console.log(`copied post ${postUrl} to ${target}`);
