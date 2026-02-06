import * as fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import glob from "glob";

import { visit } from "unist-util-visit";

import { generateMdAstFromFile } from "./utils.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname);

const SPECIAL_IMPLICIT_TARGETS = new Set(["_index.md", "_docHome.md"]);
const EXCLUDED_TOC_FILES = new Set(["TOC-pingkai.md"]);

const CLOUD_TOC_FILES = [
  "TOC-tidb-cloud.md",
  "TOC-tidb-cloud-premium.md",
  "TOC-tidb-cloud-starter.md",
  "TOC-tidb-cloud-essential.md",
];

const PREFIX_TO_TOC = [
  { prefix: "ai/", toc: "TOC-ai.md" },
  { prefix: "api/", toc: "TOC-api.md" },
  { prefix: "develop/", toc: "TOC-develop.md" },
  { prefix: "releases/", toc: "TOC-tidb-releases.md" },
  { prefix: "tidb-cloud/releases/", toc: "TOC-tidb-cloud-releases.md" },
  { prefix: "best-practices/", toc: "TOC-best-practices.md" },
];

function isExternalUrl(url = "") {
  return (
    url.startsWith("//") || url.includes("://") || url.startsWith("mailto:")
  );
}

function stripQueryAndHash(url = "") {
  const q = url.split("?")[0];
  const [p, hash] = q.split("#");
  return { path: p, hash: hash || "" };
}

function isInternalDocLink(url = "") {
  if (!url) return false;
  if (isExternalUrl(url)) return false;
  if (!url.startsWith("/")) return false;
  if (url.startsWith("/media/")) return false;
  const { path: p } = stripQueryAndHash(url);
  return p.endsWith(".md") || p.endsWith(".mdx");
}

function extractUrlsFromMarkdownFile(absPath) {
  const buf = fs.readFileSync(absPath);
  const ast = generateMdAstFromFile(buf);
  const urls = [];
  visit(ast, ["link", "definition"], (node) => {
    if (typeof node.url === "string" && node.url.trim()) {
      urls.push(node.url.trim());
    }
  });
  return urls;
}

function readTocFiles() {
  const tocFiles = glob
    .sync("TOC*.md", { cwd: ROOT, nodir: true })
    .filter((f) => !EXCLUDED_TOC_FILES.has(f))
    .sort((a, b) => a.localeCompare(b));
  return tocFiles;
}

function buildTocIndex(tocFiles) {
  const tocToPages = new Map(); // tocFile -> Set(relPathWithoutLeadingSlash)
  const anyTocPages = new Set();
  const pageToTocs = new Map(); // pageRel -> Set(tocFile)

  for (const toc of tocFiles) {
    const tocAbs = path.join(ROOT, toc);
    const urls = extractUrlsFromMarkdownFile(tocAbs);
    const pages = new Set();

    for (const url of urls) {
      if (!isInternalDocLink(url)) continue;
      const { path: p } = stripQueryAndHash(url);
      const rel = p.replace(/^\/+/, "");
      pages.add(rel);
      anyTocPages.add(rel);

      const tocs = pageToTocs.get(rel) || new Set();
      tocs.add(toc);
      pageToTocs.set(rel, tocs);
    }

    tocToPages.set(toc, pages);
  }

  return { tocToPages, anyTocPages, pageToTocs };
}

function expectedSetForTarget(targetRel, tocToPages, anyTocPages) {
  if (
    targetRel === "_index.md" ||
    targetRel.endsWith("/_index.md") ||
    targetRel === "_docHome.md" ||
    targetRel.endsWith("/_docHome.md")
  ) {
    return { ok: true };
  }

  if (
    targetRel.startsWith("tidb-cloud/") &&
    !targetRel.startsWith("tidb-cloud/releases/")
  ) {
    const union = new Set();
    for (const toc of CLOUD_TOC_FILES) {
      const set = tocToPages.get(toc);
      if (!set) continue;
      for (const p of set) union.add(p);
    }
    return {
      ok: union.has(targetRel),
      expectedLabel: "any TiDB Cloud TOC",
    };
  }

  for (const { prefix, toc } of PREFIX_TO_TOC) {
    if (targetRel.startsWith(prefix)) {
      const set = tocToPages.get(toc) || new Set();
      return { ok: set.has(targetRel), expectedLabel: toc };
    }
  }

  // Default: the target appears in any TOC*.md
  return { ok: anyTocPages.has(targetRel), expectedLabel: "any TOC*.md" };
}

function main() {
  process.chdir(ROOT);

  const verbose =
    process.env.VERBOSE_TOC === "1" ||
    process.env.VERBOSE_TOC === "true" ||
    process.env.VERBOSE === "1" ||
    process.env.VERBOSE === "true";
  const maxMissing =
    Number.parseInt(process.env.TOC_MAX_MISSING || "", 10) || 50;
  const maxFiles =
    Number.parseInt(process.env.TOC_MAX_FILES || "", 10) || 30;
  const maxLinksPerFile =
    Number.parseInt(process.env.TOC_MAX_LINKS_PER_FILE || "", 10) || 10;

  const tocFiles = readTocFiles();
//   if (tocFiles.length === 0) {
//     console.error("TOC check error: no TOC*.md files found in repo root.");
//     process.exit(1);
//   }

  const { tocToPages, anyTocPages, pageToTocs } = buildTocIndex(tocFiles);
  const buildScopePages = [...anyTocPages].sort((a, b) => a.localeCompare(b));

  const missingScopePages = [];
  const violations = [];

  for (const sourceRel of buildScopePages) {
    const sourceAbs = path.join(ROOT, sourceRel);
    if (!fs.existsSync(sourceAbs)) {
      missingScopePages.push(sourceRel);
      continue;
    }

    const urls = extractUrlsFromMarkdownFile(sourceAbs);
    for (const url of urls) {
      if (!isInternalDocLink(url)) continue;
      const { path: p } = stripQueryAndHash(url);
      const targetRel = p.replace(/^\/+/, "");

      if (SPECIAL_IMPLICIT_TARGETS.has(path.basename(targetRel))) {
        continue;
      }

      const { ok, expectedLabel } = expectedSetForTarget(
        targetRel,
        tocToPages,
        anyTocPages
      );
      if (!ok) {
        const sourceTocs = [...(pageToTocs.get(sourceRel) || new Set())].sort(
          (a, b) => a.localeCompare(b)
        );
        violations.push({ sourceRel, url, targetRel, expectedLabel, sourceTocs });
      }
    }
  }

  if (missingScopePages.length > 0) {
    // Printed below in a grouped summary.
  }

  if (violations.length > 0) {
    // Printed below in a grouped summary.
  }

  if (missingScopePages.length > 0 || violations.length > 0) {
    const bySource = new Map();
    for (const v of violations) {
      const arr = bySource.get(v.sourceRel) || [];
      arr.push(v);
      bySource.set(v.sourceRel, arr);
    }

    console.error("TOC check report: FAILED");
    console.error(
      `- Scope: pages included by TOC*.md (excluding: ${[
        ...EXCLUDED_TOC_FILES,
      ].join(", ") || "(none)"})`
    );
    console.error(`- In-scope pages: ${buildScopePages.length}`);
    console.error(
      `- Missing in-scope pages (referenced by TOC but not on disk): ${missingScopePages.length}`
    );
    console.error(
      `- TOC membership violations: ${violations.length} links in ${bySource.size} files`
    );
    console.error("");

    if (missingScopePages.length > 0) {
      console.error(
        `=== Missing pages referenced by TOC*.md (${missingScopePages.length}) ===`
      );
      console.error("");
      for (const p of missingScopePages.slice(0, maxMissing)) {
        const referencedBy = [...(pageToTocs.get(p) || new Set())].sort(
          (a, b) => a.localeCompare(b)
        );
        if (referencedBy.length > 0) {
          console.error(`- ${p}`);
          console.error(`  referenced by: ${referencedBy.join(", ")}`);
        } else {
          console.error(`- ${p}`);
        }
      }
      if (!verbose && missingScopePages.length > maxMissing) {
        console.error(
          `- ... and ${missingScopePages.length - maxMissing} more (set TOC_MAX_MISSING or VERBOSE_TOC=1 to show more)`
        );
      }
      console.error("");
    }

    if (violations.length > 0) {
      console.error(
        `=== TOC membership violations (grouped by source file) ===`
      );
      console.error("");

      const sourceFiles = [...bySource.keys()].sort((a, b) =>
        a.localeCompare(b)
      );
      const shownSourceFiles = verbose
        ? sourceFiles
        : sourceFiles.slice(0, maxFiles);
      let fileIndex = 0;
      for (const sourceRel of shownSourceFiles) {
        if (fileIndex > 0) {
          console.error("");
        }
        const list = bySource.get(sourceRel) || [];
        // Deduplicate exact URLs to reduce noise.
        const seen = new Set();
        const unique = [];
        for (const item of list) {
          const key = item.url;
          if (seen.has(key)) continue;
          seen.add(key);
          unique.push(item);
        }
        unique.sort((a, b) => a.url.localeCompare(b.url));

        console.error(`${sourceRel} (${unique.length})`);
        const shown = verbose
          ? unique
          : unique.slice(0, maxLinksPerFile);
        for (const v of shown) {
          if (v.expectedLabel === "any TOC*.md") {
            const hint =
              v.sourceTocs && v.sourceTocs.length > 0
                ? `; hint: add target to one of [${v.sourceTocs.join(", ")}]`
                : "";
            console.error(
              `  - ${v.url} (expected: present in some TOC*.md${hint})`
            );
          } else {
            console.error(`  - ${v.url} (expected: ${v.expectedLabel})`);
          }
        }
        if (!verbose && unique.length > maxLinksPerFile) {
          console.error(
            `  - ... and ${unique.length - maxLinksPerFile} more (set TOC_MAX_LINKS_PER_FILE or VERBOSE_TOC=1)`
          );
        }
        fileIndex += 1;
      }

      if (!verbose && sourceFiles.length > maxFiles) {
        console.error("");
        console.error(
          `... and ${sourceFiles.length - maxFiles} more source files (set TOC_MAX_FILES or VERBOSE_TOC=1)`
        );
      }

      console.error("=== How to fix ===");
      console.error(
        "- If the target page should be part of the site, add it to the expected TOC (per folder mapping)."
      );
      console.error(
        "- Otherwise, update the link to point to an in-scope page that is included by TOC."
      );
      console.error("");
    }

    process.exit(1);
  }

  console.log(
    `TOC check report: OK. Checked ${buildScopePages.length} in-scope pages (from TOC*.md) and found no TOC membership violations.`
  );
}

main();
