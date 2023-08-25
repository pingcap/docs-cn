---
title: 使用 Go-MySQL-Driver 连接到 TiDB
summary: 本文描述了 TiDB 和 Go-MySQL-Driver 的连接步骤，并给出了简单示例代码片段。
aliases: ['/zh/tidb/dev/dev-guide-sample-application-golang']
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# 如何用 Go-MySQL-Driver 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。**JDBC** 是 Java 的数据访问 API。[Go-MySQL-Driver](https://github.com/go-sql-driver/mysql) 是 [database/sql](https://pkg.go.dev/database/sql) 接口的 MySQL 实现。

本文档将展示如何使用 TiDB 和 Go-MySQL-Driver 来构造一个简单的 CRUD 应用程序。

## 前置要求

- 推荐 [Golang](https://go.dev/) **1.20** 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Serverless 集群](https://docs.pingcap.com/tidbcloud/dev-guide-build-cluster-in-cloud)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](https://docs.pingcap.com/zh/tidb/stable/quick-start-with-tidb#部署本地测试集群)或[部署正式 TiDB 集群](https://docs.pingcap.com/zh/tidb/stable/production-deployment-using-tiup)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 1. 克隆示例代码仓库到本地

```shell
git clone https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart.git
cd tidb-golang-sql-driver-quickstart
```

### 2. 配置连接信息

<details open>
<summary><b>(选项 1) TiDB Serverless</b></summary>

1. 在 TiDB Cloud 控制台中，打开 [Clusters](https://tidbcloud.com/console/clusters) 页面，选择你的 TiDB Serverless 集群，进入 **Overview** 页面，点击右上角的 **Connect** 按钮。
2. 确认窗口中的配置和你的运行环境一致。
    - **Endpoint Type** 为 **Public**
    - **Connect With** 为 **General**
    - Operating System 为你的运行环境
    > 如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。
3. 点击 **Generate password** 生成密码。
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。
4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 复制并粘贴对应连接字符串至 `.env` 中。

    ```properties
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值。

    TiDB Serverless 要求使用 secure connection，因此 `USE_SSL` 的值应为 `true`。

6. 保存文件。

</details>

<details>

<summary><b>(选项 2) TiDB Dedicated</b></summary>

1. 在 TiDB Cloud Web Console 中，选择你的 TiDB Dedicated 集群，进入 **Overview** 页面，点击右上角的 **Connect** 按钮。点击 **Allow Access from Anywhere**。
    > 更多配置细节，可参考 [TiDB Dedicated 标准连接教程](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

2. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

3. 复制并粘贴对应的连接字符串至 `.env` 中。需更改部分示例结果如下。

    ```properties
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值，并配置前面步骤中下载好的证书路径。

4. 保存文件。

</details>

<details>
<summary><b>(选项 3) 自建 TiDB</b></summary>

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 复制并粘贴对应的连接字符串至 `.env` 中。需更改部分示例结果如下。

    ```properties
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存文件。

</details>
