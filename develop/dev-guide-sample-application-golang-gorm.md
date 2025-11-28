---
title: 使用 GORM 连接到 TiDB
summary: 了解如何使用 GORM 连接到 TiDB。本文提供了使用 GORM 与 TiDB 交互的 Golang 示例代码片段。
---

# 使用 GORM 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[GORM](https://gorm.io/index.html) 是当前比较流行的开源 Golang ORM 框架并且适配了 TiDB 的 `AUTO_RANDOM` 等特性。同时，TiDB 为 [GORM 的默认支持数据库](https://gorm.io/zh_CN/docs/connecting_to_the_database.html#TiDB)。

本文档将展示如何使用 TiDB 和 GORM 来完成以下任务：

- 配置你的环境。
- 使用 GORM 连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Serverless、TiDB Dedicated 和本地部署的 TiDB。

## 前置需求

- 推荐 [Go](https://go.dev/) **1.20** 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```shell
git clone https://github.com/tidb-samples/tidb-golang-gorm-quickstart.git
cd tidb-golang-gorm-quickstart
```

### 第 2 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Serverless 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Endpoint Type** 为 `Public`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 如果你还没有设置密码，点击 **Create password** 生成一个随机密码。

    > **Tip:**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset password** 重新生成密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

6. 复制并粘贴对应连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值。

    TiDB Serverless 要求使用 TLS (SSL) connection，因此 `USE_SSL` 的值应为 `true`。

7. 保存 `.env` 文件。

</div>

<div label="TiDB Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Dedicated 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会出现连接对话框。

3. 在对话框中点击 **Allow Access from Anywhere**。

    更多配置细节，可参考 [TiDB Dedicated 标准连接教程（英文）](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 复制并粘贴对应的连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值。

6. 保存 `.env` 文件。

</div>

<div label="本地部署 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 复制并粘贴对应 TiDB 的连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并设置 `USE_SSL` 为 `false`。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第 3 步：运行代码并查看结果

1. 运行下述命令，执行示例代码：

    ```shell
    make
    ```

2. 查看 [`Expected-Output.txt`](https://github.com/tidb-samples/tidb-golang-gorm-quickstart/blob/main/Expected-Output.txt)，并与你的程序输出进行比较。结果近似即为连接成功。

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-golang-gorm-quickstart](https://github.com/tidb-samples/tidb-golang-gorm-quickstart)。

### 连接到 TiDB

```golang
func createDB() *gorm.DB {
    dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&tls=%s",
        ${tidb_user}, ${tidb_password}, ${tidb_host}, ${tidb_port}, ${tidb_db_name}, ${use_ssl})

    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        panic(err)
    }

    return db
}
```

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 等替换为你的 TiDB 集群的实际值。因为 TiDB Serverless 要求使用 TLS (SSL) connection，因此在连接到 TiDB Serverless 时 `${use_ssl}` 的值应为 `true`。

### 插入数据

```golang
db.Create(&Player{ID: "id", Coins: 1, Goods: 1})
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```golang
var queryPlayer Player
db.Find(&queryPlayer, "id = ?", "id")
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```golang

db.Save(&Player{ID: "id", Coins: 100, Goods: 1})
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```golang
db.Delete(&Player{ID: "id"})
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 关于 GORM 的更多使用方法，可以参考 [GORM 官方文档](https://gorm.io/zh_CN/docs/index.html) 及 GORM 官方文档中的 [TiDB 章节](https://gorm.io/zh_CN/docs/connecting_to_the_database.html#TiDB)。
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://pingkai.cn/learn)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.cn/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，寻求帮助。
