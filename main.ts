// Entry point for the GTA 6 meme bounty.
// Copies the submitted post's address (POST.json) into the output
// directory so the grader can read it back.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const repoRoot = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

const postPath = join(repoRoot, "POST.json");
const destPath = join(outDir, "POST.json");

const body = readFileSync(postPath, "utf8");
mkdirSync(outDir, { recursive: true });
writeFileSync(destPath, body);
