import * as fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import glob from "glob";

import { visit } from "unist-util-visit";

import { generateMdAstFromFile } from "./utils.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");

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

const sortByLocale = (left, right) => left.localeCompare(right);

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

function toTargetRel(url = "") {
  return stripQueryAndHash(url).path.replace(/^\/+/, "");
}

function extractInternalDocTargetsFromUrls(urls = []) {
  return urls.filter((url) => isInternalDocLink(url)).map((url) => toTargetRel(url));
}

function extractInternalDocTargetsFromMarkdownFile(absPath) {
  return extractInternalDocTargetsFromUrls(extractUrlsFromMarkdownFile(absPath));
}

function sortedValues(values = []) {
  return [...values].sort(sortByLocale);
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
    .sort(sortByLocale);
  return tocFiles;
}

function buildTocIndex(tocFiles) {
  const tocToPages = new Map(); // tocFile -> Set(relPathWithoutLeadingSlash)
  const anyTocPages = new Set();
  const pageToTocs = new Map(); // pageRel -> Set(tocFile)

  tocFiles.forEach((toc) => {
    const tocAbs = path.join(ROOT, toc);
    const pages = new Set();

    extractInternalDocTargetsFromMarkdownFile(tocAbs).forEach((rel) => {
        pages.add(rel);
        anyTocPages.add(rel);

        const tocs = pageToTocs.get(rel) || new Set();
        tocs.add(toc);
        pageToTocs.set(rel, tocs);
    });

    tocToPages.set(toc, pages);
  });

  const cloudTocPages = new Set(
    CLOUD_TOC_FILES.flatMap((toc) => [...(tocToPages.get(toc) || new Set())])
  );

  return { tocToPages, anyTocPages, pageToTocs, cloudTocPages };
}

function expectedSetForTarget(targetRel, tocToPages, anyTocPages, cloudTocPages) {
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
    return {
      ok: cloudTocPages.has(targetRel),
      expectedLabel: "any TiDB Cloud TOC",
    };
  }

  const matchedPrefix = PREFIX_TO_TOC.find(({ prefix }) =>
    targetRel.startsWith(prefix)
  );
  if (matchedPrefix) {
    const set = tocToPages.get(matchedPrefix.toc) || new Set();
    return { ok: set.has(targetRel), expectedLabel: matchedPrefix.toc };
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
  if (tocFiles.length === 0) {
    console.error("TOC check error: no TOC*.md files found in repo root.");
    process.exit(1);
  }

  const { tocToPages, anyTocPages, pageToTocs, cloudTocPages } =
    buildTocIndex(tocFiles);
  const buildScopePages = sortedValues(anyTocPages);

  const missingScopePages = [];
  const violations = [];

  buildScopePages.forEach((sourceRel) => {
    const sourceAbs = path.join(ROOT, sourceRel);
    if (!fs.existsSync(sourceAbs)) {
      missingScopePages.push(sourceRel);
      return;
    }

    extractInternalDocTargetsFromMarkdownFile(sourceAbs)
      .filter((targetRel) =>
        !SPECIAL_IMPLICIT_TARGETS.has(path.basename(targetRel))
      )
      .forEach((targetRel) => {
        const { ok, expectedLabel } = expectedSetForTarget(
          targetRel,
          tocToPages,
          anyTocPages,
          cloudTocPages
        );
        if (!ok) {
          violations.push({
            sourceRel,
            targetRel,
            expectedLabel,
          });
        }
      });
  });

  if (missingScopePages.length > 0) {
    // Printed below in a grouped summary.
  }

  if (violations.length > 0) {
    // Printed below in a grouped summary.
  }

  if (missingScopePages.length > 0 || violations.length > 0) {
    const byTarget = violations.reduce((groupedMap, violation) => {
      const current = groupedMap.get(violation.targetRel) || {
        targetRel: violation.targetRel,
        expectedLabel: violation.expectedLabel,
        sourceFiles: new Set(),
      };
      current.sourceFiles.add(violation.sourceRel);
      groupedMap.set(violation.targetRel, current);
      return groupedMap;
    }, new Map());

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
      `- TOC membership violations: ${violations.length} links across ${byTarget.size} targets`
    );
    console.error("");

    if (missingScopePages.length > 0) {
      console.error(
        `=== Missing pages referenced by TOC*.md (${missingScopePages.length}) ===`
      );
      console.error("");
      missingScopePages.slice(0, maxMissing).forEach((p) => {
        const referencedBy = sortedValues(pageToTocs.get(p) || new Set());
        if (referencedBy.length > 0) {
          console.error(`- ${p}`);
          console.error(`  referenced by: ${referencedBy.join(", ")}`);
        } else {
          console.error(`- ${p}`);
        }
      });
      if (!verbose && missingScopePages.length > maxMissing) {
        console.error(
          `- ... and ${missingScopePages.length - maxMissing} more (set TOC_MAX_MISSING or VERBOSE_TOC=1 to show more)`
        );
      }
      console.error("");
    }

    if (violations.length > 0) {
      console.error(`=== TOC membership violations (grouped by target) ===`);
      console.error("");

      const targets = [...byTarget.values()].sort((a, b) => {
        const diff = b.sourceFiles.size - a.sourceFiles.size;
        if (diff !== 0) return diff;
        return sortByLocale(a.targetRel, b.targetRel);
      });
      const shownTargets = verbose ? targets : targets.slice(0, maxFiles);

      shownTargets.forEach((item, index) => {
        if (index > 0) {
          console.error("");
        }

        const targetUrl = `/${item.targetRel}`;
        const targetTocs = sortedValues(pageToTocs.get(item.targetRel) || new Set());
        const sourceFiles = sortedValues(item.sourceFiles);

        console.error(`Target: ${targetUrl}`);
        if (targetTocs.length === 0) {
          if (item.expectedLabel === "any TOC*.md") {
            console.error(`Issue: Missing from TOC index`);
            console.error(`Expected TOC: any TOC*.md`);
          } else {
            console.error(`Issue: Missing from TOC index`);
            console.error(`Expected TOC: ${item.expectedLabel}`);
          }
        } else {
          console.error(`Issue: TOC mismatch`);
          console.error(`Current TOC: ${targetTocs.join(", ")}`);
          console.error(`Expected TOC: ${item.expectedLabel}`);
        }

        console.error(`Referenced in (${sourceFiles.length}):`);
        const shownFiles = verbose
          ? sourceFiles
          : sourceFiles.slice(0, maxLinksPerFile);
        shownFiles.forEach((sourceRel) => {
          console.error(`  - ${sourceRel}`);
        });
        if (!verbose && sourceFiles.length > maxLinksPerFile) {
          console.error(
            `  - ... and ${sourceFiles.length - maxLinksPerFile} more (set TOC_MAX_LINKS_PER_FILE or VERBOSE_TOC=1)`
          );
        }
      });

      if (!verbose && targets.length > maxFiles) {
        console.error("");
        console.error(
          `... and ${targets.length - maxFiles} more target links (set TOC_MAX_FILES or VERBOSE_TOC=1)`
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
