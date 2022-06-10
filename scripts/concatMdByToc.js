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
import { gfmFromMarkdown, gfmToMarkdown } from "mdast-util-gfm";
import { mdxjs } from "micromark-extension-mdxjs";
import { mdxFromMarkdown, mdxToMarkdown } from "mdast-util-mdx";
import { toMarkdown } from "mdast-util-to-markdown";

import { visit } from "unist-util-visit";

import {
  getAllMdList,
  generateMdAstFromFile,
  astNode2mdStr,
  writeFileSync,
} from "./utils.js";

// const copyableReg = /{{< copyable\s+(.+)\s+>}}\r?\n/g;
const copyableReg = /\\{\\{\\< copyable\s+(.+)\s+>}}\r?\n/g;

const myArgs = process.argv.slice(2);

const srcToc = myArgs[0] || "TOC.md";
const targetFile = myArgs[1] || `doc_merged.md`;

const isFileExist = (path = "") => {
  return fs.existsSync(path);
};

const handleMdAst = (mdAst, fileName = "") => {
  visit(mdAst, (node) => {
    switch (node.type) {
      case "yaml":
        const fileNameWithoutExt = fileName
          .replace(".md", "")
          .replace(".mdx", "");
        node.type = "html";
        node.value = `<a id="title-${fileNameWithoutExt}" name="title-${fileNameWithoutExt}"></a>`;
        break;
      case "html":
        if (node.value.includes(`<video`) || node.value.includes(`</video>`)) {
          node.type = "text";
          node.value = "";
        }
        break;
      case "image":
        const imgUrl = node.url;
        if (imgUrl.startsWith(`/media/`)) {
          node.url = `.${imgUrl}`;
        }
        break;
      case "link":
        const linkUrl = node.url;
        if (!linkUrl.startsWith(`http`)) {
          const mdNameWithHash = linkUrl.split(`/`).pop();
          const mdName = mdNameWithHash.replace(/\.md.*/, "");
          node.url = `#title-${mdName}`;
        }
        break;
      default:
        // console.log(node);
        break;
    }
  });
};

const handleSingleMd = (filePath) => {
  const mdFileContent = fs.readFileSync(filePath);
  const fileName = filePath.split(`/`).pop();
  const mdAst = generateMdAstFromFile(mdFileContent);
  handleMdAst(mdAst, fileName);
  const MdStr = astNode2mdStr(mdAst);
  const newMdStr = MdStr.replaceAll(copyableReg, "");
  isFileExist(`tmp/${targetFile}`)
    ? fs.appendFileSync(`tmp/${targetFile}`, newMdStr)
    : writeFileSync(`tmp/${targetFile}`, newMdStr);
};

const main = () => {
  const fileList = getAllMdList(srcToc);
  // console.log(fileList);
  // handleSingleMd("./overview.md");
  fileList.forEach((filePath) => {
    handleSingleMd(`.${filePath}`);
  });
};

main();
