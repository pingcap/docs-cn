import {
  getFileList,
  copySingleFileSync,
  copyFileWithCustomContentSync,
  removeCustomContent,
} from "./utils.js";

const contentHandler = (content = "") => {
  return removeCustomContent("tidb", content);
};

const extractFilefromList = (
  fileList = [],
  inputPath = ".",
  outputPath = "."
) => {
  fileList.forEach((filePath = "") => {
    if (
      filePath.includes(`/tidb-cloud/`) ||
      filePath.includes(`TOC-tidb-cloud.md`)
    ) {
      return;
    }
    if (filePath.endsWith(".md")) {
      copyFileWithCustomContentSync(
        `${inputPath}/${filePath}`,
        `${outputPath}/${filePath}`,
        contentHandler
      );
    } else {
      try {
        copySingleFileSync(
          `${inputPath}/${filePath}`,
          `${outputPath}/${filePath}`
        );
      } catch (error) {}
    }
  });
};

const main = () => {
  const filteredLinkList = getFileList(".");

  extractFilefromList(filteredLinkList, ".", "./tmp");
};

main();
