---
title: 使用 SQL 开始向量搜索
summary: 了解如何在 TiDB 中使用 SQL 语句快速开始向量搜索，从而为你的生成式 AI 应用提供支持。
---

# 使用 SQL 开始向量搜索

TiDB 扩展了 MySQL 语法以支持[向量搜索](/vector-search-overview.md)，并引入了[向量数据类型](/vector-search-data-types.md)和多个[向量函数](/vector-search-functions-and-operators.md)。

本文将展示如何使用 SQL 语句在 TiDB 中进行向量搜索。在本文中，你将使用 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)完成以下任务：

- 连接到 TiDB 集群
- 创建向量表
- 存储向量嵌入
- 执行向量搜索查询

> **警告：**
>
> 向量搜索目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 前置需求

为了能够顺利完成本文中的操作，你需要提前：

- 在你的机器上安装 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) (MySQL CLI)
- 准备一个 TiDB 集群

如果你还没有 TiDB 集群，可以按照以下任一种方式创建：

- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。
- 参考[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群)，创建 TiDB Cloud 集群。

## 快速开始

### 第 1 步：连接到 TiDB 集群

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="本地部署 TiDB">

在本地部署的集群启动后，在终端中执行你的集群连接命令：

以下为 macOS 上的连接命令示例：

```bash
mysql --comments --host 127.0.0.1 --port 4000 -u root
```

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，可以按照以下步骤连接到集群：

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，单击你的 TiDB Cloud Serverless 集群名，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 在连接对话框中，选择 **Connect With** 下拉列表中的 **MySQL CLI**，并保留 **Connection Type** 的默认值为 **Public**。

4. 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

5. 复制对话框中的连接命令，并粘贴到终端中执行。以下为 macOS 上的连接命令示例：

    ```bash
    mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
    ```

</div>

</SimpleTab>

### 第 2 步：创建向量表

创建表时，你可以使用 `VECTOR` 数据类型声明指定列为[向量](/vector-search-overview.md#向量嵌入)列。

例如，要创建一个带有三维 `VECTOR` 列的 `embedded_documents` 表，可以使用 MySQL CLI 执行以下 SQL 语句：

```sql
USE test;
CREATE TABLE embedded_documents (
    id        INT       PRIMARY KEY,
    -- document 列存储文档的原始内容
    document  TEXT,
    -- embedding 列存储文档的向量表示
    embedding VECTOR(3)
);
```

预期输出如下：

```text
Query OK, 0 rows affected (0.27 sec)
```

### 第 3 步：向表中插入向量

向 `embedded_documents` 表中插入三行，每一行包含数据和数据的[向量嵌入](/vector-search-overview.md#向量嵌入)：

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

> **Note**
>
> 为了方便展示，本示例简化了向量的维数，仅使用三维向量。
>
> 在实际应用中，[嵌入模型](/vector-search-overview.md#嵌入模型)通常会生成数百或数千维的向量。

### 第 4 步：查询向量表

要验证上一步中的三行数据是否已正确插入，可以查询 `embedded_documents` 表：

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

### 第 5 步：执行向量搜索查询

与全文搜索类似，在使用向量搜索时，你需要提供搜索词。

在本例中，搜索词是“一种会游泳的动物”，假设其对应的向量是 `[1,2,3]`。在实际应用中，你需要使用[嵌入模型](/vector-search-overview.md#嵌入模型)将用户的搜索词转换为向量。

执行以下 SQL 语句后，TiDB 会计算 `[1,2,3]` 与表中各向量之间的余弦距离 (`vec_cosine_distance`)，然后对这些距离进行排序并输出表中最接近搜索向量（余弦距离最小）的前三个文档。

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

搜索结果中的三个词按它们与查询向量的距离排序：距离越小，对应的 `document` 越相关。

因此，从输出结果来看，会游泳的动物很可能是一条鱼 (`fish`)，或者是一只有游泳天赋的狗 (`dog`)。

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)
- [向量搜索索引](/vector-search-index.md)