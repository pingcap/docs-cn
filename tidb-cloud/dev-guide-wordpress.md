---
title: 使用 WordPress 连接 TiDB Cloud Serverless
summary: 了解如何使用 TiDB Cloud Serverless 运行 WordPress。本教程提供分步指导，帮助您在几分钟内运行 WordPress + TiDB Cloud Serverless。
---

# 使用 WordPress 连接 TiDB Cloud Serverless

TiDB 是一个兼容 MySQL 的数据库，TiDB Cloud Serverless 是一个全托管的 TiDB 产品，而 [WordPress](https://github.com/WordPress) 是一个免费的开源内容管理系统（CMS），让用户可以创建和管理网站。WordPress 使用 PHP 编写，并使用 MySQL 数据库。

在本教程中，您可以学习如何免费使用 TiDB Cloud Serverless 运行 WordPress。

> **注意：**
>
> 除了 TiDB Cloud Serverless 外，本教程也适用于 TiDB Cloud Dedicated 和 TiDB Self-Managed 集群。但是，为了成本效益，强烈建议使用 TiDB Cloud Serverless 运行 WordPress。

## 前提条件

要完成本教程，您需要：

- 一个 TiDB Cloud Serverless 集群。如果您还没有，请按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建您自己的 TiDB Cloud 集群。

## 使用 TiDB Cloud Serverless 运行 WordPress

本节演示如何使用 TiDB Cloud Serverless 运行 WordPress。

### 步骤 1：克隆 WordPress 示例仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/Icemap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### 步骤 2：安装依赖

1. 示例仓库需要 [Docker](https://www.docker.com/) 和 [Docker Compose](https://docs.docker.com/compose/) 来启动 WordPress。如果您已经安装了它们，可以跳过这一步。强烈建议在 Linux 环境（如 Ubuntu）中运行您的 WordPress。运行以下命令安装 Docker 和 Docker Compose：

    ```shell
    sudo sh install.sh
    ```

2. 示例仓库包含 [TiDB 兼容性插件](https://github.com/pingcap/wordpress-tidb-plugin)作为子模块。运行以下命令更新子模块：

    ```shell
    git submodule update --init --recursive
    ```

### 步骤 3：配置连接信息

配置 WordPress 数据库与 TiDB Cloud Serverless 的连接。

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

    - **连接类型**设置为 `Public`。
    - **连接工具**设置为 `WordPress`。
    - **操作系统**设置为 `Debian/Ubuntu/Arch`。
    - **数据库**设置为您想要使用的数据库—例如 `test`。

4. 点击**生成密码**创建随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码或点击**重置密码**生成新密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{HOST}'  # 例如 gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{USERNAME}'  # 例如 xxxxxx.root
    TIDB_PASSWORD='{PASSWORD}'
    TIDB_DB_NAME='test'
    ```

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数。默认情况下，您的 TiDB Cloud Serverless 附带一个 `test` 数据库。如果您已经在 TiDB Cloud Serverless 集群中创建了另一个数据库，您可以将 `test` 替换为您的数据库名称。

7. 保存 `.env` 文件。

### 步骤 4：使用 TiDB Cloud Serverless 启动 WordPress

1. 执行以下命令将 WordPress 作为 Docker 容器运行：

    ```shell
    docker compose up -d
    ```

2. 如果您在本地机器上启动容器，请访问 [localhost](http://localhost/) 设置您的 WordPress 站点；如果 WordPress 在远程机器上运行，请访问 `http://<your_instance_ip>`。

### 步骤 5：确认数据库连接

1. 在 TiDB Cloud 控制台上关闭集群的连接对话框，并打开 **SQL 编辑器**页面。
2. 在左侧的**模式**标签下，点击您连接到 WordPress 的数据库。
3. 确认您现在可以在该数据库的表列表中看到 WordPress 表（如 `wp_posts` 和 `wp_comments`）。

## 需要帮助？

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。
