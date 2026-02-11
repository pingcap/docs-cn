---
title: 通过 SQL 快速上手 TiDB + AI
summary: 学习如何仅使用 SQL 语句快速上手 TiDB 向量搜索，为你的生成式 AI 应用提供支持。
aliases: ['/zh/tidb/stable/vector-search-get-started-using-sql/','/zh/tidb/dev/vector-search-get-started-using-sql/','/zh/tidbcloud/vector-search-get-started-using-sql/']
---

# 通过 SQL 快速上手 TiDB + AI

TiDB 扩展了 MySQL 语法以支持[向量搜索](/ai/concepts/vector-search-overview.md)，并引入了新的[向量数据类型](/ai/reference/vector-search-data-types.md)以及若干[向量函数](/ai/reference/vector-search-functions-and-operators.md)。

本文档演示了如何仅使用 SQL 语句快速上手 TiDB 向量搜索。你将学习如何使用 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)完成以下操作：

- 连接到你的 TiDB 集群。
- 创建向量表。
- 存储向量嵌入。
- 执行向量搜索查询。

> **注意：**
>
> - 向量搜索功能目前为 beta 版本，可能会在未提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## 前置条件

要完成本文档中的步骤，你需要：

- 在本地安装 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)（MySQL CLI）。
- 一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考[创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md)来创建属于你自己的 TiDB Cloud 集群。
- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产环境 TiDB 集群](/production-deployment-using-tiup.md)来创建本地集群。

## 快速上手

### 步骤 1. 连接到 TiDB 集群

根据你选择的 TiDB 部署方式，连接到你的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，然后点击目标集群名称进入其概览页面。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 在连接对话框中，从 **Connect With** 下拉列表中选择 **MySQL CLI**，并保持 **Connection Type** 的默认设置为 **Public**。

4. 如果你还未设置密码，点击 **Generate Password** 生成一个随机密码。

5. 复制连接命令并粘贴到你的终端中。以下是 macOS 的示例：

    ```bash
    mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
    ```

</div>
<div label="TiDB 自托管" value="tidb">

当你自托管的 TiDB 集群启动后，在终端中执行集群连接命令。

以下是 macOS 的示例连接命令：

```bash
mysql --comments --host 127.0.0.1 --port 4000 -u root
```

</div>

</SimpleTab>

### 步骤 2. 创建向量表

在创建表时，你可以通过指定 `VECTOR` 数据类型，将某一列定义为[向量](/ai/concepts/vector-search-overview.md#vector-embedding)列。

例如，要创建一个包含三维 `VECTOR` 列的 `embedded_documents` 表，可在 MySQL CLI 中执行如下 SQL 语句：

```sql
USE test;
CREATE TABLE embedded_documents (
    id        INT       PRIMARY KEY,
    -- Column to store the original content of the document.
    document  TEXT,
    -- Column to store the vector representation of the document.
    embedding VECTOR(3)
);
```

预期输出如下：

```text
Query OK, 0 rows affected (0.27 sec)
```

### 步骤 3. 向表中插入向量嵌入

向 `embedded_documents` 表中插入三条带有[向量嵌入](/ai/concepts/vector-search-overview.md#vector-embedding)的文档：

```sql
INSERT INTO embedded_documents
VALUES
    (1, 'dog', '[1,2,1]'),
    (2, 'fish', '[1,2,4]'),
    (3, 'tree', '[1,0,0]');
```

预期输出如下：

```
Query OK, 3 rows affected (0.15 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

> **注意**
>
> 本示例简化了向量嵌入的维度，仅使用三维向量进行演示。
>
> 在实际应用中，[嵌入模型](/ai/concepts/vector-search-overview.md#embedding-model)通常会生成数百甚至数千维的向量嵌入。

### 步骤 4. 查询向量表

为验证文档是否已正确插入，可查询 `embedded_documents` 表：

```sql
SELECT * FROM embedded_documents;
```

预期输出如下：

```sql
+----+----------+-----------+
| id | document | embedding |
+----+----------+-----------+
|  1 | dog      | [1,2,1]   |
|  2 | fish     | [1,2,4]   |
|  3 | tree     | [1,0,0]   |
+----+----------+-----------+
3 rows in set (0.15 sec)
```

### 步骤 5. 执行向量搜索查询

与全文搜索类似，用户在使用向量搜索时会向应用提供搜索词。

本例中，搜索词为 “a swimming animal”，其对应的向量嵌入假定为 `[1,2,3]`。在实际应用中，你需要使用嵌入模型将用户的搜索词转换为向量嵌入。

执行如下 SQL 语句，TiDB 会通过计算并排序表中向量嵌入与 `[1,2,3]` 的余弦距离（`vec_cosine_distance`），找出距离最近的三条文档。

```sql
SELECT id, document, vec_cosine_distance(embedding, '[1,2,3]') AS distance
FROM embedded_documents
ORDER BY distance
LIMIT 3;
```

预期输出如下：

```plain
+----+----------+---------------------+
| id | document | distance            |
+----+----------+---------------------+
|  2 | fish     | 0.00853986601633272 |
|  1 | dog      | 0.12712843905603044 |
|  3 | tree     |  0.7327387580875756 |
+----+----------+---------------------+
3 rows in set (0.15 sec)
```

搜索结果中的三条数据按照与查询向量的距离升序排列：距离越小，`document` 与搜索向量的相关性越高。

因此，根据输出，最有可能的“swimming animal”是 fish，其次可能是会游泳的 dog。

## 另请参阅

- [向量数据类型](/ai/reference/vector-search-data-types.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
