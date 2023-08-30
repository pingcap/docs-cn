---
title: 使用 GORM 连接到 TiDB
summary: 本文描述了 TiDB 和 GORM 的连接步骤，并给出了简单示例代码片段。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# 如何用 GORM 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[GORM](https://gorm.io/index.html) 是当前比较流行的开源 Golang ORM 框架，且 GORM 适配了 TiDB 的 `AUTO_RANDOM` 等特性，TiDB 为 [GORM 的默认支持数据库](https://gorm.io/zh_CN/docs/connecting_to_the_database.html#TiDB)。

本文档将展示如何使用 TiDB 和 GORM 来构造一个简单的 CRUD 应用程序。

## 前置要求

- 推荐 [Golang](https://go.dev/) **1.20** 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Serverless 集群](https://docs.pingcap.com/tidbcloud/dev-guide-build-cluster-in-cloud)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](https://docs.pingcap.com/zh/tidb/stable/quick-start-with-tidb#部署本地测试集群)或[部署正式 TiDB 集群](https://docs.pingcap.com/zh/tidb/stable/production-deployment-using-tiup)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

在命令行中运行以下命令，克隆示例代码仓库到本地：

```shell
git clone https://github.com/tidb-samples/tidb-golang-gorm-quickstart.git
cd tidb-golang-gorm-quickstart
```

### 第 2 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Serverless">

1. 在 TiDB Cloud Web Console 中，选择你的 TiDB Serverless 集群，进入 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，会显示连接对话框。

3. 确认窗口中的配置和你的运行环境一致。

    - **Endpoint Type** 为 `Public`
    - **Connect With** 选择 `General`
    - **Operating System** 为你的运行环境

    <Tip>如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。</Tip>

4. 点击 **Create password** 生成密码。

   <Tip>如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset password** 重新生成密码。</Tip>

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

6. 复制并粘贴对应连接字符串至 `.env` 中。需更改部分示例结果如下。

    ```properties
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值。

    TiDB Serverless 要求使用 secure connection，因此 `USE_SSL` 的值应为 `true`。

7. 保存文件。

</div>

<div label="TiDB Dedicated">

1. 在 TiDB Cloud Web Console 中，选择你的 TiDB Dedicated 集群，进入 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，会显示连接对话框。

3. 点击 **Allow Access from Anywhere**。

    更多配置细节，可参考 [TiDB Dedicated 标准连接教程](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 复制并粘贴对应的连接字符串至 `.env` 中。需更改部分示例结果如下。

    ```properties
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{user}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为 **Connect** 窗口中获得的值。

6. 保存文件。

</div>

<div label="本地部署 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 复制并粘贴对应 TiDB 的连接字符串至 `.env` 中。需更改部分示例结果如下。

    ```properties
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并设置 `USE_SSL` 为 `false`。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存文件。

</div>

</SimpleTab>

### 第 3 步：运行代码并查看结果

1. 运行下述命令，执行示例代码：

    ```shell
    make
    ```

2. 查看[示例输出](https://github.com/tidb-samples/tidb-golang-gorm-quickstart/blob/main/Expected-Output.txt)，并与你的程序输出进行比较。结果近似即为连接成功。

## 重点代码片段

你可参考以下关键代码片段，完成自己的应用开发。

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

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 等替换为你的 TiDB 集群的实际值。因为 TiDB Serverless 要求使用 secure connection，因此在使用 TiDB Serverless 时 `${use_ssl}` 的值应为 `true`。

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

## 注意事项

- 完整代码及其运行方式，见 [tidb-golang-gorm-quickstart](https://github.com/tidb-samples/tidb-golang-gorm-quickstart/blob/main/README-zh.md) GitHub 仓库。
- 关于 GORM 的更多使用方法及细节，可以参考 [GORM 官方文档](https://gorm.io/docs/) 及 GORM 官方文档中的 [TiDB 章节](https://gorm.io/docs/connecting_to_the_database.html#TiDB)。

## 下一步

- 你可以继续阅读开发者文档，以获取更多关于 TiDB 的开发者知识。例如：[插入数据](https://docs.pingcap.com/zh/tidb/stable/dev-guide-insert-data)，[更新数据](https://docs.pingcap.com/zh/tidb/stable/dev-guide-update-data)，[删除数据](https://docs.pingcap.com/zh/tidb/stable/dev-guide-delete-data)，[单表读取](https://docs.pingcap.com/zh/tidb/stable/dev-guide-get-data-from-single-table)，[事务](https://docs.pingcap.com/zh/tidb/stable/dev-guide-transaction-overview)，[SQL 性能优化](https://docs.pingcap.com/zh/tidb/stable/dev-guide-optimize-sql-overview)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/back-end-developer/)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。
