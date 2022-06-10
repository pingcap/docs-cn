import * as fs from "fs";
import path from "path";

import { fromMarkdown } from "mdast-util-from-markdown";
import { frontmatter } from "micromark-extension-frontmatter";
import { frontmatterFromMarkdown } from "mdast-util-frontmatter";
import { gfm } from "micromark-extension-gfm";
import { mdxFromMarkdown } from "mdast-util-mdx";
import { gfmFromMarkdown } from "mdast-util-gfm";

import { visit } from "unist-util-visit";

const copySingleFileSync = (srcPath, destPath) => {
  const dir = path.dirname(destPath);

  if (!fs.existsSync(dir)) {
    // console.info(`Create empty dir: ${dir}`);
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.copyFileSync(srcPath, destPath);
};

const generateMdAstFromFile = (fileContent) => {
  const mdAst = fromMarkdown(fileContent, {
    extensions: [frontmatter(["yaml", "toml"]), gfm()],
    mdastExtensions: [
      mdxFromMarkdown(),
      frontmatterFromMarkdown(["yaml", "toml"]),
      gfmFromMarkdown(),
    ],
  });
  return mdAst;
};

const extractLinkNodeFromAst = (mdAst) => {
  const linkList = [];
  visit(mdAst, (node) => {
    if (node.type === "link") {
      linkList.push(node.url);
    }
  });
  return linkList;
};

const filterLink = (srcList = []) => {
  const result = srcList.filter((item) => {
    const url = item.trim();
    if (url.endsWith(".md") || url.endsWith(".mdx")) return true;
    return false;
  });
  return result;
};

const extractFilefromList = (
  fileList = [],
  inputPath = ".",
  outputPath = "."
) => {
  fileList.forEach((filePath) => {
    copySingleFileSync(`${inputPath}/${filePath}`, `${outputPath}/${filePath}`);
  });
};

const getAllFiles = (dirPath, arrayOfFiles) => {
  const files = fs.readdirSync(dirPath);

  arrayOfFiles = arrayOfFiles || [];

  files.forEach((file) => {
    if (fs.statSync(dirPath + "/" + file).isDirectory()) {
      arrayOfFiles = getAllFiles(dirPath + "/" + file, arrayOfFiles);
    } else {
      arrayOfFiles.push(path.join(dirPath, "/", file));
    }
  });

  return arrayOfFiles;
};

export const copyDirectorySync = (srcPath, destPath) => {
  const allFiles = getAllFiles(srcPath);
  allFiles.forEach((filePath) => {
    const relativePath = path.relative(srcPath, filePath);
    copySingleFileSync(filePath, destPath + relativePath);
  });
};

const main = () => {
  const tocFile = fs.readFileSync("TOC-tidb-cloud.md");
  const mdAst = generateMdAstFromFile(tocFile);
  const linkList = extractLinkNodeFromAst(mdAst);
  const filteredLinkList = filterLink(linkList);

  extractFilefromList(filteredLinkList, ".", "./tmp");
  copySingleFileSync("TOC-tidb-cloud.md", "./tmp/TOC.md");
  copyDirectorySync("./tidb-cloud/", "./tmp/tidb-cloud/");
};

main();
