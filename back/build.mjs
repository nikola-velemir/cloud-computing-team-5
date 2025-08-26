import { build } from "esbuild";
import { glob } from "glob";
import fs from "fs-extra";
import path from "path";

const entryPoints = glob.sync("src/feature/**/index.ts");

for (const entry of entryPoints) {
  // Calculate the output file path
  const relativePath = path.relative("src", entry); // feature/.../index.ts
  const outFile = path.join("dist", relativePath).replace(/\.ts$/, ".js");

  // Ensure the folder exists
  await fs.ensureDir(path.dirname(outFile));

  await build({
    entryPoints: [entry],
    bundle: true,
    platform: "node",
    target: "node18",
    outfile: outFile,
    sourcemap: false,
    external: ["aws-sdk"],
  });

  console.log(`Built: ${entry} → ${outFile}`);
}

console.log("✅ Build complete!");
