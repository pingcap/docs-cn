---
title: 使用 SQL 开始向量搜索
summary: 了解如何使用 SQL 语句快速开始使用 TiDB Cloud 中的向量搜索，并为生成式人工智能应用提供动力。
---

# 使用 SQL 开始向量搜索

TiDB 扩展了 MySQL 语法以支持[向量搜索](/vector-search-overview.md)，并引入了[向量数据类型](/vector-search-data-types.md)和多个[向量函数](/vector-search-functions-and-operators.md)。

本文将展示如何使用 SQL 语句在 TiDB 中进行向量搜索。在本文中，你将使用 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html)完成以下任务：

- 连接到 TiDB 集群
- 创建向量表
- 存储向量嵌入
- 执行向量搜索查询

## 前置需求

为了能够顺利完成本文中的操作，你需要提前：

- 在你的机器上安装 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.4/en/mysql.html) (MySQL CLI)
- 准备一个 TiDB 集群

如果你还没有 TiDB 集群，可以按照以下任一种方式创建：

- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。
- 参考[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)，创建 TiDB Cloud 集群。

## 快速开始

### 第 1 步：连接到 TiDB 集群

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="本地部署 TiDB">

在本地部署的集群启动后，将你的集群连接命令输入至终端：

以下为 MacOS 的示例：

```bash
 mysql --comments --host 127.0.0.1 --port 4000 -u root
```

</div>

<div label="TiDB Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，单击你的 TiDB Serverless 集群名，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Endpoint Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `MySQL CLI`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 点击 **Connection String**，然后复制连接字符串。

    > **Tip:**
    >
    > 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

5. 在终端中执行连接字符串命令：

    以下为 macOS 上的连接字符串示例：

   ```bash
    mysql -u '<prefix>.root' -h '<host>' -P 4000 -D 'test' --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p'<password>'
    ```

    注意替换 `<>` 中的占位符为你的集群实际对应的值。

</div>

</SimpleTab>

### 第 2 步：创建向量表

在建表时，你可以使用 `VECTOR` 数据类型声明指定列为[向量](/vector-search-overview.md#向量嵌入)列。

例如，如需创建一张带有三维 `VECTOR` 列的 `embedded_documents` 表，可以在 MySQL CLI 中执行以下 SQL 语句：

```sql
USE test;
CREATE TABLE embedded_documents (
    id        INT       PRIMARY KEY,
    -- document 列存储 document 的原始内容
    document  TEXT,
    -- embedding 列存储 document 的向量表示
    embedding VECTOR(3)
);
```

预期输出如下：

```text
Query OK, 0 rows affected (0.27 sec)
```

### 第 3 步：向表中插入向量

向 `embedded_documents` 表中插入三行包含[向量](/vector-search-overview.md#向量嵌入)的数据：

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

与全文搜索类似，在使用向量搜索时，你需要指定搜索词。

在本例中，搜索词是“一种会游泳的动物”，假设其对应的向量是 `[1,2,3]`。在实际应用中，你需要使用嵌入模型将用户的搜索词转换为向量。

执行以下 SQL 语句后，TiDB 会计算 `[1,2,3]` 与表中各向量之间的余弦距离 (`vec_cosine_distance`)，然后对这些距离进行排序并输出表中最接近搜索向量 (余弦距离最小) 的前三个向量。

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

搜索结果中的 3 个词会按向量的远近排列：距离越小，对应的 `document` 越相关。

因此，从输出结果来看，会游泳的动物很可能是一条鱼 (`fish`)，或者是一只有游泳天赋的狗 (`dog`)。

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)