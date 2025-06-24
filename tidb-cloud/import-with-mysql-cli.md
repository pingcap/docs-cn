---
title: 使用 MySQL CLI 导入数据到 TiDB Cloud Dedicated
summary: 了解如何使用 MySQL CLI 导入数据到 TiDB Cloud Dedicated。
---

# 使用 MySQL CLI 导入数据到 TiDB Cloud Dedicated

本文档介绍如何使用 [MySQL 命令行客户端](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)将数据导入到 TiDB Cloud Dedicated。你可以从 SQL 文件或 CSV 文件导入数据。以下部分提供了从每种类型文件导入数据的分步说明。

## 前提条件

在使用 MySQL CLI 向 TiDB Cloud Dedicated 导入数据之前，你需要满足以下前提条件：

- 你可以访问你的 TiDB Cloud Dedicated 集群。如果没有，请按照[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)中的说明创建一个。
- 在本地计算机上安装 MySQL CLI。

## 步骤 1. 连接到你的 TiDB Cloud Dedicated 集群

连接到你的 TiDB 集群。

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 在左侧导航栏中，点击**设置** > **网络**。

3. 在**网络**页面的 **IP 访问列表**区域，点击**添加 IP 地址**。

4. 在对话框中，选择**允许从任何地方访问**，然后点击**确认**。

5. 在右上角，点击**连接**打开连接信息对话框。

    有关如何获取连接字符串的更多详细信息，请参见[通过公共连接连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md)。

## 步骤 2. 定义表并插入示例数据

在导入数据之前，你需要准备表结构并向其中插入实际的示例数据。以下是一个可用于创建表和插入示例数据的 SQL 文件（`product_data.sql`）示例：

```sql
-- 在你的 TiDB 数据库中创建表
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    price DECIMAL(10, 2)
);

-- 向表中插入示例数据
INSERT INTO products (product_id, product_name, price) VALUES
    (1, 'Laptop', 999.99),
    (2, 'Smartphone', 499.99),
    (3, 'Tablet', 299.99);
```

## 步骤 3. 从 SQL 或 CSV 文件导入数据

你可以从 SQL 文件或 CSV 文件导入数据。以下部分提供了从每种类型文件导入数据的分步说明。

<SimpleTab>
<div label="从 SQL 文件导入">

按照以下步骤从 SQL 文件导入数据：

1. 提供一个包含要导入数据的实际 SQL 文件（例如，`product_data.sql`）。此 SQL 文件必须包含带有实际数据的 `INSERT` 语句。

2. 使用以下命令从 SQL 文件导入数据：

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_cluster_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> < product_data.sql
    ```

> **注意：**
>
> 这里使用的默认数据库名称是 `test`，你可以手动创建自己的数据库或在 SQL 文件中使用 `CREATE DATABASE` 命令。

</div>
<div label="从 CSV 文件导入">

按照以下步骤从 CSV 文件导入数据：

1. 在 TiDB 中创建与你的数据导入需求相匹配的数据库和架构。

2. 提供一个包含要导入数据的示例 CSV 文件（例如，`product_data.csv`）。以下是 CSV 文件的示例：

    **product_data.csv:**

    ```csv
    product_id,product_name,price
    4,Laptop,999.99
    5,Smartphone,499.99
    6,Tablet,299.99
    ```

3. 使用以下命令从 CSV 文件导入数据：

    ```bash
    mysql --comments --connect-timeout 150 -u '<your_username>' -h <your_host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<your_ca_path> -p<your_password> -e "LOAD DATA LOCAL INFILE '<your_csv_path>' INTO TABLE products
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES (product_id, product_name, price);"
    ```

4. 确保将路径、表名（本例中为 `products`）、`<your_username>`、`<your_host>`、`<your_password>`、`<your_csv_path>`、`<your_ca_path>` 和其他占位符替换为你的实际信息，并根据需要将示例 CSV 数据替换为你的实际数据集。

> **注意：**
>
> 有关 `LOAD DATA LOCAL INFILE` 的更多语法详情，请参见 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)。

</div>
</SimpleTab>
