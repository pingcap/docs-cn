---
title: 自助生成 TiDB 文档 PDF 教程
summary: 介绍如何在本地定制输出符合特定场景需求的 TiDB 文档 PDF。
---

# 自助生成 TiDB 文档 PDF 教程

本教程提供了一种自助生成 PDF 格式的 TiDB 文档的方法。通过该方法，你可以在本地对 TiDB 文档目录进行自由排序和删减，定制输出符合特定场景需求的 PDF。

## 环境准备

以下准备工作只需要在第一次生成 PDF 时进行，以后再次生成 PDF 时可直接跳过。

### 准备 1：安装并配置 Docker 环境

> 预计耗时：30 分钟

下面以 macOS 或 Windows 安装 Docker Desktop 为例。

1. 安装 [Docker Desktop](https://docs.docker.com/get-docker/)。

2. 在 macOS Terminal 或者 Windows PowerShell 运行 `docker --version` 命令。

    如果看到 Docker 的版本信息，说明安装成功。

3. 配置 Docker 资源。

    1. 打开 Docker 应用程序，点击右上角的齿轮图标。
    2. 点击 **Resources**，然后将 **Memory** 设置为 `8.00 GB`。

4. 在 macOS Terminal 或者 Windows PowerShell 运行以下命令拉取用于 TiDB PDF 文档构建的 Docker 镜像：

    ```bash
    docker pull andelf/doc-build:0.1.9
    ```

### 准备 2：将 TiDB 文档仓库克隆到本地

> 预计耗时：10 分钟

TiDB 中文文档仓库的地址为 <https://github.com/pingcap/docs-cn>，英文文档仓库的地址为 <https://github.com/pingcap/docs>。

下面的步骤以克隆 TiDB 中文文档为例：

1. 打开 TiDB 中文文档仓库地址：<https://github.com/pingcap/docs-cn>。

2. 点击页面右上角的 [**Fork**](https://github.com/pingcap/docs-cn/fork) 按钮，等待 Fork 完成即可。

3. 通过以下任一方法将 TiDB 中文文档仓库克隆到本地。

    - 方法一：使用 GitHub Desktop 客户端。

        1. 安装并打开 [GitHub Desktop](https://desktop.github.com/)。
        2. 在 GitHub Desktop 中，点击 **File** > **Clone Repository**。
        3. 在 **GitHub.com** 选项卡中的 **Your Repositories** 下，选择你 Fork 出来的文档仓库，点击右下角的 **Clone**。

    - 方法二：使用以下 `git` 命令。

        ```shell
        cd $working_dir # 将 $working_dir 替换为你想放置 repo 的目录。例如，`cd ~/Documents/GitHub`
        git clone git@github.com:$user/docs-cn.git # 将 `$user` 替换为你的 GitHub ID

        cd $working_dir/docs-cn
        git remote add upstream git@github.com:pingcap/docs-cn.git # 添加上游仓库
        git remote -v
        ```

## 操作步骤

> 预计耗时：操作只需要 2 分钟，PDF 生成需要等待 0.5 到 1 个小时

1. 确保你本地 TiDB 文档仓库中的文件为上游 GitHub 文档仓库中的最新版本。

2. 按照你的需求，对 TiDB 文档目录进行自由排序和删减。

    1. 打开位于本地文档仓库根目录的 `TOC.md` 文件。
    2. 编辑 `TOC.md` 文件。例如，你可以删除所有不需要的文档章节标题和链接。

3. 按照 `TOC.md` 文件将所有文档中的章节整合到一个 Markdown 文件中。

    1. 启动 Docker 应用程序。
    2. 在 macOS Terminal 或者 Windows PowerShell 运行以下命令，进入 PDF 文档构建的 Docker 镜像：

        ```bash
        docker run -it -v ${doc-path}:/opt/data andelf/doc-build:0.1.9
        ```

        其中，`${doc-path}` 为要生成的文档在你本地的文件夹路径。例如，如果路径为 `/Users/${username}/Documents/GitHub/docs-cn`，则命令为：

        ```bash
        docker run -it -v /Users/${username}/Documents/GitHub/docs-cn:/opt/data andelf/doc-build:0.1.9
        ```

        执行后，如果提示 `WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested` 警告，可以忽略。

    3. 进入 `opt/data` 目录。

        ```bash
        cd /opt/data
        ```

    4. 将所有 Markdown 文档文件按照 `TOC.md` 整合到一个 `doc.md` 文件中。

        ```bash
        python3 scripts/merge_by_toc.py
        ```

       **期望输出：**

       在 `TOC.md` 所在的文件夹中，你将看到一个新生成的 `doc.md` 文件。

4. 生成文档 PDF：

    ```bash
    bash scripts/generate_pdf.sh
    ```

    **期望输出：**

    PDF 生成所需要的时间与文档的大小有关。对于完整的 TiDB 中文用户文档，大约需要 1 个小时。生成完成后，你将在文档所在的文件夹看到新生成的 PDF 文件 `output.pdf`。