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

const checkDestDir = (destPath) => {
  const dir = path.dirname(destPath);

  if (!fs.existsSync(dir)) {
    // console.info(`Create empty dir: ${dir}`);
    fs.mkdirSync(dir, { recursive: true });
  }
};

export const copySingleFileSync = (srcPath, destPath) => {
  checkDestDir(destPath);

  fs.copyFileSync(srcPath, destPath);
};

export const copyFileWithCustomContentSync = (srcPath, destPath, handler) => {
  const srcContent = fs.readFileSync(srcPath).toString();
  const fileContent = handler(srcContent);
  writeFileSync(destPath, fileContent);
};

export const writeFileSync = (destPath, fileContent) => {
  checkDestDir(destPath);

  fs.writeFileSync(destPath, fileContent);
};

const getMds = (src) => {
  return glob.sync(src + "/**/*.md", {
    ignore: ["**/node_modules/**", "./node_modules/**"],
  });
};

export const getMdFileList = (prefix) => {
  return getMds(prefix);
};

export const getFileList = (prefix) => {
  return glob.sync(prefix + "/**/*", {
    ignore: ["**/node_modules/**", "./node_modules/**"],
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

export const copyDirectoryWithCustomContentSync = (
  srcPath,
  destPath,
  handler
) => {
  const allFiles = getAllFiles(srcPath);
  allFiles.forEach((filePath) => {
    const relativePath = path.relative(srcPath, filePath);
    copyFileWithCustomContentSync(filePath, destPath + relativePath, handler);
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

export const removeCustomContent = (type, content = "") => {
  const TIDB_CUSTOM_CONTENT_REGEX =
    /<CustomContent +platform=["']tidb["'] *>(.|\n)*?<\/CustomContent>\n/g;
  const TIDB_CLOUD_CONTENT_REGEX =
    /<CustomContent +platform=["']tidb-cloud["'] *>(.|\n)*?<\/CustomContent>\n/g;
  if (type === "tidb") {
    return content.replaceAll(TIDB_CLOUD_CONTENT_REGEX, "");
  }
  return content.replaceAll(TIDB_CUSTOM_CONTENT_REGEX, "");
};
