import * as fs from "fs";
import path from "path";
import glob from "glob";

import { fromMarkdown } from "mdast-util-from-markdown";
import { frontmatter } from "micromark-extension-frontmatter";
import {
  frontmatterFromMarkdown,
  frontmatterToMarkdown,
} from "mdast-util-frontmatter";
import { gfm } from "micromark-extension-gfm";
import { mdxFromMarkdown, mdxToMarkdown } from "mdast-util-mdx";
import { gfmFromMarkdown, gfmToMarkdown } from "mdast-util-gfm";
import { toMarkdown } from "mdast-util-to-markdown";

import { visit } from "unist-util-visit";

export const generateMdAstFromFile = (fileContent) => {
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

// export const generateMdAstFromFile = (fileContent) => {
//   const mdAst = fromMarkdown(fileContent, {
//     extensions: [frontmatter(["yaml", "toml"]), gfm(), mdxjs()],
//     mdastExtensions: [
//       mdxFromMarkdown(),
//       frontmatterFromMarkdown(["yaml", "toml"]),
//       gfmFromMarkdown(),
//     ],
//   });
//   return mdAst;
// };

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

export const getAllMdList = (tocFile) => {
  const tocFileContent = fs.readFileSync(tocFile);
  const mdAst = generateMdAstFromFile(tocFileContent);
  const linkList = extractLinkNodeFromAst(mdAst);
  const filteredLinkList = filterLink(linkList);
  return filteredLinkList;
};

export const copySingleFileSync = (srcPath, destPath) => {
  const dir = path.dirname(destPath);

  if (!fs.existsSync(dir)) {
    // console.info(`Create empty dir: ${dir}`);
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.copyFileSync(srcPath, destPath);
};

export const writeFileSync = (destPath, fileContent) => {
  const dir = path.dirname(destPath);

  if (!fs.existsSync(dir)) {
    // console.info(`Create empty dir: ${dir}`);
    fs.mkdirSync(dir, { recursive: true });
  }

  fs.writeFileSync(destPath, fileContent);
};

const getMds = (src) => {
  return glob.sync(src + "/**/*.md");
};

export const getMdFileList = (prefix) => {
  return getMds(prefix);
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

export const astNode2mdStr = (astNode) => {
  const result = toMarkdown(astNode, {
    bullet: "-",
    extensions: [
      mdxToMarkdown(),
      frontmatterToMarkdown(["yaml", "toml"]),
      gfmToMarkdown(),
    ],
  });
  return result;
};
