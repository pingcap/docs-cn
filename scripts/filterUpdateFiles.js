import * as fs from "fs";
import path from "path";
import axios from "axios";
import { Octokit } from "octokit";

const GH_TOKEN = process.env.GH_TOKEN || "";

const octokit = GH_TOKEN
  ? new Octokit({
      auth: GH_TOKEN,
    })
  : new Octokit();

const getLocalCfg = () => {
  const fileContent = fs.readFileSync("./latest_translation_commit.json");
  const data = JSON.parse(fileContent);
  return data;
};

const writeLocalCfg = (cfg) => {
  const data = JSON.stringify(cfg);
  fs.writeFileSync("./latest_translation_commit.json", data);
};

const ghGetBranch = async (branchName = "master") => {
  const result = await octokit.request(
    `GET /repos/pingcap/docs/branches/${branchName}`,
    {
      owner: "pingcap",
      repo: "docs",
      branch: branchName,
    }
  );
  if (result.status === 200) {
    const data = result.data;
    return data;
  }
  throw new Error(`ghGetBranch error: ${result}`);
};

const ghCompareCommits = async (base = "", head = "") => {
  const basehead = `${base}...${head}`;
  const result = await octokit.request(
    `GET /repos/pingcap/docs/compare/${basehead}`,
    {
      owner: "pingcap",
      repo: "docs",
      basehead,
    }
  );
  if (result.status === 200) {
    const data = result.data;
    return data;
  }
  throw new Error(`ghGetBranch error: ${result}`);
};

const downloadFile = async (url, targetPath) => {
  const response = await axios({
    method: "GET",
    url,
    responseType: "stream",
  });
  const dir = path.dirname(targetPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  // pipe the result stream into a file on disc
  response.data.pipe(fs.createWriteStream(targetPath));
  // return a promise and resolve when download finishes
  return new Promise((resolve, reject) => {
    response.data.on("end", () => {
      resolve();
    });

    response.data.on("error", () => {
      reject();
    });
  });
};

const deleteFile = (targetFile) => {
  fs.rmSync(targetFile);
};

const handleFiles = async (fileList = []) => {
  console.log(fileList);
  for (let file of fileList) {
    const { status, raw_url, filename, previous_filename } = file;
    if (!filename.endsWith(".md")) {
      continue;
    }
    switch (status) {
      case "added":
      case "modified":
        await downloadFile(raw_url, `tmp/${filename}`);
        break;
      case "removed":
        deleteFile(filename);
        break;
      case "renamed":
        deleteFile(previous_filename);
        await downloadFile(raw_url, `tmp/${filename}`);
        break;
    }
  }
};

const main = async () => {
  const { target: branchName, sha: base } = getLocalCfg();
  const targetBranchData = await ghGetBranch(branchName);
  const head = targetBranchData?.commit?.sha;
  const comparedDetails = await ghCompareCommits(base, head);
  const files = comparedDetails?.files || [];
  handleFiles(files);
  writeLocalCfg({
    target: branchName,
    sha: head,
  });
};

main();
