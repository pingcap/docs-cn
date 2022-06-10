import {
  getAllMdList,
  copySingleFileSync,
  copyDirectorySync,
} from "./utils.js";

const extractFilefromList = (
  fileList = [],
  inputPath = ".",
  outputPath = "."
) => {
  fileList.forEach((filePath) => {
    copySingleFileSync(`${inputPath}/${filePath}`, `${outputPath}/${filePath}`);
  });
};

const main = () => {
  const filteredLinkList = getAllMdList("TOC-tidb-cloud.md");

  extractFilefromList(filteredLinkList, ".", "./tmp");
  copySingleFileSync("TOC-tidb-cloud.md", "./tmp/TOC.md");
  copyDirectorySync("./tidb-cloud/", "./tmp/tidb-cloud/");
};

main();
