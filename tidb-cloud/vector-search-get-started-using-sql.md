---
title: 通过 SQL 开始使用向量搜索
summary: 了解如何使用 SQL 语句在 TiDB 中快速开始使用向量搜索来支持你的生成式 AI 应用。
---

# 通过 SQL 开始使用向量搜索

TiDB 扩展了 MySQL 语法以支持[向量搜索](/tidb-cloud/vector-search-overview.md)，并引入了新的[向量数据类型](/tidb-cloud/vector-search-data-types.md)和多个[向量函数](/tidb-cloud/vector-search-functions-and-operators.md)。

本教程演示如何仅使用 SQL 语句开始使用 TiDB 向量搜索。你将学习如何使用 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)完成以下操作：

- 连接到你的 TiDB 集群
- 创建向量表
- 存储向量嵌入
- 执行向量搜索查询

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB 自管理版本（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 前提条件

要完成本教程，你需要：

- 在你的机器上安装 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)（MySQL CLI）。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)的说明创建你自己的 TiDB Cloud 集群。

## 开始使用

### 步骤 1. 连接到 TiDB 集群

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。将显示一个连接对话框。

3. 在连接对话框中，从**连接方式**下拉列表中选择 **MySQL CLI**，并保持**连接类型**的默认设置为**公共**。

4. 如果你还没有设置密码，点击**生成密码**以生成一个随机密码。

5. 复制连接命令并将其粘贴到你的终端中。以下是 macOS 的示例：

   ```bash
   mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
   ```

### 步骤 2. 创建向量表

创建表时，你可以通过指定 `VECTOR` 数据类型将列定义为[向量](/tidb-cloud/vector-search-overview.md#vector-embedding)列。

例如，要创建一个具有三维 `VECTOR` 列的表 `embedded_documents`，请使用 MySQL CLI 执行以下 SQL 语句：

```sql
USE test;
CREATE TABLE embedded_documents (
    id        INT       PRIMARY KEY,
    -- 用于存储文档的原始内容的列。
    document  TEXT,
    -- 用于存储文档的向量表示的列。
    embedding VECTOR(3)
);
```

预期输出如下：

```text
Query OK, 0 rows affected (0.27 sec)
```

### 步骤 3. 向表中插入向量嵌入

将三个文档及其[向量嵌入](/tidb-cloud/vector-search-overview.md#vector-embedding)插入到 `embedded_documents` 表中：

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
> 在实际应用中，[嵌入模型](/tidb-cloud/vector-search-overview.md#embedding-model)通常会生成具有数百或数千维度的向量嵌入。

### 步骤 4. 查询向量表

要验证文档是否已正确插入，请查询 `embedded_documents` 表：

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

与全文搜索类似，用户在使用向量搜索时向应用程序提供搜索词。

在本示例中，搜索词是"a swimming animal"，其对应的向量嵌入假设为 `[1,2,3]`。在实际应用中，你需要使用嵌入模型将用户的搜索词转换为向量嵌入。

执行以下 SQL 语句，TiDB 将通过计算和排序表中向量嵌入与 `[1,2,3]` 之间的余弦距离（`vec_cosine_distance`），识别出最接近的三个文档。

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

搜索结果中的三个词按照它们与查询向量的距离排序：距离越小，相应的 `document` 越相关。

因此，根据输出，这个会游泳的动物最可能是鱼，或者是一只擅长游泳的狗。

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
